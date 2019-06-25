from os.path import join, isdir, expanduser, dirname
from os import makedirs

HOTWORD_LIST_PT = [
    "Ó Inês",
    "Ó Maria",
    "Ó Flôr",
    "Ó Princesa",
    "Ei Jarbas",
    "Ó Jarbas",
    "Oi Jarbas",
    "Ei Computador",
    "Ó Computador",
    "Oi Computador",
    "liga a luz",
    "apaga a luz"
]

NEGATIVES_LIST_PT = [
    "Ó carborador",
    "Ei carborador",
    "Ei compressor",
    "Ó compressor",
    "muita dor",
    "Hey Trabalhas",
    "Hey Tralhas",
    "Hey Escapas",
    "Hey Facas",
    "Hey Beatas",
    "Hey Barbas",
    "Ó Trabalhas",
    "Ó Tralhas",
    "Ó Escapas",
    "Ó Facas",
    "Ó Beatas",
    "Ó Barbas",
    "Trabalhas",
    "Tralhas",
    "Escapas",
    "Facas",
    "Beatas",
    "Barbas"
]

SENTENCE_LIST_PT = []

DATA_PATH_PT = "/home/user/PycharmProjects/synthetic_data/data/pt"
if not isdir(DATA_PATH_PT):
    makedirs(DATA_PATH_PT)

HOTWORD_LIST = [
    "Athena",
    "Alexa",
    "Hey Siri",
    "Hey Jarbas",
    "Hey Jarvis",
    "Hey Computer",
    "Hey chatterbox",
    "Hey Mycroft",
    "Hey christopher",
    "lights on",
    "lights off"
]

NEGATIVES_LIST = [
    "hey commuter"
]

SENTENCE_LIST = []

DATA_PATH = "/home/user/PycharmProjects/synthetic_data/data/en"
if not isdir(DATA_PATH):
    makedirs(DATA_PATH)
