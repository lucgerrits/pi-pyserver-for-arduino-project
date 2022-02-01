# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, Markup, jsonify
from flask_bootstrap import Bootstrap
from datetime import datetime
import codecs
import struct
import time
from base64 import b64encode

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

bootstrap = Bootstrap(app)

mycache = []
mycache_max_size = 30


def isPostDataOK(data, ip_addr):
    total_bytes = len(data)
    print("")
    if total_bytes < 1:
        print("{} : {}".format(ip_addr, 'ERROR: Missing "angle".'))
        return 'ERROR: Missing "angle".', 400
    if total_bytes < 2:
        print("{} : bytes={} angle={} ERROR={}".format(
            ip_addr,
            total_bytes,
            int(data[0]),
            'ERROR: Missing "distance".'))
        return 'ERROR: Missing "distance".', 400
    else:
        print("{} : bytes={} angle={} distance={}".format(
            ip_addr,
            total_bytes,
            int(data[0]),
            "{:.2f}".format(struct.unpack('f', data[1:5])[0]))
        )
        return True


def parsePostData(data):
    d = dict()
    myangle = int(data[0])
    mydistance = "{:.2f}".format(struct.unpack('f', data[1:5])[0])

    # plz send file directly as bytes
    if len(data[5:]) > 2:
        print("Taille image recue:")
        print(len(data[5:]))
        myimage = "data:image/png;base64, " + \
            b64encode(data[5:]).decode("utf-8")
    else:
        myimage = "/static/user.png"

    d['angle'] = myangle
    d['distance'] = mydistance
    d['image'] = myimage
    return d


@app.route('/')
def index():
    msg_len = len(mycache)
    return render_template('index.html', messages=mycache, messages_len=msg_len)


@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        if isPostDataOK(request.data, str(request.remote_addr)) == True:
            table_len = len(mycache)
            if table_len >= mycache_max_size:
                mycache.pop(0)
            table_len = len(mycache)
            message = parsePostData(request.data)
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            mycache.append({
                "create_time": dt_string,
                "ip": str(request.remote_addr),
                "angle": message.get('angle'),
                "distance": message.get('distance'),
                "image": message.get('image')
            })
            time.sleep(0.5)  # si on a wifiesp error: augmenter ??
            return 'OK'
        else:
            return isPostDataOK(request.data, str(request.remote_addr))

    else:
        return 'ERROR: Please send POST request.', 400


if __name__ == '__main__':
    app.run(debug=True)
