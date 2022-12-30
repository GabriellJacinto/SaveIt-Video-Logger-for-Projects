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
        self.open = True
        self.rate = rate
        self.frames_per_buffer = fpb
        self.channels = channels
        self.format = pyaudio.paInt16
        self.audio_filename = filename
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      input_device_index=audio_index,
                                      frames_per_buffer = self.frames_per_buffer)
        self.audio_frames = []

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
        self.stream.start_stream()
        t_start = time.time_ns()
        while self.open:
            try:
                data = self.stream.read(self.frames_per_buffer)
                self.audio_frames.append(data)
            except Exception as e:
                print('\n' + '*'*80)
                print('PyAudio read exception at %.1fms\n' % ((time.time_ns() - t_start)/10**6))
                print(e)
                print('*'*80 + '\n')
            time.sleep(0.01)
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        waveFile = wave.open(self.audio_filename, 'wb')
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(self.audio.get_sample_size(self.format))
        waveFile.setframerate(self.rate)
        waveFile.writeframes(b''.join(self.audio_frames))
        waveFile.close()

    def stop(self):
        "Finishes the audio recording therefore the thread too"
        if self.open:
            self.open = False

    def start(self):
        "Launches the audio recording function using a thread"
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()

if __name__ == '__main__':
    global audio_thread
    audio_thread = AudioRecorder()
    audio_thread.start()