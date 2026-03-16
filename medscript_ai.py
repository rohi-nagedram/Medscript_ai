# ==========================================
# MedScript AI - Final Demo System
# Voice → Transcript → Clinical Report → JSON
# ==========================================

import requests
import whisper
import gradio as gr
import json
import re

# -----------------------------
# CONFIGURATION
# -----------------------------

GROQ_API_KEY = "YOUR_GROQ_API_KEY"

model = whisper.load_model("base")


# -----------------------------
# GENERATE CLINICAL REPORT
# -----------------------------

def generate_report(note):

    prompt = f"""
You are a clinical documentation assistant.

Create:

1. Structured Clinical Summary
2. SOAP Medical Note
3. Medication Safety Check
4. Structured JSON

JSON format:

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
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=payload)

    result = response.json()

    if "choices" not in result:
        return "API Error: " + str(result), {}

    report = result["choices"][0]["message"]["content"]

    json_data = {}

    try:
        json_match = re.search(r"\{.*\}", report, re.DOTALL)

        if json_match:
            json_data = json.loads(json_match.group())

    except:
        json_data = {}

    return report, json_data


# -----------------------------
# PROCESS AUDIO
# -----------------------------

def process_audio(audio_file):

    if audio_file is None:
        return "No audio provided", "No report", {}

    result = model.transcribe(audio_file)

    doctor_note = result["text"]

    report, json_data = generate_report(doctor_note)

    return doctor_note, report, json.dumps(json_data, indent=2)


# -----------------------------
# GRADIO UI
# -----------------------------

interface = gr.Interface(

    fn=process_audio,

    inputs=gr.Audio(
        sources=["microphone", "upload"],
        type="filepath",
        label="Doctor Voice Input"
    ),

    outputs=[
        gr.Textbox(label="Doctor Transcript"),
        gr.Textbox(label="AI Clinical Report"),
        gr.Code(label="Structured Medical Data (JSON)")
    ],

    title="MedScript AI Clinical Assistant",

    description="Convert doctor voice notes into structured clinical documentation using AI"

)

interface.launch()
