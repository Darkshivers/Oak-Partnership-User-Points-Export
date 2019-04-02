import json
import requests
import time
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

time = time.strftime('%d/%m/%Y')
url = "https://oak-partnership.co.uk/api/accounts"

querystring = {"includeBalances":"true"}

headers = {
            'Content-Type': "application/json",
                'Authorization': "Key ",
                    'Cache-Control': "no-cache",
                        'Postman-Token': "0d3fdb33-ffb5-4508-9478-790086a515df"
                            }

response = requests.request("GET", url, headers=headers, params=querystring)

jsonoutput = json.loads(response.text)

if jsonoutput == "":
    print("No Response")

for item in jsonoutput: 
    item.pop('emailAddress', None)
    item.pop('accountID', None)

pointdata = open("OpReport.csv","wb")

csvwriter = csv.writer(pointdata)

print jsonoutput

count = 0 
for key in jsonoutput: 
    if count == 0: 
        count+= 1 
        header= key.keys()
        csvwriter.writerow(header)
    csvwriter.writerow(key.values())
pointdata.close()

origin = ""
reciever = ""
gmailkey = ""
Cc1 = ""
Cc2 = ""

email = MIMEMultipart()

email['From'] = origin
email['To'] = reciever
email['Cc'] = Cc2
email['Subject'] = "Oak Partnership Report " + time

sentfile = "OpReport.csv"

attachment = open(sentfile, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % "OakPartnershipReport" + ".csv")
email.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(origin,gmailkey)
text = email.as_string()
server.sendmail(origin,[reciever, Cc2], text)
server.quit()





