import requests

def fear_greed():
    r = requests.get("https://api.alternative.me/fng/?limit=1", timeout=30)
    r.raise_for_status()
    d = r.json()["data"][0]
    return int(d["value"]), d["value_classification"]  # es. 72, "Greed"

if __name__ == "__main__":
    valore, etichetta = fear_greed()
    print(f"Fear & Greed: {valore}/100 ({etichetta})")
