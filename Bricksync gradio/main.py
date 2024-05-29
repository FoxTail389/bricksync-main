import gradio as gr
from moviepy.editor import VideoClip, ImageClip
import numpy as np
import tempfile
from wav_to_lip_func import wave_complete_mp4
import gridfs
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path("../.env"))
MONGOURL = os.getenv('MONGOURL')
client = MongoClient(MONGOURL, server_api=ServerApi('1'))
fs=gridfs.GridFS(client["audio-to-vid"],"videos")
def greet(image, audio,gender,leftpixel,Json):
    videofile: VideoClip = wave_complete_mp4(audio, ImageClip(
        image), gender, leftpixel, Json)
    #videofile: VideoClip = wave_complete_mp4("News Recording.wav", ImageClip(
    #    "News Recording.png"), "f", 1000, ((827, 596), (939, 596), (883, 585)))
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
        temp_filename = temp_file.name
        videofile.write_videofile(temp_filename,fps=24,codec='libx264',audio_codec="aac")
        with open(temp_filename, 'rb') as f:
            return fs.put(f.read(),filename = "urlpo.mp4")

theme = gr.themes.Soft(
    primary_hue=gr.themes.Color(c100="#005e86", c200="#bfdbfe", c300="#93c5fd", c400="#192c43", c50="#eff6ff", c500="#ffd900", c600="#2563eb", c700="#1d4ed8", c800="#1e40af", c900="#1e3a8a", c950="#1d3660"),
    secondary_hue="blue",
    neutral_hue=gr.themes.Color(c100="#fef3c7", c200="#fde68a", c300="#fcd34d", c400="#fbbf24", c50="#fff9ca", c500="#f59e0b", c600="#d97706", c700="#b45309", c800="#92400e", c900="#78350f", c950="#6c370f"),
    radius_size="lg",
)

gr.Interface(
    theme=theme,
    fn=greet,
    inputs=[gr.Image(type='filepath'), gr.Audio(type="filepath"), gr.Dropdown(
            ["Male", "Female"], label="Gender"
            ), gr.Slider(label="Left Pixel", minimum=0, maximum=2000), gr.JSON(value=[[827, 596], [939, 596], [883, 585]], label="Box Points")],
    outputs=["textbox"],
).launch()
#((827, 596), (939, 596), (883, 585))