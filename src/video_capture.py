from __future__ import print_function, division
import cv2
import threading
import time

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
        while self.__open:
            ret, video_frame = self.__video_cap.read()
            if ret:
                self.__video_out.write(video_frame)
                # print(str(counter) + " " + str(self.frame_counts) + " frames written " + str(timer_current))
                self.frame_counts += 1
                # counter += 1
                # timer_current = time.time() - timer_start
                time.sleep(1/self.__fps)
                gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow('recording...', gray)
                cv2.waitKey(1)
            else:
                break

    def stop(self):
        "Finishes the video recording therefore the thread too"
        print("Video done recording.", self.__open)
        if self.__open:
            print("1")
            self.__open=False
            print("2")
            self.__video_out.release()
            print("3")
            self.__video_cap.release()
            print("4")
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            print("Processing...")

    def start(self):
        "Launches the video recording function using a thread"
        video_thread = threading.Thread(target=self.record)
        video_thread.start()

if __name__ == '__main__':
    global video_thread
    video_thread = VideoRecorder()
    video_thread.start()