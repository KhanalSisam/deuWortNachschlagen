import requests
from bs4 import BeautifulSoup


def has_usage(info):
    try:
        return all([(span.name == "span" and span.has_attr("title")) or str(type(span)) == "<class 'bs4.element.NavigableString'>"
                    for span in info])
    except:
        return False


def getFromVerben(word):
    try:
        url = f"https://www.verbformen.de/?w={word}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        info = {
            "meaning": "",
            "usage": "",
            "declension": "",
            "eng": "",
        }

        if ("Es wurden keine deutschen Wörter mit" in soup.find_all("i")[0].text):
            print("kein Wort wie", word, "in Verben.de")
            return

        totalinfo = soup.find_all("section", {"class": "rBox rBoxWht"})[0]
        info["info"] = totalinfo.find(
            "p", {"class": "rInf"}).text.replace("\n", " ").strip()
        info["word"] = totalinfo.find(
            "p", {"class": ["vGrnd", "rCntr"]}).text.replace("\n", " ").strip()
        info["declension"] = totalinfo.find(
            "p", {"class": "vStm rCntr"}).text.replace("\n", " ").strip()
        others = totalinfo.find(
            "div", {"class": "rAufZu"}).find_all("p")

        if others:
            for info_ in others:
                if (info_.find("span", {"lang": "en"})):
                    info["eng"] = info_.find(
                        "span", {"lang": "en"}).text.replace("\n", " ").strip()
                elif (len(info_.find_all()) == 1 and info_.find_all()[0].name == "i"):
                    info["meaning"] = info_.find("i").text.split(";")
                elif (has_usage(info_)):
                    info["usage"] = info_.text.strip()

        # print(info)
        return info
    except:
        print(
            f"some error occured while scraping from https://www.verbformen.de/?w={word}")
        return {}
