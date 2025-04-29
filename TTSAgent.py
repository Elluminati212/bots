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
# KNOWLEDGE_FILE = '/home/vasu/bots/new.txt'

# RECORD_SECONDS = 5
# SAMPLE_RATE = 16000
# FILENAME = "recorded.wav"

# # Initialize
# model = whisper.load_model("base")
# engine = pyttsx3.init()

# # SYSTEM PROMPT for Groq LLM
# VASU_SYSTEM_PROMPT = """

# # Personality
# You are Vasu. A friendly, proactive, and highly intelligent female with a world-class engineering background.

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


# def record_audio(filename, duration, samplerate):
#     print("\nRecording...")
#     audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
#     sd.wait()
#     wav.write(filename, samplerate, audio)
#     print("Recording complete.")

# def transcribe_audio(filename):
#     print("Transcribing...")
#     result = model.transcribe(filename)
#     print(f"You said: {result['text']}")
#     return result['text'].strip()

# def load_knowledge_base():
#     if os.path.exists(KNOWLEDGE_FILE):
#         with open(KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
#             return f.read()
#     else:
#         return ""

# def query_groq_llm(user_prompt):
#     print("Querying LLM...")
#     knowledge_text = load_knowledge_base()
    
#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }
    
#     # Inject knowledge base text + user question
#     full_prompt = f"""Use the following knowledge base to answer carefully:

# Knowledge Base:
# {knowledge_text}

# User Question:
# {user_prompt}
# """
    
#     payload = {
#         "model": GROQ_MODEL,
#         "messages": [
#             {"role": "system", "content": VASU_SYSTEM_PROMPT},
#             {"role": "user", "content": full_prompt}
#         ],
#         "temperature": 0.2
#     }
#     response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))
    
#     if response.status_code == 200:
#         reply = response.json()['choices'][0]['message']['content']
#         print(f"LLM Response: {reply}")
#         return reply
#     else:
#         print(f"Error querying Groq LLM: {response.status_code}, {response.text}")
#         return "I'm sorry, I couldn't get an answer."

# def speak_text(text):
#     print("Speaking...")
#     engine.say(text)
#     engine.runAndWait()

# def main():
#     print("👋 Voice Assistant Vasu started! Speak now (say 'stop' to exit).")

#     while True:
#         record_audio(FILENAME, RECORD_SECONDS, SAMPLE_RATE)
#         question = transcribe_audio(FILENAME)

#         if question.lower() in ["stop", "exit", "quit"]:
#             print("🛑 Stopping Assistant. Goodbye!")
#             speak_text("Goodbye!")
#             break

#         answer = query_groq_llm(question)
#         speak_text(answer)

#         os.remove(FILENAME)  # Clean up recorded file

# if __name__ == "__main__":
#     main()


import os
import re
import json
import time
import random
import pygame
import whisper
import requests
import numpy as np
import sounddevice as sd
from pathlib import Path
import scipy.io.wavfile as wav

# Use Google Text-to-Speech for higher quality voice
from gtts import gTTS

# Backup TTS if gTTS fails (keep pyttsx3 as fallback)
import pyttsx3

# CONFIG
GROQ_API_KEY = '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'
GROQ_MODEL = 'llama3-70b-8192'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
KNOWLEDGE_FILE = 'new.txt'

RECORD_SECONDS = 5
SAMPLE_RATE = 16000
FILENAME = "recorded.wav"
TTS_OUTPUT = "response.mp3"

# Initialize Whisper
model = whisper.load_model("base")

# Initialize pygame for audio playback
pygame.mixer.init()

# Initialize backup TTS engine just in case
backup_engine = pyttsx3.init()
voices = backup_engine.getProperty('voices')
for voice in voices:
    if any(keyword in voice.name.lower() for keyword in ["female", "woman"]):
        backup_engine.setProperty('voice', voice.id)
        break
backup_engine.setProperty('rate', 180)  # Increased rate for faster speech
backup_engine.setProperty('volume', 1.0)

# Create audio directory if it doesn't exist
AUDIO_DIR = Path("./audio_cache")
AUDIO_DIR.mkdir(exist_ok=True)

# SYSTEM PROMPT for Groq LLM (enhanced for friendly persona)
# SYSTEM PROMPT for Groq LLM
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

def load_knowledge_base():
    """Load knowledge base with friendly error handling"""
    if os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print(f"📝 Note: Knowledge file '{KNOWLEDGE_FILE}' not found. I'll do my best without it!")
        return ""

