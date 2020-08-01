import requests
import json,schedule,time
import pandas as pd
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re


def global_news_update():
    url = "https://www.worldometers.info/coronavirus/"
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    urls = []
    heading = []
    for news in soup.find_all('div', class_='news_post'):
        heading.append(news.text)
        for url in news.find_all('a', class_='news_source_a'):
            urls.append(url.get('href'))
    clear_data = []
    for i in heading:
    #     clean=i.str.replace('[^\w\s]'," ")
        clean = re.sub(r'[\n]', ' ', i)
        clear_data.append(clean)
    final_news = []
    for i in clear_data:
        final_news.append(i.replace('source', ''))
    df_news_zipped = list(zip(final_news, urls))
    df_news = pd.DataFrame(df_news_zipped, columns=['Title', 'Source'])
    news = []
    for i, title in enumerate(df_news['Title']):
        news.append({'id':i, 'title':title})
    return heading


