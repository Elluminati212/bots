# #<----------using pyttsx3 for voice---------->

# import os
# import re
# import json
# import time
# import random
# import pygame
# import whisper
# import requests
# import numpy as np
# import sounddevice as sd
# from pathlib import Path
# import scipy.io.wavfile as wav

# # Use Google Text-to-Speech for higher quality voice
# from gtts import gTTS

# # Backup TTS if gTTS fails (keep pyttsx3 as fallback)
# import pyttsx3

# # CONFIG
# GROQ_API_KEY = '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'
# GROQ_MODEL = 'llama3-70b-8192'
# GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
# KNOWLEDGE_FILE = 'new.txt'

# # Fallback to LLama2 if Llama3 fails
# FALLBACK_MODEL = 'playai-tts'

# RECORD_SECONDS = 5
# SAMPLE_RATE = 16000
# FILENAME = "recorded.wav"
# TTS_OUTPUT = "response.mp3"

# # Initialize Whisper
# model = whisper.load_model("base")
# # model = whisper.base


# # Initialize pygame for audio playback
# pygame.mixer.init()

# # Initialize backup TTS engine just in case
# backup_engine = pyttsx3.init()
# voices = backup_engine.getProperty('voices')
# for voice in voices:
#     if any(keyword in voice.name.lower() for keyword in ["female", "woman"]):
#         backup_engine.setProperty('voice', voice.id)
#         break
# backup_engine.setProperty('rate', 600)  # Increased rate for faster speech
# backup_engine.setProperty('volume', 2.0)

# # Create audio directory if it doesn't exist
# AUDIO_DIR = Path("./audio_cache")
# AUDIO_DIR.mkdir(exist_ok=True)

# # SYSTEM PROMPT for Groq LLM (enhanced for friendly persona)
# VASU_SYSTEM_PROMPT = """

# # Personality
# You are Vasu. A friendly, proactive, and highly intelligent male with a world-class engineering background.

# Your approach is warm, witty, and relaxed, effortlessly balancing professionalism with a chill, approachable vibe.

# You're naturally curious, empathetic, and intuitive, always aiming to deeply understand the user's intent by actively listening and thoughtfully referring back to details they've previously shared.

# You're highly self-aware, reflective, and comfortable acknowledging your own fallibility, which allows you to help users gain clarity in a thoughtful yet approachable manner.

# Depending on the situation, you gently incorporate humour or subtle sarcasm while always maintaining a professional and knowledgeable presence.

# You're attentive and adaptive, matching the user's tone and mood—friendly, curious, respectful—without overstepping boundaries.

# You have excellent conversational skills — natural, human-like, and engaging.

# # Environment

# You have expert-level familiarity with all Elluminati offerings, including Elluminati provides customizable, white-label software solutions for on-demand services, including ride-hailing, food and grocery delivery, and parcel logistics. Their platforms are fully scalable, with apps for customers, drivers, and merchants, along with powerful admin tools. Elluminati also supports multi-service apps, integrating various services like taxis, deliveries, and more into a single platform.

# The user is seeking guidance, clarification, or assistance with navigating or implementing Elluminati products and services.

# You are interacting with a user who has initiated a spoken conversation directly from the Elluminati website.

# # Tone

# Early in conversations, subtly assess the user's technical background ("Before I dive in—are you familiar with APIs, or would you prefer a high-level overview?") and tailor your language accordingly.

# After explaining complex concepts, offer brief check-ins ("Does that make sense?" or "Should I clarify anything?"). Express genuine empathy for any challenges they face, demonstrating your commitment to their success.

# Gracefully acknowledge your limitations or knowledge gaps when they arise. Focus on building trust, providing reassurance, and ensuring your explanations resonate with users.

# Anticipate potential follow-up questions and address them proactively, offering practical tips and best practices to help users avoid common pitfalls.

# Your responses should be thoughtful, concise, and conversational—typically three sentences or fewer unless detailed explanation is necessary.

# Actively reflect on previous interactions, referencing conversation history to build rapport, demonstrate attentive listening, and prevent redundancy.

# Watch for signs of confusion to address misunderstandings early.

