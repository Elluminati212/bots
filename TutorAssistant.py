import os
import json
import fitz
import uvicorn
import requests
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# from fastapi import FastAPI, File, UploadFile, Form, HTTPExceptionfrom 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "/home/elluminati/bots/uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Ensure the directory has the correct permissions
os.chmod(UPLOAD_DIR, 0o755)

# CONFIG
GROQ_API_KEY = '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'  # Replace with your actual Groq API key : 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
GROQ_MODEL = 'llama3-70b-8192'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# System prompt for Tutor Assistant Agent
TUTOR_ASSISTANT_PROMPT = """
You are an expert Tutor Assistant Agent designed to help students master subjects by creating interactive learning experiences.

Your tasks:
1. Analyze the provided study material or topic.
2. Generate relevant questions, quizzes, and practice tests based on the content.
3. Provide scoring and detailed feedback for each answer.
4. Offer explanations and additional resources for improvement.

Be clear, concise, and educational in your responses. Tailor the difficulty level to the student's needs.
"""

def query_groq_llm(study_material, num_questions=5):
    print("Generating questions and quizzes...")

    user_prompt = f"""
Based on the following study material, generate {num_questions} questions for a quiz:

Study Material:
\"\"\"
{study_material}
\"\"\"

For each question:
1. Provide the question
2. List 4 multiple-choice options (A, B, C, D)
3. Indicate the correct answer
4. Give a brief explanation for the correct answer

Format the output as a JSON object with the following structure:
{{
    "questions": [
        {{
            "question": "Question text here",
            "options": {{
                "A": "Option A text",
                "B": "Option B text",
                "C": "Option C text",
                "D": "Option D text"
            }},
            "correct_answer": "Correct option letter",
            "explanation": "Explanation for the correct answer"
        }},
        // ... more questions ...
    ]
}}

Ensure that your response is a valid JSON object and nothing else.
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": TUTOR_ASSISTANT_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3  # Slightly creative but mostly factual
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content'].strip()
        
        # Attempt to parse the content as JSON
        try:
            json_content = json.loads(content)
            return json.dumps(json_content)  # Ensure it's a valid JSON string
        except json.JSONDecodeError:
            # If parsing fails, attempt to extract JSON from the content
            import re
            json_match = re.search(r'(\{.*\})', content, re.DOTALL)
            if json_match:
                try:
                    json_content = json.loads(json_match.group(1))
                    return json.dumps(json_content)
                except json.JSONDecodeError:
                    raise ValueError("Failed to extract valid JSON from LLM response")
            else:
                raise ValueError("No JSON-like structure found in LLM response")
    except requests.RequestException as e:
        print(f"Error querying Groq LLM: {e}")
        return None
    except ValueError as e:
        print(f"Error processing LLM response: {e}")
        return None

def extract_text_from_pdf(file_path):
    try:
        with fitz.open(file_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        print(f"⚠️ Failed to read PDF: {e}")
        return None

class QuizRequest(BaseModel):
    topic: Optional[str] = None
    num_questions: int = 5

@app.post("/generate_quiz")
async def generate_quiz(
    file: Optional[UploadFile] = File(None),
    topic: Optional[str] = Form(None),
    num_questions: int = Form(5)
):
    if file:
        try:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            
            study_material = extract_text_from_pdf(file_path)
            os.remove(file_path)  # Clean up the uploaded file
            
            if not study_material:
                raise HTTPException(status_code=400, detail="Failed to extract text from PDF.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    elif topic:
        study_material = topic
    else:
        raise HTTPException(status_code=400, detail="Please provide either a file or a topic.")

    quiz_json = query_groq_llm(study_material, num_questions)
    if quiz_json:
        try:
            quiz_data = json.loads(quiz_json)
            return JSONResponse(content=quiz_data)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse quiz data: {str(e)}")
    else:
        raise HTTPException(status_code=500, detail="Failed to generate quiz. Please try again.")

class AnswerSubmission(BaseModel):
    answers: dict
    
# after i also want user to task the quiz and submit their answers
# and then check their answers
# and get feedback score 

# @app.post("/submit")
# async def submit_answers(answers: AnswerSubmission):
#     quiz_json = query_groq_llm(answers.answers["study_material"], answers.answers["num_questions"])
#     if quiz_json:
#         try:
#             quiz_data = json.loads(quiz_json)
#             correct_answers = {q["question"]: q["correct_answer"] for q in quiz_data["questions"]}
#             submitted_answers = {q: answers.answers.get(q, "") for q in correct_answers.keys()}
#             feedback = {q: {"correct": submitted == correct_answers[q], "answer": correct_answers[q]} for q, submitted in submitted_answers.items()}
#             return JSONResponse(content=feedback)
#         except json.JSONDecodeError as e:
#             raise HTTPException(status_code=500, detail=f"Failed to parse quiz data: {str(e)}")
#     else:
#         raise HTTPException(status_code=500, detail="Failed to generate quiz. Please try again.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
