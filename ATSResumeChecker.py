# import os
# import json
# import fitz
# import requests

# # CONFIG
# GROQ_API_KEY = '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'  # <<<< Replace with your real API key
# GROQ_MODEL = 'llama3-70b-8192'
# GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# # System prompt for ATS Resume Checker Agent
# ATS_RESUME_CHECKER_PROMPT = """
# You are an ATS Resume Checker Agent.

# Your task:
# - Analyze the given resume for compatibility with Applicant Tracking Systems (ATS).
# - Evaluate formatting, keyword optimization, structure, and readability.
# - Provide a detailed ATS Score (0-100).
# - Highlight issues that could cause parsing problems.
# - Suggest specific improvements to optimize the resume for better ATS performance.
# - Provide expert tips to enhance its chances of passing ATS filters.

# Be professional, clear, and actionable in your feedback.
# """

# def query_groq_llm(resume_text):
#     print("Analyzing resume for ATS compliance...")

#     user_prompt = f"""
# Here is the resume:

# \"\"\"
# {resume_text}
# \"\"\"

# Instructions:
# - Provide an ATS Score (0-100)
# - Detailed comments on formatting, keyword optimization, structure, readability
# - Specific improvement suggestions
# - Expert optimization tips
# """

#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }
    
#     payload = {
#         "model": GROQ_MODEL,
#         "messages": [
#             {"role": "system", "content": ATS_RESUME_CHECKER_PROMPT},
#             {"role": "user", "content": user_prompt}
#         ],
#         "temperature": 0.3  # more structured and factual
#     }

#     response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))
    
#     if response.status_code == 200:
#         return response.json()['choices'][0]['message']['content'].strip()
#     else:
#         print(f"❌ Error querying Groq LLM: {response.status_code}, {response.text}")
#         return None

# def load_resume(file_path):
#     """Load a single resume from a PDF or text file."""
#     if not os.path.exists(file_path):
#         print(f"❌ File not found: {file_path}")
#         return None
    
#     if file_path.endswith('.pdf'):
#         try:
#             with fitz.open(file_path) as doc:
#                 text = ""
#                 for page in doc:
#                     text += page.get_text()
#             return text
#         except Exception as e:
#             print(f"⚠️ Failed to read PDF {file_path}: {e}")
#             return None
#     elif file_path.endswith('.txt'):
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return f.read()
#     else:
#         print("❌ Unsupported file format. Please upload a .pdf or .txt file.")
#         return None

# def save_results_to_file(result_text, filename):
#     """Save feedback report to a text file."""
#     with open(filename, 'w', encoding='utf-8') as f:
#         f.write(result_text)
#     print(f"✅ ATS Report saved to: {filename}")

# def main():
#     print("🤖 Welcome to the ATS Resume Checker Agent!")

#     # Define paths
#     resume_path = "/home/vasu/bots/uploads/resume.pdf"  # <<< Adjust if needed
#     output_file = "/home/vasu/bots/results/ATS_Resume_Feedback.txt"

#     resume_text = load_resume(resume_path)

#     if not resume_text:
#         print("❌ No resume found or failed to load.")
#         return

#     result_text = query_groq_llm(resume_text)

#     if result_text:
#         save_results_to_file(result_text, output_file)
#         print("\n✅ Resume analysis complete! Check the ATS_Resume_Feedback.txt file for detailed feedback.")
#     else:
#         print("❌ Failed to analyze resume. Please try again.")

# if __name__ == "__main__":
#     main()


# ATSResumeChecker.py

import os
import json
import requests
import fitz  # PyMuPDF for PDFs

# CONFIG
GROQ_API_KEY = 'your_groq_api_key_here'  # <<< Replace with your Groq API key
GROQ_MODEL = 'llama3-70b-8192'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# System prompt for the Agent (based on your goal)
ATS_RESUME_CHECKER_PROMPT = """
You are an ATS Resume Checker Agent helping job seekers optimize their resumes for Applicant Tracking Systems (ATS).

Your task:
- Analyze the uploaded resume against ATS standards.
- Evaluate formatting, keyword optimization, readability, structure, and overall ATS compatibility.
- Provide:
  - An ATS Resume Score (0-100)
  - Detailed comments on each major parameter (formatting, keywords, structure, readability)
  - Identify any issues causing parsing problems
  - Personalized suggestions for improvement
  - Expert tips to make the resume stand out
- Be professional, clear, and actionable in your feedback.

Your goal is to help users quickly optimize and increase their chances of passing ATS scans.
"""

def query_groq_llm(resume_text):
    """Send resume content to Groq and get analysis."""
    print("Analyzing resume for ATS compliance...")

    user_prompt = f"""
Here is a resume:

\"\"\"
{resume_text}
\"\"\"

Instructions:
- Provide an ATS Resume Score (0-100)
- Evaluate formatting, keyword optimization, structure, readability
- Identify parsing issues
- Give personalized suggestions
- Provide expert ATS tips
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": ATS_RESUME_CHECKER_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        print(f"❌ Error querying Groq LLM: {response.status_code} {response.text}")
        return None

def load_resume(file_path):
    """Load text from a PDF or .txt resume."""
    if not os.path.exists(file_path):
        print(f"❌ Resume file not found: {file_path}")
        return None
    
    if file_path.endswith('.pdf'):
        try:
            with fitz.open(file_path) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
            return text.strip()
        except Exception as e:
            print(f"⚠️ Failed to read PDF: {e}")
            return None
    elif file_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"⚠️ Failed to read TXT: {e}")
            return None
    else:
        print("❌ Unsupported file format. Please upload a .pdf or .txt file.")
        return None

def save_results_to_file(result_text, filename):
    """Save ATS feedback to a file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(result_text)
    print(f"✅ ATS Resume Feedback saved at: {filename}")

def main():
    print("🤖 Welcome to the ATS Resume Checker Agent!")

    resume_path = "/home/vasu/bots/uploads/resume.pdf"  # Adjust if needed
    output_file = "/home/vasu/bots/results/ATS_Resume_Feedback.txt"

    resume_text = load_resume(resume_path)

    if not resume_text:
        print("❌ No resume found or failed to load.")
        return

    result_text = query_groq_llm(resume_text)

    if result_text:
        save_results_to_file(result_text, output_file)
        print("\n✅ Resume analysis complete! Check the ATS_Resume_Feedback.txt file for detailed feedback.")
    else:
        print("❌ Failed to analyze resume. Please try again.")

if __name__ == "__main__":
    main()
