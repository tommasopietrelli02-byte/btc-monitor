import os
import requests

# I segreti NON stanno piu' nel codice.
# - Online (GitHub Actions): arrivano dalle variabili d'ambiente (Secrets).
# - In locale: arrivano dal file config_locale.py (che NON va caricato online).
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    try:
        import config_locale
        TOKEN = TOKEN or config_locale.TELEGRAM_TOKEN
        CHAT_ID = CHAT_ID or config_locale.TELEGRAM_CHAT_ID
    except ImportError:
        pass

if not TOKEN or not CHAT_ID:
    raise RuntimeError(
        "Mancano TELEGRAM_TOKEN / TELEGRAM_CHAT_ID "
        "(variabili d'ambiente online, oppure file config_locale.py in locale)."
    )

def invia(testo):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.get(url, params={"chat_id": CHAT_ID, "text": testo}, timeout=30)
    r.raise_for_status()

if __name__ == "__main__":
    invia("✅ Test: il monitor BTC è collegato.")
    print("Messaggio inviato.")
