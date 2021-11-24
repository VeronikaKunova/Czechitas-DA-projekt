
import requests
from bs4 import BeautifulSoup
import json
import csv

def month(themonth):
    if(themonth=="červenec" or themonth=="července"):
        return 7
    elif(themonth=="srpna" or themonth=="srpen"):
        return 8
    elif(themonth=="Září"):
        return 9
    elif(themonth=="října" or themonth=="říjen"):
        return 10
    else:
        return 0

def datetonumeric(stringdate):
    spliteddate=stringdate.split()
    day=spliteddate[0]
    day=day[0:len(day)-1]
    day=int(day)
    year=int(spliteddate[2])
    themonth=month(spliteddate[1])
    if(themonth==0):
        return ""
    if(themonth==10 and day>7):
        return ""
    return f'{day}/{themonth}/{year}'





count=0
with open('bleskoutput.csv', 'w', newline='', encoding="UTF-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';' )
    spamwriter.writerow(['id_clanku','zdroj','datum','title','perex','text','url'])
    for i in range(1,10):
        r=requests.get(f'https://www.blesk.cz/volby?page={i}')
        soup = BeautifulSoup(r.text, 'html.parser')
        articles=soup.select(".list-article-horizontal-middle")
        for article in articles:

            try:
            # id=(json.loads(article['data-track-list']))['item']['id']
                id_clanku=f'BL000{count}'
                urlselector=(article.select("h2 a"))
                url=(urlselector[0])['href']
                r=requests.get(url)
                soup=BeautifulSoup(r.text, 'html.parser')
                dateselector=soup.select('div.date')
                date=(dateselector[0]).get_text()
                date=datetonumeric(date)
                if(date!=""):
                    titleselector=soup.select('h1')
                    title=titleselector[0].get_text()
                    title=title.replace(",",",")
                    pretextselector=soup.select("div.perex p")
                    pretext=pretextselector[0].get_text()
                    pretext=pretext.replace(",",",")
                    alltext=soup.select('div.content p')
                    maintext=""
                    for text in alltext:
                        maintext=maintext + (text.get_text()).replace("\n",",")
                        maintext=maintext+"\n"
                    maintext=maintext.replace(",",",")
                    spamwriter.writerow([id_clanku,'Blesk',date,title,pretext,maintext,url])
                    count=count+1
            except:
                print("wrong request")
            
