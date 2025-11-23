import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import tkinter as tk
from tkinter import filedialog, messagebox
# ---------------------------
# Core meme generator logic
# ---------------------------
def generate_meme(video_path, top_text, bottom_text, output_path):

    clip = VideoFileClip(video_path)
    W, H = clip.size

    def make_text(txt, pos_y):
        return (TextClip(txt,
                        fontsize=50,
                        font="Arial-Bold",
                        color="white",
                        stroke_color="black",
                        stroke_width=2,
                        method="caption",
                        size=(W-100, None))
                .set_position(("center", pos_y))
                .set_duration(clip.duration))

    # Top and bottom captions
