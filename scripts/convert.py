import subprocess
from os import listdir, makedirs, walk
from os.path import join, isdir, isfile, dirname

def convert_dir(SOURCE_DIR, DEST_DIR, overwrite=False):
    if not isdir(DEST_DIR):
        makedirs(DEST_DIR)

    exts = ["mp3", "wav"]
    for wav in listdir(SOURCE_DIR):
        if wav.split(".")[-1] not in exts:
            # non audio file, skip
            if isdir(join(SOURCE_DIR, wav)):
                # TODO recursive
                print("skipping directory", wav)
            else:
                print("unrecognized format, skipping", wav)
            continue
        print("converting ", wav)
        if wav.endswith(".wav"):
            converted = join(DEST_DIR, wav)
        else:
            converted = join(DEST_DIR, wav + ".wav")
        wav = join(SOURCE_DIR, wav)
        if isfile(converted) and not overwrite:
            print("converted file already exists, skipping")
        else:
            cmd = ["ffmpeg", "-i", wav, "-acodec", "pcm_s16le", "-ar",
                   "16000", "-ac", "1", "-f", "wav", converted, "-y"]

            subprocess.call(cmd)


SAMPLES_PATH = join(dirname(dirname(__file__)), "data")

for root, dirs, files in walk(SAMPLES_PATH, topdown=False):
    convert_dir(root, root, True)
