from termcolor import cprint, colored
import os
from verben import getFromVerben
from wiki import fromWiki
from addtoanki import addToAnki, noteDict
from audio import play_audio


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def isword(word):
    return not any(i.isdigit() for i in word)


print("keys: 'q':quit, 'ex':examples,'r': replay audio 'eng':translations, 'exall':all examples, 'a':add to anki, 'i':info, 'h':help")


def main():
    wiki = {}
    info = {}
    os.system("")
    ex_indx = 1
    while True:
        cmd = input(
            "Enter a word or a command: ")
        match cmd:
            case "q":
                return
            case x if x.strip() == "a" and wiki:
                try:
                    ex_nums = input("enter the number of example: ")

                    # wtf, the past me is just too smart for the present me
                    # took the nums from input splitted it, converted to int and extracted the example it was referring to
                    examples = [wiki["examples"][i-1]
                                for i in [int(num) for num in ex_nums.split(" ")]]
                    noteData = []
                    for example in examples:
                        noteData.append({
                            "example": example,
                            "eng": info.get("eng", " "),
                            "word": info.get("word", " "),
                            "detail": info.get("word", " "),
                            "info": info.get("info", " "),
                            "usage": info.get("usage", " "),
                            "declension": info.get("declension", " "),
                            "meanings": wiki.get("meanings", " "),
                            "sounds": wiki.get("sounds", " ")
                        })
                    addToAnki(noteData)

                except ValueError:
                    cprint("enter a valid sequence/number", "red")
                except IndexError:
                    cprint(
                        "provide a valid example number. \n note: example indexing starts from 0 not 1", "red")

            case x if x.strip() == "ex" and wiki:
                if ex_indx <= len(wiki["examples"]):
                    print(
                        f"{bcolors.OKGREEN} {ex_indx}) {wiki['examples'][ex_indx - 1]} {bcolors.ENDC}")
                    ex_indx += 1
                else:
                    ex_indx = 1
                    print(
                        f"{bcolors.OKGREEN} {ex_indx}) {wiki['examples'][ex_indx - 1]} {bcolors.ENDC}")

            case x if x.strip() == "r" and wiki:
                [play_audio(sound_link)
                 for sound_link in wiki["sounds"]]

            case x if x.strip() == "exall" and wiki:
                for i in range(len(wiki["examples"])):
                    print(
                        f"{bcolors.OKGREEN} {i+1}) {wiki['examples'][i]} {bcolors.ENDC}")

            case x if x.strip() == "eng" and wiki:
                cprint(info['eng'], "cyan")

            case word if word.strip() and "-q" not in word:
                ex_indx = 1
                if isword(word):
                    cprint(bcolors.OKBLUE + "looking up..." + bcolors.ENDC)
                    info = getFromVerben(word)
                    if info:
                        cprint(info["info"], "yellow")
                        print(bcolors.HEADER + info["word"] + bcolors.ENDC)
                        print(bcolors.HEADER +
                              info["declension"] + bcolors.ENDC)
                        cprint(info["usage"], "yellow")

                    # for getting the root word. had some problem with the recursive method used in wiki
                    # rootWord = info["word"].replace("·", "").split(" ")[-1]
                    # print(rootWord)
                    wiki = fromWiki(word)
                    if wiki:
                        for meaning in wiki["meanings"]:
                            print(bcolors.OKGREEN + meaning + bcolors.ENDC)
                        [play_audio(sound_link)
                         for sound_link in wiki["sounds"]]
                else:
                    cprint("Enter a valid word", "red")

            # for a quick lookup
            case word if "-q" in word.strip():
                word = word.replace("-q", "").strip()
                quickInfo = getFromVerben(word)
                if quickInfo:
                    cprint(quickInfo["eng"], "yellow")
                else:
                    cprint("Enter a valid word", "cyan")

            case _:
                cprint("Enter a word first.", "red")


main()
