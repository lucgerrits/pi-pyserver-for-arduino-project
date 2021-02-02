# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, Markup, jsonify
from flask_bootstrap import Bootstrap
from datetime import datetime
import codecs

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

bootstrap = Bootstrap(app)

mycache = []
mycache_max_size = 50


def isPostDataOK(data):
    total_bytes = len(data)

    # test bytes for ID, angle and distance
    # So: 6 + 6 + 6 bytes = 18 bytes minimum
    if total_bytes < 6:
        return 'ERROR: Missing "id".', 400
    if total_bytes < 12:
        return 'ERROR: Missing "angle".', 400
    if total_bytes < 18:
        return 'ERROR: Missing "distance".', 400
    else:
        return True


def parsePostData(data):
    data = data.strip()
    d = dict()
    myid = data[0:6].decode("ascii")
    myangle = data[6:12].decode("ascii")
    mydistance = data[12:18].decode("ascii")

    # file in hex encoding doesn't work
    # myimage = codecs.encode(data[18:], 'base64').decode("ascii")

    # plz send file directly as an PNG base64 string
    myimage = data[18:].decode("ascii")

    d['id'] = myid
    d['angle'] = myangle
    d['distance'] = mydistance
    d['image'] = myimage
    return d


@app.route('/')
def index():
    msg_len = len(mycache)
    # msg_range = []
    # i = 0
    # for i in range(int(msg_len), 0, -1):
    #     msg_range.append(int(i))
    # print(msg_len)
    # print(msg_range)
    return render_template('index.html', messages=mycache, messages_len=msg_len) #, messages_range=msg_range


@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        if isPostDataOK(request.data) == True:
            table_len = len(mycache)
            if table_len >= mycache_max_size:
                mycache.pop(0)
            table_len = len(mycache)
            message = parsePostData(request.data)
            # print(message)
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            mycache.append({
                "create_time": dt_string,
                # "id": message.get('id'),
                "id": table_len+1,
                "angle": message.get('angle'),
                "distance": message.get('distance'),
                "image": message.get('image')
            })
            return 'OK'
        else:
            return isPostDataOK(request.data)

    else:
        return 'ERROR: Please send POST request.', 400


if __name__ == '__main__':
    app.run(debug=True)
