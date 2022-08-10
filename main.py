import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from datetime import date
import streamlit as st

my_email = "ndmcroom7207@gmail.com"
password = st.secrets["password"]


def send_mail(send_from, send_to, subject, text, files=None,
              server="smtp.gmail.com"):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        part = MIMEApplication(f.read(), Name=f.name)
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % f.name
        msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(send_from, send_to, msg.as_string())


today = date.today()
st.title("Mail Your Data")
st.info("請自行修改以下欄位")
mail_option = st.radio("Provide Email Address", ('From Mail Address List', 'Type Your Own'), horizontal=True)

if mail_option == 'From Mail Address List':
    mail_address = st.multiselect("To whom", ["ylchang@mail.ndmctsgh.edu.tw", "zyliu0712@gmail.com", "cutlinda1200@gmail.com"])
else:
    single_mail = st.text_input("Your email address")
    mail_address = [single_mail]

title = st.text_input("主旨: ", value=f"{today}_Skanit 分析結果")
# content = st.text_area("信件內容: ", value="")
content = st.text_area('信件內容: ',
                       '''Sample Harvest Date:
Experimental Aim:
Note:
     ''')
attachments = st.file_uploader("副件檔案", accept_multiple_files=True)

if mail_address and attachments is not None:
    if st.button("Send"):
        send_mail("ndmcroom7207@gmail.com", mail_address, title, content, files=attachments)
        st.balloons()
        st.success("Sent")
