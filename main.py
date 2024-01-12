from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import os

html_doc = requests.get("https://fitcvut.statuspage.io").text

soup = BeautifulSoup(html_doc, 'html.parser')
divs = soup.find_all('div', {'class': 'component-inner-container'})

d = {system: status for system, status in map(lambda x: (x.find("span", {"class": "name"}).string.strip(),x.find("span", {"class": "component-status"}).string.strip()) ,divs)}

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
