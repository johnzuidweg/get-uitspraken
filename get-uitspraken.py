#!/usr/bin/python3
import requests, pickle, telegram, json
# install telegram with pip3 install python-telegram-bot

URL = "https://uitspraken.rechtspraak.nl/api/zoek"
PICKLE_FILE = "uitspraken-pickle.bin"

# Telegram
#BOT = telegram.Bot('')
#CHAT_ID = 

def get_uitspraken(term):
    json = {
        "StartRow":0,
        "PageSize":10,
        "ShouldReturnHighlights":True,
        "ShouldCountFacets":True,
        "SortOrder":"PublicatieDatumDesc",
        "SearchTerms":[{"Term":term,"Field":"AlleVelden"}]
    }
    response = requests.post(URL, json=json)
    results = response.json()["Results"]
    result_urls = set()
    for result in results:
        result_urls.add(result["DeeplinkUrl"])
    return result_urls

try:
    f = open(PICKLE_FILE, 'rb')
    old_uitspraken = pickle.load(f)
except (FileNotFoundError, EOFError) as e:
    old_uitspraken = set()

uitspraken = get_uitspraken("126nba") | get_uitspraken("126uba") | get_uitspraken("126zpa") | get_uitspraken("126ffa")

new_uitspraken = uitspraken - old_uitspraken

if new_uitspraken:

    for uitspraak in new_uitspraken:
        #BOT.sendMessage(chat_id=CHAT_ID, text=f"Nieuwe uitspraak: {uitspraak}")
        print(f"Nieuwe uitspraak: {uitspraak}")

    f = open(PICKLE_FILE, "wb")
    pickle.dump(uitspraken, f, protocol=pickle.HIGHEST_PROTOCOL)
