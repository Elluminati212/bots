import os
import json
import requests

# CONFIG
GROQ_API_KEY = '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'
GROQ_MODEL = 'llama3-70b-8192'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# System prompt for Blog Writer Agent
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

Your output should be a ready-to-publish blog article that resonates with readers and ranks well on search engines.
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
        "temperature": 0.5  # more factual, less creative
    }

    response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        print(f"Error querying Groq LLM: {response.status_code}, {response.text}")
        return None

def save_blog_to_file(blog_text, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(blog_text)
    print(f"📝 Blog saved at: {filename}")

def main():
    print("✍️ Welcome to the Blog Writer Agent!")
    
    topic = input("Enter the blog topic: ").strip()
    
    keywords_input = input("Enter keywords to target (comma-separated, or press Enter to skip): ").strip()
    keywords = [k.strip() for k in keywords_input.split(',')] if keywords_input else []

    tone = input("Enter the preferred tone of voice (e.g., friendly, professional, conversational), or press Enter for default: ").strip()
    
    while True:
        try:
            length_choice = int(input("Desired blog length? (Enter 500, 1000, 1500, 2000+ words): ").strip())
            if length_choice < 100:
                print("Please enter a realistic blog length (500 words or more).")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    blog_text = query_groq_llm(topic, keywords, tone, length_choice)

    if blog_text:
        safe_topic = topic.replace(' ', '_')
        blog_filename = f"{safe_topic}_blog.txt"
        save_blog_to_file(blog_text, blog_filename)

        print("\n✅ Blog writing complete! Ready for publishing.")
    else:
        print("❌ Failed to generate blog content. Please try again.")

if __name__ == "__main__":
    main()
