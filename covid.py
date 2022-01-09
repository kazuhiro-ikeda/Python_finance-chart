import streamlit as st
import datetime
import pandas as pd
from urllib.request import Request, urlopen

# タイトル描画
st.title('COVID-19 Data Visualization')

dt_now = datetime.datetime.now()
st.text('現在日時:' + dt_now.strftime('%Y年%m月%d日 %H:%M:%S'))

# 単日PCR検査陽性者数の集計情報
st.markdown('## PCR 検査陽性者数(単日) 集計情報')
# CSVデータの読み込み
df = pd.read_csv(
    'https://www.mhlw.go.jp/content/pcr_positive_daily.csv', parse_dates=True, index_col=0)
df = df.agg(['sum', 'mean', 'max', 'min'])
df = df.rename(index={'sum': '合計',
                      'mean': '平均',
                      'max': '最大',
                      'min': '最小'})
# テーブル描画
st.table(df)

# 県別感染者情報
st.markdown('## 県別感染者情報')

# 県別感染者データ読み込み
# Pandas.read_csvでは403となったため、urllibを使用する。
req = Request(
    'https://www3.nhk.or.jp/n-data/opendata/coronavirus/nhk_news_covid19_prefectures_daily_data.csv')
req.add_header(
    'User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
content = urlopen(req)
df = pd.read_csv(
    content, index_col=0, parse_dates=True)

# 都道府県選択セレクトボックス
option = st.selectbox(
    '都道府県',
    ('北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'))

# 選択した都道府県データを抽出
df = df[df['都道府県名'] == option]
column_name = '月別感染者数( '+option+' )'
df = df.rename(
    columns={'各地の感染者数_1日ごとの発表数': column_name})
df = df.loc[:, [column_name]]

# 月別合計値を取得
df = df.resample('M').sum()

# 折れ線グラフ描画
st.line_chart(df)