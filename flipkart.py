import requests
import re
import smtplib
import time
import datetime
from validate_email import validate_email
from bs4            import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/81.0.4044.122 Safari/537.36'}

price_list = []


def input_url():
    global URL
    while True:
        URL = input("Enter Flipkart Product URL: \n")
        pattern = re.compile(r"^((http)s?:\/\/)")
        http_check = re.match(pattern, URL)

        pattern1 = r"flipkart.com\/[a-zA-Z0-9\-]+\/p\/[a-zA-Z0-9]{16}\/?([\/|?]{1})?([a-zA-Z0-9\=\&\_\-\.]*)"
        flipkart_check = re.findall(pattern1, URL)

        if http_check and flipkart_check:
            return URL
        elif http_check is None and flipkart_check:
            URL = "https://" + URL
            return URL
        else:
            print("Enter valid URL")


def input_email():
    global email
    while True:
        email = input("Enter your email address: \n")
        # pattern = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
        # result = re.match(pattern, email)
        if validate_email(email):
            return email
        else:
            print("Invalid Email")


def first_instance():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find('span', {'class': "_35KyD6"}).get_text()

    price = soup.find('div', {'class': "_1vC4OE _3qQ9m1"}).get_text()
    price = price.replace(",", '')
    initial_price = float(price[1:])
    price_list.append(initial_price)
    print(title)
    print(str(initial_price) + " at " + str(datetime.datetime.now()))


def loop():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    price = soup.find('div', {'class': "_1vC4OE _3qQ9m1"}).get_text()
    price = price.replace(",", '')
    price = float(price[1:])
    if (price < price_list[0]):
        price_list.append(price)
        price_list.sort()
        print("********************************************")
        print("Rs." + str(price) + " at " + str(datetime.datetime.now()))
        print("********************************************")
        send_mail(email, URL)


def send_mail(email, URL):
    global server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
    except BaseException:
        print('Something went wrong...')

    server.login('SENDER EMAIL', 'PASSWORD')

    subject = 'Price Alert!'
    body = 'Check ' + URL
    message = 'Subject: {}\n\n{}'.format(subject, body)
    server.sendmail(
        'SENDER EMAIL',
        email,
        message
    )
    print("Mail Sent!")


if __name__ == '__main__':
    print("*** Bot running ***")
    URL = input_url()
    email = input_email()
    first_instance()
    while True:
        loop()
        time.sleep(60)
