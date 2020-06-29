import requests
import json
import random


def udict(term):
    udict_def = requests.get(f'https://api.urbandictionary.com/v0/define?term={term}')
    choice = random.choice(range(len(udict_def.json()["list"])))
    term = udict_def.json()["list"][choice]["word"]
    definition = udict_def.json()["list"][choice]["definition"]
    author = udict_def.json()["list"][choice]["author"]
    example = udict_def.json()["list"][choice]["example"]
    thumbs_up = udict_def.json()["list"][choice]["thumbs_up"]
    thumbs_down = udict_def.json()["list"][choice]["thumbs_down"]
    permalink = udict_def.json()["list"][choice]["permalink"]

    udict_dict = {
        'term': term,
        'definition': definition,
        'author': author,
        'example': example,
        'thumbs_up': thumbs_up,
        'thumbs_down': thumbs_down,
        'permalink': permalink,
    }

    return udict_dict

