from settings import HOTWORD_LIST_PT as HOTWORD_LIST, \
    NEGATIVES_LIST_PT as NEGATIVES_LIST, \
    SENTENCE_LIST_PT as SENTENCE_LIST, \
    DATA_PATH_PT as DATA_PATH
from os.path import join, isdir, exists
from os import makedirs
import subprocess


def convert(path):
    print("converting", path)
    args = ["ffmpeg", "-i", path, "-acodec", "pcm_s16le", "-ar", "16000",
            "-ac", "1", "-f", "wav", path.replace(".mp3", ".wav"), "-y"]
    subprocess.call(args)


def delete(path):
    print("deleting", path)
    args = ["rm", path]
    subprocess.call(args)


import boto3


class Polly:
    key_id = "xxx"
    secret_key = "xxxx"
    region = 'us-east-1'
    session = boto3.Session(aws_access_key_id=key_id,
                            aws_secret_access_key=secret_key,
                            region_name=region).client('polly')

    @staticmethod
    def get_tts(sentence, wav_file, voice, text_type="text", overwrite=False):
        if exists(wav_file.replace(".mp3", ".wav")) and not overwrite:
            return
        response = Polly.session.synthesize_speech(
            OutputFormat="mp3",
            Text=sentence,
            TextType=text_type,
            VoiceId=voice)

        with open(wav_file, 'wb') as f:
            f.write(response['AudioStream'].read())
        convert(wav_file)
        delete(wav_file)


def create_google():
    from gtts import gTTS

    engine_name = "gtts"
    for w in HOTWORD_LIST:
        w_path = join(DATA_PATH, w).replace(" ", "_")
        if not isdir(w_path):
            makedirs(w_path)

        wp_path = join(w_path, w + "-" + engine_name + ".mp3").replace(" ",
                                                                       "_")
        tts = gTTS(w)
        tts.save(wp_path)

    for w in NEGATIVES_LIST:
        w_path = join(DATA_PATH, w).replace(" ", "_")
        if not isdir(w_path):
            makedirs(w_path)
        wp_path = join(w_path, w + "-" + engine_name + ".mp3").replace(" ",
                                                                       "_")
        tts = gTTS(w)
        tts.save(wp_path)

    for idx, w in enumerate(SENTENCE_LIST):
        w_path = join(DATA_PATH, str(idx + 1)).replace(" ", "_")
        if not isdir(w_path):
            makedirs(w_path)
        wp_path = join(w_path,
                       str(idx + 1) + "-" + engine_name + ".mp3").replace(" ",
                                                                          "_")
        tts = gTTS(w)
        tts.save(wp_path)


def create_polly():
    engine_name = "polly"
    voices = ["Vitoria", "Ricardo", "Ines", "Cristiano"]
    for w in HOTWORD_LIST:
        w_path = join(DATA_PATH, w).replace(" ", "_")
        if not isdir(w_path):
            makedirs(w_path)

        for voice in voices:
            wp_path = join(w_path,
                           w + "-" + voice + "-" + engine_name +
                           ".mp3").replace(" ", "_")
            Polly.get_tts(w, wp_path, voice)

    for w in NEGATIVES_LIST:
        w_path = join(DATA_PATH, w).replace(" ", "_")
        if not isdir(w_path):
            makedirs(w_path)
        for voice in voices:
            wp_path = join(w_path,
                           w + "-" + voice + "-" + engine_name +
                           ".mp3").replace(" ", "_")
            Polly.get_tts(w, wp_path, voice)

    for idx, w in enumerate(SENTENCE_LIST):
        w_path = join(DATA_PATH, str(idx + 1)).replace(" ", "_")
        if not isdir(w_path):
            makedirs(w_path)
        for voice in voices:
            wp_path = join(w_path,
                           str(idx + 1) + "-" + voice + "-" + engine_name +
                           ".mp3").replace(" ", "_")
            Polly.get_tts(w, wp_path, voice)


