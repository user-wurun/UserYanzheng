import os
import time
import tkinter as tk
from tkinter import Menu, messagebox
import qrcode
import webbrowser
from flask import Flask, request
import sv_ttk
import threading
import subprocess
import pyotp
import configparser

app = Flask(__name__)

@app.route('/')
def index():
    return '''
 <!DOCTYPE html>
<html>
<head>
    <title>验证身份</title>
    <style>
        body {
            text-align: center;
            margin-top: 100px;
        }

        .container {
            width: 300px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            font-size: 24px;
        }

        p {
            font-size: 16px;
        }

        button {
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            background-color: #4CAF50;
            color: #fff;
            text-decoration: none;
            border: none;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>请点击下方按钮完成身份验证</h1>
        <p><a href="/verify" target="_blank"><button>点击验证</button></a></p>
    </div>
</body>
</html>


    '''

@app.route('/verify')
def ok():
    print("Success")  # 在控制台打印"Success"
    subprocess.Popen(["C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"])#以打开Microsoft Edge为例
    time.sleep(1)
    # 等待另一个软件执行完毕
    os._exit(0)

def verify():
    ok()
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>验证成功</title>
            <style>
                body {
                    text-align: center;
                    margin-top: 100px;
                }
                h1 {
                    font-size: 24px;
                }
            </style>
            <script>
                window.onload = function() {
                    window.opener.showSuccess();
                    window.close();
                };
            </script>
        </head>
        <body>
            <h1>验证成功！</h1>
        </body>
        </html>
    '''

def open_webpage():
    webbrowser.open("http://localhost:5000")  # Flask应用的URL

def generate_qrcode():
    config = configparser.ConfigParser()
    config.read('config.ini')
    # Flask应用的URL
    url = config.get('forout', 'url')
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # 保存二维码图片
    img.save("qrcode.png")

    # 显示二维码图片
    image = tk.PhotoImage(file="qrcode.png")
    label.config(image=image)
    label.image = image

def start_flask():
    app.run(port=5000)

if __name__ == '__main__':
    window = tk.Tk()
    sv_ttk.set_theme("dark")

    # 创建主窗口
    def exit():
        messagebox.showwarning("退出","即将退出")
        os._exit(0)
    def setting():
        messagebox.showinfo("关于","本软件由个人开发")
    def jihuo():
        messagebox.showinfo("激活","已激活\r\n" +"激活类型：永久激活")
    def usbkey():
        try:
            usb_drive_path = 'E:/'  # 请根据实际U盘路径修改
            # 检查文件是否存在
            file_path = os.path.join(usb_drive_path, 'key.txt')
            if os.path.exists(file_path):
                ok()
            else:
                messagebox.showwarning("警告","未检测到安全密钥。请插入安全密钥，然后重试。")
        except:
            messagebox.showwarning("警告","未检测到安全密钥。请插入安全密钥，然后重试。")

    window.title("身份验证")
    mebubar = Menu(window)
    mebubar.add_command(label="关于", command=setting)
    mebubar.add_command(label="使用安全密钥", command=usbkey)
    mebubar.add_command(label="激活", command=jihuo)
    mebubar.add_command(label="退出", command=exit)
    window.config (menu=mebubar)
    lbl = tk.Label(window, text="你正在申请打开受管控的应用，请扫码完成身份验证或输入验证码", font=("Arial Bold", 15))
    lbl.pack(pady=20)
    window.geometry("800x800")

    # 创建标签用于显示二维码
    label = tk.Label(window)
    label.pack(pady=20)

    def clicked():
        string = config.get('forout', 'key')#2FA(使用TOTP)的值
        seckey = string#base64.b32encode(string.encode(encoding="utf-8"))
        mfakey = pyotp.TOTP(seckey)
        endkey = mfakey.now()
        print(seckey)
        print(endkey)
        a = entry.get()
        print(type(a))
        if a == "":
            messagebox.showerror("错误","请输入验证码")
        else:
            try:
                aaaa = int(entry.get())
                if mfakey.verify(aaaa):
                    ok()
                else:
                    messagebox.showinfo("错误", "验证码错误")
            except:
                messagebox.showerror("警告","无效的输入内容")

    #2FA
    twofa = tk.Label(window, text="备选验证方案，请在此输入验证码", font=("Arial Bold", 15))
    twofa.pack(pady=20)
    entry = tk.Entry(window)
    entry.pack(pady=10)

    button = tk.Button(window, text="确定", command=clicked)
    button.pack()

    # 创建Flask应用的线程并启动

    # 生成二维码并显示
    generate_qrcode()

    def start_flask_in_thread():
        flask_thread = threading.Thread(target=start_flask)
        flask_thread.start()

    start_flask_in_thread()

    def stop_flask():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def on_window_close():
        stop_flask()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_window_close)

    # 运行GUI主循环
    window.mainloop()
