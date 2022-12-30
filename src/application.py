from __future__ import print_function, division
import cv2 as cv
import numpy as np
import threading
import time
import subprocess
import tkinter as tk
import customtkinter as ctk
import logging

from src.audio_capture import AudioRecorder
from src.video_capture import VideoRecorder
from src.managers import FileManager, SettingsManager

class Application:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.__timer = 60

        self.__window = ctk.CTk()
        self.__window.geometry("400x240")

        self.__file_manager = FileManager()
        self.__settings_manager = SettingsManager(self.__file_manager)

        global video_thread
        global audio_thread
        video_thread = VideoRecorder()
        audio_thread = AudioRecorder()
    
    def draw_window(self):
        pass

    def select_gojects(self):
        pass 

    def on_mouse_event(self, event, x, y, flags, param):
        pass

    def daily_log_button_press(self):
        #show screen for choosing goals
        #when done, show prelude for 45s
        #iterate for each goal for 15s. 
        self.select_gojects()
        self.start_AVrecording()
        time.sleep(self.__timer)
        self.stop_AVrecording()
        self.__file_manager.file_manager()
        
    def project_log_button_press(self):
        pass

    def settings_button_press(self):
        pass
    
    def process_data_button_press(self):
        pass

    def start_AVrecording(self):
        audio_thread.start()
        video_thread.start()

    def stop_AVrecording(self,filename="test"):
        audio_thread.stop()
        frame_counts = video_thread.frame_counts
        elapsed_time = time.time() - video_thread.start_time
        recorded_fps = frame_counts / elapsed_time
        print("total frames " + str(frame_counts))
        print("elapsed time " + str(elapsed_time))
        print("recorded fps " + str(recorded_fps))
        video_thread.stop()

        # Makes sure the threads have finished
        while threading.active_count() > 1:
            time.sleep(1)

        # Merging audio and video signal
        if abs(recorded_fps - 6) >= 0.01:    # If the fps rate was higher/lower than expected, re-encode it to the expected
            print("Re-encoding")
            cmd = "ffmpeg -r " + str(recorded_fps) + " -i ./data/temp_video.avi -pix_fmt yuv420p -r 6 ./data/temp_video2.avi"
            subprocess.call(cmd, shell=True)
            print("Muxing")
            cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i ./data/temp_audio.wav -i ./data/temp_video2.avi -pix_fmt yuv420p ./data/" + filename + ".avi"
            subprocess.call(cmd, shell=True)
        else:
            print("Normal recording\nMuxing")
            cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i ./data/temp_audio.wav -i ./data/temp_video.avi -pix_fmt yuv420p ./data/" + filename + ".avi"
            subprocess.call(cmd, shell=True)
            print("..")

    def __call__(self):
        button = ctk.CTkButton(master=self.__window, text="CTkButton", command=self.daily_log_button_press)
        button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.__window.mainloop()

if __name__ == '__main__':
    app = Application()
    file = FileManager()
    #manager = SettingsManager(file)
    app.start_AVrecording()
    time.sleep(60)
    app.stop_AVrecording()
    file.file_manager()
