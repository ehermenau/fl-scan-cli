import sys
import requests

base_url = "https://scan.fetchlabs.io"


def checkHealth(base_url: str) -> None:
    r = requests.get(f"{base_url}/healthz")
    data = r.json()
    if data["status"] == "ok" and r.status_code == 200:
        print(f"{base_url}: Healthy and ready to receive code!")
        return
    else:
        print(f"{base_url} is not healthy...try again later.")
        sys.exit()


if __name__ == "__main__":
    checkHealth(base_url=base_url)
