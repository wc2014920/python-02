import flask
from flask import Flask, render_template, request, jsonify, url_for, redirect
# render_template 內建函數，渲染模板，它需要一個『模板』來提供渲染的格式
import os
port = int(os.environ.get("PORT", 5000))
from csv import reader
import numpy as np
import requests

app = Flask(__name__)  # 沒有其它的用意，如此flask才會知道你的root在何處!

# 將 csv file 轉至 list [Type]
with open('stat/Stat.csv', 'r', encoding='utf-8', newline='') as csv_file:
    csv_reader = reader(csv_file)
    # Passing the cav_reader object to list() to get a list of lists
    list_of_rows = np.array(list(csv_reader))
    Stat_all = list_of_rows[1:, 3]
    StationName_unique_only_column = (np.unique(Stat_all))  # 取得所有車站名稱(唯一值，不重複)
    LineNum_all = list(list_of_rows[1:, 0])
    LineName_all = list(list_of_rows[1:, 1])
    Line = list(map(lambda x, y: x + "線: " + y, LineNum_all, LineName_all))
    Line1 = list(np.unique(np.array(Line)))
    myList = [i.split("線: ")[0] for i in Line1]
    myList1 = [i.split("線: ")[1] for i in Line1]


@app.route("/")  # 導入首頁
def redirect():
    return flask.redirect('/HOME/')


@app.route("/HOME/")
@app.route("/HOME/<VAL>")  # 導入首頁
@app.route("/HOME/0/<back>")
def home(VAL=0, back=0):
    value = myList
    value2 = myList1
    if VAL != 0:  # 車線代號
        print("VAL = ", VAL)
        val = (np.where(np.array(LineNum_all) == VAL))
        print(val)
        VAL = list(np.unique(Stat_all[val[0]]))
        data = []
        length = []
        if len(VAL) != 0:
            length.append(len(VAL))
        else:
            length.append(0)
        for i in range(len(VAL)):
            try:  # 若有5筆資料的情況下正常執行上述功能 i從0到5
                data.append(VAL[i])  # 溫度
            except:  # 若資料庫內不足5筆則執行填入0資料以湊齊5筆 進行初始化圖表
                data.append(0)
        chart = {'data': VAL, 'length': length}
        return jsonify(chart)
    else:
        if back != 0:
            return render_template('home.html', back=back)
        else:
            return render_template('home.html', value=value, value2=value2)




@app.route("/request/send/", methods=["GET", "POST"])
def SendorDeined():

    header = {'Content-Type':"application/json"}
    dict = request.values
    print(dict)
    print(f"{dict['inputGroupSelect01']} ---  {dict['inputGroupSelect02']}")
    my_params = {'BusLine':str(dict['inputGroupSelect01']), 'StartStation':str(dict['inputGroupSelect02'])}
    r = requests.post('http://node-redapptry.mybluemix.net/getnodered', json =my_params,headers=header)
    print(r)
    return flask.redirect(url_for('home', back="感謝使用"))


if __name__ == "__main__":  # 如果主程式執行
    # app.config['TEMPLATES_AUTO_RELOAD'] = True  # 當template有修改會自動更新
    app.run(port=port, debug=True)  # 將web server啟動
