import json, os
from prezzo import prezzo_btc
from sentiment import fear_greed
from notizie import notizie_rilevanti
from notifica import invia

STATO = "stato.json"
SOGLIA_PCT = 2.0   # % di variazione dall'ultimo controllo che fa scattare l'allarme

def leggi_stato():
    if os.path.exists(STATO):
        with open(STATO) as f:
            return json.load(f)
    return {"ultimo_prezzo": None}

def salva_stato(stato):
    with open(STATO, "w") as f:
        json.dump(stato, f)

def controlla():
    prezzo, var24h = prezzo_btc()
    stato = leggi_stato()
    precedente = stato["ultimo_prezzo"]

    if precedente is not None:
        variazione = (prezzo - precedente) / precedente * 100
        if abs(variazione) >= SOGLIA_PCT:
            direzione = "📈 su" if variazione > 0 else "📉 giù"
            valore, etichetta = fear_greed()
            invia(f"{direzione} {variazione:+.2f}% dall'ultimo controllo\n"
                  f"BTC ora: {prezzo:,.0f} EUR ({var24h:+.2f}% 24h)\n"
                  f"Sentiment: {valore}/100 ({etichetta})")

    stato["ultimo_prezzo"] = prezzo
    salva_stato(stato)
    print(f"Controllato: {prezzo:,.0f} EUR (precedente: {precedente})")

    for titolo, link in notizie_rilevanti():
        invia(f"📰 {titolo}\n{link}")

if __name__ == "__main__":
    controlla()
