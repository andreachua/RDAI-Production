import gradio as gr
from fastapi import FastAPI
from speakerId import speakerIdService


app = FastAPI()

asr_manager = speakerIdService()

io = gr.Interface(
    fn = asr_manager.predict,
    inputs=[gr.Audio()],
    outputs=[gr.Textbox(label="Speaker Prediction")]
)

app = gr.mount_gradio_app(app, io, path="/")
