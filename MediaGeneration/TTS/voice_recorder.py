# import required libraries
import msvcrt
import os
from pathlib import Path
import queue
import sys
from PIL import Image 
import sounddevice as sd
import soundfile as sf
import threading 
from definitions import MEDIA_URL
from logger import Logger


def get_image_prompts_and_record_audio():
    for file in AudioRecorder.get_all_folder_files("Images"):
        image = Image.open(file)
        image.show()
        file_name = Path(file).stem
        AudioRecorder().record_audio_clip(file_name)
        image.close()

class AudioRecorder:
    def __init__(self):
        self.queue = queue.Queue()
        self.stop_recording = False


    def record_audio_clip(self, filename: str):
        Logger.info(f"Entering {self.record_audio_clip.__name__}")

        output_file = f"{MEDIA_URL}\\MP3s\\{filename}.wav"
        for file in self.get_all_folder_files("MP3s"):
            if file == output_file:
                os.remove(file)
        try:
            with sf.SoundFile(output_file,
                                        mode='x', samplerate=44100,
                                        channels=2, subtype=None) as file:

                with sd.InputStream(samplerate=44100, channels=2, callback=self.callback):
                    Logger.info(f"New recording started: {file.name}")
                    try:
                        stop_recording_thread = threading.Thread(target=self.stop_mic_recording, args=(file,))
                        stop_recording_thread.start()
                        while not self.stop_recording:
                            file.write(self.queue.get())
                        file.flush()
                        file.close()
                        try_again = input("Do you want to retry the recording? (y/n)")
                        if try_again == "y":
                            self.stop_recording = False
                            self.queue.queue.clear()
                            return self.record_audio_clip(filename)

                    except RuntimeError as re:
                        Logger.warning(f"{re}. If recording was stopped by the user, then this can be ignored")
        except:
            raise Exception("Could not record file.")


    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            Logger.warning(status, file=sys.stderr)
        self.queue.put(indata.copy())

    def stop_mic_recording(self, sound_file: sf.SoundFile):
        Logger.info("Press enter to stop recording...")
        input()

        try:
            self.stop_recording = True

        except RuntimeError as e:
            Logger.info(f"Error stopping/saving {sound_file.name}. Make sure the file exists and can be modified")
            Logger.info(f"RunTimeError: \n{e}")

    @staticmethod
    def get_all_folder_files(folder_name) -> list[str]:
        """
        Gets all Images files in the image music folder.
        :return: All music files in the background music folder.
        """
        # list to store files
        files = []

        dir_path = f"{MEDIA_URL}\\{folder_name}\\"

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(dir_path + path)

        return files