def create_polly_ssml():
    engine_name = "polly"
    voices = ["Vitoria", "Ricardo", "Ines", "Cristiano"]
    effects = [
        ('<amazon:effect vocal-tract-length="+20%">',
         '</amazon:effect>',
         'strong'),
        ('<amazon:effect vocal-tract-length="-20%">',
         '</amazon:effect>',
         'weak'),
        # ("<amazon:effect name=\"whispered\">",
        # "</amazon:effect>",
        # "whispered"),
        ("<prosody rate='0.7'>",
         "</prosody>",
         "slow"),
        ("<prosody rate='1.25'>",
         "</prosody>",
         "fast"),
        ('<amazon:effect phonation="soft">',
         '</amazon:effect>',
         "softly"),
        # ("<amazon:auto-breaths>",
        # "</amazon:auto-breaths>",
        # "auto_breaths"),
        ("<prosody pitch='-10%'>",
         "</prosody>",
         "low_pitch"),
        ("<prosody pitch='+10%'>",
         "</prosody>",
         "high_pitch")
    ]

    for w in HOTWORD_LIST:
        w_path = join(DATA_PATH, w).replace(" ", "_")
        if not isdir(w_path):
            makedirs(w_path)

        for voice in voices:
            for effect in effects:
                wp_path = join(w_path,
                               w + "-" + voice + "-" + effect[2] + "-" +
                               engine_name + ".mp3").replace(" ", "_")

                w2 = "<speak>" + effect[0] + w + effect[1] + "</speak>"
                Polly.get_tts(w2, wp_path, voice, "ssml")

    for w in NEGATIVES_LIST:
        w_path = join(DATA_PATH, w).replace(" ", "_")
        if not isdir(w_path):
            makedirs(w_path)
        for voice in voices:
            for effect in effects:
                wp_path = join(w_path,
                               w + "-" + voice + "-" + effect[2] + "-" +
                               engine_name + ".mp3").replace(" ", "_")

                w2 = "<speak>" + effect[0] + w + effect[1] + "</speak>"
                Polly.get_tts(w2, wp_path, voice, "ssml")

    for idx, w in enumerate(SENTENCE_LIST):
        w_path = join(DATA_PATH, str(idx + 1)).replace(" ", "_")
        if not isdir(w_path):
            makedirs(w_path)
        for voice in voices:
            for effect in effects:
                wp_path = join(w_path,
                               str(idx + 1) + "-" + voice + "-" + effect[
                                   2] + "-" +
                               engine_name + ".mp3").replace(" ", "_")

                w2 = "<speak>" + effect[0] + w + effect[1] + "</speak>"
                Polly.get_tts(w2, wp_path, voice, "ssml")


def create_polly_mixed_ssml():
    engine_name = "polly"
    voices = ["Vitoria", "Ricardo", "Ines", "Cristiano"]
    effects = [
        ('<amazon:effect vocal-tract-length="+20%">',
         '</amazon:effect>',
         'strong'),
        ('<amazon:effect vocal-tract-length="-20%">',
         '</amazon:effect>',
         'weak'),
        # ("<amazon:effect name=\"whispered\">",
        # "</amazon:effect>",
        # "whispered"),
        ("<prosody rate='0.7'>",
         "</prosody>",
         "slow"),
        ("<prosody rate='1.25'>",
         "</prosody>",
         "fast"),
        ('<amazon:effect phonation="soft">',
         '</amazon:effect>',
         "softly"),
        # ("<amazon:auto-breaths>",
        # "</amazon:auto-breaths>",
        # "auto_breaths"),
        ("<prosody pitch='-10%'>",
         "</prosody>",
         "low_pitch"),
        ("<prosody pitch='+10%'>",
         "</prosody>",
         "high_pitch")
    ]

    mixes = [
        (0, 2, "strong_slow"),
        (0, 3, "strong_fast"),
        (0, 5, "strong_low_pitch"),
        (0, 6, "strong_high_pitch"),
        (1, 2, "weak_slow"),
        (1, 3, "weak_fast"),
        (1, 5, "weak_low_pitch"),
        (1, 6, "weak_high_pitch"),
        (2, 5, "slow_low_pitch"),
        (2, 6, "slow_high_pitch"),
        (3, 5, "fast_low_pitch"),
        (3, 6, "fast_high_pitch")

    ]
    for w in HOTWORD_LIST:
        w_path = join(DATA_PATH, w).replace(" ", "_")
        if not isdir(w_path):
            makedirs(w_path)

        for voice in voices:
            for m in mixes:
                effect1 = effects[m[0]]
                effect2 = effects[m[1]]
                wp_path = join(w_path,
                               w + "-" + voice + "-" + m[2] + "-" +
                               engine_name + ".mp3").replace(" ", "_")

                w2 = "<speak>" + effect2[0] + effect1[0] + w + effect1[1] + \
                     effect2[1] + "</speak>"
                Polly.get_tts(w2, wp_path, voice, "ssml")

    for w in NEGATIVES_LIST:
        w_path = join(DATA_PATH, w).replace(" ", "_")
        if not isdir(w_path):
            makedirs(w_path)
        for voice in voices:
            for m in mixes:
                effect1 = effects[m[0]]
                effect2 = effects[m[1]]
                wp_path = join(w_path,
                               w + "-" + voice + "-" + m[2] + "-" +
                               engine_name + ".mp3").replace(" ", "_")

                w2 = "<speak>" + effect2[0] + effect1[0] + w + effect1[1] + \
                     effect2[1] + "</speak>"
                Polly.get_tts(w2, wp_path, voice, "ssml")

    for idx, w in enumerate(SENTENCE_LIST):
        w_path = join(DATA_PATH, str(idx + 1)).replace(" ", "_")
        if not isdir(w_path):
            makedirs(w_path)
        for voice in voices:
            for m in mixes:
                effect1 = effects[m[0]]
                effect2 = effects[m[1]]
                wp_path = join(w_path,
                               str(idx + 1) + "-" + voice + "-" + m[2] + "-" +
                               engine_name + ".mp3").replace(" ", "_")

                w2 = "<speak>" + effect2[0] + effect1[0] + w + \
                     effect1[1] + effect2[1] + "</speak>"
                Polly.get_tts(w2, wp_path, voice, "ssml")


if __name__ == "__main__":
    create_polly_mixed_ssml()
    create_polly_ssml()
    create_polly()
    # create_google()
    # create_responsive_voice()
