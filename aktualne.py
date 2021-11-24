
from os import pipe
import requests
from bs4 import BeautifulSoup
import json
import csv


def datetonumeric(stringdate):
    spliteddate=stringdate.split()
    data=[]
    for m in spliteddate:
        data.append((m.split("."))[0])
    ladate=[]
    for m in data:
        if(m.isdigit()==True):
            ladate.append(m)
    day=int(ladate[0])
    themonth=int(ladate[1])
    year=int(ladate[2])
    if(themonth >10 or themonth < 7):
        return ""
    if(themonth==10 and day>7):
        return ""
    return f'{day}/{themonth}/{year}'



count=0
with open('aktualneoutput.csv', 'w', newline='', encoding="UTF-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';')
    spamwriter.writerow(['id_clanku','zdroj','datum','title','perex','text','url'])
    for i in range(0,8):
        r=requests.get(f'https://zpravy.aktualne.cz/parlamentni-volby-2021/l~8480f6185fc711ebb0f60cc47ab5f122/?offset={i*20}')
        soup = BeautifulSoup(r.text, 'html.parser')
        articles=soup.select(".small-box--article")
        for article in articles:

            try:
            # id=(json.loads(article['data-track-list']))['item']['id']
                id_clanku=f'AK000{count}'
                urlselector=(article.select("a"))
                url=f"https://zpravy.aktualne.cz{(urlselector[0])['href']}"
                r=requests.get(url)
                soup=BeautifulSoup(r.text, 'html.parser')
                dateselector=soup.select('div.author__date')
                date=(dateselector[0]).get_text()
                date=datetonumeric(date)
                print(date)
                if(date!=""):
                    titleselector=soup.select('h1.article-title')
                    title=titleselector[0].get_text()
                    title=title.replace(",",",")
                    pretextselector=soup.select("div.article__perex")
                    pretext=pretextselector[0].get_text()
                    pretext=pretext.replace(",",",")
                    alltext=soup.select('#article-content p')
                    maintext=""
                    for text in alltext:
                        maintext=maintext + (text.get_text()).replace("\n",",")
                        maintext=maintext+"\n"
                    maintext=maintext.replace(",",",")
                    spamwriter.writerow([id_clanku,'aktualne',date,title,pretext,maintext,url])
                    count=count+1
            except:
                print("wrong request")
            
