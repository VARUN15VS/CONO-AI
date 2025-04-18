import cv2
import numpy as np
from ffpyplayer.player import MediaPlayer
import customtkinter as ctk
from PIL import Image, ImageTk

class VideoPlayer(ctk.CTkToplevel):
    def __init__(self, video_path):
        super().__init__()
        self.title("Advanced Media Player")
        self.geometry("800x600")

        # Create video label (for video display)
        self.video_label = ctk.CTkLabel(self, text="")
        self.video_label.pack(expand=True, fill='both')

        # Controls Frame for buttons and sliders
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.pack(side='bottom', fill='x')

        # Pause/Play button
        self.pause_button = ctk.CTkButton(self.controls_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(side='left', padx=5)

        # Stop button
        self.stop_button = ctk.CTkButton(self.controls_frame, text="Stop", command=self.stop_video)
        self.stop_button.pack(side='left', padx=5)

        # Volume slider
        self.volume_slider = ctk.CTkSlider(self.controls_frame, from_=0, to=100, command=self.set_volume)
        self.volume_slider.set(50)  # Default to 50%
        self.volume_slider.pack(side='right', padx=5)

        # Timeline slider for video progress
        self.timeline_slider = ctk.CTkSlider(self.controls_frame, from_=0, to=100, command=self.seek_video)
        self.timeline_slider.pack(fill='x', expand=True, side='left', padx=5)

        # Media controls for seeking and fullscreen
        self.forward_button = ctk.CTkButton(self.controls_frame, text="Forward 5s", command=self.forward)
        self.forward_button.pack(side='left', padx=5)

        self.backward_button = ctk.CTkButton(self.controls_frame, text="Backward 5s", command=self.backward)
        self.backward_button.pack(side='left', padx=5)

        self.fullscreen_button = ctk.CTkButton(self.controls_frame, text="Fullscreen", command=self.toggle_fullscreen)
        self.fullscreen_button.pack(side='left', padx=5)

        # Initialize variables for video and player
        self.paused = False
        self.video_path = video_path
        self.video = None
        self.player = None
        self.is_fullscreen = False
        self.total_duration = 0

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start playing the video
        self.open_file()

    def open_file(self):
        if not self.video_path:
            return

        self.video = cv2.VideoCapture(self.video_path)
        self.player = MediaPlayer(self.video_path)

        self.paused = False
        self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.total_duration = self.total_frames / self.fps

        self.timeline_slider.configure(to=self.total_duration)
        self.update_video()

    def toggle_pause(self):
        if self.paused:
            self.paused = False
            self.pause_button.configure(text="Pause")
            self.update_video()  # Resume video updates
        else:
            self.paused = True
            self.pause_button.configure(text="Play")

    def stop_video(self):
        self.paused = True
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.player.seek(0, relative=False)
        self.timeline_slider.set(0)

    def set_volume(self, value):
        if self.player:
            self.player.set_volume(float(value) / 100)

    def seek_video(self, value):
        # Seek both video and audio
        if self.player:
            self.player.seek(float(value), relative=False)
        if self.video:
            frame_number = int(float(value) * self.fps)
            self.video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    def forward(self):
        current_time = self.get_current_position()
        new_time = min(current_time + 5, self.total_duration)
        self.player.seek(new_time, relative=False)

    def backward(self):
        current_time = self.get_current_position()
        new_time = max(current_time - 5, 0)
        self.player.seek(new_time, relative=False)

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.attributes('-fullscreen', False)
            self.is_fullscreen = False
            self.fullscreen_button.configure(text="Fullscreen")
        else:
            self.attributes('-fullscreen', True)
            self.is_fullscreen = True
            self.fullscreen_button.configure(text="Exit Fullscreen")

    def get_current_position(self):
        if self.player:
            current_time = self.player.get_pts()
            if current_time is not None:
                return current_time
        return 0

    def update_video(self):
        if self.paused:
            return

        grabbed, frame = self.video.read()
        if not grabbed:
            print("End of media")
            self.stop_video()
            return

        # Resize and show the video frame
        frame = cv2.resize(frame, (self.video_label.winfo_width(), self.video_label.winfo_height()))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(image=img)

        self.video_label.configure(image=img_tk)
        self.video_label.image = img_tk

        # Update the timeline slider
        current_position = self.get_current_position()
        self.timeline_slider.set(current_position)

        # Schedule the next frame update
        self.after(int(1000 / self.fps), self.update_video)

    def on_closing(self):
        if self.video and self.video.isOpened():
            self.video.release()
        if self.player:
            self.player.close_player()
        self.destroy()
