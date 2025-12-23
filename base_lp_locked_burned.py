import requests, time

def lp_locked_burned():
    print("Base — LP Locked/Burned Detector (instant after launch)")
    seen = set()

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/pairs/base")
            for pair in r.json().get("pairs", []):
                addr = pair["pairAddress"]
                if addr in seen: continue

                age = time.time() - pair.get("pairCreatedAt", 0) / 1000
                if age > 180: continue  # старше 3 мин

                lp_burned = "burned" in pair.get("labels", [])
                lp_locked = "locked" in pair.get("labels", [])

                if lp_burned or lp_locked:
                    token = pair["baseToken"]["symbol"]
                    action = "BURNED" if lp_burned else "LOCKED"
                    print(f"LP {action}!\n"
                          f"{token} — LP {action.lower()} in {age:.0f}s\n"
                          f"Liq: ${pair['liquidity']['usd']:,.0f}\n"
                          f"https://dexscreener.com/base/{addr}\n"
                          f"→ Massive trust signal — dev can't rug LP\n"
                          f"{'TRUST'*25}")
                    seen.add(addr)

        except:
            pass
        time.sleep(3.9)

if __name__ == "__main__":
    lp_locked_burned()
