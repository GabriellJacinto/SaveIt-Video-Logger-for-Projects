from __future__ import print_function, division
import cv2
import threading
import time
from datetime import datetime
import tkinter as tk

class CaptureFeedback:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if not self.vid.isOpened():
            return (return_value, None)

        return_value, frame = self.vid.read()
        if return_value:
            # Return a boolean success flag and the current frame converted to BGR
            return (return_value, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            return (return_value, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


class VideoRecorder():
    "Video class based on openCV"
    def __init__(self, name="./data/temp_video.avi", fourcc="MJPG", sizex=640, sizey=480, camindex=0, fps=30):
        self.__open = True
        self.__device_index = camindex
        self.__fps = fps                  # fps should be the minimum constant rate at which the camera can
        self.__fourcc = fourcc            # capture images (with no decrease in speed over time; testing is required)
        self.__frameSize = (sizex, sizey) # video formats and sizes also depend and vary according to the camera used
        self.__video_filename = name
        self.__video_cap = cv2.VideoCapture(self.__device_index, cv2.CAP_DSHOW)
        #if not self.__video_cap.isOpened():
        #    raise ValueError("Unable to open video source", self.__device_index)
        self.__width = self.__video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.__height = self.__video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.__video_writer = cv2.VideoWriter_fourcc(*self.__fourcc)
        self.frame_counts = 1

    @property
    def video_filename(self):
        return self.__video_filename
    
    @video_filename.setter
    def video_filename(self, name):
        self.__video_filename = name

    def record(self):
        "Video starts being recorded"
        # counter = 1
        self.__video_out = cv2.VideoWriter(self.__video_filename, self.__video_writer, self.__fps, self.__frameSize)
        timer_start = time.time()
        timer_current = 0
        self.start_time = time.time()
        time_label = datetime.now()
        while self.__open:
            ret, video_frame = self.__video_cap.read()
            if ret:
                time_text = datetime.now() - time_label
                font = cv2.FONT_HERSHEY_PLAIN
                gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
                cv2.putText(video_frame, str(datetime.now()), (20,40), font, 2, (255,255,255), 2, cv2.LINE_AA) 
                self.__video_out.write(video_frame)
                # print(str(counter) + " " + str(self.frame_counts) + " frames written " + str(timer_current))
                self.frame_counts += 1
                # counter += 1
                # timer_current = time.time() - timer_start
                time.sleep(1/self.__fps)
                cv2.putText(gray, str(time_text), (20,40), font, 2, (255,255,255), 2, cv2.LINE_AA) 
                cv2.imshow('recording...', gray)
                cv2.waitKey(1)
            else:
                break

    def stop(self):
        "Finishes the video recording therefore the thread too"
        print("Video done capturing.", self.__open)
        if self.__open:
            print("1")
            self.__open=False
            print("2")
            self.__video_out.release()
            print("3")
            self.__video_cap.release()
            print("4")
            cv2.destroyAllWindows()
            print("5")
            cv2.waitKey(1)
            print("Processing...")

    def __call__(self):
        "Launches the video recording function using a thread"
        video_thread = threading.Thread(target=self.record)
        video_thread.start()

if __name__ == '__main__':
    global video_thread
    video_thread = VideoRecorder()
    video_thread()