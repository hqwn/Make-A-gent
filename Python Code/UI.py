import gradio as gr
import threading
from Langchain_agent import ask_ai_gradio
import Talk
from Talk import run_jarvis

running = False

def start_jarvis():
    global current_status
    global running

    if not running:
        running = True

        thread = threading.Thread(target=run_jarvis, daemon=True)
        thread.start()
    
def status_update():
    if Talk.status == '':
        return "Jarvis hasn't started yet!"
    else:
        return Talk.status

with gr.Blocks() as demo:

    with gr.TabItem("Normal text-text chat with your AI Agent"):
        gr.ChatInterface(
            fn=ask_ai_gradio,
            textbox=gr.Textbox(placeholder="Ask a question to your AI Agent", container=False, scale=7),
            title="Your AI Agent",
            examples=["Hi", "What is 1+1?", "What's a good movie to watch?"]
        )
    
    with gr.TabItem("Voice Assistant for your AI Agent"):

        gr.Markdown('This is for you to talk to your AI Agent just like an AI voice assistant, status updates will be displayed below')
        gr.Markdown('Click the button to start Jarvis, and activate Jarvis (Always stays on after activating)')

        textbox = gr.Textbox(label='Status', value="Jarvis hasn't started yet!")
        start = gr.Button("Start Jarvis")

        start.click(
            fn=start_jarvis,
            inputs=None,
            outputs=textbox
        )

        timer = gr.Timer(.2)
        timer.tick(fn=status_update, outputs=textbox)

demo.launch(theme="Monochrome")