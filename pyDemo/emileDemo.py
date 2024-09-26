import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

# 发送邮件 subject 邮件主题 content 邮件正文
def sendEmail(subject,content):
    # 邮箱参数
    smtp_server = 'smtp.qq.com'  # SMTP服务器地址
    smtp_port = 465  # SMTP服务器端口
    email_account = '1020229033@qq.com'  # 你的邮箱账号
    with open("C:\\Users\\wsd\\Desktop\\qqSQM.txt", 'r', encoding='utf-8') as file:
        # 读取文件内容 你的邮箱授权码
        email_password = file.read()
    # 邮件内容
    sender_name = 'Email Assistant'  # 发件人姓名
    sender_email = '1020229033@qq.com'  # 发件人邮箱地址
    sender = formataddr((sender_name, sender_email))  # 格式化发件人信息
    #print(sender)
    receivers = ['1020229033@qq.com']  # 收件人邮箱地址，给自己发送就写自己的邮箱
    #subject = '邮件主题'  # 邮件主题
    #content = '这是邮件正文内容'  # 邮件正文

    # 构建邮件对象
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = sender
    msg['To'] = sender  # 如果收件人也是自己
    msg['Subject'] = Header(subject, 'utf-8')
    #print(msg)
    # 发送邮件
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(email_account, email_password)
        server.sendmail(sender_email, receivers, msg.as_string())  # 使用邮箱地址作为 sendmail 的第一个参数
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("邮件发送失败，原因：", e)
    finally:
        server.quit()
        


if __name__ == '__main__':
    sendEmail('测试邮件','这是测试邮件')