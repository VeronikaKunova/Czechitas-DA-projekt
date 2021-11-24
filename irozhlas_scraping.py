from os import pipe
import requests
from bs4 import BeautifulSoup
import json
import csv



def datetonumeric(stringdate):
    spliteddate=stringdate.split()
    thedate=spliteddate[0].split("-")
    year=int(thedate[0])
    themonth=int(thedate[1])
    day=int(thedate[2])
    if(themonth >10 or themonth < 7):
        return ""
    if(themonth==10 and day>7):
        return ""
    return f'{day}/{themonth}/{year}'



count=0
with open('C:\Czechitas\Projekt\scraping\irozhlasoutput.csv', 'w', newline='', encoding="UTF-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';' )
    spamwriter.writerow(['id_clanku','zdroj','datum','title','perex','text','url'])
    for i in range(0,3):
        r=requests.get(f'https://www.irozhlas.cz/volby?page={i}')
        soup = BeautifulSoup(r.text, 'html.parser')
        articles=soup.select(".c-articles__list")
        for article in articles:

            try:
            # id=(json.loads(article['data-track-list']))['item']['id']
                id_clanku=f'IR000{count+1}'
                urlselector=(article.select("h3 a"))
                url=f"https://www.irozhlas.cz{(urlselector[0])['href']}"
                r=requests.get(url)
                soup=BeautifulSoup(r.text, 'html.parser')
                dateselector=soup.select('time')
                date=((dateselector[0]))['datetime']
                date=datetonumeric(date)
                print(date)
                if(date!=""):
                    titleselector=soup.select('#article-news-full-8597080')
                    if(len(titleselector)==0):
                        titleselector=soup.select('h1')
                    title=titleselector[0].get_text()
                    title=title.replace(",",",")
                    title=title.replace("\n",",")
                    
                    pretextselector=soup.select("#main > div > article > div > div > div > header > p.text-bold--m.text-md--m.text-lg")
                    if(len(pretextselector)==0):
                        pretextselector=soup.select("p")
                    pretext=pretextselector[3].get_text()
                    pretext=pretext.replace(",",",")
                    alltext=soup.select('.col--main .b-detail > p')
                    if(len(alltext)==0):
                        alltext=soup.select("p")
                    alltext[4:]
                    maintext=""
                    for text in alltext:
                        maintext=maintext + (text.get_text()).replace("\n",",")
                        maintext=maintext+"\n"
                    maintext=maintext.replace(",",",")
                    titel="the title missed"
                    pretext="the pretext missed"
                    maintext="the main text missed"
                    spamwriter.writerow([id_clanku,'irozhlas',date,title,pretext,maintext,url])
                    count=count+1
            except:
                print("wrong request")
       
            
