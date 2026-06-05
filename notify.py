#!/usr/bin/env python3
"""Send a notification to ntfy.sh topic revolut-crypto-djima-7q3z."""
import sys
import requests

NTFY_URL = "https://ntfy.sh/revolut-crypto-djima-7q3z"
TITLE = "Djimagem Finance sugests"


def send(message: str, priority: str = "default", tags: str = "bar_chart,money_with_wings") -> bool:
    try:
        r = requests.post(
            NTFY_URL,
            data=message.encode("utf-8"),
            headers={
                "Title": TITLE,
                "Priority": priority,
                "Tags": tags,
            },
            timeout=20,
        )
        return r.status_code == 200
    except Exception as e:
        print(f"ntfy error: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Teste"
    ok = send(msg)
    print("Enviado" if ok else "Falhou")
