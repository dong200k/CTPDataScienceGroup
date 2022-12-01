import streamlit as st
import numpy as np
import pandas as pd
import re
import plotly.figure_factory as ff
from streamlit_option_menu import option_menu
from PIL import Image

ctp_logo = Image.open("images/ctp icon.png")
st.set_page_config(
    page_icon=ctp_logo,
    layout="wide"
)

# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 1

def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="",  # required
                menu_icon="",
                options=["Dataset Details",
                         "Which state has the highest salary?",
                         "Which sector provides the highest salary?",
                         "Which industry provides the highest salary?",
                         "A correlation between revenue and salary?",
                         "Correlation between the number of competitors and salary range?"],  # required
                styles={
                    "nav-link": {"font-size": "15px"},
                    "menu-title": {"font-size": "18px"},
                    "container": {"padding": "10px!important"},
                    "icon": {"font-size": "15px"}
                },
                default_index=0,  # optional
            )
        return selected

    if example == 2:
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Dataset Details",
                     "Which state has the highest salary?",
                     "Which sector provides the highest salary?",
                     "Which industry provides the highest salary?",
                     "A correlation between revenue and salary?",
                     "Correlation between the number of competitors and salary range?"],  # required
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected

    if example == 3:
        # 2. horizontal menu with custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Home", "Projects", "Contact"],  # required
            icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )
        return selected


selected = streamlit_menu(example=EXAMPLE_NO)

if selected == "Dataset Details":
    # Create a page header
    st.header("Dataset")

    df = pd.read_csv('data/DS_DA_BS.csv')
    # Clean salary column: we only want yearly salaries
    for ind in df.index:
        if re.search("Hour|-1", df['Salary Estimate'][ind]):
            df.drop([ind], inplace=True)

    # Clean null value
    df.replace(['-1'], [np.nan], inplace=True)
    df.replace(['-1.0'], [np.nan], inplace=True)
    df.replace([-1], [np.nan], inplace=True)


    # Find min, max, and mean salaries
    def extract_numbers_max(x):
        temp = re.findall(r'[0-9]+', x)
        return max([int(i) for i in temp])


    def extract_numbers_min(x):
        temp = re.findall(r'[0-9]+', x)
        return min([int(i) for i in temp])


    df['min salary'] = df['Salary Estimate'].apply(extract_numbers_min)
    df['max salary'] = df['Salary Estimate'].apply(extract_numbers_max)
    df['mean salary'] = (df['min salary'] + df['max salary']) / 2


    # extract states
    def state_extract(x):
        return x.split(',')[-1]


    df['states'] = df['Location'].apply(state_extract)
    with st.expander("Click here to view the data"):
        st.markdown("Here is our data:")
        st.dataframe(data=df[['Job Title', 'role', 'states', 'Sector', 'Company Name', 'mean salary']], width=None,
                     height=None)

    st.markdown("**DS,DA,BA Salaries Comparison**")
    DS_salaries = list(df[df['role'] == 'DS']['mean salary'])
    DA_salaries = list(df[df['role'] == 'DA']['mean salary'])
    BA_salaries = list(df[df['role'] == 'BA']['mean salary'])
    hist_data = [DS_salaries, DA_salaries, BA_salaries]
    fig = ff.create_distplot(
        hist_data, ['DS', 'DA', 'BA'])
    st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(
            df.groupby(['role'])['mean salary'].aggregate(['count', 'mean', 'std', 'median']).sort_values(by='mean',
                                                                                                          ascending=False))
        st.caption(
            'The table above shows the job count for DS, BA, and DA. In addition, mean, std, and median of salaries are displayed in the table.')
    with col2:
        st.markdown('''
    * A **Data Scientist** specializes in high-level data manipulation, including writing complex algorithms and computer programming. **Business Analysts** are more focused on creating and interpreting reports on how the business is operating day to day, and providing recommendations based on their findings.
    * Data analysts and business analysts both help drive data-driven decision-making in their organizations. Data analysts tend to work more closely with the data itself, while business analysts tend to be more involved in addressing business needs and recommending solutions.''')

    st.markdown("### Data Sources")
    st.markdown("[Data Scientist Jobs](https://www.kaggle.com/datasets/andrewmvd/data-scientist-jobs)")
    st.markdown("[Business Analyst Job Listings](https://www.kaggle.com/datasets/andrewmvd/business-analyst-jobs)")
    st.markdown("[Data Analyst Jobs](https://www.kaggle.com/datasets/andrewmvd/data-analyst-jobs)")


if selected == "Which state has the highest salary?":
    st.header("Which state has the highest salary?")

if selected == "Which sector provides the highest salary?":
    st.header("Which sector provides the highest salary?")

if selected == "Which industry provides the highest salary?":
    st.header("Which industry provides the highest salary?")

if selected == "A correlation between revenue and salary?":
    st.header("A correlation between revenue and salary?")

if selected == "Correlation between the number of competitors and salary range?":
    st.header("Correlation between the number of competitors and salary range?")




