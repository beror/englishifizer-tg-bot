from langdetect import detect, detect_langs
from spellchecker import SpellChecker

from string import punctuation

def get_spelling_mistakes_count(string_to_process):
    spelling_mistakes_count = 0
    spell_checker = SpellChecker()
    words = remove_punctuation(string_to_process.lower()).split()

    for word in words:
        if word in spell_checker or is_number(word):
            print("\"" + word + "\" is spelled correctly")
        else:
            spelling_mistakes_count += 1
            print("\"" + word + "\" is spelled incorrectly")

    return spelling_mistakes_count

def remove_punctuation(string_to_process):
    return string_to_process.translate(str.maketrans('', '', punctuation))

def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False