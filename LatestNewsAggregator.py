import os
import json
import requests
from datetime import datetime

# CONFIG
GROQ_API_KEY = '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'   # <-- Replace with your key
GROQ_MODEL = 'llama3-70b-8192'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# System prompt for News Aggregator Agent
NEWS_AGGREGATOR_PROMPT = """
You are a professional Latest News Aggregator Agent.

Your tasks:
- Simulate scanning over 7,000 trusted news sources and platforms.
- Find and summarize the most important and recent news updates about the provided topic.
- Deliver a concise and easy-to-read news digest in natural language, suitable for a busy professional.
- Focus on high-quality, credible, and globally relevant news.
- Summarize in a way that's engaging but factual (no fake headlines or clickbait).

Structure the output with:
- Main Headlines (short)
- Brief Summaries (2–3 sentences per news story)
- Date of News

Output should be clear, easy to skim, and ready to share.
"""

def query_groq_llm(topic):
    print("📰 Aggregating latest news...")

    today_date = datetime.now().strftime("%B %d, %Y")

    user_prompt = f"""
Today's Date: {today_date}

News Topic: {topic}

Instructions:
- Simulate scanning 7k+ news sources.
- Curate 5-7 top news stories around the topic.
- For each story, provide:
    - Headline
    - 2–3 sentence summary
    - Mention today's date

Write naturally, suitable for a daily news digest.
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": NEWS_AGGREGATOR_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3  # Informative, less creative
    }

    response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        print(f"❌ Error querying Groq LLM: {response.status_code}, {response.text}")
        return None

def save_news_to_file(news_text, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(news_text)
    print(f"✅ News summary saved to: {filename}")

def main():
    print("🌍 Welcome to the Latest News Aggregator Agent!")

    topic = input("Enter the News Topic you want updates on (e.g., Technology, Finance, Sports): ").strip()

    if not topic:
        print("❌ Please enter a valid topic.")
        return

    news_summary = query_groq_llm(topic)

    if news_summary:
        print("\n🗞️ --- Latest News Summary ---\n")
        print(news_summary)

        today_date = datetime.now().strftime("%Y-%m-%d")
        safe_topic = topic.replace(' ', '_').lower()
        output_filename = f"{safe_topic}_news_digest_{today_date}.txt"

        save_news_to_file(news_summary, output_filename)

        print(f"\n📩 You can now share or store the summary from: {output_filename}")
    else:
        print("❌ Failed to generate news summary. Please try again.")

if __name__ == "__main__":
    main()
