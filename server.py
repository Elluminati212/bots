import os
import shutil
import uvicorn
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from TTSAgent import query_groq_llm, transcribe_audio, speak_text

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_FOLDER = "/home/elluminati/bots/uploads"
RESULT_FOLDER = "/home/elluminati/bots/results"
AUDIO_FOLDER = "/home/elluminati/bots/audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# BLOG WRITER
@app.post("/blog")
async def blog_writer(topic: str = Form(...), keywords: str = Form(""), tone: str = Form(""), length: int = Form(1000)):
    try:
        from BlogWriter import query_groq_llm, save_blog_to_file
        keywords_list = [k.strip() for k in keywords.split(',')] if keywords else []
        blog_text = query_groq_llm(topic, keywords_list, tone, length)
        if blog_text:
            filename = f"{topic.replace(' ', '_')}_blog.txt"
            save_blog_to_file(blog_text, os.path.join(RESULT_FOLDER, filename))
            return {"filename": filename, "message": "Blog created successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})
    return JSONResponse(status_code=500, content={"message": "Blog generation failed"})

# RESUME RANKER
@app.post("/resume")
async def resume_ranker(top_n: int = Form(...)):
    try:
        from HRResumeRanker import main as hr_main
        hr_main(top_n)
        return {"message": "Resumes ranked successfully. Check results folder.", "filename": "Ranked_Candidates_Report.txt"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})


# NEWS AGGREGATOR
@app.post("/news")
async def news_aggregator(topic: str = Form(...)):
    try:
        from LatestNewsAggregator import query_groq_llm, save_news_to_file
        news_text = query_groq_llm(topic)
        if news_text:
            today_date = datetime.now().strftime("%Y-%m-%d")
            safe_topic = topic.replace(' ', '_').lower()
            filename = f"{safe_topic}_news_digest_{today_date}.txt"
            save_news_to_file(news_text, os.path.join(RESULT_FOLDER, filename))
            return {"filename": filename, "message": "News summary created"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})
    return JSONResponse(status_code=500, content={"message": "News aggregation failed"})

# PODCAST CREATOR
@app.post("/podcast")
async def podcast_creator(topic: str = Form(...), length_choice: int = Form(5)):
    try:
        from PodcastCreator import query_groq_llm, generate_audio, save_blog_to_file
        blog_text = query_groq_llm(topic, length_choice)
        if blog_text:
            safe_topic = topic.replace(' ', '_')
            blog_filename = f"{safe_topic}_blog.txt"
            audio_mp3_filename = f"{safe_topic}_podcast.mp3"
            audio_wav_filename = f"{safe_topic}_podcast.wav"
            save_blog_to_file(blog_text, os.path.join(RESULT_FOLDER, blog_filename))
            generate_audio(blog_text, os.path.join(RESULT_FOLDER, audio_mp3_filename), os.path.join(RESULT_FOLDER, audio_wav_filename))
            return {
                "blog_file": blog_filename,
                "audio_file": audio_wav_filename,
                "message": "Podcast created successfully"
            }
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})
    return JSONResponse(status_code=500, content={"message": "Podcast creation failed"})

@app.post("/voicechat")
async def voice_chat(file: UploadFile = File(...)):
    try:
        temp_path = os.path.join(AUDIO_FOLDER, file.filename)
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        question = transcribe_audio(temp_path)
        answer = query_groq_llm(question)
        
        speak_text(answer)
        os.remove(temp_path)

        return {"question": question, "answer": answer}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})

# UPLOAD files (for JD and resumes)
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": file.filename, "message": "File uploaded successfully"}


# ✅ DOWNLOAD FILE API
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(RESULT_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')
    else:
        return JSONResponse(status_code=404, content={"message": "File not found"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


