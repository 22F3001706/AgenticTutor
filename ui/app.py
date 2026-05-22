# WHY GRADIO?
# Gradio lets you build web UIs with pure Python.
# No HTML/CSS/JS needed. Perfect for AI apps.
# Every UI element is a Python function call.

import gradio as gr
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.loader import load_and_split
from rag.embeddings import build_vectorstore, load_vectorstore
from rag.chain import build_chain
from gtts import gTTS
import tempfile

# ── CONFIG ──────────────────────────────────────────────
# This is your content map.
# To add more classes/subjects/chapters, just edit this dict.
CONTENT = {
    "Class 9": {
        "Science": {
            "Ch 1 - Matter in our surroundings":   "BOOKS/C9S/CH1.pdf",
            "Ch 2 - Is matter around us pure?":    "BOOKS/C9S/CH2.pdf",
            "Ch 3 - Atoms and molecules":          "BOOKS/C9S/CH3.pdf",
            "Ch 4 - Structure of the atom":        "BOOKS/C9S/CH4.pdf",
        },
        "Maths": {
            "Ch 1 - Number systems":               "BOOKS/C9M/CH1.pdf",
        }
    }
}

# ── HELPERS ─────────────────────────────────────────────
def get_subjects(class_name):
    # When class changes → update subject dropdown choices
    subjects = list(CONTENT.get(class_name, {}).keys())
    return gr.Dropdown(choices=subjects, value=subjects[0] if subjects else None)

def get_chapters(class_name, subject):
    # When subject changes → update chapter dropdown choices
    chapters = list(CONTENT.get(class_name, {}).get(subject, {}).keys())
    return gr.Dropdown(choices=chapters, value=chapters[0] if chapters else None)

def load_chapter(class_name, subject, chapter):
    pdf_path = CONTENT[class_name][subject][chapter]

    if not os.path.exists(pdf_path):
        return "<p>PDF not found.</p>", None, f"PDF not found at {pdf_path}"

    vs_path = f"vectorstore/{class_name}_{subject}_{chapter}".replace(" ", "_")

    if os.path.exists(vs_path):
        vectorstore = load_vectorstore(vs_path)
        msg = f"Loaded: {chapter}"
    else:
        chunks = load_and_split(pdf_path)
        vectorstore = build_vectorstore(chunks, vs_path)
        msg = f"Ready: {chapter}"

    chain = build_chain(vectorstore)

    # Fix — use relative path directly, not absolute
    pdf_html = f'''
    <iframe
        src="/gradio_api/file={pdf_path}"
        width="100%"
        height="500px"
        style="border: none; border-radius: 8px;">
    </iframe>
    '''
    return pdf_html, chain, msg

def answer_question(question, chain, chat_history, voice_on):
    if chain is None:
        return chat_history, None, "Please load a chapter first!"

    if not question.strip():
        return chat_history, None, ""

    answer = chain.invoke(question)

    # Gradio 6 uses dict format instead of tuples
    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": answer})

    audio_path = None
    if voice_on:
        try:
            tts = gTTS(text=answer, lang='en', slow=False)
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(tmp.name)
            audio_path = tmp.name
        except Exception:
            pass

    return chat_history, audio_path, ""

def transcribe_audio(audio_path):
    # Converts voice input → text using whisper (optional)
    # For now returns placeholder — we'll add whisper later
    return "Voice input received (whisper coming soon)"

# ── UI LAYOUT ────────────────────────────────────────────
# WHY gr.Blocks()?
# Blocks gives you full control over layout.
# gr.Interface() is simpler but too rigid for multi-step UIs.

with gr.Blocks(title="K AI Study Companion") as app:

    # State variables — persist across interactions
    # gr.State() is like a hidden variable that survives button clicks
    chain_state = gr.State(None)

    gr.Markdown("# AI Study Companion")
    gr.Markdown("Select your class, subject and chapter to begin.")

    # ── ROW 1: Selectors ──
    with gr.Row():
        class_dd = gr.Dropdown(
            choices=list(CONTENT.keys()),
            value="Class 9",
            label="Class"
        )
        subject_dd = gr.Dropdown(
            choices=list(CONTENT["Class 9"].keys()),
            value="Science",
            label="Subject"
        )
        chapter_dd = gr.Dropdown(
            choices=list(CONTENT["Class 9"]["Science"].keys()),
            label="Chapter"
        )
        load_btn = gr.Button("Load Chapter", variant="primary")

    status_txt = gr.Textbox(label="Status", interactive=False, max_lines=1)

    # ── ROW 2: PDF + Chat ──
    with gr.Row():

        # Left: PDF viewer
        with gr.Column(scale=1):
            pdf_viewer = gr.HTML(label="Chapter PDF", value="<p style='color:var(--body-text-color)'>Load a chapter to view PDF here.</p>")

        # Right: Chat
        with gr.Column(scale=1):
            chatbot = gr.Chatbot(
                label="Ask anything about this chapter",
                height=400,  
                value=[]
            )

            # Voice toggle
            voice_toggle = gr.Checkbox(label="Voice output", value=False)

            # Text input row
            with gr.Row():
                question_box = gr.Textbox(
                    placeholder="Ask a question about this chapter...",
                    label="",
                    scale=4
                )
                send_btn = gr.Button("Send", variant="primary", scale=1)

            # Voice input
            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="Or speak your question"
            )

            # Audio output (for voice responses)
            audio_output = gr.Audio(
                label="Voice response",
                autoplay=True,
                visible=False
            )

    # ── EVENTS ──────────────────────────────────────────
    # WHY .change()? Runs function whenever dropdown value changes
    class_dd.change(
        fn=get_subjects,
        inputs=[class_dd],
        outputs=[subject_dd]
    )

    subject_dd.change(
        fn=get_chapters,
        inputs=[class_dd, subject_dd],
        outputs=[chapter_dd]
    )

    # Load chapter → update PDF viewer + chain state
    load_btn.click(
        fn=load_chapter,
        inputs=[class_dd, subject_dd, chapter_dd],
        outputs=[pdf_viewer, chain_state, status_txt]
    )

    # Send button → get answer
    send_btn.click(
        fn=answer_question,
        inputs=[question_box, chain_state, chatbot, voice_toggle],
        outputs=[chatbot, audio_output, status_txt]
    ).then(
        fn=lambda: ("", gr.Audio(visible=True)),  # clear input, show audio
        outputs=[question_box, audio_output]
    )

    # Also send on Enter key
    question_box.submit(
        fn=answer_question,
        inputs=[question_box, chain_state, chatbot, voice_toggle],
        outputs=[chatbot, audio_output, status_txt]
    ).then(
        fn=lambda: "",
        outputs=[question_box]
    )

    # Voice input → transcribe → fill question box
    audio_input.change(
        fn=transcribe_audio,
        inputs=[audio_input],
        outputs=[question_box]
    )

# ── RUN ──────────────────────────────────────────────────
if __name__ == "__main__":
    app.launch(
        server_port=7860,
        theme=gr.themes.Soft(),
        allowed_paths=[os.path.abspath("BOOKS")]
    )