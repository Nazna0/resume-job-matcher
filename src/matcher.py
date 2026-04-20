"""
matcher.py
Computes a composite match score between resume and job description.
Uses:
  1. Keyword overlap score (40%)
  2. TF-IDF cosine similarity (60%)
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.extractor import extract_keywords


def _tfidf_similarity(text1: str, text2: str) -> float:
    """Compute cosine similarity between two texts using TF-IDF."""
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000
    )
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except Exception:
        return 0.0


def _keyword_overlap_score(resume_kw: set, jd_kw: set) -> tuple:
    """
    Returns (score 0-1, matched_keywords, missing_keywords).
    Score = matched / total_jd_keywords
    """
    if not jd_kw:
        return 0.0, set(), set()

    matched = resume_kw & jd_kw
    missing = jd_kw - resume_kw
    score = len(matched) / len(jd_kw)
    return score, matched, missing


def compute_match_score(resume_text: str, job_text: str) -> tuple:
    """
    Main function. Returns:
        (composite_score_int, matched_keywords, missing_keywords, all_jd_keywords)
    """
    resume_kw = extract_keywords(resume_text)
    jd_kw = extract_keywords(job_text)

    kw_score, matched, missing = _keyword_overlap_score(resume_kw, jd_kw)
    tfidf_score = _tfidf_similarity(resume_text, job_text)

    # Weighted composite score
    composite = (kw_score * 0.40) + (tfidf_score * 0.60)

    # Normalise to 0-100 and cap
    final_score = min(int(round(composite * 100)), 100)

    # Boost: if keyword overlap is very high, reflect that
    if kw_score >= 0.8:
        final_score = max(final_score, 75)

    return final_score, matched, missing, jd_kw
