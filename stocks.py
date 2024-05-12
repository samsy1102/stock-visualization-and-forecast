from datetime import date
import streamlit as st
import yfinance as yf
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go

# Set up your Streamlit app layout
st.write("Welcome")

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stocks')

stocks = ('VEDL.NS','TATASTEEL.NS','BANKBARODA.NS','SBIN.NS')
selected_stock = st.selectbox('Select dataset for prediction', stocks)

n_months = st.slider('Months of prediction:', 1, 5)
period = n_months * 30

# Move the logout button to the top left corner using HTML
logout_button_html = """
    <div style="position: absolute; top: 10px; right: 10px;">
        <form action='http://localhost:8501'>
            <input type='submit' value='Logout'>
        </form>
    </div>
"""


# Button for forex page
Forex_button = """
    <div style="position: absolute; top: 10px; left: 10px;">
        <form action='http://localhost:8503'>
            <input type='submit' value='Forex'>
        </form>
    </div>
"""

st.markdown(Forex_button, unsafe_allow_html=True)

st.markdown(logout_button_html, unsafe_allow_html=True)


@st.cache_resource
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("   ")
data = load_data(selected_stock)


st.subheader('Raw data')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.update_layout(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()


# Forecast with ARIMA
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

model = sm.tsa.ARIMA(df_train['y'], order=(10,3,9))
results = model.fit()

forecast_steps = period
forecast = results.forecast(steps=forecast_steps)

st.subheader('Forecast data')
forecast_index = pd.date_range(start=df_train['ds'].iloc[-1], periods=forecast_steps+1, freq='D')[1:]
forecast_df = pd.DataFrame({'ds': forecast_index, 'yhat': forecast})

st.write(forecast_df.tail())

st.write(f'Forecast plot for {n_months} Months')
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df_train['ds'], y=df_train['y'], name='Actual'))
fig1.add_trace(go.Scatter(x=forecast_index, y=forecast, name='Forecast'))
fig1.update_layout(title_text=f'Forecast for {n_months} Months', xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig1)
