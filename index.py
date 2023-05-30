from flask import Flask, render_template, request
import requests  # pip install requests
from urllib.parse import urlencode, unquote
import json
import csv
from dotenv import load_dotenv
import os


load_dotenv()
buskey = os.environ.get("BUS_KEY")  # 버스키 공용키 가져옴
print(buskey)
app = Flask(__name__)

# 버스 딕셔너리 생성
bs_dict = {}
terminalserch_dict = {}

# csv 파일 불러오기 2
with open("C:/oyh/Pyhton/bus/Terminalserch.csv", mode="r") as inp:
    reader = csv.reader(inp)
    terminalserch_dict = {rows[0]: rows[1] for rows in reader}

# print(terminalserch_dict)

# csv 파일 불러오기 3
busclass_dict = {}

with open("C:/oyh/Pyhton/bus/Busclass.csv", mode="r") as inp1:
    reader = csv.reader(inp1)
    busclass_dict = {rows[0]: rows[1] for rows in reader}

    # print(busclass_dict)

# csv 파일 불러오기 4
Searchcitycode_dict = {}

with open("C:/oyh/Pyhton/bus/Searchcitycode.csv", mode="r") as inp2:
    reader = csv.reader(inp2)
    busclass_dict = {rows[0]: rows[1] for rows in reader}

    # print(Searchcitycode_dict)


# 1
def Businformation(depTerminalId, arrTerminalId, depPlandDate, busGradeId):
    url = (
        "https://apis.data.go.kr/1613000/ExpBusInfoService/getStrtpntAlocFndExpbusInfo"
    )
    queryString = "?" + urlencode(  # url을 앤코딩해주는 역할
        {
            "serviceKey": unquote(buskey),
            "pageNo": "1",
            "numOfRows": "10",
            "_type": "json",
            "depTerminalId": depTerminalId,
            "arrTerminalId": arrTerminalId,
            "depPlandTime": depPlandDate,
            "busGradeId": busGradeId,
        }
    )

    # print(url + queryString)
    response = requests.get(url + queryString)
    r_dict = json.loads(response.text)

    r_response = r_dict.get("response")
    r_body = r_response.get("body")
    r_item = r_body.get("items")

    item_list = r_item.get("item")

    result_list = []

    for item in item_list:
        depPlaceNm = item.get("depPlaceNm")
        arrPlaceNm = item.get("arrPlaceNm")
        # depPlandDate
        depPlandTime = item.get("depPlandTime")
        arrPlandTime = item.get("arrPlandTime")
        charge = item.get("charge")  # 돈
        # gradeNm = item.get("gradeNm")
        # routeId = item.get("routeId")
        print(arrPlaceNm, arrPlandTime, charge, depPlaceNm, depPlandTime)
        result_list.append(
            [depPlaceNm, arrPlaceNm, depPlandDate, depPlandTime, arrPlandTime, charge]
        )

    print(result_list)
    return result_list


# 2
def busterminalsearch():
    url = "https://apis.data.go.kr/1613000/ExpBusInfoService/getExpBusTrminlList"
    queryString = "?" + urlencode(
        {
            "serviceKey": unquote(buskey),
            "pageNo": "1",
            "numOfRows": "229",
            "_type": "json",
        }
    )
    # print(url + queryString)
    response = requests.get(url + queryString)
    r_dict = json.loads(response.text)
    r_response = r_dict.get("response")
    r_body = r_response.get("body")
    r_item = r_body.get("items")

    item_list = r_item.get("item")

    f = open("Terminalserch.csv", "w")
    # csv파일 데이터 만드는 방법
    for item in item_list:
        cityname = item.get("terminalNm")
        citycode = item.get("terminalId")
        data = cityname + "," + str(citycode) + "\n"
        f.write(data)

    # print(item_list)


# 3
def busclasssearch():
    url = "https://apis.data.go.kr/1613000/ExpBusInfoService/getExpBusGradList"

    queryString = "?" + urlencode({"serviceKey": unquote(buskey), "_type": "json"})
    # print(url + queryString)
    response = requests.get(url + queryString)
    r_dict = json.loads(response.text)

    r_response = r_dict.get("response")
    r_body = r_response.get("body")
    r_item = r_body.get("items")

    item_list = r_item.get("item")

    f = open("Busclass.csv", "w")
    # csv파일 데이터 만드는 방법
    for item in item_list:
        cityname = item.get("gradeNm")
        citycode = item.get("gradeId")
        data = cityname + "," + str(citycode) + "\n"
        f.write(data)

    # print(item_list)


# 4
def Searchcitycode():
    url = "https://apis.data.go.kr/1613000/ExpBusInfoService/getCtyCodeList"
    queryString = "?" + urlencode(
        {
            "serviceKey": unquote(buskey),
            "_type": "json",
        }
    )
    # print(url + queryString)

    response = requests.get(url + queryString)

    r_dict = json.loads(response.text)
    # print(r_dict)

    r_response = r_dict.get("response")
    r_body = r_response.get("body")
    r_item = r_body.get("items")

    item_list = r_item.get("item")

    # print(bs_dict)
    f = open("Searchcitycode.csv", "w")
    # csv파일 데이터 만드는 방법
    for item in item_list:
        cityname = item.get("cityName")
        citycode = item.get("cityCode")
        data = cityname + "," + str(citycode) + "\n"
        f.write(data)


def getcityid():
    reversed_dict = dict(map(reversed, bs_dict.items()))


@app.route("/", methods=["GET", "POST"])
def index():
    print("index")
    print(request.method)
    if request.method == "POST":
        try:
            # if len(bs_dict) == 0:
            #     Searchcitycode()

            # start_id = request.form["startname"]
            startname = request.form["startname"]
            print(startname)
            start_id = terminalserch_dict.get(startname)
            print(start_id)

            # arrival_id = request.form["arrivalname"]
            arrivalname = request.form["arrivalname"]
            print(arrivalname)
            arrival_id = terminalserch_dict.get(arrivalname)
            print(arrival_id)

            date_name = request.form["date_name"]
            print(date_name)

            busGradeId = request.form["busGradeId"]
            print(busGradeId)
            result_list = Businformation(start_id, arrival_id, date_name, busGradeId)

        except:
            return render_template("index.html")

        # temp, weather = getWeather(city_id)

        return render_template(
            "index.html",
            list=result_list,  #  start_name=start_name, arrival_name=arrival_name
        )
    else:
        if len(bs_dict) == 0:
            # Searchcitycode()
            getcityid()
            # busterminalsearch()  # csv 파일 만들어서 호출 x
            # busclasssearch()
        return render_template("index.html")


if __name__ == "__main__":
    # BusStop_dict()
    app.run(host="0.0.0.0", port=5001)
