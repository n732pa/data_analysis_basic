import pandas as pd
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS
from konlpy.tag import Okt
import collections

def req_url(url):
    res = requests.get(url).text
    soup = BeautifulSoup(res) 
    return soup  
   
def data_create():
    url='https://news.naver.com/breakingnews/section/101/259'
    soup = req_url(url)
    temp = soup.select_one('ul.sa_list').select('li',limit=5)

    new_list=[]
    for li in temp:
        new_info = {'title':li.select_one('strong.sa_text_strong').text,
                    'date':li.select_one('div.sa_text_datetime.is_recent').text,
                    'news_url':li.select_one('a')['href']}
        new_list.append(new_info)
    
    for new in new_list:
        new_url = new['news_url']
        soup = req_url(new_url)

        body = soup.select_one('article.go_trans._article_content')
        new_content = body.text.replace('\n','').strip()
        new['news_content'] = new_content

    df = pd.DataFrame(new_list)

    return df

def text_vis(df):
    okt = Okt()
    clist = []
    for word in df['news_content']:
        token = okt.pos(word)
        for word,tag in token:
            if tag in ['Noun','Adjective']:
                clist.append(word)
    counts = collections.Counter(clist)
    tag = counts.most_common(100)
    s_words=STOPWORDS.union({'있다','이','것'})       

    fpath ='C:/Windows/Fonts/malgunbd.ttf'
    wc = WordCloud(font_path=fpath, background_color='white',stopwords=s_words)
    cloud = wc.generate_from_frequencies(dict(tag))

    plt.figure(figsize=(10,8))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()

if __name__=='main':
    df = data_create()
    text_vis(df)

