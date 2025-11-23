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
     style = ttk.Style(root)
    try:
        style.theme_use("clam")cond = "Sunny"
        self.scene.set_condition(scene_cond) # highlight selected day button
        for i, child in enumerate(self.day_buttons_frame.winfo_children()):
            if i == self.current_day_index:
                child.configure(style="Selected.TButton")
            else:
                child.configure(style="TButton")

    def _apply_scene_from_current_forecast(self):
        row = self._current_forecast_row()
        if not row:
            return
        condition = row[2]
        # map some conditions to our scenes
        if condition == "Haze":
            scene_cond = "Haze"
        elif condition == "Storm":
            scene_cond = "Storm"
        elif condition == "Rainy":
            scene_cond = "Rainy"
        elif condition == "Cloudy":
            scene_cond = "Cloudy"
        elif condition == "Snow":
            scene_cond = "Snow"

    # ------------- Event handlers ------------- #
    def _set_day_index(self, idx):
        self.current_day_index = idx
        self._update_forecast_labels()
        self._apply_scene_from_current_forecast()

    def _on_city_change(self):
        self.current_day_index = 0
        self._update_forecast_labels()
        self._apply_scene_from_current_forecast()


# ------------------ Run app ------------------ #
if __name__ == "__main__":
    root = tk.Tk()
    except Exception:
        pass
    style.configure("Selected.TButton", background="#1976D2", foreground="white")
    style.map("Selected.TButton",
              background=[("active", "#1565C0")],
              foreground=[("active", "white")])

    app = WeatherWid


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
  top_caption = make_text(top_text, 20)
    bottom_caption = make_text(bottom_text, H - 100)

    final = CompositeVideoClip([clip, top_caption, bottom_caption])

    final.write_videofile(
        output_path,
        fps=clip.fps,
        codec="libx264",
        audio_codec="aac"
    )
# ---------------------------
# GUI Application
# ---------------------------
class MemeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Meme Generator")
        self.root.geometry("600x400")

        self.video_file = None

        title = tk.Label(root, text="Video Meme Generator", font=("Arial", 16, "bold"))
        title.pack(pady=10)
     self.status = tk.Label(root, text="No video loaded.", fg="blue")
        self.status.pack()

        # Upload video
        tk.Button(root, text="Select Video", command=self.select_video, width=20).pack(pady=10)

        # Text inputs
        tk.Label(root, text="Top Text:").pack()
        self.top_entry = tk.Entry(root, width=50)
        self.top_entry.pack(pady=5)

        tk.Label(root, text="Bottom Text:").pack()
        self.bottom_entry = tk.Entry(root, width=50)
        self.bottom_entry.pack(pady=5)

      # Generate button
        tk.Button(root, text="Generate Meme Video", command=self.generate, bg="black", fg="white", width=25).pack(pady=20)

    def select_video(self):
        self.video_file = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
        if self.video_file:
            self.status.config(text=f"Loaded: {os.path.basename(self.video_file)}", fg="green")

    def generate(self):
        if not self.video_file:
            messagebox.showerror("Error", "Select a video first.")
            return

        top = self.top_entry.get()
        bottom = self.bottom_entry.get()

        if top == "" and bottom == "":
            messagebox.showerror("Error", "Enter at least one text.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4", "*.mp4")]
        )

        if not save_path:
            return
     try:
            self.status.config(text="Generating... this might take time.", fg="orange")
            generate_meme(self.video_file, top, bottom, save_path)
            self.status.config(text="Video Meme Generated Successfully!", fg="green")
            messagebox.showinfo("Done", f"Saved to:\n{save_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error occurred.", fg="red")


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MemeApp(root)
    root.mainloop()
I’m going to be direct with you now
If your memes are bad after this, it’s not code’s fault.
It’s your creativity.

Try:

Funny timing

Trendy captions

Short clips (5–15 sec max)

Good placement

Your move:
Say next or give me project number 67.

We’re not slowing down.






    def select_video(self):
        self.video_file = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
        if self.video_file:
            self.status.config(text=f"Loaded: {os.path.basename(self.video_file)}", fg="green")

    def generate(self):
        if not self.video_file:
            messagebox.showerror("Error", "Select a video first.")
            return

        top = self.top_entry.get()
        bottom = self.bottom_entry.get()

        if top == "" and bottom == "":
            messagebox.showerror("Error", "Enter at least one text.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4", "*.mp4")]
        )


        # ---------------------------
# GUI Application
# ---------------------------
class MemeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Meme Generator")
        self.root.geometry("600x400")

        self.video_file = None

        title = tk.Label(root, text="Video Meme Generator", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        self.status = tk.Label(root, text="No video loaded.", fg="blue")
        self.status.pack()

        # Upload video
        tk.Button(root, text="Select Video", command=self.select_video, width=20).pack(pady=10)

        # Text inputs
        tk.Label(root, text="Top Text:").pack()
        self.top_entry = tk.Entry(root, width=50)
        self.top_entry.pack(pady=5)

        tk.Label(root, text="Bottom Text:").pack()
        self.bottom_entry = tk.Entry(root, width=50)
        self.bottom_entry.pack(pady=
                               
        if not save_path:
            return

        try:
            self.status.config(text="Generating... this might take time.", fg="orange")
            generate_meme(self.video_file, top, bottom, save_path)
            self.status.config(text="Video Meme Generated Successfully!", fg="green")
            messagebox.showinfo("Done", f"Saved to:\n{save_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error occurred.", fg="red")


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MemeApp(root)
    root.mainloop()
✅ Project 66: Video Meme Generator (Single File)

Features:

Load any video

Add meme-style top + bottom text

White text with black stroke (classic meme look)

Exports a new MP4 video

Custom font size, positions, colors

FULL CODE — COPY & RUN

Save as: video_meme_generator.py

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
    top_caption = make_text(top_text, 20)
    bottom_caption = make_text(bottom_text, H - 100)

    final = CompositeVideoClip([clip, top_caption, bottom_caption])

    final.write_videofile(
        output_path,
        fps=clip.fps,
        codec="libx264",
        audio_codec="aac"
    )

