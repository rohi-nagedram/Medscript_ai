# MedScript AI - Final Version (Clean for GitHub)

import os
import requests
import whisper
import gradio as gr
import json
import re

# Load API Key securely
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Load Whisper model
model = whisper.load_model("base")

# -------------------------
# GENERATE CLINICAL REPORT
# -------------------------
def generate_report(note):

    prompt = f"""
You are a clinical documentation assistant.

STRICT RULES:
- Do NOT invent information
- Do NOT infer diagnosis unless explicitly mentioned
- Only use given transcript

Return EXACT format:

===CLINICAL SUMMARY===
Write a professional summary in 2–3 sentences.

===SOAP NOTE===
Use format:
S:
O:
A:
P:

===MEDICATION SAFETY===
If no issues, say:
"No medication risks identified based on transcript."

===JSON===
{{
 "chief_complaint": "",
 "symptoms": [],
 "diagnosis": "",
 "medication": "",
 "dosage": "",
 "frequency": "",
 "follow_up": ""
}}

Doctor Note:
{note}
"""

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if "choices" not in result:
        return "Error generating report", "", "", ""

    report = result["choices"][0]["message"]["content"]

    return report


# -------------------------
# PROCESS AUDIO
# -------------------------
def process_audio(audio):

    if audio is None:
        return "No audio provided", "", "", ""

    audio_path = audio

    # Transcribe
    result = model.transcribe(audio_path)
    transcript = result["text"]

    # Fix common errors
    transcript = transcript.replace("ml", "mg")
    transcript = transcript.strip().capitalize()

    # Generate report
    report = generate_report(transcript)

    # Extract sections
    summary = extract_section(report, "CLINICAL SUMMARY")
    soap = extract_section(report, "SOAP NOTE")
    safety = extract_section(report, "MEDICATION SAFETY")

    return transcript, summary, soap, safety


# -------------------------
# EXTRACT SECTION
# -------------------------
def extract_section(text, section_name):
    pattern = rf"===\s*{section_name}\s*===\n(.*?)(?=\n===|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else "Not found"


# -------------------------
# UI
# -------------------------
interface = gr.Interface(
    fn=process_audio,
    inputs=gr.Audio(type="filepath"),
    outputs=[
        gr.Textbox(label="Doctor Transcript"),
        gr.Textbox(label="Clinical Summary"),
        gr.Textbox(label="SOAP Note"),
        gr.Textbox(label="Medication Safety")
    ],
    title="MedScript AI Clinical Assistant",
    description="Convert doctor voice notes into structured clinical documentation"
)

interface.launch()
