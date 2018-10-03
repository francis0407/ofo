import pymysql

last_time = 0

def db_refresh_start_time():
    try:
        db = pymysql.connect("182.254.209.161", "root", "123456", "db_ofo", charset="utf8", port=3306)
        cursor = db.cursor()
        select = "select * from ofo_record"
        cursor.execute(select)
        result = cursor.fetchall()
        return result[-1][1],1
    except:
        print("Error")
        return 0,0

def cal_time(time_string):
    hour = time_string[-8:-6]
    min = time_string[-5:-3]
    sec = time_string[-2:]

    return hour*60*60 + min*60 + sec

def send_email(time):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    sender = "m303316727@163.com"
    receiver = "303316727@qq.com"
    subject = "爬虫已停止"
    content = "爬虫已停止，上次停止时间%s"%(time)
    smtps = "smtp.163.com"
    username = "m303316727@163.com"
    password = "m180040303"

    msg = MIMEText(content,'plain','utf-8')
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = Header(subject,'utf-8')

    smtp = smtplib.SMTP()
    smtp.set_debuglevel(1)
    smtp.connect(smtps,25)
    print(username,password)

    smtp.login(username,password)
    print("abc")
    smtp.sendmail(sender,receiver,msg.as_string())
    smtp.send()
    return 0


def detect():
    import time
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    last_time,flag = db_refresh_start_time()
    if not flag:
        return 1
    if cal_time(cur_time) - cal_time(last_time) > 1800:
        send_email(last_time)
        return 0
    else:
        return 1

send_email("123")

