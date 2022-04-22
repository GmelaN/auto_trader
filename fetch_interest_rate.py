import requests as req
from bs4 import BeautifulSoup
import datetime as dt
import csv

url = "https://ecos.bok.or.kr/mobile/100KeyStatCtl.jsp?actionType=statView&gubunCode="
kbank_code = {
    "youdonsong_code": "K01120",
    "gijun_gumli": "K02010",
    "gukgochae_3": "K02051",
    "gukgochae_5": "K02061",
    "loan_gumli_final": "K02310"
}

data=[]

for code in kbank_code.keys():
    response = req.get(url + kbank_code[code])

    if response.status_code != 200:
        raise RuntimeError

    bs = BeautifulSoup(response.text, "lxml")
    table = bs.find("table")

    for i in table.findAll("td", {"class": "td3"}):
        csv_date = i.text

        if len(csv_date) == 4: # year
            res = dt.datetime(int(csv_date), 1, 1)
        elif len(csv_date) >= 5:
            tmp = csv_date.split(csv_date[4])
            year = int(tmp[0])

            if len(tmp) > 2: # yyyy.mm.dd
                month = int(tmp[1])
                day = int(tmp[2])
        
            else:
                if len(tmp[1]) > 2: # yyyy.mm.qq/qq
                    t = tmp[1].split(tmp[1][1])
                    month = int(t[0]) * 3 - 2
                    day = 1
                else: # yyyy.mm
                    month = int(tmp[1])
                    day = 1

            res = dt.datetime(year, month, day)
        else: # broken
            res = dt.datetime(0,0,0)

        data.append([res.strftime("%Y%m%d")])

    contents = bs.findAll("td", {"class": "td"})
    for i in range(len(contents)):
        data[i].append(contents[i].text.strip())

with open("k_bank.csv", 'w', encoding="UTF8") as f:
    writer = csv.writer(f)
    writer.writerows(data)