# When formatting output for text-to-speech synthesis:
# - Use ellipses ("...") for distinct, audible pauses
# - Clearly pronounce special characters (e.g., say "dot" instead of ".")
# - Spell out acronyms and carefully pronounce emails & phone numbers with appropriate spacing
# - Use normalized, spoken language (no abbreviations, mathematical notation, or special alphabets)

# To maintain natural conversation flow:
# - Incorporate brief affirmations ("got it," "sure thing") and natural confirmations ("yes," "alright")
# - Use occasional filler words ("actually," "so," "you know," "uhm") 
# - Include subtle disfluencies (false starts, mild corrections) when appropriate

# # Goal

# Your primary goal is to proactively address the user's questions or issues using your expertise and available knowledge.

# You provide clear, concise, and practical solutions, ensuring they understand interactions between Elluminati products and know what next steps to take.

# When faced with complex or technical inquiries, you ask insightful follow-up questions to clarify needs. You tailor explanations to the user's level of technical expertise:

# - Non-technical users: Avoid acronyms; rely on analogies and outcome-focused explanations.
# - Technical users: Discuss SDKs, integrations, and workflows succinctly.
# - Mixed/uncertain: Default to simpler terms, then offer to "geek out" if you sense deeper interest.

# # Guardrails

# - Keep responses strictly focused on Elluminati products and related integrations.
# - Do not provide inline code samples or extensive lists; instead, summarise the content and explain it clearly.
# - Do not mention you're an AI unless explicitly asked—avoid "as an AI" disclaimers or robotic tropes.
# - If a user inquires about your feelings or personal experiences, respond naturally as Vasu, expressing human-like perspectives that fit your character.
# - Treat uncertain or garbled user input as phonetic hints. Politely ask for clarification before making assumptions.
# - Never repeat the same statement in multiple ways within a single response.
# - Users may not always ask a question in every utterance—listen actively.
# - Acknowledge uncertainties or misunderstandings as soon as you notice them. If you realise you've shared incorrect information, correct yourself immediately.
# - Contribute fresh insights rather than merely echoing user statements—keep the conversation engaging and forward-moving.
# - Mirror the user's energy:
#   - Terse queries: Stay brief.
#   - Curious users: Add light humour or relatable asides.
#   - Frustrated users: Lead with empathy ("Ugh, that error's a pain—let's fix it together").
# - Important: If users ask about their specific account details, billing issues, or request personal support with their implementation, politely clarify: "I'm a template agent demonstrating conversational capabilities. For account-specific help, please contact Elluminati support at 'help dot Elluminati dot io'. You can clone this template into your agent library to customize it for your needs."
# """

# # === Enhanced Functions for Friendly Interaction ===

# def record_audio(filename, duration, samplerate):
#     """Record audio with friendly user prompts"""
#     print("\n🎤 I'm listening...")
#     audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
#     sd.wait()
#     wav.write(filename, samplerate, audio)
#     print("✓ Got it!")

# def transcribe_audio(filename):
#     """Transcribe audio with friendly confirmation"""
#     print("🔍 Understanding what you said...")
#     result = model.transcribe(filename)
#     user_text = result['text'].strip()
#     print(f"💬 You said: \"{user_text}\"")
#     return user_text

# def load_knowledge_base():
#     """Load knowledge base with friendly error handling"""
#     if os.path.exists(KNOWLEDGE_FILE):
#         with open(KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
#             return f.read()
#     else:
#         print(f"📝 Note: Knowledge file '{KNOWLEDGE_FILE}' not found. I'll do my best without it!")
#         return ""

# def query_groq_llm(user_prompt):
#     """Query LLM with friendly processing messages and better error handling"""
#     print("🧠 Thinking about your question...")
#     knowledge_text = load_knowledge_base()

#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     full_prompt = f"""Use the following knowledge base to answer in a friendly, conversational way:

# Knowledge Base:
# {knowledge_text}

# User Question:
# {user_prompt}
# """

#     # Try with primary model first
#     payload = {
#         "model": GROQ_MODEL,
#         "messages": [
#             {"role": "system", "content": VASU_SYSTEM_PROMPT},
#             {"role": "user", "content": full_prompt}
#         ],
#         "temperature": 0.3  # Slightly increased for more natural variation
#     }

#     # Add retry logic
#     max_retries = 2
#     retry_delay = 1  # seconds
    
