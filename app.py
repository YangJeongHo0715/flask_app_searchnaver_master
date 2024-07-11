from flask import Flask, render_template, request, jsonify
from crawling_script import crawler
from text_mining import text_preprocessing, extract_keywords
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def index():
    data = []
    keywords_data = []  # 추가된 키워드 빈도수 데이터

    if request.method == 'POST':
        maxpage = request.form['maxpage']
        query = request.form['query']
        sort = request.form['sort']
        s_date = request.form['s_date']
        e_date = request.form['e_date']

        # 크롤링 함수 호출
        df = crawler(maxpage, query, sort, s_date, e_date)
        data = df.to_dict('records')

        # 텍스트마이닝을 위한 기사 내용 전처리 및 키워드 추출
        all_contents = ' '.join(df['contents'].apply(text_preprocessing))
        keywords = extract_keywords(all_contents, n=10)
        keywords_data = [{'keyword': keyword, 'count': count} for keyword, count in keywords]

    return render_template('index.html', data=data, keywords_data=keywords_data)

if __name__ == '__main__':
    app.run(debug=True)
