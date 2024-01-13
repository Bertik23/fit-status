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

if d["KOSapi"] == "Operational":
    requests.get("https://status.stepech.com/api/push/kVr7zi8yUp?status=up&msg=OK&ping=")
if d["Grades"] == "Operational":
    requests.get("https://status.stepech.com/api/push/VwDihrJ87M?status=up&msg=OK&ping=")
if d["OAuth"] == "Operational":
    requests.get("https://status.stepech.com/api/push/TGSmNYxUQz?status=up&msg=OK&ping=")
if d["PrintFIT"] == "Operational":
    requests.get("https://status.stepech.com/api/push/uDZNKcNcXs?status=up&msg=OK&ping=")
if d["Courses"] == "Operational":
    requests.get("https://status.stepech.com/api/push/juLzSsJ0HM?status=up&msg=OK&ping=")
if d["USERapi"] == "Operational":
    requests.get("https://status.stepech.com/api/push/Dd77wfsFAp?status=up&msg=OK&ping=")
if d["ProjectsFIT"] == "Operational":
    requests.get("https://status.stepech.com/api/push/tgALXYoAX6?status=up&msg=OK&ping=")
if d["GitLab"] == "Operational":
    requests.get("https://status.stepech.com/api/push/kzl3sgRBhX?status=up&msg=OK&ping=")
if d["WebFIT"] == "Operational":
    requests.get("https://status.stepech.com/api/push/QgyWvDciqi?status=up&msg=OK&ping=")

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
