import json, os, csv
from datetime import datetime, timezone
from prezzo import prezzo_btc
from sentiment import fear_greed
from notizie import notizie_rilevanti
from stato_mercato import riassunto
from notifica import invia

STATO = "stato.json"
STORICO = "storico.csv"
SOGLIA_PCT = 2.0   # % di variazione dall'ultimo controllo che fa scattare l'allarme

def leggi_stato():
    if os.path.exists(STATO):
        with open(STATO) as f:
            return json.load(f)
    return {"ultimo_prezzo": None}

def salva_stato(stato):
    with open(STATO, "w") as f:
        json.dump(stato, f)

def registra_storico(riga):
    nuovo = not os.path.exists(STORICO)
    with open(STORICO, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nuovo:
            w.writerow(["data_ora_utc", "prezzo_eur", "var_24h_pct",
                        "var_dal_precedente_pct", "fear_greed", "fear_greed_classe"])
        w.writerow(riga)

def controlla():
    prezzo, var24h = prezzo_btc()
    valore, etichetta = fear_greed()
    notizie = notizie_rilevanti()
    stato = leggi_stato()
    precedente = stato["ultimo_prezzo"]

    variazione = None
    allarme_prezzo = False
    if precedente is not None:
        variazione = (prezzo - precedente) / precedente * 100
        allarme_prezzo = abs(variazione) >= SOGLIA_PCT

    # Notifica (con riassunto descrittivo) solo se c'e' un movimento o una notizia
    if allarme_prezzo or notizie:
        testo = riassunto(prezzo, valore, etichetta, len(notizie))
        if allarme_prezzo:
            direzione = "📈 su" if variazione > 0 else "📉 giù"
            intestazione = (f"⚠️ Movimento: {direzione} {variazione:+.2f}% "
                            f"dall'ultimo controllo ({var24h:+.2f}% 24h)\n\n")
            testo = intestazione + testo
        invia(testo)

    for titolo, link in notizie:
        invia(f"📰 {titolo}\n{link}")

    ora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    var_prec = f"{variazione:.2f}" if variazione is not None else ""
    registra_storico([ora, f"{prezzo:.0f}", f"{var24h:.2f}", var_prec, valore, etichetta])

    stato["ultimo_prezzo"] = prezzo
    salva_stato(stato)
    print(f"Controllato: {prezzo:,.0f} EUR (precedente: {precedente}) - riga salvata in {STORICO}")

if __name__ == "__main__":
    controlla()
