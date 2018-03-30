from flask import Flask, render_template
from flask_sockets import Sockets
import datetime
import time


app = Flask(__name__)
sockets = Sockets(app)


# 这个接口是websocket的接口
@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        now = datetime.datetime.now().isoformat() + 'Z'
        ws.send(now)  # 发送数据
        time.sleep(1)


# 这个是测试的路由
@app.route('/')
def hello():
    return 'Hello World!'


# 显示前端页面
@app.route('/index/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()