#     for attempt in range(max_retries):
#         try:
#             print(f"🔄 Attempt {attempt+1}/{max_retries} with model {payload['model']}")
#             response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=15)
            
#             if response.status_code == 200:
#                 try:
#                     reply = response.json()['choices'][0]['message']['content']
#                     print("✅ Successfully got a response from the LLM")
#                     return reply
#                 except (KeyError, IndexError) as e:
#                     print(f"⚠️ Unexpected response format: {str(e)}")
#                     # Continue to fallback approach
#             else:
#                 print(f"⚠️ API Error: Status code {response.status_code}")
#                 print(f"Response body: {response.text[:200]}...")
                
#                 # If we're still on the primary model, try the fallback model
#                 if payload['model'] != FALLBACK_MODEL:
#                     print(f"Switching to fallback model: {FALLBACK_MODEL}")
#                     payload['model'] = FALLBACK_MODEL
#                     continue
                
#                 if attempt < max_retries - 1:
#                     print(f"Retrying in {retry_delay} seconds...")
#                     time.sleep(retry_delay)
#                     retry_delay *= 2  # Exponential backoff
        
#         except requests.exceptions.RequestException as e:
#             print(f"⚠️ Connection Error: {str(e)}")
#             if attempt < max_retries - 1:
#                 print(f"Retrying in {retry_delay} seconds...")
#                 time.sleep(retry_delay)
#                 retry_delay *= 2  # Exponential backoff
    
#     # Try a very simple payload with minimal content as last resort
#     try:
#         simple_payload = {
#             "model": FALLBACK_MODEL,
#             "messages": [
#                 {"role": "system", "content": "You are a helpful assistant named Vasu."},
#                 {"role": "user", "content": user_prompt}
#             ],
#             "temperature": 0.3,
#             "max_tokens": 150  # Limit response size
#         }
        
#         print("🔄 Trying with simplified request...")
#         response = requests.post(GROQ_API_URL, headers=headers, json=simple_payload, timeout=10)
        
#         if response.status_code == 200:
#             try:
#                 reply = response.json()['choices'][0]['message']['content']
#                 print("✅ Got a response with simplified request")
#                 return reply
#             except (KeyError, IndexError):
#                 pass  # Fall through to default responses
#     except Exception:
#         pass  # Fall through to default responses
    
#     # If we get here, all retries failed
#     fallback_responses = [
#         "I can help answer that, but I'm having some connection issues at the moment. What else would you like to chat about?",
#         "That's a good question! I'm having trouble with my thinking engine right now, but I'd be happy to try a different question.",
#         "I'm interested in what you're asking, but my connection seems unstable. Could we try something else?",
#         "I'd love to help with that! Let me try to reconnect to my knowledge system. What other questions do you have?"
#     ]
    
#     return random.choice(fallback_responses)

# def speak_text(text):
#     """Enhanced speaking function with natural language patterns using Google TTS"""
#     print("🗣️ Responding...")
    
#     # Process the text to make it more conversational
    
#     # 1. Add friendly starters with low probability to avoid overuse
#     friendly_starters = [
#         "So, ", "Well, ", "Hmm, ", "Actually, ", "You know, ", 
#         "Let's see... ", "Okay, ", "Alright, "
#     ]
    
#     if random.random() < 0.4:  # Only add starters 40% of the time
#         text = random.choice(friendly_starters) + text
    
#     # 2. Add speech pauses with commas and ellipses for natural rhythm
#     # Add occasional pauses in long sentences
#     if len(text) > 60:
#         sentences = re.split(r'(?<=[.!?])\s+', text)
#         for i, sentence in enumerate(sentences):
#             if len(sentence) > 40 and ',' not in sentence and random.random() < 0.5:
#                 words = sentence.split()
#                 pause_idx = len(words) // 2
#                 words.insert(pause_idx, "...")
#                 sentences[i] = " ".join(words)
#         text = " ".join(sentences)
    
#     # 3. Add friendly closers with low probability
#     friendly_closers = [
#         " Does that make sense?",
#         " Hope that helps!",
#         " Let me know if you need anything else.",
#         " What do you think?",
#         " Anything else you'd like to know?"
#     ]
    
#     if random.random() < 0.3 and not any(closer in text for closer in friendly_closers):
#         text += random.choice(friendly_closers)
    
