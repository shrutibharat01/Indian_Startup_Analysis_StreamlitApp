""" Root of the Web Application """

import pandas as pd
import streamlit as st
from validation import validation
import plotly.express as px
import matplotlib.pyplot as plt


# ----------------------------------------------- Utility functions -------------------------------------------------------
# line breaks
def lb(n=1):  
    for _ in range(n):
        st.markdown('''
        <br>
        ''', unsafe_allow_html=True)

# Header
def page_header(title, color, size=2.8, top=50, bottom=50):
    st.markdown(f"""
    <h1 style="text-align: center; color: {color}; font-size: {size}rem; margin-top: -{top}px; margin-bottom: -{bottom}px">
    {title}
    </h1>
    """, unsafe_allow_html=True)

# Sub heading
def text(txt):
    st.markdown(f"""
    <p style="text-align: center; font-size: 1.5rem">
    {txt}
    </p>
    """, unsafe_allow_html=True)


# Dataset
df = pd.read_csv('Startup_clean_data.csv')

# Page Configuration ...
ch_color = "#040D12"
st.set_page_config(layout='wide', page_title='Startup Analysis', page_icon='📊')


# ------------------------------------------------- Front Page ----------------------------------------------------------- 


def main():
    page_header(title='Indian Startup Funding Dashboard',color='lightblue', size=2.5, top=80)
    lb(3)
    c1, c2, c3 = st.columns((3, 8, 3), gap='medium')
    with c2:
        st.image('Cover_image.png', caption='Front cover image', use_column_width='auto')
        lb()
        st.markdown("""
        ##### A detailed analysis of Indian Startups based on a **Kaggle** dataset.
        Choose an analysis option from the **dropdown menu** in the sidebar to view the corresponding details. 📊
        """)
        st.markdown("""
        > Dataset link - [Indian Startup Funding](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding)
        """)


def overall():
    """Provides an overall analysis of the dataset with metrics and visualizations."""
    # Total invested amount
    total = round(df['Amount in Rs.'].sum())
    # Max amount infused in a startup
    max = df.groupby('Startup Name')['Amount in Rs.'].max().sort_values(ascending=False).head(1).values[0]
    # Avg ticket size
    mean = df.groupby('Startup Name')['Amount in Rs.'].sum().mean()
    # Total funded startups
    # num_startups = df['Startup Name'].nunique()

    # Rendered items ...
    page_header(title="Overall Analysis", color="lightblue", size=2.25)

    # Columns
    c1, c2, c3, c4 = st.columns(4, gap='large')

    with c1:
        st.metric('Total Investment', str(total) + 'Cr')
    with c2:
        st.metric('Maximum Investment', str(max) + 'Cr')
    with c3:
        st.metric('Average Investment', str(mean) + 'Cr')
    # with c4:
    #     st.metric('Funded startups' + str(num_startups))

    c5, padding, c6 = st.columns((10, 2, 10), gap='medium')
    c7, padding, c8 = st.columns((10, 2, 10), gap='medium')


    # Month on month graph using line chart
    with c5:
        st.subheader('Month on Month Graph')

        opt = st.selectbox('Select the type of aggregation', ['Total Investment', 'Investment Count'])

        if opt == "Total Investment":
            tdf = validation.momg1(df)
            st.line_chart(data=tdf, x='Month-Year', y='Amount in Crores')

        elif opt == "Investment Count":
            tdf2 = validation.momg2(df)
            st.line_chart(data=tdf2, x='Month-Year', y='Count of investments')

    # Top 5 sectors using pie chart
    with c6:
        st.subheader('Top 5 Sectors')
        cp = validation.catpie(df)
        top5 = px.pie(
            labels=cp.index.values,
            values=cp.values,
            names=cp.index.values,
            height=400,
            width=500,
            color_discrete_sequence=px.colors.sequential.Tealgrn_r,
            hole=0.4
        )
        st.plotly_chart(top5)

    # Top 5 startups using slider
    with c7:
        st.subheader('Top 5 Startups')
        year1 = st.slider('Choose year for Startups', 2015, 2020, 2017)
        top5 = validation.top5start(df, year1)
        st.dataframe(top5, width=600)

    # Top 5 investors using slider
    with c8:
        st.subheader('Top 5 Investors')
        year2 = st.slider('Choose year for Investors', 2015, 2020, 2017)
        top5 = validation.top5inv(df, year2)
        st.dataframe(top5, width=600)


