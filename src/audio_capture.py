#!/usr/bin/env python
# -*- coding: utf-8 -*-
# VideoRecorder.py
# sauce: https://github.com/JRodrigoF/AVrecordeR
# sauce2: https://stackoverflow.com/questions/14140495/how-to-capture-a-video-and-audio-in-python-from-a-camera-or-webcam

from __future__ import print_function, division
import pyaudio
import wave
import threading
import time

class AudioRecorder():
    "Audio class based on pyAudio and Wave"
    def __init__(self, filename="./data/temp_audio.wav", rate=44100, fpb=2**12, channels=1, audio_index=0):
        self.__open = True
        self.__rate = rate
        self.__frames_per_buffer = fpb
        self.__channels = channels
        self.__format = pyaudio.paInt16
        self.__audio_filename = filename
        self.__audio = pyaudio.PyAudio()
        self.__stream = self.__audio.open(format=self.__format,
                                      channels=self.__channels,
                                      rate=self.__rate,
                                      input=True,
                                      input_device_index=audio_index,
                                      frames_per_buffer = self.__frames_per_buffer)
        self.__audio_frames = []
 
    @property
    def audio_filename(self):
        return self.__audio_filename
    
    @audio_filename.setter
    def audio_filename(self, name):
        self.__audio_filename = name

    def list_audio_devices(name_filter=None):
        pa = pyaudio.PyAudio()
        device_index = None
        sample_rate = None
        for x in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(x)
            print(pa.get_device_info_by_index(x))
            if name_filter is not None and name_filter in info['name']:
                device_index = info['index']
                sample_rate = int(info['defaultSampleRate'])
                break
        return device_index, sample_rate

    def record(self):
        "Audio starts being recorded"
        self.__stream.start_stream()
        t_start = time.time_ns()
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
        "Finishes the audio recording therefore the thread too"
        if self.__open:
            self.__open = False

    def start(self):
        "Launches the audio recording function using a thread"
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()

if __name__ == '__main__':
    global audio_thread
    audio_thread = AudioRecorder()
    audio_thread.start()