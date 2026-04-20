# 🎯 AI Resume–Job Match Scorer

> **An NLP + LLM-powered web app that scores how well your resume matches a job description, identifies skill gaps, and gives personalised AI improvement tips.**

Built as part of the **PypSpiders / TestYantra Data Science Internship**.

---

## 🚀 Live Demo

> Run locally with: `streamlit run app.py`

---

## 📸 Features

| Feature | Description |
|---|---|
| 🎯 Match Score | Composite score using TF-IDF cosine similarity + keyword overlap |
| ✅ Matched Skills | Keywords from the JD that your resume already covers |
| ❌ Missing Skills | Skills you need to add to pass ATS filters |
| 📊 Visual Analysis | Gauge chart + skill gap bar chart (Plotly) |
| 🤖 AI Feedback | Personalised tips from Groq LLaMA 3 |
| 📥 Download Report | Export your results as a .txt file |

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **NLP / ML:** Scikit-learn (TF-IDF, Cosine Similarity), Custom keyword extractor
- **LLM:** Groq API (LLaMA 3 8B)
- **Visualisation:** Plotly
- **Language:** Python 3.10+

---

## 📁 Project Structure

```
resume_job_matcher/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example            # API key template
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── extractor.py        # Keyword extraction (NLP)
│   ├── matcher.py          # TF-IDF + keyword overlap scoring
│   ├── llm_feedback.py     # Groq LLaMA 3 AI feedback
│   └── visualizer.py      # Plotly charts
│
└── sample_data/
    ├── sample_resume.txt   # Demo resume
    └── sample_job.txt      # Demo job description
```

---

## ⚡ Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Nazna0/resume-job-matcher.git
cd resume-job-matcher
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
```bash
cp .env.example .env
# Edit .env and add your Groq API key
# Get a FREE key from: https://console.groq.com
```

### 5. Run the app
```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 🔑 API Key Setup (Groq — Free)

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up for free
3. Click **API Keys** → **Create API Key**
4. Copy the key and paste it in your `.env` file:
   ```
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
   ```

> The app works without an API key too — it falls back to rule-based feedback.

---

## 📊 How the Score is Calculated

```
Match Score = (Keyword Overlap × 40%) + (TF-IDF Cosine Similarity × 60%)
```

| Score Range | Verdict |
|---|---|
| 75% – 100% | 🟢 Strong Match |
| 50% – 74% | 🟡 Moderate Match |
| 0% – 49% | 🔴 Weak Match |

---

## 👩‍💻 Author

**Fathimathu Nasna SP**
B.Tech AI & Data Science 

- GitHub: [@Nazna0](https://github.com/Nazna0)
