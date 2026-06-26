# 🧠 Context-Aware Semantic Matcher (CASM)

CASM is an AI-powered recruiter screening assistant built using Streamlit and the Google Gemini API. It allows recruiters to upload a job description alongside a batch of candidate resumes in PDF format, extracting and parsing the text to generate an AI-ranked shortlist with custom matching scores and logical rationales.

## 🚀 Features
* **Batch Resume Processing:** Upload multiple candidate PDF resumes at the same time.
* **Contextual Semantic Analysis:** Evaluates candidates based on skills, frameworks, and requirements rather than simple keyword matching.
* **Automated Leaderboard:** Auto-sorts candidates from highest match percentage to lowest.
* **Granular AI Rationales:** Provides a clear, one-sentence justification detailing exactly why a candidate received their score.
* **Secure Environment Design:** Built using separate environment variables to completely protect sensitive API keys.

---

## 🛠️ Tech Stack
* **Frontend/UI:** Streamlit
* **AI Engine:** Google Gemini (`gemini-2.5-flash`) via the `google-genai` SDK
* **PDF Parsing:** PyPDF2
* **Environment Management:** Python-dotenv

---

## 📦 Local Installation & Setup

Follow these steps to get a local copy of CASM up and running on your computer:

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name