def startups(btn1, df, startup):
    if btn1:
        dfs = validation.startup_details(df, startup)
        rnd = validation.round_inv(df, startup)
        inv = validation.startup_inv(df, startup)

        pad1, col, pad2 = st.columns((2, 8, 2), gap='small')

        with col:
            st.header(startup)
            st.divider()
            st.subheader('Overall details')
            st.dataframe(dfs)

            c1, pad, c2 = st.columns((10, 1, 10), gap='small')

            with c1:
                st.subheader('Stage')
                st.dataframe(rnd)

            with c2:
                st.subheader("Investor(s)")
                st.dataframe(inv)

    else:
        lb(2)
        text(
            "Select a <b style='color:#93B1A6'>startup</b> name from the dropdown menu located in the <b>sidebar</b> to view their details.")


def investors(btn2, df, investor):
    if btn2:
        st.header(investor)
        st.divider()

        col1, padd, col2 = st.columns((7, 2, 7), gap='small')
        col3, padd, col4 = st.columns((7, 2, 7), gap='small')
        col5, padd, col6 = st.columns((7, 2, 7), gap='small')

        # Recent investors
        with col1:
            recent = validation.recent_inv(df, investor)
            st.subheader('Most recent investments')
            st.dataframe(recent)

        # Top 5 investors
        with col2:
            top5 = validation.big_inv(df, investor)
            st.subheader('Top 5 investments')

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(top5['Startup Name'], top5['Amount in Cr.'], color="lightblue")

            # Chart Color Customization ...
            ax.set_facecolor(ch_color)
            fig.set_facecolor(ch_color)

            # Chart LEGEND colors ...
            ax.tick_params(axis='x', colors='white', labelsize=8)
            ax.tick_params(axis='y', colors='white', labelsize=8)

            # Chart BORDER colors ...
            ax.spines['top'].set_color(ch_color)
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color(ch_color)

            plt.xlabel("Startup", color="white", fontsize=10)
            plt.ylabel("Amount in Crores", color="white", fontsize=10)

            st.pyplot(fig)

        # Sector wise investors
        with col3:
            sec = validation.sector_inv(df, investor)
            st.subheader("Sectors of investment")
            pie1 = px.pie(
                labels=sec.index.values,
                values=sec.values,
                names=sec.index.values,
                hole=0.4,
                height=400,
                width=500,
                color_discrete_sequence=px.colors.sequential.Teal
            )
            st.plotly_chart(pie1)

        # City in which investment has done
        with col4:
            city = validation.city(df, investor)
            st.subheader("Cities of investment")
            pie3 = px.pie(labels=city.index.values,
                          values=city.values,
                          names=city.index.values,
                          hole=0.4,
                          height=400,
                          width=500,
                          color_discrete_sequence=px.colors.sequential.Darkmint_r
                          )
            st.plotly_chart(pie3)

        # Investment stages
        with col5:
            stg = validation.stage_inv(df, investor)
            st.subheader("Stages of investment")
            pie2 = px.pie(
                labels=stg.index.values,
                values=stg.values,
                names=stg.index.values,
                hole=0.4,
                height=400,
                width=500,
                color_discrete_sequence=px.colors.sequential.Blugrn_r
            )
            st.plotly_chart(pie2)

        # Year on year investment
        with col6:
            yearly = validation.yrinv(df, investor)
            st.subheader("Year on year investment")
            st.line_chart(yearly, y='Amount in Crores')

    else:
        lb(2)
        text(
            "Select an <b style='color:lightblue'>investor</b> name from the dropdown menu located in the <b>sidebar</b> to view their details.")


# ---------------------------------- S I D E B A R ---------------------------------- #


st.sidebar.title('Startup Funding Analysis')

lb()

option = st.sidebar.selectbox('Choose analysis option', ["Drop Down", "Overall Analysis", "Startups", "Investors"])

if option == "Drop Down":
    main()
elif option == "Overall Analysis":
    overall()
elif option == "Startups":
    page_header(title="Startup Analysis", color="lightblue", size=2.5)
    startup = st.sidebar.selectbox("Select a startup", df['Startup Name'].unique().tolist())
    btn1 = st.sidebar.button('Find Startup details')
    startups(btn1, df, startup)
elif option == "Investors":
    page_header(title="Investor Analysis", color="lightblue", size=2.5)
    investor = st.sidebar.selectbox("Select an investor", validation.investor_list(df))
    btn2 = st.sidebar.button('Find Investor details')
    investors(btn2, df, investor)
