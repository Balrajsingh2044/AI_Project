import gradio as gr
import time
from PIL import Image, ImageDraw
from gtts import gTTS
import os
import warnings
from robust_transcriber import robust_transcribe

warnings.filterwarnings("ignore")

# ==========================================
# MOCK BACKEND FUNCTION
# (Simulates what Shreyansh's FastAPI will eventually return)
# ==========================================
def run_full_assessment(video_file, audio_file):
    if video_file is None:
        raise gr.Error("Please upload a task video first!")
        
    time.sleep(2) # Simulate AI processing time for dramatic effect
    
    # 1. Mock Deepfake Check
    deepfake_status = "### ✅ **Integrity Check: PASSED**\n*No deepfake or looped video detected.*"
    
    # 2. Mock Technique Score & Heatmap
    score = 87.5
    # Create a dummy Grad-CAM heatmap image (Red/Green/Yellow blocks)
    heatmap = Image.new('RGB', (300, 200), color='black')
    draw = ImageDraw.Draw(heatmap)
    draw.rectangle([20, 20, 140, 180], fill='red')      # Poor technique area
    draw.rectangle([150, 20, 280, 180], fill='green')    # Good technique area
    draw.text((80, 10), "Grad-CAM Heatmap", fill="white")
    
    # 3. Mock Fair Wage Range (Pulling logic from your Day 3 Bayesian GNN)
    wage_range_text = "### 💰 **Fair Wage Range (95% Confidence)**\n# ₹3,706  —  ₹4,264\n*Expected Base: ₹3,985*"
    
    # 4. REAL Vernacular Audio Feedback using Robust Transcriber
    if audio_file:
        hindi_text, english_text, confidence = robust_transcribe(audio_file, language="hindi")
        feedback_text = f"ट्रान्सक्रिप्शन: {hindi_text} | Confidence: {confidence}"
    else:
        feedback_text = "कोई ऑडियो नहीं मिला।"

    audio_filename = "feedback_hindi.mp3"

    try:
        tts = gTTS(text=feedback_text, lang='hi')
        tts.save(audio_filename)
    except Exception as e:
        audio_filename = None # Fallback if internet fails
            
    return deepfake_status, score, heatmap, wage_range_text, audio_filename

# ==========================================
# BUILD THE GRADIO INTERFACE (gr.Blocks)
# ==========================================
with gr.Blocks(title="Skill Assessment MVP - Dashboard", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛠️ AI Skill Assessment & Fair Wage Dashboard")
    gr.Markdown("Upload a task video and a voice note to receive an integrity check, technique score, and fair wage prediction.")
    
    with gr.Row():
        # LEFT COLUMN: INPUTS
        with gr.Column(scale=1):
            gr.Markdown("### 📥 Inputs")
            video_input = gr.Video(label="Upload Task Video", height=300)
            audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="Worker Voice Note (Hindi/Tamil)")
            submit_btn = gr.Button("🚀 Run Full AI Assessment", variant="primary", size="lg")
            
        # RIGHT COLUMN: OUTPUTS (DASHBOARD)
        with gr.Column(scale=1):
            gr.Markdown("### 📊 Assessment Dashboard")
            
            # 1. Deepfake Status
            deepfake_out = gr.Markdown(label="Integrity Status", value="*Waiting for assessment...*")
            
            # 2. Technique Score & Heatmap
            with gr.Row():
                score_out = gr.Number(label="Technique Score (%)", interactive=False)
                heatmap_out = gr.Image(label="Technique Heatmap (Grad-CAM)", height=200)
                
            # 3. Fair Wage Range
            wage_out = gr.Markdown(label="Fair Wage Range (95% Confidence)", value="*Waiting...*")
            
            # 4. Vernacular Audio Feedback
            gr.Markdown("### 🔊 Vernacular Audio Feedback")
            tts_out = gr.Audio(label="AI Feedback (Hindi)", type="filepath", interactive=False)

    # Link button to function
    submit_btn.click(
        fn=run_full_assessment,
        inputs=[video_input, audio_input],
        outputs=[deepfake_out, score_out, heatmap_out, wage_out, tts_out]
    )

if __name__ == "__main__":
    demo.launch()