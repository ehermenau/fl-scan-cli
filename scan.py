import sys
import requests
import json

base_url = "https://scan.fetchlabs.io"
file = "/home/user/git_repos/edge-first-infra/gitops/hub/apps/10-scanner/manifests/networkpolicy.yaml"


def checkHealth(base_url: str) -> None:
    r = requests.get(f"{base_url}/healthz")
    data = r.json()
    if data["status"] == "ok" and r.status_code == 200:
        print(f"{base_url}: Healthy and ready to receive code!")
        return
    else:
        print(f"{base_url} is not healthy...try again later.")
        sys.exit()


def loadFile(file: str):
    with open(file, mode="r") as filehandler:
        return filehandler.read()


def uploadScan(format: str, code: str):
    headers = {"Content-Type": "application/json"}
    data = {"content": code, "format": format}
    r = requests.post(f"{base_url}/api/v1/scan", json=data, headers=headers)
    return r


def findFormat(file: str) -> str:
    if file.endswith(".tf"):
        format = "terraform"
    elif file.endswith(".yaml") or file.endswith(".yml"):
        format = "kubernetes"
    else:
        print(
            "Invalid file type. Scanner only accepts Kubernetes manifests or HCL code."
        )
        sys.exit()

    return format


def printResults(json_r: dict) -> None:
    if not json_r["summary"]["critical"]:
        print("No critical vulns found!")


if __name__ == "__main__":
    checkHealth(base_url=base_url)
    format = findFormat(file)
    code = loadFile(file)
    result = uploadScan(format, code)
    json_r = result.json()
    printResults(json_r)
