# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd

st.title('Get Bitcoin Price')

# Display slider
days = st.slider('No of Days', 1, 365, 30)

# Providing currency selection option using Radio button
currency = st.radio(
     "Currency",
     ('CAD', 'USD', 'INR'))

# Passing parameters as query string to the API
r = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?', 
                  params={'vs_currency': currency, 'days':days,'interval':'daily'})


# Formatting data for chart once request is successful.
if r.status_code == 200:
    APIOutput = r.json()
    
    APIOutput_df = pd.DataFrame.from_dict(APIOutput['prices'])
    APIOutput_df.columns = ['Date', 'Valuation']
    APIOutput_df.Date = pd.to_datetime(APIOutput_df['Date'],unit='ms')
    APIOutput_df = APIOutput_df.set_index('Date')


# Plotting chart.
st.line_chart(APIOutput_df, use_container_width=True)

# Displaying mean value of the price.
st.write("Average price during this time was ", (APIOutput_df['Valuation'].mean())," in ",currency)