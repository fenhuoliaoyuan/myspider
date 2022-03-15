import smtplib
from email.header import Header
from email.mime.text import MIMEText


def my_send_email(title, content_html, from_email, to_email):
    # 邮件内容
    message = MIMEText(content_html, 'html', 'utf-8')
    # 邮件信息
    message['Subject'] = Header(title, 'utf-8')
    message['From'], message['To'] = from_email, to_email

    # 使用qq邮箱服务，发送邮件
    smtpObj = smtplib.SMTP_SSL('smtp.qq.com', 465)
    smtpObj.login(from_email, 'urxraodnpjntdhjg')  # 授权码
    smtpObj.sendmail(from_email, [to_email], message.as_string())
    smtpObj.quit()


if __name__ == '__main__':
    list_all = ['刚刚','过高']
    my_send_email("标题：来自python的测试邮件",
                  "<h1>更新视频个数为：{}<h1>更新的视频文件详情列表为：<br>{}".format(len(list_all),'<br>'.join(list_all)),
                  "2319423737@qq.com",
                  "2319423737@qq.com", )
