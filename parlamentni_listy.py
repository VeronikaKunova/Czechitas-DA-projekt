
import requests
from bs4 import BeautifulSoup
import json
import csv


def datetonumeric(stringdate):
    spliteddate=stringdate.split()
    data=(spliteddate[0]).split(".")
    day=int(data[0])
    themonth=int(data[1])
    year=int(data[2])
    if(themonth >10 or themonth < 7):
        return ""
    if(themonth==10 and day>7):
        return ""
    return f'{day}/{themonth}/{year}'



count=0
with open('parlamentnilistyoutput.csv', 'w', newline='', encoding="UTF-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';')
    spamwriter.writerow(['id_clanku','zdroj','datum','title','perex','text','url'])
    for i in range(20,70):
        r=requests.get(f'https://www.parlamentnilisty.cz/special/Volby%202021?p={i}')
        soup = BeautifulSoup(r.text, 'html.parser')
        articles=soup.select(".articles-list ul.list-unstyled li")
        for article in articles:

            try:
            # id=(json.loads(article['data-track-list']))['item']['id']
                id_clanku=f'PA000{count+1}'
                urlselector=(article.select("a"))
                url=f"https://www.parlamentnilisty.cz{(urlselector[0])['href']}"
                r=requests.get(url)
                soup=BeautifulSoup(r.text, 'html.parser')
                dateselector=soup.select('div.time')
                date=(dateselector[0]).get_text()
                date=datetonumeric(date)
                print(date)
                if(date!=""):
                    titleselector=soup.select('.article-header h1')
                    title=titleselector[0].get_text()
                    title=title.replace(",",",")
                    pretextselector=soup.select("p.brief")
                    pretext=pretextselector[0].get_text()
                    pretext=pretext.replace(",",",")
                    alltext=soup.select('.article-content > p')
                    maintext=""
                    for text in alltext:
                        maintext=maintext + (text.get_text()).replace("\n",",")
                        maintext=maintext+"\n"
                    maintext=maintext.replace(",",",")
                    spamwriter.writerow([id_clanku,'parlamentnilisty',date,title,pretext,maintext,url])
                    count=count+1
            except:
                print("wrong request")
            break
            
