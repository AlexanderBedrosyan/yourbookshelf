from django import template
import requests

register = template.Library()

@register.simple_tag
def translate_text_to(word):
    url = "https://api.mymemory.translated.net/get"

    params = {
        'q': word,
        'langpair': 'en|bg'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()['responseData']['translatedText']
    else:
        return word