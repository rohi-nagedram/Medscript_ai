# MedScript AI 🩺

MedScript AI is an AI-powered clinical documentation assistant that converts doctor voice notes into structured medical reports.

## 🚀 Features

- Voice → Text using Whisper
- Clinical Summary generation
- SOAP Note (Subjective, Objective, Assessment, Plan)
- Medication Safety Check
- Structured JSON output

## 🧠 How it Works

1. Doctor records voice note
2. Whisper converts speech to text
3. LLM (Groq API) generates structured medical report
4. Output displayed in clean UI

## 🏗️ Architecture

Audio Input → Whisper → LLM (Groq) → Structured Output → Gradio UI

## ⚙️ Tech Stack

- Python
- Whisper (Speech-to-Text)
- Groq API (LLM)
- Gradio (UI)
- Hugging Face Spaces (Deployment)

## 📦 Setup

```bash
pip install -r requirements.txt
