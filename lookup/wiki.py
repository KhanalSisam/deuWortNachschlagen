import requests
from bs4 import BeautifulSoup
from audio import play_audio


def filterWikiMeanings(meanings):
    new_meanings = []
    for meaning in meanings:
        if all([False if meaning in meaning_ else True for meaning_ in new_meanings]):
            new_meanings.append(meaning)
    return new_meanings


def fromWiki(word):
    try:
        url = f"https://de.wiktionary.org/wiki/{word}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content,  "html.parser")

        if soup.find_all(text="Dieser Eintrag existiert noch nicht!"):
            print("kein Wort wie", word, "in de.wikitionary.org")
            return

        # checking audio
        sounds = soup.find_all("img", {"alt": "Lautsprecherbild"})
        if sounds:
            sounds_link = [sound.find_next("a")["href"] for sound in sounds]
        else:
            sounds_link = []

        # checking if the word is root word or not
        # doesnt work as expected, but still as a back up, this case is covered by using root word from verben
        if soup.find("span", {"id": "Konjugierte_Form"}):
            root_word_table = soup.find_all("table", attrs={
                'style': 'border:1px solid #aaaaaa;background-color:#F5FFFA;padding:5px;font-size: 95%;'})[0]

            #  if yes, getting the rootword
            root_word = root_word_table.find("a").text
            print("The root word is: ", root_word)

            # play sound
            [play_audio(sound_link) for sound_link in sounds_link]

            # recursively calling
            return fromWiki(root_word)
        else:
            # getting meanings  --- ---  left for intransitive and transitive
            meanings_html = soup.find_all("p", string="Bedeutungen:")[
                0].find_next("dl")
            meanings_html = meanings_html.find_all("dd")
            meanings = [meaning_html.text for meaning_html in meanings_html]
            meanings = filterWikiMeanings(meanings)

            # getting examples
            examples_html = soup.find_all("p", string="Beispiele:")[
                0].find_next("dl")
            examples_html = examples_html.find_all("dd")
            examples = [example_html.text for example_html in examples_html]

            return {"examples": examples, "meanings": meanings, "sounds": sounds_link}
    except:
        print(
            f"some error occurred while scraping from https://de.wiktionary.org/wiki/{word}")
        return False