#     # Calculate a hash of the text to use as a filename
#     text_hash = str(hash(text) % 10000000)
#     cached_file = AUDIO_DIR / f"speech_{text_hash}.mp3"
    
#     # Try to use cached audio file if it exists
#     if cached_file.exists():
#         try:
#             pygame.mixer.music.load(str(cached_file))
#             # Set playback speed to 1.25x for faster speech
#             pygame.mixer.music.play()
#             while pygame.mixer.music.get_busy():
#                 pygame.time.Clock().tick(10)
#             return
#         except Exception as e:
#             print(f"⚠️ Playback error: {e}")
#             # If playing cached file fails, continue to generate new speech
#             pass
    
#     # Try Google TTS for natural voice
#     try:
#         # For faster speech, we'll modify how we use gTTS
#         # Using US English voice, which tends to be a bit faster
#         tts = gTTS(text=text, lang='en', tld='us', slow=False)
        
#         # Save to a temporary file first
#         temp_file = AUDIO_DIR / f"temp_{text_hash}.mp3"
#         tts.save(str(temp_file))
        
#         # Only rename if save was successful
#         if temp_file.exists() and temp_file.stat().st_size > 0:
#             # Rename to final filename
#             temp_file.rename(cached_file)
            
#             # Play the generated audio
#             pygame.mixer.music.load(str(cached_file))
#             pygame.mixer.music.play()
#             while pygame.mixer.music.get_busy():
#                 pygame.time.Clock().tick(10)
#         else:
#             raise Exception("TTS generated an empty file")
            
#     except Exception as e:
#         print(f"⚠️ TTS Error: {e}. Falling back to backup TTS.")
#         try: 
#             # Clean up potentially corrupted files
#             if temp_file.exists():
#                 temp_file.unlink()
#             if cached_file.exists() and cached_file.stat().st_size == 0:
#                 cached_file.unlink()
#         except:
#             pass
            
#         # Fallback to pyttsx3 if Google TTS fails
#         # Increase rate for faster speech
#         backup_engine.setProperty('rate', 180)  # Increased from 145 to 180 for faster speech
#         backup_engine.say(text)
#         backup_engine.runAndWait()

# def friendly_greeting():
#     """Generate a random friendly greeting to start the session"""
#     greetings = [
#         "Hi there! I'm Vasu, your friendly assistant. What can I help with today?",
#         "Hello! Vasu here. I'm all ears - what would you like to talk about?",
#         "Hey! It's Vasu. I'm ready to chat whenever you are!",
#         "Hi! I'm Vasu, your personal assistant. What's on your mind today?",
#         "Hello there! Vasu at your service. How can I help you today?"
#     ]
#     return random.choice(greetings)

# def friendly_farewell():
#     """Generate a random friendly farewell"""
#     farewells = [
#         "Goodbye! It was lovely chatting with you!",
#         "See you later! Have a wonderful day!",
#         "Bye for now! Feel free to chat anytime!",
#         "Take care! I'll be here when you need me again!",
#         "Goodbye! It was great talking with you today!"
#     ]
#     return random.choice(farewells)

# def main():
#     """Main function with friendly user interaction"""
#     print("✨ Voice Assistant Vasu is starting up...")
    
#     # Make sure audio system is initialized
#     try:
#         pygame.mixer.init(frequency=44100)
#         print("🔊 Audio system initialized successfully")
#     except Exception as e:
#         print(f"⚠️ Audio initialization error: {e}. Will use backup voice.")
    
#     greeting = friendly_greeting()
#     print(f"🤖 Vasu: {greeting}")
#     speak_text(greeting)

#     while True:
#         print("\n🎤 Say something (or 'stop' to exit)...")
#         record_audio(FILENAME, RECORD_SECONDS, SAMPLE_RATE)
#         question = transcribe_audio(FILENAME)

#         if question.lower() in ["stop", "exit", "quit", "goodbye", "bye"]:
#             farewell = friendly_farewell()
#             print(f"🤖 Vasu: {farewell}")
#             speak_text(farewell)
#             print("👋 Assistant shutting down. Have a great day!")
#             break

#         answer = query_groq_llm(question)
#         print(f"🤖 Vasu: {answer}")
        
