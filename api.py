import requests
import urllib

print("HexShell API Interactive Console")

while True:
    try:
        cmd = input(">> ")
        data = {"pw": "83X58311", "cmd": cmd}
        data = urllib.parse.urlencode(data)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        res = requests.post("http://127.0.0.1:8967/", headers=headers, data=data)
        print(res.status_code)
    except KeyboardInterrupt:
        print("\n\nCtrl-C detected\nExiting...")
        exit()
