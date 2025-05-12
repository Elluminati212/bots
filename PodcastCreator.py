import os
import json
import requests
from gtts import gTTS
from pydub import AudioSegment  # To convert mp3 to wav if needed

# CONFIG
GROQ_API_KEY = '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'
GROQ_MODEL = 'llama3-70b-8192'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

PODCAST_CREATOR_PROMPT = """
You are an expert Podcast Content Creator.

Your task is to take a given topic and generate an engaging blog post that could be used for a podcast.

The blog post should be well-structured, easy to listen to, and sound natural when read aloud. Avoid overly technical jargon unless necessary, and keep a friendly, informative tone.

Make sure to format it in short, clear sentences to sound good in audio format. 

Include a brief intro, several main points, and a nice closing.

Write naturally like a human podcast host speaking to listeners!
"""

def query_groq_llm(topic, length_choice):
    print("Generating blog content...")
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    user_prompt = f"""Create a podcast-friendly blog post about the topic: "{topic}".
The blog should be suitable for a {length_choice}-minute podcast.
Keep a natural, conversational tone and structure it for easy listening."""
    
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": PODCAST_CREATOR_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }
    
    response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        print(f"Error querying Groq LLM: {response.status_code}, {response.text}")
        return None

def generate_audio(text, audio_mp3_filename, audio_wav_filename):
    print("Generating full audio using gTTS...")
    tts = gTTS(text=text, lang='en')
    tts.save(audio_mp3_filename)
    print(f"MP3 Audio saved as {audio_mp3_filename}")

    # Convert MP3 to WAV
    sound = AudioSegment.from_mp3(audio_mp3_filename)
    sound.export(audio_wav_filename, format="wav")
    print(f"WAV Audio saved as {audio_wav_filename}")

