import sys
from PyQt6.QtWidgets import (
    QMessageBox, QFileDialog,
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QTextEdit, QVBoxLayout, QGridLayout,
)
import os
import json
import requests
from PyQt6.QtCore import Qt

# CONFIG (same as before)
GROQ_API_KEY = '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'
GROQ_MODEL = 'llama3-70b-8192'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# System prompt for Blog Writer Agent (same as before)
BLOG_WRITER_PROMPT = """
You are a professional Blog Writer Agent specialized in creating high-quality, SEO-optimized, EEAT-compliant blog posts.

Your tasks:
- Perform research on trending and top-ranking blogs around the topic.
- Ensure alignment with Google's EEAT guidelines: Expertise, Experience, Authoritativeness, Trustworthiness.
- Integrate the provided keywords naturally throughout the blog.
- Match the requested tone of voice (friendly, professional, conversational, technical, etc.).
- Target the requested word count range.
- Structure the blog properly with a strong introduction, clear body sections, and an engaging conclusion.
- Write in natural, human-like language, avoiding robotic or repetitive phrasing.
"""

def query_groq_llm(topic, keywords, tone, length_choice):
    print("Generating blog content...")
    keyword_list = ', '.join(keywords) if keywords else "No specific keywords."
    tone_instruction = tone if tone else "Neutral and informative tone."
    word_count_instruction = f"Target approximately {length_choice} words."
    user_prompt = f"""
Topic: {topic}

Keywords: {keyword_list}

Tone: {tone_instruction}

Length: {word_count_instruction}

Please research top-performing blogs, align with SEO best practices, and write a complete blog article ready for publishing. Focus on natural readability and engagement.
"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": BLOG_WRITER_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        if 'choices' in data and data['choices'] and 'message' in data['choices'][0] and 'content' in data['choices'][0]['message']:
            return data['choices'][0]['message']['content'].strip()
        else:
            return "Error: Could not extract content from the API response."
    except requests.exceptions.RequestException as e:
        return f"Error querying Groq LLM: {e}"
    except json.JSONDecodeError:
        return "Error: Could not decode JSON response from the API."

class BlogWriterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blog Writer Agent (PyQt)")
        self.setGeometry(100, 100, 800, 600)  # Initial window size
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        # Input Fields
        layout.addWidget(QLabel("Blog Topic:"), 0, 0)
        self.topic_input = QLineEdit()
        layout.addWidget(self.topic_input, 0, 1)

        layout.addWidget(QLabel("Keywords (comma-separated):"), 1, 0)
        self.keywords_input = QLineEdit()
        layout.addWidget(self.keywords_input, 1, 1)

        layout.addWidget(QLabel("Tone of Voice (optional):"), 2, 0)
        self.tone_input = QLineEdit()
        layout.addWidget(self.tone_input, 2, 1)

        layout.addWidget(QLabel("Desired Length (words):"), 3, 0)
        self.length_input = QLineEdit()
        self.length_input.setFixedWidth(100)
        layout.addWidget(self.length_input, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        # Generate Button
        self.generate_button = QPushButton("Generate Blog")
        self.generate_button.clicked.connect(self.generate_blog)
        layout.addWidget(self.generate_button, 4, 0, 1, 2)

        # Output Area
        layout.addWidget(QLabel("Generated Blog Content:"), 5, 0, 1, 2)
        self.blog_output = QTextEdit()
        self.blog_output.setReadOnly(True)
        layout.addWidget(self.blog_output, 6, 0, 1, 2)

        # Save Button
        self.save_button = QPushButton("Save Blog")
        self.save_button.clicked.connect(self.save_blog)
        self.save_button.setEnabled(False)  # Initially disabled
        layout.addWidget(self.save_button, 7, 0, 1, 2)

        self.setLayout(layout)

    def generate_blog(self):
        topic = self.topic_input.text().strip()
        keywords_str = self.keywords_input.text().strip()
        keywords = [k.strip() for k in keywords_str.split(',')] if keywords_str else []
        tone = self.tone_input.text().strip()
        length_str = self.length_input.text().strip()

        if not topic:
            QMessageBox.critical(self, "Error", "Please enter a blog topic.")
            return

        try:
            length_choice = int(length_str)
            if length_choice < 100:
                QMessageBox.critical(self, "Error", "Please enter a realistic blog length (100 words or more).")
                return
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid number for the desired length.")
            return

        self.blog_output.setText("Generating...")
        QApplication.processEvents()  # Keep UI responsive

        generated_text = query_groq_llm(topic, keywords, tone, length_choice)

        if generated_text:
            self.blog_output.setText(generated_text)
            self.save_button.setEnabled(True)
        else:
            self.blog_output.setText("❌ Failed to generate blog content. Check console for details.")
            self.save_button.setEnabled(False)

    def save_blog(self):
        blog_content = self.blog_output.toPlainText()
        if not blog_content:
            QMessageBox.information(self, "Info", "No blog content to save.")
            return

        topic = self.topic_input.text().strip().replace(' ', '_')
        filename, _ = QFileDialog.getSaveFileName(self, "Save Blog", f"{topic}_blog.txt", "Text Files (*.txt)")

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(blog_content)
                QMessageBox.information(self, "Success", f"Blog saved at: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BlogWriterApp()
    ex.show()
    sys.exit(app.exec())