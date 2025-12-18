from PyPDF2 import PdfReader
from scipy.io.wavfile import write as write_wav
from ollama import chat
from IPython.display import display, Audio
from kokoro_onnx import Kokoro
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

class PodcastGenerator:
	def __init__(self, file):
		self.file = file

		self.raw_text  = None
		self.index     = None
		self.chunks    = None
		self.questions = None
		self.answers   = None
		self.script    = None
		self.audio     = None
		self.sample_rate = None

	def read_file(self):
		# Uses self.file_name to read the file into self.raw_text
		
		reader = PdfReader(self.file)
		paper_text = ''

		for page in reader.pages:
			paper_text += page.extract_text()

		self.raw_text = paper_text
	
	def split_text_and_embed(self):
		# Uses self.raw_text and RecursiveCharacterTextSplitter to split into chunks
		# Embeds the chunks and stores self.index and self.chunks

		splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
		splits = splitter.split_text(self.raw_text)

		embeddings = embedding_model.encode(splits)

		dim   = embeddings.shape[1]
		index = faiss.IndexFlatL2(dim)
		index.add(embeddings)

		self.index  = index
		self.chunks = splits
	
	def generate_questions(self):
		# Generate Key Questions
		messages = [
			{
				'role': 'user',

				'content': f"""
				Create an engaging podcast script conversation between two hosts discussing this research paper.

				But before you begin any script writing read through the paper and identify 5-10 key questions that the listener needs to understand.
				
				These will form the basis of your podcast script.
				
				Do not try and find the answers just identify the questions.
				
				Return the questions separated by new-lines.

				Questions should just be plain-text with no formatting or question numbers.
				
				Paper Text: {self.raw_text}"""
			}
		]

		response  = chat(model='gpt-oss:120b-cloud', messages=messages) 
		questions = response['message']['content']

		questions = list(filter(lambda x: x != '', questions.split('\n')))
		self.questions = questions

	def find_answers(self):
		# Generate Answers to the questions

		prompt = '''Answer each question using the provided context. For each question, provide:

		1. Key Terms (1 sentence): Define any technical terms in the question
		2. Simple Answer (2-3 sentences): Explain in plain English
		3. Detailed Answer (3-4 sentences): Technical explanation with evidence from context

		Rules:
		- Be concise - no repetition across the three parts
		- Prioritize information from context chunks
		- Skip obvious definitions
		- Format answers in this way: Question: Answer

		Questions and Context:
		'''

		search_queries = embedding_model.encode(self.questions)
		
		for i, question in enumerate(self.questions):
			search_query = search_queries[i].reshape(1, -1)
			_, positions = self.index.search(search_query, k=3)
			relevant_chunks = [self.chunks[p] for p in positions[0]]

			prompt += f'\n**Question {i+1}:** {question}\n'
			prompt += '**Context:**\n'
			prompt += '\n'.join([f'- {chunk}' for chunk in relevant_chunks])
			prompt += '\n'

		prompt += '\n\nGenerate the answers now:'

		messages = [{
			'role': 'user',
			'content': prompt
		}]

		response = chat(model='gpt-oss:120b-cloud', messages=messages)
		self.answers = response['message']['content']

	def write_script(self):
		messages = [
			{
			'role': 'user',
			'content': f"""
				Create a concise 7-minute podcast script between Sarah and Michael discussing an academic paper.

				CRITICAL CONSTRAINTS:
				- Maximum 1000 words total (strictly enforce this)
				- No repetition - each point mentioned ONCE only
				- Plain text only - no special symbols, asterisks, or formatting marks
				- Spell out ALL acronyms on first use (e.g., "Natural Language Processing or NLP")
				- Spell out numbers and years e.g. 0.24 should be 'zero point two-four' and 1999 should be 'nineteen-ninety-nine'

				FORMAT:
				SARAH: [dialogue]
				MICHAEL: [dialogue]

				CONTENT RULES:
				1. 20-second intro: Quick hello and paper topic
				2. Cover KEY insights only (skip minor details)
				3. Use plain English - avoid jargon
				4. No rehashing - if a concept is explained, move on
				5. 20-second outro: One main takeaway

				STYLE:
				- Direct and punchy
				- Cut filler words
				- Assume intelligent audience (no over-explaining)
				- Natural speech patterns

				QUESTIONS AND ANSWERS (use selectively, not all):
				{self.answers}

				Generate exactly 1000 words or less:"""
			
			}]
		
		response = chat(model='gpt-oss:120b-cloud', messages=messages)
		self.script = response['message']['content']
	
	def generate_audio(self):
		sentences = list(filter(lambda x: x.strip() != '', self.script.split('\n')))

		formatted_sentences = []

		for sentence in sentences:
			speaker, text = re.findall(r'(^[A-Z]+):(.+)', sentence)[0]
			text = text.strip()

			if speaker == 'SARAH':
				voice = 'af_sarah'
			elif speaker == 'MICHAEL':
				voice = 'am_michael'

			formatted_sentences.append({
				'voice': voice,
				'text': text
			})

		kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
		audio = []

		for sentence in formatted_sentences:
			voice = sentence["voice"]
			text = sentence["text"]
			
			samples, sample_rate = kokoro.create(
				text,
				voice=voice,
				speed=1.0,
				lang="en-us",
			)
			audio.append(samples)

		self.audio = np.concatenate(audio)
		self.sample_rate = sample_rate
