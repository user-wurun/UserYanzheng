import tkinter as tk
import qrcode
import requests

# 创建二维码并保存为图片
def generate_qrcode(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')
    qr_img.save('qrcode.png')

# 检查确认状态
def check_confirmation():
    response = requests.get('http://localhost:5000/')
    confirmed = response.text == 'True'
    if confirmed:
        # 在此处执行下一步操作
        print('执行下一步操作')
    else:
        window.after(1000, check_confirmation)  # 每隔1秒检查一次确认状态

# 创建GUI窗口
window = tk.Tk()
window.title('身份验证')
window.geometry('300x300')

# 生成并显示二维码
data = 'verification_data'  # 替换为你自己的验证数据
generate_qrcode(data)
image = tk.PhotoImage(file='qrcode.png')
label = tk.Label(window, image=image)
label.pack(pady=20)

# 启动确认状态检查
check_confirmation()

# 运行GUI主循环
window.mainloop()
