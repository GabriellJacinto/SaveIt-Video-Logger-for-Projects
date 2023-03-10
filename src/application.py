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
from pygrabber.dshow_graph import FilterGraph

from src.config import *
from src.audio_capture import AudioRecorder
from src.video_capture import VideoRecorder, CaptureFeedback
from src.widgets import Spinbox, GojectCheckbox, ScrollableFrame
from src.toplevelwindows import GojectEditWindow, GojectSelectWindow, ProcessDataWindow
from src.app_managers import FileManager, SettingsManager

ctk.set_appearance_mode(APP_COLOR_THEME)
ctk.set_default_color_theme(APP_WIDGETS_COLORS)

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.__file_manager = FileManager()
        self.__settings_manager = SettingsManager(self.__file_manager)

    @property
    def settings_manager(self):
        return self.__settings_manager

    def draw_window(self):
        self.title(MAIN_WINDOW_NAME)
        self.geometry(f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.draw_left_frame()
        self.draw_right_frame()
        self.draw_center_frame()

    def draw_right_frame(self):
        self.right_sidebar_frame = ctk.CTkFrame(self, width=RIGHT_FRAME_WIDTH, corner_radius=0)
        self.right_sidebar_frame.grid(row=0, column=2, rowspan=4, sticky = "nsew")
        self.right_sidebar_frame.grid_rowconfigure(5, weight=1)

        self.select_gojects_label = ctk.CTkLabel(self.right_sidebar_frame, text="Selected Gojects", font=ctk.CTkFont(size=20, weight="bold"))
        self.select_gojects_label.grid(row=0, column=2, padx=20, pady=(20, 10))

        # create scrollable frame
        self.scrollable_frame = ScrollableFrame(self.right_sidebar_frame, width=RIGHT_FRAME_WIDTH)
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 10), pady=(10, 10))
            
    def draw_center_frame(self):
        self.center_frame = ctk.CTkFrame(self, width=140, corner_radius=0,fg_color="transparent")
        self.center_frame.grid(row=0, column=1, rowspan=6)
        self.center_frame.grid_rowconfigure(5, weight=1)
        
        label1 = ctk.CTkLabel(self.center_frame, text=LL_MESSAGE, font=ctk.CTkFont(size=12, slant="roman"), text_color="gray")
        label2 = ctk.CTkLabel(self.center_frame, text=QL_MESSAGE, font=ctk.CTkFont(size=12, slant="roman"), text_color="gray")
        label1.grid(row=1, pady=(0,60), sticky="N")
        label2.grid(row=0, sticky="N")

        # Load an image using OpenCV
        self.cv_img = cv.cvtColor(cv.imread("./utils/bg.jpg"), cv.COLOR_BGR2RGB)
        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        height, width, no_channels = self.cv_img.shape
        # Create a canvas that can fit the above image
        self.canvas = tk.Canvas(self.center_frame, width = width, height = height, bd=0, highlightthickness=0, relief='ridge', bg="black")
        self.canvas.grid(row=2, pady=(0,80), column=0)
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        #self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        # Add a PhotoImage to the Canvas
        #self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        self.record_button=ctk.CTkButton(self.center_frame, text="Choose a camera device", state="disabled", fg_color="transparent")
        self.record_button.grid(row=3, padx=20, pady=10)

        self.video_progressbar = ctk.CTkProgressBar(self.center_frame, progress_color = "blue", width=600)
        self.video_progressbar.grid(row=4, padx=20, pady=10)
        self.video_progressbar.set(0)
        
    def draw_left_frame(self):
        self.left_sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.left_sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.left_sidebar_frame.grid_rowconfigure(5, weight=1)

        #Title
        self.title_label = ctk.CTkLabel(self.left_sidebar_frame, text="Personal Video Logger", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        #Quick Log Button
        self.quicklog_button = ctk.CTkButton(self.left_sidebar_frame, command=lambda:self.draw_gojects_selection_window("quick_log"), text = "Quick Log", state="disabled")
        self.quicklog_button.grid(row=1, column=0, padx=20, pady=10)
        #Long Log Button
        self.long_log_button = ctk.CTkButton(self.left_sidebar_frame, command=lambda:self.draw_gojects_selection_window("long_log"), text="Long Log", state="disabled")
        self.long_log_button.grid(row=2, column=0, padx=20, pady=10)
        #Config Gojects Button
        self.config_gojects_button = ctk.CTkButton(self.left_sidebar_frame, command=self.draw_gojects_edit_window, text = "Gojects Configuration")
        self.config_gojects_button.grid(row=3, column=0, padx=20, pady=10)
        #Process Data Button
        self.process_data_button = ctk.CTkButton(self.left_sidebar_frame, command=self.draw_process_data_window, text="Process Data", state="disabled")
        self.process_data_button.grid(row=4, column=0, padx=20, pady=10)
        #get the available video devices
        self.graph = FilterGraph()
 
        # fill combobox with video devices
        self.camera_device_options = ctk.CTkOptionMenu(self.left_sidebar_frame, values=self.graph.get_input_devices(), command=self.camera_device_selection)
        self.camera_device_options.grid(row=5, column=0, padx=20, pady=(20, 10))
        self.camera_device_options.set("Device")
        
        #Quick Log Duration Spinbox
        self.quick_log_label = ctk.CTkLabel(self.left_sidebar_frame, text="Quick Log Duration", anchor="w")
        self.quick_log_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.quick_log_spinbox = Spinbox(self.left_sidebar_frame, width=120, min_value=DEFAULT_MIN_QUICKLOG_TIME, max_value=DEFAULT_MAX_QUICKLOG_TIME)
        self.quick_log_spinbox.grid(row=8, column=0, padx=20, pady=(10, 10))

        #Long Log Duration Spinbox
        self.long_log_label = ctk.CTkLabel(self.left_sidebar_frame, text="Long Log Duration", anchor="w")
        self.long_log_label.grid(row=9, column=0, padx=20, pady=(10, 0))

        self.long_log_spinbox = Spinbox(self.left_sidebar_frame, step_size=15, width=120, min_value=DEFAULT_MIN_LONGLOG_TIME, max_value=DEFAULT_MAX_LONGLOG_TIME)
        self.long_log_spinbox.grid(row=10, column=0, padx=20, pady=(10, 10))
    
    def draw_gojects_selection_window(self, record_type: str):
        self.gojects_selection_window = GojectSelectWindow(main_window=self, record_type=record_type)

    def draw_gojects_edit_window(self):
        self.gojects_edit_window = GojectEditWindow(main_window=self)

    def draw_process_data_window(self):
        self.process_data_window = ProcessDataWindow(main_window=self, data = "To implement")

    def draw_selected_gojects(self, selected_gojects_id):
        selected_gojects_widgets = []
        for id in selected_gojects_id:
            goject_checkbox = GojectCheckbox(master=self.scrollable_frame.scrollable_canvas,name=self.__settings_manager.goject_buffer[id].name, status=self.__settings_manager.goject_buffer[id].status, type=self.__settings_manager.goject_buffer[id].type)
            selected_gojects_widgets.append(goject_checkbox)
        self.update()
        return selected_gojects_widgets
    
    def camera_device_selection(self, _):
        print("trying to open camera: " + self.camera_device_options.get())   

        for i, device in enumerate(self.graph.get_input_devices() ):   
            if device == self.camera_device_options.get():
                self.video_source = i

        # main window
        #self.vid = CaptureFeedback(self.video_source)

        # Create a canvas that can fit the above video source size
        #self.canvas.grid_remove()
        #self.canvas = tk.Canvas(self.center_frame, width = self.vid.width, height = self.vid.height, bd=0, highlightthickness=0, relief='ridge', bg="black")
        #self.canvas.grid(row=0, column=0)

        self.long_log_button.configure(state="normal")
        self.quicklog_button.configure(state="normal")
        self.record_button.configure(text="Select Log Type", fg_color="blue")


        self.delay = 15
        #self.update_caputre()

    def update_caputre(self):
        # Get a frame from the video source
        return_value, frame = self.vid.get_frame()        

        if return_value:
            try:
                #frame = self.analyzeFrame(frame) <-- this is where you would put your image processing code, see webcam_qr.py
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

            except BaseException:
                    import sys
                    print(sys.exc_info()[0])
                    import traceback
                    print(traceback.format_exc())                
            finally:
                pass    

        self.after(self.delay, self.update_caputre)


    def start_quick_log(self, selected_gojects):
        current_goject_checkbox = self.draw_selected_gojects(selected_gojects)
        number_of_gojects = len(current_goject_checkbox)
        ratio_number = 1/len(current_goject_checkbox)
        timer = self.quick_log_spinbox.get()
        
        #Updating UI
        self.record_button.configure(text="Recording for {} s...".format(timer*number_of_gojects), fg_color="red")
        self.update()
        
        #TO DO: when done seleting, show prelude for 45s (video or animation)
        for checkbox in current_goject_checkbox:
            
            #Updating UI
            checkbox.set_progressbar_value()
            checkbox.set_checkbox_value()
            
            #Recording
            clean_status = checkbox.status.replace(" ", "_")
            name = "{}-{}".format(clean_status, datetime.today().strftime('%Y-%m-%d_%H-%M-%S'))
            folder = checkbox.name.replace(" ", "_")
            self.record_and_save(timer, type_recording="Quick_Logs", folder_name=folder, file_name=name)
            
            #Updating UI
            print("Done recording. Saving {} in {} folder".format(name,folder))
            self.video_progressbar.set(ratio_number)
            ratio_number += ratio_number
            self.update()

        #Updating and Cleaning UI 
        self.clean_update_window(current_goject_checkbox)
        
    def start_long_log(self, selected_gojects):
        current_goject_checkbox = self.draw_selected_gojects(selected_gojects)
        number_of_gojects = len(current_goject_checkbox)
        ratio_number = 1/len(current_goject_checkbox)
        timer = self.long_log_spinbox.get()
        
        #Updating UI
        self.record_button.configure(text="Recording for {} s...".format(timer*number_of_gojects), fg_color="red")
        self.update()

        #TO DO: when done selecting, show prelude for 15s (video)
        for checkbox in current_goject_checkbox:
            
            #Updating UI
            checkbox.set_progressbar_value()
            checkbox.set_checkbox_value()
            
            #Recording
            clean_status = checkbox.status.replace(" ", "_")
            name = "{}-{}".format(clean_status, datetime.today().strftime('%Y-%m-%d_%H-%M-%S'))
            folder = checkbox.name.replace(" ", "_")
            self.record_and_save(timer, type_recording="Long_Logs", folder_name=folder, file_name=name)
            
            #Updating UI
            print("Done recording. Saving {} in {} folder".format(name,folder))
            self.video_progressbar.set(ratio_number)
            ratio_number += ratio_number
            self.update()
        
        #Updating and Cleaning UI
        self.clean_update_window(current_goject_checkbox)
    
    def clean_update_window(self, checkboxes):
        self.record_button.configure(text="Done!", fg_color="green")
        self.update()
        time.sleep(WAIT_TO_CLEAN_TIME)
        self.video_progressbar.set(0)
        for checkbox in checkboxes:
            checkbox.delete()
        self.record_button.configure(text="Select Log Type", fg_color="blue")

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
        video_thread = VideoRecorder(camindex=self.video_source)
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