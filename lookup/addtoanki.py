import json
import urllib.request


def invoke(req):
    requestJson = json.dumps(req).encode('utf-8')
    response = json.load(urllib.request.urlopen(
        urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


def exampleDict(examples):
    exDict = {}
    for i in range(len(examples)):
        exDict[f"exmp{i+1}"] = examples[i]
        if i >= 4:
            break
    return exDict


def noteDict(wordinfo):
    return {
        "deckName": "Mining",
        "modelName": "words with examples",
        "fields": {
                    "word": wordinfo.get("word", " "),
                    "word_declension": wordinfo.get("declension", " "),
                    "meaning": "-$#$-".join(wordinfo.get("meanings", " ")),
                    "english": wordinfo.get("eng", " "),
                    "usage": wordinfo.get("usage", " "),
                    "exmp": wordinfo.get("example", " "),
                    "detail": wordinfo.get("detail", " "),
                    "info": wordinfo.get("info", " "),
        },
        "options": {
            "allowDuplicate": True,
            "duplicateScope": "deck",
            "duplicateScopeOptions": {
                "deckName": "Default",
                "checkChildren": False,
                "checkAllModels": False
            }
        },
        "tags": [
            wordinfo["word"]
        ],
        "audio": [{
            "url": "http:" + link,
            "filename": f"{link.split('/')[-1]}.mp3",
            "skipHash": "7e2c2f954ef6051373ba916f000168dc",
            "fields": [
                        "word_audio"
            ]
        } for link in wordinfo["sounds"]]
    }


def addToAnki(wordsinfo):
    res = invoke({
        "action": "addNotes",
        "version": 6,
        "params": {
            "notes": [noteDict(wordinfo) for wordinfo in wordsinfo]
        }
    })

    print(res)


def ankify():
    pass


# addToAnki({
#     "example": "examples",
#     "detail": "sgsesssssssssssss",
#     "eng": 'info["eng"]',
#     "word": "as",
#     "usage": 'info["usage"]',
#     "declension": 'info["declension"]',
#     "meanings": ["meanings", "okay"],
#     "sounds": 'wiki["sounds"]'
# })
