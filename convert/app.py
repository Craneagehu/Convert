#-*- coding:utf-8 -*-
import time

import requests
from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
from lxml import etree

app = Flask(__name__)


@app.route('/api/convert',methods=['GET', 'POST'])
def convert():
    dict = {
        "人民币": "CNY",
        "港元": "HKD",
        "台币": "TWD",
        "欧元": "EUR",
        "美元": "USD",
        "英镑": "GBP",
        "澳元": "AUD",
        "韩元": "KRW",
        "日元": "JPY"

    }

    if request.method == 'GET':
        _from = request.args.get('from')
        _to = request.args.get('to')
        value = request.args.get('value')
        url ='http://qq.ip138.com/hl.asp'
        params = {
            'from':dict[_from],
            'to':dict[_to],
            'q':value
        }
        res = requests.get(url,params=params)
        res.encoding = 'utf-8'
        e = etree.HTML(res.content)
        data = {}
        data['status'] = 'ok'
        data['rate'] = e.xpath('//div[@class="bd"]/table/tr[3]/td[2]/p/text()')[0]
        data['timestamp']= round(time.time())
        data['result'] = e.xpath('//div[@class="bd"]/table/tr[3]/td[3]/p/text()')[0]
        data = jsonify(data)
        return data


if __name__ == '__main__':
    app.config["JSON_AS_ASCII"] = False
    #app.run(debug=True,host= '0.0.0.0',port=5000)
    WSGIServer(('0.0.0.0', 6001), app).serve_forever()
