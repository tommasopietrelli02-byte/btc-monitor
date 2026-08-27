import json, os, feedparser

FEED = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
]
PAROLE = ["bitcoin", "btc", "sec", "etf", "fed", "regulat", "ban",
          "hack", "musk", "trump", "lawsuit", "halving"]
VISTI = "notizie_viste.json"

def gia_visti():
    if os.path.exists(VISTI):
        with open(VISTI) as f:
            return set(json.load(f))
    return set()

def salva_visti(ids):
    with open(VISTI, "w") as f:
        json.dump(list(ids)[-500:], f)

def notizie_rilevanti():
    visti = gia_visti()
    nuove = []
    for url in FEED:
        for e in feedparser.parse(url).entries:
            titolo = e.get("title", "")
            link = e.get("link", "")
            if not link or link in visti:
                continue
            if any(p in titolo.lower() for p in PAROLE):
                nuove.append((titolo, link))
            visti.add(link)
    salva_visti(visti)
    return nuove

if __name__ == "__main__":
    for titolo, link in notizie_rilevanti():
        print(f"- {titolo}")
    print("--- FINE ---")
