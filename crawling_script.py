from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re


def date_cleansing(test):
    try:
        pattern = r'\d+\.(\d+)\.(\d+)\.'
        r = re.compile(pattern)
        match = r.search(test).group(0)
        return match
    except AttributeError:
        pattern = r'\w* (\d\w*)'
        r = re.compile(pattern)
        match = r.search(test).group(1)
        return match


def contents_cleansing(contents):
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '', str(contents)).strip()
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '', first_cleansing_contents).strip()
    third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
    return third_cleansing_contents


def crawler(maxpage, query, sort, s_date, e_date):
    title_text = []
    link_text = []
    source_text = []
    date_text = []
    contents_text = []

    s_from = s_date.replace(".", "")
    e_to = e_date.replace(".", "")
    page = 1
    maxpage_t = (int(maxpage) - 1) * 10 + 1

    while page <= maxpage_t:
        url = (f"https://search.naver.com/search.naver?where=news&query={query}"
               f"&sort={sort}&ds={s_date}&de={e_date}&nso=so%3Ar%2Cp%3Afrom{s_from}to{e_to}%2Ca%3A&start={page}")
        try:
            response = requests.get(url)
            response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
        except requests.exceptions.RequestException as e:
            print(f"HTTP 요청 중 오류 발생: {e}")
            break

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"BeautifulSoup 파싱 중 오류 발생: {e}")
            break

        atags = soup.select('.news_tit')
        for atag in atags:
            title_text.append(atag.text)
            link_text.append(atag['href'])

        source_lists = soup.select('.info_group > .press')
        for source_list in source_lists:
            source_text.append(source_list.text)

        date_lists = soup.select('.info_group > span.info')
        for date_list in date_lists:
            if "면" not in date_list.text:
                date_text.append(date_list.text)

        contents_lists = soup.select('.news_dsc')
        for contents_list in contents_lists:
            contents_text.append(contents_cleansing(contents_list))

        page += 10

    result = {
        "date": date_text,
        "title": title_text,
        "source": source_text,
        "contents": contents_text,
        "link": link_text
    }
    df = pd.DataFrame(result)

    # 데이터프레임에서 빈 데이터가 포함된 행을 제거합니다.
    df = df.dropna().reset_index(drop=True)
    return df
