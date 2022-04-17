import requests as req
from bs4 import BeautifulSoup
import csv

url_interest_rate = "https://ecos.bok.or.kr/mobile/100KeyStatCtl.jsp?actionType=statView&gubunCode=K02010"

response = req.get(url_interest_rate)

if response.status_code != 200:
    raise RuntimeError

bs = BeautifulSoup(response.text, "lxml")
table = bs.find("table")
interest_rates = []

for i in table.findAll("td", {"class": "td3"}):
    interest_rates.append([i.text.strip()])

interests = table.findAll("td", {"class": "td"})
for i in range(len(interest_rates)):
    interest_rates[i].append(interests[i].text.strip())

with open("interest_rate.csv", 'w', encoding="UTF8") as f:
    writer = csv.writer(f)
    writer.writerows(interest_rates)