def save_blog_to_file(blog_text, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(blog_text)
    print(f"Blog saved as {filename}")

def main():
    print("🎙️ Welcome to the Podcast Creator Agent!")
    topic = input("Enter the topic for your podcast: ").strip()

    while True:
        try:
            length_choice = int(input("How long should the podcast be? (Enter minutes, e.g., 3, 5, 8, 12): ").strip())
            if length_choice <= 0:
                print("Please enter a positive number.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    blog_text = query_groq_llm(topic, length_choice)

    if blog_text:
        safe_topic = topic.replace(' ', '_')
        blog_filename = f"{safe_topic}_blog.txt"
        audio_mp3_filename = f"{safe_topic}_podcast.mp3"
        audio_wav_filename = f"{safe_topic}_podcast.wav"

        save_blog_to_file(blog_text, blog_filename)
        generate_audio(blog_text, audio_mp3_filename, audio_wav_filename)

        print("\n✅ Podcast creation complete!")
        print(f"📝 Blog saved at: {blog_filename}")
        print(f"🎧 Audio podcast saved at: {audio_wav_filename}")
    else:
        print("❌ Failed to generate podcast content. Please try again.")


if __name__ == "__main__":
    main()






































































#2
# import os
# import json
# import wave
# import pyttsx3
# import requests
# import tempfile

# # CONFIG
# GROQ_API_KEY = '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'
# GROQ_MODEL = 'llama3-70b-8192'
# GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# # Initialize
# engine = pyttsx3.init()

# # System prompt for Podcast Creator
# PODCAST_CREATOR_PROMPT = """
# You are an expert Podcast Content Creator.

# Your task is to take a given topic and generate an engaging blog post that could be used for a podcast.

# The blog post should be well-structured, easy to listen to, and sound natural when read aloud. Avoid overly technical jargon unless necessary, and keep a friendly, informative tone.

# Make sure to format it in short, clear sentences to sound good in audio format. 

# Include a brief intro, several main points, and a nice closing.

# Write naturally like a human podcast host speaking to listeners!
# """

# def query_groq_llm(topic, length_choice):
#     print("Generating blog content...")
    
#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }
    
#     user_prompt = f"""Create a podcast-friendly blog post about the topic: "{topic}".
# The blog should be suitable for a {length_choice}-minute podcast.
# Keep a natural, conversational tone and structure it for easy listening."""
    
#     payload = {
#         "model": GROQ_MODEL,
#         "messages": [
#             {"role": "system", "content": PODCAST_CREATOR_PROMPT},
#             {"role": "user", "content": user_prompt}
#         ],
#         "temperature": 0.7
#     }
    
#     response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))
    
#     if response.status_code == 200:
#         return response.json()['choices'][0]['message']['content'].strip()
#     else:
#         print(f"Error querying Groq LLM: {response.status_code}, {response.text}")
#         return None

# def split_text(text, max_length=500):
#     sentences = text.split('. ')
#     chunks = []
#     current_chunk = ""

#     for sentence in sentences:
#         if len(current_chunk) + len(sentence) < max_length:
#             current_chunk += sentence + ". "
#         else:
#             chunks.append(current_chunk.strip())
#             current_chunk = sentence + ". "
#     if current_chunk:
#         chunks.append(current_chunk.strip())
#     return chunks

# def generate_audio(text, audio_filename):
#     print("Generating audio...")
    
#     text_chunks = split_text(text, max_length=500)
#     temp_files = []
    
#     for i, chunk in enumerate(text_chunks):
#         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
#         temp_files.append(temp_file.name)
#         engine.save_to_file(chunk, temp_file.name)
#         engine.runAndWait()
#         temp_file.close()
    
#     # Now combine all temp wav files into final output
#     with wave.open(audio_filename, 'wb') as output_wav:
#         with wave.open(temp_files[0], 'rb') as w:
#             output_wav.setparams(w.getparams())
        
#         for temp_filename in temp_files:
#             with wave.open(temp_filename, 'rb') as w:
#                 output_wav.writeframes(w.readframes(w.getnframes()))
    
#     # Cleanup temp files
#     for f in temp_files:
#         os.remove(f)

#     print(f"Audio saved as {audio_filename}")

# def save_blog_to_file(blog_text, filename):
#     with open(filename, 'w', encoding='utf-8') as f:
#         f.write(blog_text)
#     print(f"Blog saved as {filename}")

# def main():
#     print("🎙️ Welcome to the Podcast Creator Agent!")
#     topic = input("Enter the topic for your podcast: ").strip()
#     print("How long should the podcast be?")
#     print("1. 5 minutes")
#     print("2. 10 minutes")
#     choice = input("Enter 1 or 2: ").strip()

#     if choice == "1":
#         length_choice = "5"
#     elif choice == "2":
#         length_choice = "10"
#     else:
#         print("Invalid choice. Defaulting to 5 minutes.")
#         length_choice = "5"

#     blog_text = query_groq_llm(topic, length_choice)

#     if blog_text:
#         blog_filename = f"{topic.replace(' ', '_')}_blog.txt"
#         audio_filename = f"{topic.replace(' ', '_')}_podcast.wav"

#         save_blog_to_file(blog_text, blog_filename)
#         generate_audio(blog_text, audio_filename)

#         print("\n✅ Podcast creation complete!")
#         print(f"📝 Blog saved at: {blog_filename}")
#         print(f"🎧 Audio podcast saved at: {audio_filename}")
#     else:
#         print("❌ Failed to generate podcast content. Please try again.")

# if __name__ == "__main__":
#     main()


#1
# import os
# import json
# import whisper
# import pyttsx3
# import requests
# import numpy as np
# import sounddevice as sd
# import scipy.io.wavfile as wav

# # CONFIG
# GROQ_API_KEY = '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'
# GROQ_MODEL = 'llama3-70b-8192'  
# GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# SAMPLE_RATE = 16000

# # Initialize
# engine = pyttsx3.init()

# # SYSTEM PROMPT for Groq LLM
# PODCAST_CREATOR_PROMPT = """
# You are an expert Podcast Content Creator.

# Your task is to take a given topic and generate an engaging blog post that could be used for a podcast.

# The blog post should be well-structured, easy to listen to, and sound natural when read aloud. Avoid overly technical jargon unless necessary, and keep a friendly, informative tone.

# Make sure to format it in short, clear sentences to sound good in audio format. 

# Include a brief intro, several main points, and a nice closing.

# Write naturally like a human podcast host speaking to listeners!
# """

# def query_groq_llm(topic):
#     print("Generating blog content...")
    
#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }
    
#     user_prompt = f"""Create a podcast-friendly blog post about the topic: "{topic}".
# Remember to write in a natural, conversational tone as if speaking to an audience."""

#     payload = {
#         "model": GROQ_MODEL,
#         "messages": [
#             {"role": "system", "content": PODCAST_CREATOR_PROMPT},
#             {"role": "user", "content": user_prompt}
#         ],
#         "temperature": 0.7
#     }
    
#     response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))
    
#     if response.status_code == 200:
#         reply = response.json()['choices'][0]['message']['content']
#         print("Blog content generated!")
#         return reply.strip()
#     else:
#         print(f"Error querying Groq LLM: {response.status_code}, {response.text}")
#         return None

# def save_blog_to_file(blog_text, filename):
#     with open(filename, 'w', encoding='utf-8') as f:
#         f.write(blog_text)
#     print(f"Blog saved as {filename}")

# def generate_audio(blog_text, audio_filename):
#     print("Generating audio...")

#     engine.setProperty('rate', 150)  # You can tweak voice speed here if needed
#     engine.save_to_file(blog_text, audio_filename)
#     engine.runAndWait()

#     print(f"Audio saved as {audio_filename}")

# def main():
#     print("🎙️ Welcome to the Podcast Creator Agent!")
#     topic = input("Enter the topic for your podcast: ").strip()

#     blog_text = query_groq_llm(topic)

#     if blog_text:
#         blog_filename = f"{topic.replace(' ', '_')}_blog.txt"
#         audio_filename = f"{topic.replace(' ', '_')}_podcast.wav"

#         save_blog_to_file(blog_text, blog_filename)
#         generate_audio(blog_text, audio_filename)

#         print("\n✅ Podcast creation complete!")
#         print(f"📝 Blog saved at: {blog_filename}")
#         print(f"🎧 Audio podcast saved at: {audio_filename}")
#     else:
#         print("❌ Failed to generate podcast content. Please try again.")

# if __name__ == "__main__":
#     main()
