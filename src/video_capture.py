from __future__ import print_function, division
import cv2
import threading
import time

class VideoRecorder():
    "Video class based on openCV"
    def __init__(self, name="./data/temp_video.avi", fourcc="MJPG", sizex=640, sizey=480, camindex=0, fps=30):
        self.open = True
        self.device_index = camindex
        self.fps = fps                  # fps should be the minimum constant rate at which the camera can
        self.fourcc = fourcc            # capture images (with no decrease in speed over time; testing is required)
        self.frameSize = (sizex, sizey) # video formats and sizes also depend and vary according to the camera used
        self.video_filename = name
        self.video_cap = cv2.VideoCapture(self.device_index, cv2.CAP_DSHOW)
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
        self.frame_counts = 1

    def record(self):
        "Video starts being recorded"
        # counter = 1
        timer_start = time.time()
        timer_current = 0
        self.start_time = time.time()
        while self.open:
            ret, video_frame = self.video_cap.read()
            if ret:
                self.video_out.write(video_frame)
                # print(str(counter) + " " + str(self.frame_counts) + " frames written " + str(timer_current))
                self.frame_counts += 1
                # counter += 1
                # timer_current = time.time() - timer_start
                time.sleep(1/self.fps)
                gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow('recording...', gray)
                cv2.waitKey(1)
            else:
                break

    def stop(self):
        "Finishes the video recording therefore the thread too"
        if self.open:
            self.open=False
            self.video_out.release()
            self.video_cap.release()
            cv2.destroyAllWindows()

    def start(self):
        "Launches the video recording function using a thread"
        video_thread = threading.Thread(target=self.record)
        video_thread.start()

if __name__ == '__main__':
    global video_thread
    video_thread = VideoRecorder()
    video_thread.start()