from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import os
os.system(f"git pull")

html_doc = requests.get("https://fitcvut.statuspage.io").text

soup = BeautifulSoup(html_doc, 'html.parser')
divs = soup.find_all('div', {'class': 'component-inner-container'})

d = {system: status for system, status in map(lambda x: (x.find("span", {"class": "name"}).string.strip(),x.find("span", {"class": "component-status"}).string.strip()) ,divs)}

requests.get("https://status.stepech.com/api/push/5otNVgAJbb?status=up&msg=OK&ping=")


codes = {
    "KOSapi": "kVr7zi8yUp",
    "Grades": "VwDihrJ87M",
    "OAuth":  "TGSmNYxUQz",
    "PrintFIT": "uDZNKcNcXs",
    "Courses": "juLzSsJ0HM",
    "USERapi": "Dd77wfsFAp",
    "ProjectsFIT": "tgALXYoAX6",
    "GitLab": "kzl3sgRBhX",
    "WebFIT": "QgyWvDciqi"
}

for (system, token) in codes.items():
    if d[system] == "Operational":
        print(f"{system} is Operational according to FIT status.")
        r = requests.get(f"https://status.stepech.com/api/push/{token}?status=up&msg=Operational&ping=")
        print(f"UptimeKuma ping: {system}", r.status_code, r.text)
    else:
        print(f"{system} is {d[system]} according to FIT status.")
        r = requests.get(f"https://status.stepech.com/api/push/{token}?status=down&msg={d[system]}&ping=")
        print(f"UptimeKuma ping: {system}", r.status_code, r.text)


# if d["KOSapi"] == "Operational":
#     r = requests.get("https://status.stepech.com/api/push/kVr7zi8yUp?status=up&msg=OK&ping=")
#     print("KOSapi", r.status_code, r.content)
# if d["Grades"] == "Operational":
#     r = requests.get("https://status.stepech.com/api/push/VwDihrJ87M?status=up&msg=OK&ping=")
#     print("Grades", r.status_code, r.content)
# if d["OAuth"] == "Operational":
#     r = requests.get("https://status.stepech.com/api/push/TGSmNYxUQz?status=up&msg=OK&ping=")
#     print("OAuth", r.status_code, r.content)
# if d["PrintFIT"] == "Operational":
#     r = requests.get("https://status.stepech.com/api/push/uDZNKcNcXs?status=up&msg=OK&ping=")
#     print("PrintFIT", r.status_code, r.content)
# if d["Courses"] == "Operational":
#     r = requests.get("https://status.stepech.com/api/push/juLzSsJ0HM?status=up&msg=OK&ping=")
#     print("Courses", r.status_code, r.content)
# if d["USERapi"] == "Operational":
#     r = requests.get("https://status.stepech.com/api/push/Dd77wfsFAp?status=up&msg=OK&ping=")
#     print("USERapi", r.status_code, r.content)
# if d["ProjectsFIT"] == "Operational":
#     r = requests.get("https://status.stepech.com/api/push/tgALXYoAX6?status=up&msg=OK&ping=")
#     print("ProjectsFIT", r.status_code, r.content)
# if d["GitLab"] == "Operational":
#     r = requests.get("https://status.stepech.com/api/push/kzl3sgRBhX?status=up&msg=OK&ping=")
#     print("GitLab", r.status_code, r.content)
# if d["WebFIT"] == "Operational":
#     r = requests.get("https://status.stepech.com/api/push/QgyWvDciqi?status=up&msg=OK&ping=")
#     print("WebFIT", r.status_code, r.content)

with open("display.html") as f:
    html_display = BeautifulSoup(f.read(), "html.parser")


with open("data.json", "r") as f:
    curr: dict[str, dict[str, str]] = json.load(f)
    curr[datetime.now().isoformat()] = d
with open("data.json", "w") as f:
    json.dump(curr, f)


systems = set(i for (_, sys) in curr.items() for i in sys.keys())

print(systems)

html_display.find("table").replace_with("".join(["<table>", "<th>Timestamp</th>", "".join(f"<th>{sys}</th>" for sys in systems),
    "".join(f"<tr><td>{stamp}</td>{''.join(f'<td class={t[sys]}>{t[sys]}</td>' for sys in systems)}</tr>" for (stamp, t) in curr.items()),
                                       "</table>"] ))

with open("display.html", "w") as f_output:
    f_output.write(html_display.prettify().replace("&lt;","<").replace("&gt;", ">"))

os.system("git add data.json display.html")
os.system(f"git -c commit.gpgsign=false commit -m 'Run {datetime.now().isoformat()}'")
os.system(f"git push")
