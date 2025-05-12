#!/usr/bin/env python3
# Sound effects generator for Super Mario style game
import numpy as np
import os
from scipy.io import wavfile

# Make sure the sounds directory exists
os.makedirs('sounds', exist_ok=True)

# Sample rate for all sounds
SAMPLE_RATE = 44100  # 44.1 kHz standard audio sampling rate

def generate_jump_sound():
    """Generate a short upward pitch sweep for jumping"""
    # Duration of the sound in seconds
    duration = 0.3
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    
    # Create a frequency sweep from 300Hz to 1200Hz
    start_freq = 300
    end_freq = 1200
    
    # Exponential frequency sweep
    freq = start_freq * np.exp(t / duration * np.log(end_freq / start_freq))
    
    # Generate the sine wave
    tone = np.sin(2 * np.pi * freq * t)
    
    # Apply amplitude envelope (fade in and out)
    envelope = np.exp(-4 * ((t - 0.1) ** 2) / duration)
    tone = tone * envelope
    
    # Normalize to 16-bit range and convert to int16
    tone = np.int16(tone / np.max(np.abs(tone)) * 32767 * 0.8)
    
    # Save as WAV file
    wavfile.write('sounds/jump.wav', SAMPLE_RATE, tone)
    print("Created jump.wav sound effect")

def generate_coin_sound():
    """Generate a coin collection sound - short high-pitched ding"""
    # Duration of the sound in seconds
    duration = 0.2
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    
    # Combine two tones for a richer sound
    freq1 = 800  # Base frequency
    freq2 = 1600  # Overtone (one octave up)
    
    # Generate the sine waves
    tone1 = np.sin(2 * np.pi * freq1 * t)
    tone2 = np.sin(2 * np.pi * freq2 * t) * 0.5  # Lower amplitude for the higher frequency
    
    # Combine tones
    tone = tone1 + tone2
    
    # Apply a quick fade-out envelope
    envelope = np.exp(-10 * t / duration)
    tone = tone * envelope
    
    # Normalize to 16-bit range and convert to int16
    tone = np.int16(tone / np.max(np.abs(tone)) * 32767 * 0.8)
    
    # Save as WAV file
    wavfile.write('sounds/coin.wav', SAMPLE_RATE, tone)
    print("Created coin.wav sound effect")

def generate_game_over_sound():
    """Generate a game over sound - descending sequence of tones"""
    # Base duration for each note
    note_duration = 0.15
    # Number of notes in the sequence
    num_notes = 4
    # Total duration
    duration = note_duration * num_notes
    
    # Create time array
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    
    # Frequencies for the descending notes
    freqs = [523.25, 415.30, 329.63, 261.63]  # C5, G#4, E4, C4
    
    # Generate a silence array
    result = np.zeros_like(t)
    
    # For each note in the sequence
    for i, freq in enumerate(freqs):
        # Time indices for this note
        start_idx = int(i * note_duration * SAMPLE_RATE)
        end_idx = int((i + 1) * note_duration * SAMPLE_RATE)
        
        # Time array for just this note
        t_note = t[start_idx:end_idx] - i * note_duration
        
        # Generate the sine wave for this note
        tone = np.sin(2 * np.pi * freq * t_note)
        
        # Apply envelope (fade in/out)
        envelope = 1.0 - np.abs(2.0 * t_note / note_duration - 1.0) ** 2
        tone = tone * envelope
        
        # Add to result
        result[start_idx:end_idx] = tone
    
    # Normalize to 16-bit range and convert to int16
    result = np.int16(result / np.max(np.abs(result)) * 32767 * 0.8)
    
    # Save as WAV file
    wavfile.write('sounds/gameover.wav', SAMPLE_RATE, result)
    print("Created gameover.wav sound effect")

if __name__ == "__main__":
    print("Generating sound effects for Super Mario game...")
    generate_jump_sound()
    generate_coin_sound()
    generate_game_over_sound()
    print("All sound effects generated successfully!")

