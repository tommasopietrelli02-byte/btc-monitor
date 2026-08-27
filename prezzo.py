import requests

def prezzo_btc():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "eur", "include_24hr_change": "true"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    dati = r.json()["bitcoin"]
    return dati["eur"], dati["eur_24h_change"]

if __name__ == "__main__":
    prezzo, var24h = prezzo_btc()
    print(f"BTC: {prezzo:,.0f} EUR  ({var24h:+.2f}% nelle 24h)")
