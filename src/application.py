from __future__ import print_function, division
from datetime import datetime
import cv2 as cv
import numpy as np
import threading
import time
import subprocess
import tkinter as tk
import customtkinter as ctk
import PIL.Image, PIL.ImageTk
import logging

from src.config import *
from src.audio_capture import AudioRecorder
from src.video_capture import VideoRecorder
from src.goject import Goject
from src.managers import FileManager, SettingsManager

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.__file_manager = FileManager()
        self.__settings_manager = SettingsManager(self.__file_manager)

        self.__quick_log_timer = 15
        self.__long_log_timer = 60

    def long_log_optionmenu_select(self, value):
        num, _ = value.split()
        self.__long_log_timer = int(num)
        
    def quick_log_optionmenu_select(self, value):
        num, _ = value.split()
        self.__quick_log_timer = int(num)

    def draw_window(self):
        self.title("InProgress: Personal Video Logger")
        self.geometry(f"{WIDTH}x{HEIGHT}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.draw_left_frame()
        self.draw_right_frame()
        self.draw_center_image()

    def draw_right_frame(self):
        self.right_sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.right_sidebar_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.right_sidebar_frame.grid_rowconfigure(5, weight=1)

        self.seg_button_1 = ctk.CTkSegmentedButton(self.right_sidebar_frame,values=["Goals", "Projects"])
        self.seg_button_1.grid(row=0, column=2, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.seg_button_1.set("Goals")

        # create scrollable textbox
        #tk_textbox = tk.Text(self.right_sidebar_frame, highlightthickness=0)
        #tk_textbox.grid(row=1, column=2, sticky="nsew")

        # create CTk scrollbar
        ctk_textbox_scrollbar = ctk.CTkScrollbar(self.right_sidebar_frame) #, command=tk_textbox.yview)
        ctk_textbox_scrollbar.grid(row=1, column=3, sticky="ns")

        # connect textbox scroll event to CTk scrollbar
        #tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

        self.checkbox_1 = ctk.CTkCheckBox(master=self.right_sidebar_frame, text="Objetivo X")
        self.checkbox_1.grid(row=1, column=2, pady=(20, 10), padx=20, sticky="n")

        self.status_label = ctk.CTkLabel(self.right_sidebar_frame, text="Status")
        self.status_label.grid(row=1, column=2, padx=20, pady=(10, 0))
        
    def draw_center_image(self):
        self.center_frame = ctk.CTkFrame(self, width=140, corner_radius=0,fg_color="transparent")
        self.center_frame.grid(row=0, column=1, rowspan=4)
        self.center_frame.grid_rowconfigure(5, weight=1)
        # Load an image using OpenCV
        self.cv_img = cv.cvtColor(cv.imread("./utils/bg.jpg"), cv.COLOR_BGR2RGB)
        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        self.height, self.width, no_channels = self.cv_img.shape
        # Create a canvas that can fit the above image
        self.canvas = tk.Canvas(self.center_frame, width = self.width, height = self.height, bd=0, highlightthickness=0, relief='ridge', bg="black")
        self.canvas.grid(row=0, column=0)
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        # Add a PhotoImage to the Canvas
        #self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        # Button that lets the user blur the image
        self.btn_blur=ctk.CTkButton(self.center_frame, command=lambda:print("works bro"), text="Record")
        self.btn_blur.grid(row=1, padx=20, pady=10)
        
    def draw_left_frame(self):
        self.left_sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.left_sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.left_sidebar_frame.grid_rowconfigure(5, weight=1)

        #Title
        self.title_label = ctk.CTkLabel(self.left_sidebar_frame, text="Personal Video Logger", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        #Quick Log Button
        self.quicklog_button = ctk.CTkButton(self.left_sidebar_frame, command=self.quick_log_button_press, text = "Quick Log")
        self.quicklog_button.grid(row=1, column=0, padx=20, pady=10)
        #Long Log Button
        self.long_log_button = ctk.CTkButton(self.left_sidebar_frame, command=self.long_log_button_press, text="Long Log")
        self.long_log_button.grid(row=2, column=0, padx=20, pady=10)
        #Config Gojects Button
        self.config_gojects_button = ctk.CTkButton(self.left_sidebar_frame, command=self.settings_gojects_button_press, text = "Gojects Configuration")
        self.config_gojects_button.grid(row=3, column=0, padx=20, pady=10)
        #Process Data Button
        self.process_data_button = ctk.CTkButton(self.left_sidebar_frame, command=self.process_data_button_press, text="Process Data")
        self.process_data_button.grid(row=4, column=0, padx=20, pady=10)
        #Quick Log Duration Option
        self.quick_log_label = ctk.CTkLabel(self.left_sidebar_frame, text="Quick Log Duration", anchor="w")
        self.quick_log_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.quick_log_optionemenu = ctk.CTkOptionMenu(self.left_sidebar_frame, values=["15 s", "25 s", "30 s"],
                                                                       command=self.quick_log_optionmenu_select)
        self.quick_log_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        #Quick Log Duration Option
        self.long_log_label = ctk.CTkLabel(self.left_sidebar_frame, text="Long Log Duration", anchor="w")
        self.long_log_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.long_log_optionemenu = ctk.CTkOptionMenu(self.left_sidebar_frame, values=["1 min", "2 min", "3 min"],
                                                                       command=self.long_log_optionmenu_select)
        self.long_log_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))
        
    def create_progress_bar_block(self, goject: Goject):
        pass

    def select_gojects(self):
        pass 

    def quick_log_button_press(self):
        self.select_gojects()
        #when done, show prelude for 45s
        #iterate for each goal for 15s. Once done, change the box status to blocked
        self.record_and_save(self.__quick_log_timer, "Quick_Logs")
        #clear the right_sidebar
        
    def long_log_button_press(self):
        self.select_gojects()
        #TO DO: when done, show prelude for 15s
        #create project bar
        #iterate for each project for 1min. 
        self.record_and_save(self.__long_log_timer, "Long_Logs")

    def settings_gojects_button_press(self):
        pass
    
    def process_data_button_press(self):
        pass

    def record_and_save(self, duration, type_recording="Undefined", folder_name="Type-Untitled", file_name=datetime.today().strftime('%Y-%m-%d_%H-%M-%S')):
        self.__save_dir = self.__file_manager.file_manager(type_recording,folder_name)
        
        self.start_AVrecording()
        print("recording for ", duration, " s...")
        time.sleep(duration)
        self.stop_AVrecording(self.__save_dir,file_name)
        self.__file_manager.file_cleaner(self.__save_dir)

    def start_AVrecording(self):
        global video_thread
        global audio_thread
        video_thread = VideoRecorder()
        audio_thread = AudioRecorder()
        
        audio_thread.audio_filename = self.__save_dir + "temp_audio.wav"
        video_thread.video_filename = self.__save_dir + "temp_video.avi"

        audio_thread.start()
        video_thread.start()

    def stop_AVrecording(self,save_dir, filename="test"):
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
            cmd = "ffmpeg -r " + str(recorded_fps) + " -i {dir}temp_video.avi -pix_fmt yuv420p -r 6 {dir}temp_video2.avi".format(dir=save_dir)
            subprocess.call(cmd, shell=True)
            print("Muxing")
            cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i {dir}temp_audio.wav -i {dir}temp_video2.avi -pix_fmt yuv420p {dir}".format(dir=save_dir) + filename + ".avi"
            subprocess.call(cmd, shell=True)
        else:
            print("Normal recording\nMuxing")
            cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i {dir}temp_audio.wav -i {dir}temp_video.avi -pix_fmt yuv420p {dir}".format(dir=save_dir) + filename + ".avi"
            subprocess.call(cmd, shell=True)
            print("..")

    def __call__(self):
        self.draw_window()
        self.mainloop()

if __name__ == '__main__':
    app = Application()
    file = FileManager()
    #manager = SettingsManager(file)
    app.start_AVrecording()
    time.sleep(60)
    app.stop_AVrecording()
    file.file_manager()