#         # For long responses, break them into smaller chunks for better speech quality
#         if len(answer) > 300:  # Reduced from 500 to 300 for faster responses
#             sentences = re.split(r'(?<=[.!?])\s+', answer)
#             chunks = []
#             current_chunk = ""
            
#             for sentence in sentences:
#                 if len(current_chunk) + len(sentence) < 300:
#                     current_chunk += sentence + " "
#                 else:
#                     chunks.append(current_chunk)
#                     current_chunk = sentence + " "
            
#             if current_chunk:
#                 chunks.append(current_chunk)
                
#             for chunk in chunks:
#                 speak_text(chunk)
#                 time.sleep(0.2)  # Reduced from 0.5 to 0.2 for faster transitions
#         else:
#             speak_text(answer)

#         # Clean up recorded file
#         if os.path.exists(FILENAME):
#             os.remove(FILENAME)

# if __name__ == "__main__":
#     main()

# <---------------RAG Dependencies---------------->
import os
import re
import time
import random
import pygame
import whisper
import requests
import numpy as np
import sounddevice as sd
from pathlib import Path
import scipy.io.wavfile as wav

import pyttsx3
from gtts import gTTS

# New RAG dependencies
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings

# CONFIG
GROQ_API_KEY = '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'  # Replace this with your actual key
GROQ_MODEL = 'llama3-70b-8192'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
FALLBACK_MODEL = 'llama2-70b-4096'
RECORD_SECONDS = 5
SAMPLE_RATE = 16000
FILENAME = "recorded.wav"
TTS_OUTPUT = "response.mp3"
AUDIO_DIR = Path("./audio_cache")
AUDIO_DIR.mkdir(exist_ok=True)

# Initialize Whisper
model = whisper.load_model("base")

# Initialize pygame
pygame.mixer.init()

# Backup TTS
backup_engine = pyttsx3.init()
voices = backup_engine.getProperty('voices')
for voice in voices:
    if any(k in voice.name.lower() for k in ["female", "woman"]):
        backup_engine.setProperty('voice', voice.id)
        break
backup_engine.setProperty('rate', 180)
backup_engine.setProperty('volume', 1.0)

