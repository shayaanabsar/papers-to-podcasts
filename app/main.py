import streamlit as st
from backend import PodcastGenerator

st.set_page_config(
    page_title="Papers-to-Podcasts",
    page_icon="🎙️",
    layout="centered"
)

st.title('🎙️ Papers-to-Podcasts')
st.write('Convert academic papers into engaging podcast conversations')

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("📚 **Upload PDF**")
    st.caption("Any academic paper")
with col2:
    st.markdown("🤖 **AI Processing**")
    st.caption("Key insights extracted")
with col3:
    st.markdown("🎧 **Listen**")
    st.caption("Podcast ready")

st.markdown("---")

st.markdown("### 📄 Upload Your Paper")
file_name = st.file_uploader(
    label="Choose a PDF file",
    type='pdf',
    help="Upload an academic paper in PDF format"
)

if file_name:
    st.success(f"✓ File uploaded: {file_name.name}")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    generator = PodcastGenerator(file_name)
    
    status_text.markdown("**Step 1/5:** 📖 Reading and processing your paper...")
    progress_bar.progress(10)
    with st.spinner('Analyzing document structure...'):
        generator.read_file()
        generator.split_text_and_embed()
    progress_bar.progress(20)
    
    status_text.markdown("**Step 2/5:** 💡 Identifying key questions...")
    with st.spinner('Extracting main topics and concepts...'):
        generator.generate_questions()
    progress_bar.progress(40)
    
    st.markdown("### 🎯 Key Questions Identified")
    with st.expander("View identified questions", expanded=True):
        for i, question in enumerate(generator.questions, 1):
            st.markdown(f"**Q{i}.** {question.strip()}")
    
    status_text.markdown("**Step 3/5:** 🔍 Finding answers in the paper...")
    with st.spinner('Searching through content...'):
        generator.find_answers()
    progress_bar.progress(60)
    
    status_text.markdown("**Step 4/5:** ✍️ Writing the podcast script...")
    with st.spinner('Crafting engaging dialogue...'):
        generator.write_script()
    progress_bar.progress(80)
    
    st.markdown("### 📝 Podcast Script")
    with st.expander("View generated script"):
        st.markdown(generator.script)
    
    status_text.markdown("**Step 5/5:** 🎙️ Generating audio (this may take a few minutes)...")
    with st.spinner('Creating podcast audio...'):
        generator.generate_audio()
    progress_bar.progress(100)
    
    status_text.empty()
    progress_bar.empty()
    
    st.success("✅ Podcast generated successfully!")
    
    st.markdown("### 🎧 Your Podcast")
    st.audio(generator.audio, sample_rate=generator.sample_rate)


st.markdown("---")
st.caption("Made with ❤️ | Perfect for learning on the go 🚶‍♂️🎧")