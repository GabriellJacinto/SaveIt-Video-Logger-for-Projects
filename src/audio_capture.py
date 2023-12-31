#!/usr/bin/env python
# -*- coding: utf-8 -*-
# VideoRecorder.py
# sauce: https://github.com/JRodrigoF/AVrecordeR
# sauce2: https://stackoverflow.com/questions/14140495/how-to-capture-a-video-and-audio-in-python-from-a-camera-or-webcam

from __future__ import print_function, division
import time
import wave
import threading
import pyaudio

class AudioRecorder:
    "Audio class based on pyAudio and Wave"
    def __init__(self, filename='temp_audio.wav', channels=1, rate=44100, frames_per_buffer=1024, format=pyaudio.paInt16):
        self.__audio_filename = filename
        self.__channels = channels
        self.__rate = rate
        self.__frames_per_buffer = frames_per_buffer
        self.__format = format
        self.__audio_frames = []
        self.__open = False
        self.__audio = pyaudio.PyAudio()
        self.__stream = self.__audio.open(format=self.__format,
                                        channels=self.__channels,
                                        rate=self.__rate,
                                        input=True,
                                        frames_per_buffer=self.__frames_per_buffer)
    
    @property
    def audio_filename(self):
        return self.__audio_filename

    @audio_filename.setter
    def audio_filename(self, value):
        self.__audio_filename = value

    def record(self):
        self.__open = True
        t_start = time.time_ns()

        try:
            while self.__open:
                try:
                    data = self.__stream.read(self.__frames_per_buffer)
                    self.__audio_frames.append(data)
                except Exception as e:
                    print('\n' + '*'*80)
                    print('PyAudio read exception at %.1fms\n' % ((time.time_ns() - t_start)/10**6))
                    print(e)
                    print('*'*80 + '\n')
                time.sleep(0.01)
        finally:
            self.__stream.stop_stream()
            self.__stream.close()
            self.__audio.terminate()

            waveFile = wave.open(self.__audio_filename, 'wb')
            waveFile.setnchannels(self.__channels)
            waveFile.setsampwidth(self.__audio.get_sample_size(self.__format))
            waveFile.setframerate(self.__rate)
            waveFile.writeframes(b''.join(self.__audio_frames))
            waveFile.close()

    def stop(self):
        self.__open = False

    def __call__(self):
        record_thread = threading.Thread(target=self.record)
        record_thread.start()

if __name__ == '__main__':
    # Example usage:
    recorder = AudioRecorder()
    recorder()
    