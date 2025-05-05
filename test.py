import os
import json
import requests
from fpdf import FPDF
import fitz  # For PDF parsing
from fastapi import FastAPI, Request
from fastapi import UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse


# === CONFIG ===
GROQ_API_KEY = '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'
GROQ_MODEL = 'llama3-70b-8192'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

OUTPUT_DIR = "/home/vasu/bots/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BLOG_WRITER_PROMPT = """
You are a Blog Writing Agent.
- When the user gives a topic, generate a complete high-quality blog post.
- After generating the blog, ask the user: "Would you like to save this blog? If yes, choose 'PDF' or 'Text'."
- Wait for the user’s confirmation.
- Once confirmed, say: "Saving the blog..." and return 'SAVE:PDF' or 'SAVE:TEXT' on a new line for the backend to parse.
Only include one command per interaction. Do not try to download anything yourself.
"""

app = FastAPI()
app.mount("/files", StaticFiles(directory=OUTPUT_DIR), name="files")

def query_groq_chat(messages):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.5
    }
    response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"Groq API Error: {response.status_code} - {response.text}")

def save_as_text(content, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def save_as_pdf(content, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in content.split('\n'):
        if line.strip():
            pdf.multi_cell(0, 10, line)
    pdf.output(path)
    return path

@app.get("/", response_class=HTMLResponse)
def chat_page():
    return """
    <html>
    <head>
        <title>📝 Blog Chat Agent</title>
    </head>
    <body>
        <h2>📝 Blog Chat Agent</h2>
        <div id="chat" style="border:1px solid #ccc; padding:10px; height:300px; overflow:auto;"></div>
        <form id="chatForm">
            <textarea name="user_input" rows="4" cols="70" placeholder="Ask me to write a blog..."></textarea><br>
            <button type="submit">Send</button>
        </form>
        <script>
            const form = document.getElementById("chatForm");
            const chatDiv = document.getElementById("chat");
            let history = [{"role": "system", "content": `""" + BLOG_WRITER_PROMPT + """`}];
            let blogContent = "";

            form.onsubmit = async (e) => {
                e.preventDefault();
                const user_input = form.user_input.value.trim();
                if (!user_input) return;
                form.user_input.value = "";
                chatDiv.innerHTML += "<b>You:</b> " + user_input + "<br>";
                history.push({ role: "user", content: user_input });

                const response = await fetch("/chat", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({ history })
                });
                const data = await response.json();
                const reply = data.reply;
                chatDiv.innerHTML += "<b>🤖:</b> " + reply.replace(/\\n/g, "<br>") + "<br>";
                chatDiv.scrollTop = chatDiv.scrollHeight;
                history.push({ role: "assistant", content: reply });

                // Extract blog content by excluding save commands or prompts
                const lines = reply.split('\\n');
                const blogOnly = lines.filter(line =>
                    !line.startsWith('SAVE:') &&
                    !line.includes('Would you like to save')
                ).join('\\n');

                // Update blogContent only if valid new blog text detected
                if (blogOnly.trim().length > 100) {
                    blogContent = blogOnly;
                }

                // Check for save command
                if (reply.includes("SAVE:PDF") || reply.includes("SAVE:TEXT")) {
                    const format = reply.includes("PDF") ? "pdf" : "text";
                    const saveRes = await fetch("/save", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({ content: blogContent, format: format })
                    });

                    const fileData = await saveRes.json();
                    if (fileData.download_url) {
                        chatDiv.innerHTML += `<b>📎 Download:</b> <a href="${fileData.download_url}" target="_blank">${fileData.download_url}</a><br>`;
                    } else {
                        chatDiv.innerHTML += `<b>⚠️ Error:</b> ${fileData.error}<br>`;
                    }
                    chatDiv.scrollTop = chatDiv.scrollHeight;
                }
            };
        </script>
    </body>
    </html>
    """

@app.post("/chat")
async def chat_handler(request: Request):
    data = await request.json()
    history = data.get("history", [])
    try:
        reply = query_groq_chat(history)
        return JSONResponse({"reply": reply})
    except Exception as e:
        return JSONResponse({"reply": f"Error: {str(e)}"})

@app.post("/save")
async def save_handler(request: Request):
    data = await request.json()
    content = data["content"].strip()
    format = data["format"]
    
    if not content:
        return JSONResponse({"error": "Cannot save empty blog content."}, status_code=400)

    filename = "blog_post"
    if format == "pdf":
        path = save_as_pdf(content, filename + ".pdf")
    else:
        path = save_as_text(content, filename + ".txt")
    
    return {"download_url": f"/files/{os.path.basename(path)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
