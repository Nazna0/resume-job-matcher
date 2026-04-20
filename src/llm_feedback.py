"""
llm_feedback.py
Gets personalised AI feedback from Groq (LLaMA 3) about how to improve
the resume for the specific job description.
"""

import os
from groq import Groq


def get_llm_feedback(
    resume_text: str,
    job_text: str,
    score: int,
    missing_keywords: list,
    matched_keywords: list
) -> str:
    """
    Calls Groq LLaMA 3 to generate personalised resume improvement feedback.
    Falls back to a rule-based response if API key is not configured.
    """
    api_key = os.environ.get("GROQ_API_KEY", "")

    if not api_key:
        return _rule_based_feedback(score, missing_keywords, matched_keywords)

    try:
        client = Groq(api_key=api_key)

        # Truncate inputs to avoid token limit
        resume_snippet = resume_text[:2000]
        job_snippet = job_text[:2000]
        missing_str = ", ".join(missing_keywords[:15]) if missing_keywords else "None"
        matched_str = ", ".join(matched_keywords[:15]) if matched_keywords else "None"

        prompt = f"""You are an expert career coach and ATS (Applicant Tracking System) specialist.

A candidate has submitted their resume for a job. Here are the details:

MATCH SCORE: {score}%
MATCHED SKILLS: {matched_str}
MISSING SKILLS: {missing_str}

RESUME SNIPPET:
{resume_snippet}

JOB DESCRIPTION SNIPPET:
{job_snippet}

Please provide:
1. **Overall Assessment** (2-3 sentences about their fit)
2. **Top 3 Improvements** (specific, actionable bullet points)
3. **Skills to Add/Learn** (from missing keywords, with brief learning resource)
4. **Resume Rewrite Tip** (one specific sentence they should add/change)

Be concise, specific, and encouraging. Format using markdown bold headings."""

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return _rule_based_feedback(score, missing_keywords, matched_keywords)


def _rule_based_feedback(score: int, missing: list, matched: list) -> str:
    """
    Fallback feedback when no API key is set.
    """
    lines = []

    if score >= 75:
        lines.append("**Overall Assessment:** Great news — your resume is a strong match for this role! You already have most of the required skills. Focus on tailoring your bullet points to mirror the job description's language.")
    elif score >= 50:
        lines.append("**Overall Assessment:** You have a moderate match with this role. With a few targeted improvements, you can significantly boost your chances of passing the ATS filter.")
    else:
        lines.append("**Overall Assessment:** Your resume currently has a low match score. This may be due to missing keywords or a mismatch in skill set. Consider building the missing skills or targeting more aligned roles.")

    if missing:
        top_missing = missing[:5]
        lines.append(f"\n**Top Skills to Add:** {', '.join(top_missing)}")
        lines.append("Consider adding these to your Skills section if you have experience with them, or start learning the top ones via free resources (Coursera, fast.ai, Kaggle).")

    if matched:
        lines.append(f"\n**Your Strengths for This Role:** {', '.join(matched[:5])}")
        lines.append("Make sure these skills are prominently mentioned in your experience bullet points, not just listed in a Skills section.")

    lines.append("\n**Resume Rewrite Tip:** Quantify your achievements. Replace 'worked on ML models' with 'Built and deployed 3 ML models achieving 92% accuracy, reducing manual effort by 40%'.")

    lines.append("\n*💡 Add your GROQ_API_KEY in `.env` for full LLaMA 3 AI feedback.*")

    return "\n".join(lines)