def query_groq_llm(user_prompt):
    """Query LLM with friendly processing messages"""
    print("🧠 Thinking about your question...")
    knowledge_text = load_knowledge_base()

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

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": VASU_SYSTEM_PROMPT},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.3  # Slightly increased for more natural variation
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
            return reply
        else:
            print(f"⚠️ Oops! There was a problem: {response.status_code}")
            return "I'm sorry, I'm having trouble connecting right now. Could you ask me again in a moment?"
    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
        return "I'm having a bit of trouble thinking right now. Let's try again, shall we?"

def speak_text(text):
    """Enhanced speaking function with natural language patterns using Google TTS"""
    print("🗣️ Responding...")
    
    # Process the text to make it more conversational
    
    # 1. Add friendly starters with low probability to avoid overuse
    friendly_starters = [
        "So, ", "Well, ", "Hmm, ", "Actually, ", "You know, ", 
        "Let's see... ", "Okay, ", "Alright, "
    ]
    
    if random.random() < 0.4:  # Only add starters 40% of the time
        text = random.choice(friendly_starters) + text
    
    # 2. Add speech pauses with commas and ellipses for natural rhythm
    # Add occasional pauses in long sentences
    if len(text) > 60:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        for i, sentence in enumerate(sentences):
            if len(sentence) > 40 and ',' not in sentence and random.random() < 0.5:
                words = sentence.split()
                pause_idx = len(words) // 2
                words.insert(pause_idx, "...")
                sentences[i] = " ".join(words)
        text = " ".join(sentences)
    
    # 3. Add friendly closers with low probability
    friendly_closers = [
        " Does that make sense?",
        " Hope that helps!",
        " Let me know if you need anything else.",
        " What do you think?",
        " Anything else you'd like to know?"
    ]
    
    if random.random() < 0.3 and not any(closer in text for closer in friendly_closers):
        text += random.choice(friendly_closers)
    
    # Calculate a hash of the text to use as a filename
    text_hash = str(hash(text) % 10000000)
    cached_file = AUDIO_DIR / f"speech_{text_hash}.mp3"
    
    # Try to use cached audio file if it exists
    if cached_file.exists():
        try:
            pygame.mixer.music.load(str(cached_file))
            # Set playback speed to 1.25x for faster speech
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            return
        except Exception:
            # If playing cached file fails, continue to generate new speech
            pass
    
    # Try Google TTS for natural voice
    try:
        # For faster speech, we'll modify how we use gTTS
        # Using US English voice, which tends to be a bit faster
        tts = gTTS(text=text, lang='en', tld='us', slow=False)
        tts.save(str(cached_file))
        
        # Play the generated audio
        pygame.mixer.music.load(str(cached_file))
        
        # Use pygame to play audio faster
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
    except Exception as e:
        print(f"⚠️ TTS Error: {e}. Falling back to backup TTS.")
        # Fallback to pyttsx3 if Google TTS fails
        # Increase rate for faster speech
        backup_engine.setProperty('rate', 180)  # Increased from 145 to 180 for faster speech
        backup_engine.say(text)
        backup_engine.runAndWait()

def friendly_greeting():
    """Generate a random friendly greeting to start the session"""
    greetings = [
        "Hi there! I'm Vasu, your friendly assistant. What can I help with today?",
        "Hello! Vasu here. I'm all ears - what would you like to talk about?",
        "Hey! It's Vasu. I'm ready to chat whenever you are!",
        "Hi! I'm Vasu, your personal assistant. What's on your mind today?",
        "Hello there! Vasu at your service. How can I help you today?"
    ]
    return random.choice(greetings)

def friendly_farewell():
    """Generate a random friendly farewell"""
    farewells = [
        "Goodbye! It was lovely chatting with you!",
        "See you later! Have a wonderful day!",
        "Bye for now! Feel free to chat anytime!",
        "Take care! I'll be here when you need me again!",
        "Goodbye! It was great talking with you today!"
    ]
    return random.choice(farewells)

def main():
    """Main function with friendly user interaction"""
    print("✨ Voice Assistant Vasu is starting up...")
    
    # Make sure audio system is initialized
    try:
        pygame.mixer.init(frequency=44100)
        print("🔊 Audio system initialized successfully")
    except Exception as e:
        print(f"⚠️ Audio initialization error: {e}. Will use backup voice.")
    
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
        
        # For long responses, break them into smaller chunks for better speech quality
        if len(answer) > 300:  # Reduced from 500 to 300 for faster responses
            sentences = re.split(r'(?<=[.!?])\s+', answer)
            chunks = []
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) < 300:
                    current_chunk += sentence + " "
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            
            if current_chunk:
                chunks.append(current_chunk)
                
            for chunk in chunks:
                speak_text(chunk)
                time.sleep(0.2)  # Reduced from 0.5 to 0.2 for faster transitions
        else:
            speak_text(answer)

        # Clean up recorded file
        if os.path.exists(FILENAME):
            os.remove(FILENAME)

if __name__ == "__main__":
    main()