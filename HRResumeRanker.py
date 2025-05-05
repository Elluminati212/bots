import os
import json
import fitz
import requests
import pandas as pd

# CONFIG
GROQ_API_KEY = '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'
GROQ_MODEL = 'llama3-70b-8192'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# System prompt for HR Resume Ranker Agent
HR_RESUME_RANKER_PROMPT = """
You are an expert HR Resume Screening Agent.

Your tasks:
- Analyze resumes (CVs) in relation to a provided Job Description (JD).
- Score each resume based on its relevance to the JD: skills, experience, education, and job fit.
- Rank the resumes from best match to least match.
- For each candidate, generate a brief insight: explain why they are a strong (or weaker) match for the job.

Focus on practical relevance, skill alignment, and experience suitability. Be concise, fair, and professional.
"""

def query_groq_llm(jd, resumes, top_n):
    print("Analyzing resumes...")

    resumes_text = ""
    for idx, resume in enumerate(resumes):
        resumes_text += f"\nResume {idx+1}:\n{resume}\n"

    user_prompt = f"""
Job Description (JD):
{jd}

Received Resumes:
{resumes_text}

Instructions:
- Rank all resumes based on their relevance to the JD.
- Provide a ranking list of the top {top_n} candidates.
- For each top candidate, give a short insight about why they are a strong match.

Output format: 
1. Candidate {{number}}: Relevance Score: {{score}}/100
Insight: {{brief explanation}}

Only include the top {top_n} candidates in the final result.
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": HR_RESUME_RANKER_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2  # factual, analytical
    }

    response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        print(f"Error querying Groq LLM: {response.status_code}, {response.text}")
        return None

def load_resumes_from_folder(folder_path):
    resumes = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".pdf"):
            # Extract text from PDF
            try:
                with fitz.open(file_path) as doc:
                    text = ""
                    for page in doc:
                        text += page.get_text()
                resumes.append(text)
            except Exception as e:
                print(f"⚠️ Failed to read {filename}: {e}")
        elif filename.endswith(".txt"):
            # (Optional) If you still want to allow .txt files also
            with open(file_path, 'r', encoding='utf-8') as f:
                resumes.append(f.read())
    return resumes


def save_results_to_file(result_text, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(result_text)
    print(f"✅ Results saved to: {filename}")

def main(top_n):
    print("🤝 Welcome to the HR Resume Ranker Agent!")

    # Predefined paths
    jd_path = "/home/elluminati/bots/uploads/job_description.txt"
    resumes_folder = "/home/elluminati/bots/uploads/"

    if not os.path.exists(jd_path):
        print(f"❌ Job Description file not found at {jd_path}")
        return
    if not os.path.isdir(resumes_folder):
        print(f"❌ Resumes folder not found at {resumes_folder}")
        return

    from HRResumeRanker import load_resumes_from_folder, save_results_to_file, query_groq_llm  # import your functions inside
    with open(jd_path, 'r', encoding='utf-8') as f:
        jd = f.read()

    resumes = load_resumes_from_folder(resumes_folder)

    if not resumes:
        print("❌ No resumes found in the provided folder.")
        return

    result_text = query_groq_llm(jd, resumes, top_n)

    if result_text:
        output_file = "/home/elluminati/bots/results/Ranked_Candidates_Report.txt"
        save_results_to_file(result_text, output_file)
        print("\n🏆 Ranking complete! Check the 'Ranked_Candidates_Report.txt' file for results.")
    else:
        print("❌ Failed to analyze resumes. Please try again.")



# if __name__ == "__main__":
    # main()
    
    
if __name__ == "__main__":
    top_n = int(input("How many top candidates to shortlist? (e.g., 5, 10): ").strip())
    main(top_n)