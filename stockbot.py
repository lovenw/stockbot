print ("HelloWorld")

import requests
from bs4 import BeautifulSoup
import re

#보유주식종목
my_list = ['INTC', 'AMD', 'TSLA']

#현재 주식 가격 가져오기
for stock in my_list:
    
    currentPrice_URL="https://finance.yahoo.com/quote/{}".format(stock)

    req = requests.get(currentPrice_URL)
    html = req.text

    soup = BeautifulSoup(html,'html.parser')#, from_encoding='utf-8')
    text = soup.find('span',{'class':'Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)'})

    text = str(text)

    text=re.sub('<.+?>','',text, 0).strip()
    print(stock+' : '+ text)