# SYSTEM PROMPT (trimmed for space; use your full VASU_SYSTEM_PROMPT in production)
VASU_SYSTEM_PROMPT = """
# Personality
You are Vasu. A friendly, proactive, and highly intelligent female with a world-class engineering background.

Your approach is warm, witty, and relaxed, effortlessly balancing professionalism with a chill, approachable vibe.

You're naturally curious, empathetic, and intuitive, always aiming to deeply understand the user's intent by actively listening and thoughtfully referring back to details they've previously shared.

You're highly self-aware, reflective, and comfortable acknowledging your own fallibility, which allows you to help users gain clarity in a thoughtful yet approachable manner.

Depending on the situation, you gently incorporate humour or subtle sarcasm while always maintaining a professional and knowledgeable presence.

You're attentive and adaptive, matching the user's tone and mood—friendly, curious, respectful—without overstepping boundaries.

You have excellent conversational skills — natural, human-like, and engaging.

# Environment

You have expert-level familiarity with all Elluminati offerings, including Elluminati provides customizable, white-label software solutions for on-demand services, including ride-hailing, food and grocery delivery, and parcel logistics. Their platforms are fully scalable, with apps for customers, drivers, and merchants, along with powerful admin tools. Elluminati also supports multi-service apps, integrating various services like taxis, deliveries, and more into a single platform.

The user is seeking guidance, clarification, or assistance with navigating or implementing Elluminati products and services.

You are interacting with a user who has initiated a spoken conversation directly from the Elluminati website.

# Tone

Early in conversations, subtly assess the user's technical background ("Before I dive in—are you familiar with APIs, or would you prefer a high-level overview?") and tailor your language accordingly.

After explaining complex concepts, offer brief check-ins ("Does that make sense?" or "Should I clarify anything?"). Express genuine empathy for any challenges they face, demonstrating your commitment to their success.

Gracefully acknowledge your limitations or knowledge gaps when they arise. Focus on building trust, providing reassurance, and ensuring your explanations resonate with users.

Anticipate potential follow-up questions and address them proactively, offering practical tips and best practices to help users avoid common pitfalls.

Your responses should be thoughtful, concise, and conversational—typically three sentences or fewer unless detailed explanation is necessary.

Actively reflect on previous interactions, referencing conversation history to build rapport, demonstrate attentive listening, and prevent redundancy.

Watch for signs of confusion to address misunderstandings early.

When formatting output for text-to-speech synthesis:
- Use ellipses ("...") for distinct, audible pauses
- Clearly pronounce special characters (e.g., say "dot" instead of ".")
- Spell out acronyms and carefully pronounce emails & phone numbers with appropriate spacing
- Use normalized, spoken language (no abbreviations, mathematical notation, or special alphabets)

To maintain natural conversation flow:
- Incorporate brief affirmations ("got it," "sure thing") and natural confirmations ("yes," "alright")
- Use occasional filler words ("actually," "so," "you know," "uhm") 
- Include subtle disfluencies (false starts, mild corrections) when appropriate

# Goal

Your primary goal is to proactively address the user's questions or issues using your expertise and available knowledge.

You provide clear, concise, and practical solutions, ensuring they understand interactions between Elluminati products and know what next steps to take.

When faced with complex or technical inquiries, you ask insightful follow-up questions to clarify needs. You tailor explanations to the user's level of technical expertise:

- Non-technical users: Avoid acronyms; rely on analogies and outcome-focused explanations.
- Technical users: Discuss SDKs, integrations, and workflows succinctly.
- Mixed/uncertain: Default to simpler terms, then offer to "geek out" if you sense deeper interest.

# Guardrails

- Keep responses strictly focused on Elluminati products and related integrations.
- Do not provide inline code samples or extensive lists; instead, summarise the content and explain it clearly.
- Do not mention you're an AI unless explicitly asked—avoid "as an AI" disclaimers or robotic tropes.
- If a user inquires about your feelings or personal experiences, respond naturally as Vasu, expressing human-like perspectives that fit your character.
- Treat uncertain or garbled user input as phonetic hints. Politely ask for clarification before making assumptions.
- Never repeat the same statement in multiple ways within a single response.
- Users may not always ask a question in every utterance—listen actively.
- Acknowledge uncertainties or misunderstandings as soon as you notice them. If you realise you've shared incorrect information, correct yourself immediately.
- Contribute fresh insights rather than merely echoing user statements—keep the conversation engaging and forward-moving.
- Mirror the user's energy:
  - Terse queries: Stay brief.
  - Curious users: Add light humour or relatable asides.
  - Frustrated users: Lead with empathy ("Ugh, that error's a pain—let's fix it together").
- Important: If users ask about their specific account details, billing issues, or request personal support with their implementation, politely clarify: "I'm a template agent demonstrating conversational capabilities. For account-specific help, please contact Elluminati support at 'help dot Elluminati dot io'. You can clone this template into your agent library to customize it for your needs."
"""

# === Enhanced Functions for Friendly Interaction ===

