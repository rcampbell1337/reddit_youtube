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
    """
    Shows image prompts to the user then records a new voice audio file for them.
    """
    for file in AudioRecorder.get_all_folder_files("Images"):
        record_audio_file(file)

def record_audio_file(file: str, retry=False) -> None:
    """
    Shows image prompts to the user then records a new voice audio file for them.
    """
    if not retry:
        image = Image.open(file)
        image.show()
    file_name = Path(file).stem
    input("Press enter when you are ready to record...")
    AudioRecorder().record_audio_clip(file_name)                        
    try_again = input("Do you want to retry the recording? (y/n)")
    if try_again == "y":
        record_audio_file(file, retry=True)  
    image.close()

class AudioRecorder:
    """
    Class which handles the recording of voice audio files.
    """
    def __init__(self):
        self.queue = queue.Queue()
        self.stop_recording = False


    def record_audio_clip(self, filename: str) -> None:
        """
        Records an audio clip which is started and stopped by a user submitting input.
        :param: filename The name that the file will be saved as.
        """
        Logger.info(f"Entering {self.record_audio_clip.__name__}")

        output_file = f"{MEDIA_URL}\\MP3s\\{filename}.wav"

        self.delete_existing_mp3_files(output_file)

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

                    except RuntimeError as re:
                        Logger.warning(f"{re}. If recording was stopped by the user, then this can be ignored")
        except:
            raise Exception("Could not record file.")


    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            Logger.warning(status, file=sys.stderr)
        self.queue.put(indata.copy())

    def delete_existing_mp3_files(self, output_file: str) -> None:
        """
        Deletes existing mp3 files from the MP3s folder.
        :param: output_file The file to check for deletion.
        """
        for file in self.get_all_folder_files("MP3s"):
            if file == output_file:
                Logger.info(f"Deleting file: {output_file}")
                os.remove(file)


    def stop_mic_recording(self, sound_file: sf.SoundFile) -> None:
        """
        Stops the recording of an audio file when the user submits an input.
        :param: sound_file The file the audio is being recorded to.
        """
        Logger.info(f"Entering {self.stop_mic_recording.__name__}")
        input("Press enter to stop recording...")

        try:
            self.stop_recording = True

        except RuntimeError as e:
            Logger.info(f"Error stopping/saving {sound_file.name}. Make sure the file exists and can be modified")
            Logger.info(f"RunTimeError: \n{e}")

    @staticmethod
    def get_all_folder_files(folder_name) -> list[str]:
        """
        Gets all files in a given folder.
        :return: All files in a given folder.
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