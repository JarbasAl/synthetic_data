import speech_recognition as sr
from speech_recognition import Recognizer
from os.path import dirname, join, isfile
from os import walk

SAMPLES_PATH = join(dirname(dirname(__file__)), "data", "en")

lang = "en-us"

# SAMPLES_PATH = join(dirname(dirname(__file__)), "data", "pt")


# lang = "pt"

recognizer = Recognizer()


def transcribe(path):
    audio = read_wave_file(path)
    try:
        text = recognizer.recognize_google(audio, None, lang)
        return text
    except:
        return "UNK"


def read_wave_file(wave_file_path):
    '''
    reads the wave file at provided path and return the expected
    Audio format
    '''
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(wave_file_path) as source:
        audio = r.record(source)
    return audio


flagged_files = []
good_files = []
delim = ", "

# resume transcription
skip = []
if isfile(SAMPLES_PATH + "/bad_stt.txt"):
    with open(SAMPLES_PATH + "/bad_stt.txt", "r") as f:
        for line in f.readlines():
            name, word, stt = line.strip().split(delim)
            flagged_files.append((name, word, stt))
            skip.append(name)
if isfile(SAMPLES_PATH + "/good_stt.txt"):
    with open(SAMPLES_PATH + "/good_stt.txt", "r") as f:
        for line in f.readlines():
            name, word, stt = line.strip().split(delim)
            good_files.append((name, word, stt))
            skip.append(name)

with open(SAMPLES_PATH + "/bad_stt.txt", "w") as bad_stt:
    with open(SAMPLES_PATH + "/good_stt.txt", "w") as good_stt:
        for root, dirs, files in walk(SAMPLES_PATH, topdown=False):
            for name in files:
                if name in skip:
                    continue
                if name.endswith(".wav"):
                    word = root.split("/")[-1].replace("_", " ")
                    text = transcribe(join(root, name))

                    if word != text:
                        print("WRONG!", text, name)
                        flagged_files.append((name, word, text))
                        bad_stt.write(
                            name + delim + word + delim + text + "\n")
                    else:
                        print("OK!", text, name)
                        good_files.append((name, word, text))
                        good_stt.write(
                            name + delim + word + delim + text + "\n")
