# Description: This script uses the BeautifulSoup and UrlLib2 modules to loop through the first six pages of a blog,
# and send an email with titles and links using the Smtplib module to all posts made on the current day.


import datetime
import bs4 as bs
import urllib2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create variable holding today's date
now = datetime.datetime.today()
day = '%02d' % now.day
month = '%02d' % now.month
today_date = str(now.year) + "-" + str(month) + "-" + str(day)


def send_daily():
    list_of_urls = ["Url1.com", "Url2.com", "Url3.com", "Url4.com", "Url5.com", "Url6.com"]

    # Create a dictionary holding the headline and URL of every post that matches today's date
    daily = {}
    for url in list_of_urls:
        sauce = urllib2.urlopen(url)
        soup = bs.BeautifulSoup(sauce, 'lxml')
        for headline in soup.find_all("h3", class_="j-e-title"):
            for time in soup.find_all('time'):
                if time.has_attr('datetime'):
                    page_time = time['datetime']
                    if page_time == today_date:
                        all_links = headline.find_all("a")
                        for link in all_links:
                            daily[headline.text] = link.get("href")

    email_user = 'private@gmail.com'
    email_send = 'private@gmail.com'
    subject = 'Daily Links'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    # Convert dictionary values into format that allows them to be sent by email
    for i in daily:
        hl_links = i.encode('utf-8') + str(daily[i])
        msg.attach(MIMEText(hl_links, 'plain'))
        text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, 'private')
    server.sendmail(email_user, email_send, text)
    server.quit()


send_daily()

