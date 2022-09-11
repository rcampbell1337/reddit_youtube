from typing import List

import pyttsx3


def pyttsx3_text_to_speech(things_to_say: List[str], relative_path: str) -> None:
    converter = pyttsx3.init()

    converter.setProperty('rate', 250)

    converter.setProperty('volume', 0.7)

    converter.setProperty('voice',
                          'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_GEORGE_11.0')

    if len(things_to_say) > 0:
        [converter.save_to_file(thing_to_say, f"{relative_path}/MP3s/{index}.mp3")
            for index, thing_to_say
            in enumerate(things_to_say)]
    else:
        converter.save_to_file(things_to_say[0], f"{relative_path}/MP3s/title.mp3")

    converter.runAndWait()
