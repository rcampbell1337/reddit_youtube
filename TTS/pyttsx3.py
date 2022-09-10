import pyttsx3


def pyttsx3_text_to_speech(things_to_say: str) -> None:
    converter = pyttsx3.init()

    converter.setProperty('rate', 250)

    converter.setProperty('volume', 0.7)

    converter.setProperty('voice',
                          'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_GEORGE_11.0')

    for thing_to_say in things_to_say:
        converter.say(thing_to_say)
        print(thing_to_say)

    converter.runAndWait()
