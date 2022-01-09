import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime
import numpy as np

st.title('株価取得')

days = 20
tickers = {
    'apple': 'AAPL',
    'Facebook': 'FB',
    'Google': 'GOOGL',
    'Microsoft': 'MSFT',
    'Netflix': 'NFLX',
    'amazon': 'AMZN'
}

df = pd.DataFrame()

for company in tickers.keys():
    tkr = yf.Ticker(tickers[company])
    hist = tkr.history(f'{days}d')
    hist.index = hist.index.strftime('%d %B %Y')
    hist = hist[['Close']]
    hist.columns = [company]
    hist = hist.T
    hist.index.name = 'Name'
    df = pd.concat([df, hist])

df
