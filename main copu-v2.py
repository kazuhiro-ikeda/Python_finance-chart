import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('株価可視化アプリ')

st.sidebar.write(
    """
        # GAFA株価
        こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
    """
)

st.sidebar.write(
    """
        ## 表示日数選択
    """
)

days = st.sidebar.slider('日数', 1, 50, 20)

st.write(
    f"""
        ### 過去 **{days}日間** のGAFA株価
    """
)

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

st.sidebar.write(
    """
        ## 株価の範囲指定
    """
)

ymin, ymax = st.sidebar.slider(
    '範囲を指定してください。',
    0.0,
    3500.0,
    (0.0, 3500.0)
)

tickers = {
    'apple': 'AAPL',
    'facebook': 'FB',
    'google': 'GOOGL',
    'microsoft': 'MSFT',
    'netflix': 'NFLX',
    'amazon': 'AMZN',
    'トヨタ自動車': '7203.T'
}

df = get_data(days, tickers)

companies = st.multiselect(
    '会社名を選択してください',
    list(df.index),
    ['google', 'apple']
)

if not companies:
    st.error('1社は選択してください')
else:
    data = df.loc[companies]
    st.write('#### 株価USD', data.sort_index())



companies = ['apple', 'facebook', 'google', 'microsoft', 'netflix', 'amazon', 'トヨタ自動車']
data = df.loc[companies]
data = data.sort_index(ascending=False)
data = data.T.reset_index()
data = pd.melt(data, id_vars=['index']).rename(
    columns={
        'index': 'Date',
        'value': 'Stock Prices(USD)'
    }
)
data

ymin, ymax = (250, 300)
chart = (
    alt.Chart(data).mark_line(opacity=0.8, clip=True).encode(
        x="Date:T",
        y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
        color='Name:N'
    )
)

chart

st.subheader('おまけ')
aapl = yf.Ticker('AAPL')

aapl_data = aapl.actions.head()
aapl_data

'配当金'
aapl_dividends = aapl.dividends
st.line_chart(aapl_dividends)

'stock'
aapl_stock = aapl.actions['Stock Splits']
st.line_chart(aapl_stock)

'Tickerの情報取得'
sector = aapl.info['sector']  # 情報を取得
f'セクター：{sector}'
#aapl.info
