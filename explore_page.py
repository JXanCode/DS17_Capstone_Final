import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


def load_data():
    df = pd.read_csv('data/friday_data_1976.csv')
    df.set_index('model_date',inplace=True)
    return df

st.cache_data
friday_1976 = load_data()

def show_explore_page():
    st.title('Explore the relationship between 10-year U.S. Treasury yields and the S&P 500')
    st.write('Data is from September 1976 to January 2024 ')



# Yield comparison with S&P 500 plot
    #fig, ax = plt.subplots()
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=friday_1976.index, y=friday_1976['DGS10'], name="10-year yield"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=friday_1976.index, y=friday_1976['^GSPC'], name="S&P 500",marker=dict(color='Green')),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="10-year U.S. Treasury yield (%) vs. S&P 500 Index"
        )

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=12, label="1y", step="month", stepmode="backward"),
                dict(count=36, label="3y", step="month", stepmode="backward"),
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(count=10, label="10y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )


    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="10-year U.S. Treasury yield (%)", secondary_y=False)
    fig.update_yaxes(title_text="S&P 500 Index", secondary_y=True)

    st.plotly_chart(fig)



# Box plot
    st.write('The following box plot examines the spread of 3-month percentage changes in the S&P 500 according to the coinciding change in 10-year U.S. Treasury yields.')

    fig = px.box(friday_1976, x="DGS10_change_range", y="^GSPC_13WChange")

    fig.update_layout(
        title_text="3-month % Change in S&P 500 based on coinciding change in 10-year U.S. Treasury yield"
    )

    fig.update_xaxes(title_text="3-month change in 10-year U.S. Treasury yield")
    fig.update_yaxes(title_text="3-month % change in S&P 500")

    st.plotly_chart(fig)


# Reward-risk table
    st.write('The following table describes the historical reward-to-risk profile of the S&P 500 according to the coinciding change in 10-year U.S. Treasury yields.')
    st.write("Results are based on 3-month rolling periods, except for the 'Reward-to-risk' ratio which is annualized.")

    # To see how the S&P 500 (GSPC) moves coincidentally to changes in DGS10

    DGS10_change_comp = friday_1976.groupby('DGS10_change_range')['^GSPC_13WChange'].agg(['mean','std','min','max'])

    # Calculate reward-to-risk using annualized average return and annualized volatility
    DGS10_change_comp['Reward-to-risk'] = ( DGS10_change_comp['mean'] / DGS10_change_comp['std'] ) * 4**0.5

    DGS10_change_comp.columns = ['mean (%)','std (%)','min (%)', 'max (%)', 'Reward-to-risk']


    st.dataframe(DGS10_change_comp)