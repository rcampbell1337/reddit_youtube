from typing import List

import pyttsx3


def pyttsx3_text_to_speech(things_to_say) -> None:
    converter = pyttsx3.init()

    converter.setProperty('rate', 250)

    converter.setProperty('volume', 0.7)

    converter.setProperty('voice',
                          'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_GEORGE_11.0')

    if isinstance(things_to_say, List):
        [converter.say(thing_to_say) for thing_to_say in things_to_say]
    else:
        converter.say(things_to_say)

    converter.runAndWait()
