import os
import streamlit as st
import PyPDF2
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 API Key not found! Please make sure you have a .env file with your GEMINI_API_KEY.")
    st.stop()

client = genai.Client(api_key=api_key)

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        resume_text = ""
        for page in range(len(reader.pages)):
            text = reader.pages[page].extract_text()
            if text:
                resume_text += text
        return resume_text
    except Exception:
        return ""

st.set_page_config(page_title="CASM AI Recruiter", layout="wide")
st.title("🧠 Context-Aware Semantic Matcher (CASM)")
st.markdown("Upload a Job Description and a batch of resumes to get an AI-ranked shortlist.")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("1. Job Description")
    jd_input = st.text_area("Paste the Job Description here:", height=300, 
                            value="Job Title: Junior AI Developer\nRequirements:\n- Python and AI API experience\n- Gemini or Llama model familiarity")

with col2:
    st.header("2. Candidate Resumes")
    uploaded_files = st.file_uploader("Upload PDF Resumes", type="pdf", accept_multiple_files=True)
    
    if st.button("🚀 Run AI Matcher", type="primary"):
        if not uploaded_files:
            st.warning("Please upload at least one resume!")
        elif not jd_input:
            st.warning("Please provide a job description!")
        else:
            with st.spinner("AI is analyzing and ranking candidates..."):
                candidate_results = []
                
                for uploaded_file in uploaded_files:
                    resume_text = extract_text_from_pdf(uploaded_file)
                    
                    if not resume_text:
                        st.error(f"Could not read {uploaded_file.name}")
                        continue
                    
                    prompt = f"""
                    Compare this Candidate Resume against the Job Description.
                    Job Description: {jd_input}
                    Candidate Resume: {resume_text}
                    
                    Provide your evaluation in this format:
                    SCORE: [0-100]
                    RATIONALE: [1-sentence summary citing the resume]
                    """
                    
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt,
                        )
                        
                        ai_output = response.text
                        score = 0
                        rationale = ai_output
                        
                        for line in ai_output.split("\n"):
                            if "SCORE:" in line:
                                try:
                                    score = int(''.join(filter(str.isdigit, line)))
                                except:
                                    score = 0
                            if "RATIONALE:" in line:
                                rationale = line.replace("RATIONALE:", "").strip()
                                
                        candidate_results.append({
                            "name": uploaded_file.name,
                            "score": score,
                            "rationale": rationale
                        })
                    except Exception as e:
                        st.error(f"Error evaluating {uploaded_file.name}. Ensure your API key is valid.")
                
                candidate_results.sort(key=lambda x: x["score"], reverse=True)
                
                st.subheader("🏆 Ranked Shortlist")
                for rank, candidate in enumerate(candidate_results, 1):
                    with st.expander(f"**#{rank} | {candidate['name']}** - Match: {candidate['score']}%"):
                        st.write(f"**AI Rationale:** {candidate['rationale']}")