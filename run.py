import time, traceback
from monitor import controlla

INTERVALLO_SEC = 300  # ogni 5 minuti

print("Monitor BTC avviato. Premi Ctrl+C per fermare.")
while True:
    try:
        controlla()
    except Exception:
        traceback.print_exc()
    time.sleep(INTERVALLO_SEC)
