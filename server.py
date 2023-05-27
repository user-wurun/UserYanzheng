from flask import Flask, render_template, request

app = Flask(__name__)

# 全局变量，用于存储确认状态
confirmation_status = False

@app.route('/')
def index():
    global confirmation_status
    # 渲染网页模板，并传递确认状态
    return render_template('index.html', confirmed=confirmation_status)

@app.route('/confirm', methods=['POST'])
def confirm():
    global confirmation_status
    # 接收确认请求
    confirmation_status = True
    # 在此处执行下一步操作，比如发送信号给客户端进行下一步操作
    print('执行下一步操作')
    return 'OK'

if __name__ == '__main__':
    app.run()
