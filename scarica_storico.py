import csv, requests
from datetime import datetime, timezone

GIORNI = 365   # giorni di storico da scaricare (max 365 sul piano gratuito CoinGecko)
FILE = "storico_passato.csv"

def scarica():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "eur", "days": GIORNI}
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    prezzi = r.json()["prices"]   # lista di [timestamp_ms, prezzo]
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["data", "prezzo_eur"])
        for ms, prezzo in prezzi:
            giorno = datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d")
            w.writerow([giorno, f"{prezzo:.0f}"])
    print(f"Salvate {len(prezzi)} righe in {FILE} (ultimi {GIORNI} giorni).")

if __name__ == "__main__":
    scarica()
