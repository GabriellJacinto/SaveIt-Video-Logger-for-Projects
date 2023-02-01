from src.application import Application
from codecarbon import EmissionsTracker

#tracker = EmissionsTracker()
#tracker.start()

if __name__ == "__main__":
    app = Application()
    app()

else: 
    import cv2
    import pyaudio
    import wave

    # Set the video and audio recording parameters
    video_capture = cv2.VideoCapture(0)
    video_fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_fps = 20.0
    video_framesize = (640, 480)
    video_filename = "recording.avi"

    # Initialize the video writer
    video_writer = cv2.VideoWriter(video_filename, video_fourcc, video_fps, video_framesize)

    # Start the audio recording
    audio_frames = []
    audio_format = pyaudio.paInt16
    audio_channels = 2
    audio_rate = 44100
    audio_chunk = 1024
    audio_duration = 15

    audio = pyaudio.PyAudio()
    audio_stream = audio.open(format=audio_format, channels=audio_channels, rate=audio_rate, input=True, frames_per_buffer=audio_chunk)

    # Record for 15 seconds
    for i in range(0, int(audio_rate / audio_chunk * audio_duration)):
        video_ret, video_frame = video_capture.read()
        video_writer.write(video_frame)
        audio_data = audio_stream.read(audio_chunk)
        audio_frames.append(audio_data)

    # Stop the audio recording
    audio_stream.stop_stream()
    audio_stream.close()
    audio.terminate()

    # Save the audio recording to a file
    audio_filename = "recording.wav"
    audio_wavefile = wave.open(audio_filename, 'wb')
    audio_wavefile.setnchannels(audio_channels)
    audio_wavefile.setsampwidth(audio.get_sample_size(audio_format))
    audio_wavefile.setframerate(audio_rate)
    audio_wavefile.writeframes(b''.join(audio_frames))
    audio_wavefile.close()

    # Release the video and audio resources
    video_capture.release()
    video_writer.release()

    from moviepy.editor import *

    def merge_video_audio(video_file, audio_file, output_file):
        # Load the video and audio files
        video = VideoFileClip(video_file)
        audio = AudioFileClip(audio_file)

        # Add the audio to the video
        final_video = video.set_audio(audio)
        #video.write_videofile()
        # Save the final video with audio
        final_video.write_videofile(output_file, fps=20)

    # Example usage:
    merge_video_audio("recording.avi", "recording.wav", "recording_with_audio.mp4")

#tracker.stop()