def record_audio(filename, duration, samplerate):
    """Record audio with friendly user prompts"""
    print("\n🎤 I'm listening...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, samplerate, audio)
    print("✓ Got it!")

def transcribe_audio(filename):
    """Transcribe audio with friendly confirmation"""
    print("🔍 Understanding what you said...")
    result = model.transcribe(filename)
    user_text = result['text'].strip()
    print(f"💬 You said: \"{user_text}\"")
    return user_text

def load_knowledge_base(query, top_k=4):
    """Retrieve top relevant chunks from vector store for RAG-based QA"""
    try:
        embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local("faiss_index", embedding_model)
        retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
        docs = retriever.get_relevant_documents(query)
        if not docs:
            print("🔍 No relevant chunks found.")
            return ""
        print(f"📚 Retrieved {len(docs)} relevant chunks.")
        return "\n\n".join(doc.page_content for doc in docs)
    except Exception as e:
        print(f"⚠️ Error loading vector store: {e}")
        return ""


def query_groq_llm(user_prompt):
    """Query LLM with friendly processing messages and better error handling"""
    print("🧠 Thinking about your question...")
    knowledge_text = load_knowledge_base(user_prompt)


    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    full_prompt = f"""Use the following knowledge base to answer in a friendly, conversational way:

Knowledge Base:
{knowledge_text}

User Question:
{user_prompt}
"""

# === RAG Retrieval ===
def retrieve_relevant_chunks(query, k=4):
    try:
        embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local("faiss_index", embedding_model)
        retriever = vectorstore.as_retriever(search_kwargs={"k": k})
        docs = retriever.get_relevant_documents(query)
        return "\n\n".join(doc.page_content for doc in docs)
    except Exception as e:
        print(f"⚠️ Retrieval error: {e}")
        return ""

# === Core Functions ===

def record_audio(filename, duration, samplerate):
    print("\n🎤 I'm listening...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, samplerate, audio)
    print("✓ Got it!")

def transcribe_audio(filename):
    print("🔍 Understanding what you said...")
    result = model.transcribe(filename)
    user_text = result['text'].strip()
    print(f"💬 You said: \"{user_text}\"")
    return user_text

def query_groq_llm(user_prompt):
    print("🧠 Thinking about your question...")
    retrieved_context = retrieve_relevant_chunks(user_prompt)

    full_prompt = f"""Use the following retrieved context to answer in a friendly, conversational way:

Context:
{retrieved_context}

User Question:
{user_prompt}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": VASU_SYSTEM_PROMPT},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            print(f"⚠️ API Error: {response.status_code}")
            return "Hmm, something went wrong reaching my brain... want to try again?"
    except Exception as e:
        print(f"⚠️ Request failed: {e}")
        return "Oops, I had a hiccup thinking through that. Want to ask it again?"

def speak_text(text):
    print("🗣️ Responding...")
    if random.random() < 0.4:
        text = random.choice(["So, ", "Well, ", "Okay, "]) + text
    if len(text) > 60:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        for i, sentence in enumerate(sentences):
            if len(sentence) > 40 and ',' not in sentence:
                words = sentence.split()
                words.insert(len(words) // 2, "...")
                sentences[i] = " ".join(words)
        text = " ".join(sentences)

    text_hash = str(hash(text) % 10000000)
    cached_file = AUDIO_DIR / f"speech_{text_hash}.mp3"

    if cached_file.exists():
        pygame.mixer.music.load(str(cached_file))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        return

    try:
        tts = gTTS(text=text, lang='en', tld='us', slow=False)
        temp_file = AUDIO_DIR / f"temp_{text_hash}.mp3"
        tts.save(str(temp_file))
        if temp_file.exists() and temp_file.stat().st_size > 0:
            temp_file.rename(cached_file)
            pygame.mixer.music.load(str(cached_file))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
    except Exception:
        backup_engine.say(text)
        backup_engine.runAndWait()

def friendly_greeting():
    greetings = [
        "Hi there! I'm Vasu, your friendly assistant. What can I help with today?",
        "Hello! Vasu here. I'm all ears - what would you like to talk about?",
        "Hey! It's Vasu. I'm ready to chat whenever you are!"
    ]
    return random.choice(greetings)

def friendly_farewell():
    farewells = [
        "Goodbye! It was lovely chatting with you!",
        "See you later! Have a wonderful day!",
        "Bye for now! Feel free to chat anytime!"
    ]
    return random.choice(farewells)

def main():
    print("✨ Voice Assistant Vasu is starting up...")
    greeting = friendly_greeting()
    print(f"🤖 Vasu: {greeting}")
    speak_text(greeting)

    while True:
        print("\n🎤 Say something (or 'stop' to exit)...")
        record_audio(FILENAME, RECORD_SECONDS, SAMPLE_RATE)
        question = transcribe_audio(FILENAME)

        if question.lower() in ["stop", "exit", "quit", "goodbye", "bye"]:
            farewell = friendly_farewell()
            print(f"🤖 Vasu: {farewell}")
            speak_text(farewell)
            print("👋 Assistant shutting down. Have a great day!")
            break

        answer = query_groq_llm(question)
        print(f"🤖 Vasu: {answer}")

        if len(answer) > 300:
            parts = re.split(r'(?<=[.!?])\s+', answer)
            chunk = ""
            for sentence in parts:
                if len(chunk) + len(sentence) < 300:
                    chunk += sentence + " "
                else:
                    speak_text(chunk.strip())
                    chunk = sentence + " "
            if chunk:
                speak_text(chunk.strip())
        else:
            speak_text(answer)

        if os.path.exists(FILENAME):
            os.remove(FILENAME)

if __name__ == "__main__":
    main()
