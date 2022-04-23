from bs4 import BeautifulSoup
import requests
import datetime as dt
import csv

### 추후 별도 파일로 관리될 옵션 목록 ###
START = "20200101"
END = "20220420"

KBANK_CODE = {
    "youdonsong_code": "K01120",
    "gijun_gumli": "K02010",
    "gukgochae_3": "K02051",
    "gukgochae_5": "K02061",
    "loan_gumli_final": "K02310"
}
##########################################



HEADER = ["date"] + list(KBANK_CODE.keys())
LEN_ATTRIB = len(KBANK_CODE)
DATE_IDX = 0



def binSearch(query, data, query_column_idx):
    begin, end = 0, len(data) - 1
    
    while begin <= end:
        mid = (begin + end) // 2

        if data[mid][query_column_idx] == query:
            return mid
        elif data[mid][query_column_idx] > query:
            end = mid - 1
        else:
            begin = mid + 1

        mid = (begin + end) // 2

    return None # 찾는 값 없음

def fetch_data():
    result = [] # 결과 리스트 준비 - 날짜 정보 기록
    i = dt.datetime.strptime(START, "%Y%m%d")
    while i <= dt.datetime.strptime(END, "%Y%m%d"):
        result.append([i.strftime("%Y%m%d")] + ([""] * LEN_ATTRIB))
        i += dt.timedelta(1)

    url = "https://ecos.bok.or.kr/mobile/100KeyStatCtl.jsp?actionType=statView&gubunCode="
    attrib_idx = 0 # 속성 인덱스 저장

    for code in KBANK_CODE.keys():
        response = requests.get(url + KBANK_CODE[code])

        if response.status_code != 200:
            raise RuntimeError

        bs = BeautifulSoup(response.text, "lxml")

        date = bs.findAll("td", {"class": "td3"})
        contents = bs.findAll("td", {"class": "td"})

        for i in range(len(date)): # 날짜 열 처리
            csv_date = date[i].text

            if len(csv_date) == 4: # 연도만 있는 경우
                res = dt.datetime(int(csv_date), 1, 1)
            elif len(csv_date) >= 5:
                tmp = csv_date.split(csv_date[4])
                year = int(tmp[0])

                if len(tmp) > 2: # 연도.월.날짜
                    month = int(tmp[1])
                    day = int(tmp[2])
            
                else:
                    if len(tmp[1]) > 2: # 연도, 분기
                        t = tmp[1].split(tmp[1][1])
                        month = int(t[0]) * 3 - 2
                        day = 1
                    else: # 연도, 월
                        month = int(tmp[1])
                        day = 1

                res = dt.datetime(year, month, day)
            else: # 처리 불가능한 경우 -> 반영하지 않음
                continue

            # 결과 리스트에 저장할 위치 탐색
            append_idx = binSearch(res.strftime("%Y%m%d"), result, DATE_IDX)

            if append_idx != None: # 저장할 위치에 기록
                result[append_idx][attrib_idx + 1] = contents[i].text.strip()

        attrib_idx += 1

    return result
