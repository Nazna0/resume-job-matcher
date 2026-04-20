"""
extractor.py
Extracts relevant keywords from text using spaCy + custom tech keyword list.
"""

import re
import string

# ── Comprehensive tech / skill keyword list ───────────────────────
TECH_KEYWORDS = {
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "r", "scala",
    "go", "rust", "kotlin", "swift", "php", "ruby", "matlab", "bash", "shell",
    "sql", "nosql", "html", "css",

    # ML / DL frameworks
    "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "xgboost",
    "lightgbm", "catboost", "hugging face", "transformers", "spacy", "nltk",
    "opencv", "mediapipe", "fastai",

    # LLMs / GenAI
    "llm", "llms", "gpt", "gpt-4", "chatgpt", "openai", "groq", "llama",
    "llama3", "mistral", "gemini", "claude", "langchain", "llamaindex",
    "rag", "fine-tuning", "prompt engineering", "vector database", "embeddings",
    "faiss", "chromadb", "pinecone",

    # Data tools
    "pandas", "numpy", "matplotlib", "seaborn", "plotly", "scipy",
    "excel", "power bi", "tableau", "looker", "metabase",

    # Big data
    "spark", "hadoop", "hive", "kafka", "airflow", "dbt", "databricks",
    "bigquery", "snowflake", "redshift",

    # Databases
    "mysql", "postgresql", "postgres", "mongodb", "redis", "sqlite",
    "cassandra", "dynamodb", "firebase",

    # Cloud
    "aws", "azure", "gcp", "google cloud", "s3", "ec2", "lambda",
    "sagemaker", "vertex ai", "cloud run",

    # DevOps / Tools
    "git", "github", "gitlab", "docker", "kubernetes", "jenkins",
    "ci/cd", "maven", "ansible", "terraform", "fastapi", "flask",
    "django", "streamlit", "gradio", "rest api", "graphql",

    # Concepts
    "machine learning", "deep learning", "natural language processing",
    "nlp", "computer vision", "data science", "data analysis",
    "data engineering", "mlops", "feature engineering", "eda",
    "neural network", "cnn", "rnn", "lstm", "transformer", "bert",
    "classification", "regression", "clustering", "recommendation",
    "time series", "forecasting", "a/b testing", "statistics",
    "hypothesis testing", "linear algebra", "probability",

    # Soft / domain
    "agile", "scrum", "communication", "leadership", "problem solving",
    "teamwork", "analytical", "research", "presentation",
}


def _clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s\.\+\#\/\-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_keywords(text: str) -> set:
    """
    Returns a set of tech/skill keywords found in `text`.
    Handles multi-word phrases (e.g. 'machine learning', 'natural language processing').
    """
    cleaned = _clean_text(text)
    found = set()

    # Multi-word first (longest match wins)
    multi_word = sorted([k for k in TECH_KEYWORDS if " " in k], key=len, reverse=True)
    for phrase in multi_word:
        if phrase in cleaned:
            found.add(phrase)
            cleaned = cleaned.replace(phrase, "")  # avoid double-counting

    # Single-word tokens
    tokens = set(cleaned.split())
    for token in tokens:
        token_clean = token.strip(string.punctuation)
        if token_clean in TECH_KEYWORDS:
            found.add(token_clean)

    return found
