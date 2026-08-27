import statistics
import requests

def _prezzi_giornalieri(giorni=30):
    # Con days > 90 CoinGecko restituisce punti GIORNALIERI (con days <= 90 sono orari).
    # Scarichiamo 180 giorni e teniamo gli ultimi (giorni+1) punti giornalieri.
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "eur", "days": 180}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    prezzi = [p[1] for p in r.json()["prices"]]
    return prezzi[-(giorni + 1):]

def _volatilita_label(vol_pct):
    if vol_pct < 2:
        return "bassa"
    if vol_pct < 4:
        return "media"
    return "alta"

def riassunto(prezzo, valore_fg, etichetta_fg, n_notizie=0):
    prezzi = _prezzi_giornalieri(30)
    media = sum(prezzi) / len(prezzi)
    scarto = (prezzo - media) / media * 100
    posizione = "sopra" if scarto >= 0 else "sotto"

    # volatilita' = deviazione standard dei rendimenti giornalieri (in %)
    rend = [(prezzi[i] - prezzi[i - 1]) / prezzi[i - 1] * 100
            for i in range(1, len(prezzi))]
    vol = statistics.pstdev(rend) if len(rend) > 1 else 0.0

    return (
        "📊 Stato mercato (solo descrizione, NON un consiglio):\n"
        f"Prezzo: {prezzo:,.0f} EUR\n"
        f"Media 30g: {media:,.0f} EUR ({posizione} media, {scarto:+.1f}%)\n"
        f"Volatilita 30g: {_volatilita_label(vol)} ({vol:.1f}%/giorno)\n"
        f"Sentiment: {valore_fg}/100 ({etichetta_fg})\n"
        f"Notizie rilevanti stavolta: {n_notizie}"
    )

if __name__ == "__main__":
    from prezzo import prezzo_btc
    from sentiment import fear_greed
    p, _ = prezzo_btc()
    v, e = fear_greed()
    print(riassunto(p, v, e, 0))
