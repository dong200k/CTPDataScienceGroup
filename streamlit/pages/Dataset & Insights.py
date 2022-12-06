import folium
from streamlit_option_menu import option_menu
from PIL import Image
from streamlit_folium import st_folium
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.express as px

ctp_logo = Image.open("images/ctp icon.png")
st.set_page_config(
    page_icon=ctp_logo,
    layout="wide"
)

# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 1

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
    state = x.split(',')[-1]
    return state

df['states'] = df['Location'].apply(state_extract)

df_map = df
df_company= df
df_revenues= df

def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="",  # required
                menu_icon="",
                options=["Introduce DS/DA/BA Dataset",
                         "Insight of DS/DA/BA By Sectors",
                         "Insight of DS/DA/BA By States",
                         "Insight of DS/DA/BA By Company Size & Revenue"],  # required
                styles={
                    "nav-link": {"font-size": "15px"},
                    "menu-title": {"font-size": "18px"},
                    "container": {"padding": "10px!important"},
                    "icon": {"font-size": "15px"}
                },
                default_index=0,  # optional
            )
        return selected
    #
    # if example == 2:
    #     # 2. horizontal menu w/o custom style
    #     selected = option_menu(
    #         menu_title=None,  # required
    #         options=["Dataset Details",
    #                  "All Data Science Jobs Salary By Sectors",
    #                  "Which sector provides the highest salary?",
    #                  "Which industry provides the highest salary?",
    #                  "A correlation between revenue and salary?",
    #                  "Correlation between the number of competitors and salary range?"],  # required
    #         menu_icon="cast",  # optional
    #         default_index=0,  # optional
    #         orientation="horizontal",
    #     )
    #     return selected
    #
    # if example == 3:
    #     # 2. horizontal menu with custom style
    #     selected = option_menu(
    #         menu_title=None,  # required
    #         options=["Home", "Projects", "Contact"],  # required
    #         icons=["house", "book", "envelope"],  # optional
    #         menu_icon="cast",  # optional
    #         default_index=0,  # optional
    #         orientation="horizontal",
    #         styles={
    #             "container": {"padding": "0!important", "background-color": "#fafafa"},
    #             "icon": {"color": "orange", "font-size": "25px"},
    #             "nav-link": {
    #                 "font-size": "25px",
    #                 "text-align": "left",
    #                 "margin": "0px",
    #                 "--hover-color": "#eee",
    #             },
    #             "nav-link-selected": {"background-color": "green"},
    #         },
    #     )
    #     return selected


selected = streamlit_menu(example=EXAMPLE_NO)

if selected == "Introduce DS/DA/BA Dataset":
    # Create a page header
    st.header("DS/DA/BA Dataset")

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

if selected == "Insight of DS/DA/BA By Sectors":

    st.header("Insight of DS/DA/BA By Sectors")

    tab1, tab2 = st.tabs(["Comparison", "Sector with highest numer of Jobs in DS/DA/BA"])
    with tab1:
        options1 = st.multiselect('Add More Sectors To Compare',
                                  ['Information Technology',
                                   'Business Services',
                                   'Finance',
                                   'Health Care',
                                   'Biotech & Pharmaceuticals',
                                   'Insurance',
                                   'Manufacturing',
                                   'Education',
                                   'Government'], default=(['Biotech & Pharmaceuticals']))

        df_filtered_sectors = df[df.Sector.isin(options1)]

        data_sector = df_filtered_sectors.groupby('Sector')[
            ['min salary', 'max salary', 'mean salary']].mean().sort_values(
            ['mean salary', 'min salary', 'max salary'], ascending=False)

        st.dataframe(data_sector)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=data_sector.index,
            y=data_sector['mean salary'],
            name='Mean Salary'
        ))
        fig.add_trace(go.Bar(
            x=data_sector.index,
            y=data_sector['min salary'],
            name='Minimum Salary'
        ))
        fig.add_trace(go.Bar(
            x=data_sector.index,
            y=data_sector['max salary'],
            name='Maximum Salary'
        ))

        fig.update_layout(title='Salaries in Different Sectors', barmode='group')
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        color = plt.cm.plasma(np.linspace(0, 1, 9))
        ax1 = df['Sector'].value_counts().sort_values(ascending=False).head(9).plot.bar(color=color)
        plt.title("Sector with highest number of Jobs in DS/DA/BA")
        plt.xlabel("Sector")
        plt.ylabel("Count")
        st.pyplot(ax1.get_figure(), clear_figure=True)

        data_sector = df[df['Sector'].isin(
            ['Information Technology', 'Business Services', 'Finance', 'Health Care', 'Biotech & Pharmaceuticals'
                , 'Insurance', 'Manufacturing', 'Education', 'Government'])].groupby('Sector')[
            ['min salary', 'max salary', 'mean salary']].mean().sort_values(['mean salary', 'min salary', 'max salary'],
                                                                            ascending=False).head(8)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=data_sector.index,
            y=data_sector['mean salary'],
            name='Mean Salary'
        ))

        fig.add_trace(go.Bar(
            x=data_sector.index,
            y=data_sector['min salary'],
            name='Minimum Salary'
        ))

        fig.add_trace(go.Bar(
            x=data_sector.index,
            y=data_sector['max salary'],
            name='Maximum Salary'
        ))

        fig.update_layout(title='Salaries in Different Sectors', barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        * More jobs can be found in IT and Financial Industry
        * Biotech and IT have higher pay''')


if selected == "Insight of DS/DA/BA By States":
    st.header("Insight of DS/DA/BA By States")

    tab1, tab2 = st.tabs(["Top 8 States for DA/DS/BA", "Geographic Data Visualization"])
    with tab1:
        selected_states = [' TX', ' CA', ' NY', ' IL', ' AZ', ' PA', ' FL', ' OH', ' NJ']
        df_states_DS = pd.DataFrame(
            np.zeros((len(selected_states), 3)),
            index=selected_states,
            columns=['DS', 'DA', 'BA'])
        for i in selected_states:
            for j in ['DS', 'DA', 'BA']:
                df_states_DS.at[i, j] = len(df[(df['states'] == i) & (df['role'] == j)])

        ax = df_states_DS.head(8).plot.bar(stacked=True)
        plt.xlabel('State')
        plt.ylabel('Job Count')
        plt.title('Top 8 States for DS/DA/BA')
        fig1 = ax.get_figure()
        st.pyplot(fig1, clear_figure=True)

        df_ny = df[df['states'] == ' NY']
        df_tx = df[df['states'] == ' TX']
        df_ca = df[df['states'] == ' CA']
        p1, p2, p3 = st.columns(3)


        def plotting_function(df):
            DS_salaries = list(df[df['role'] == 'DS']['mean salary'])
            DA_salaries = list(df[df['role'] == 'DA']['mean salary'])
            BA_salaries = list(df[df['role'] == 'BA']['mean salary'])

            hist_data = [DS_salaries, DA_salaries, BA_salaries]
            fig = ff.create_distplot(
                hist_data, ['DS', 'DA', 'BA'])
            st.plotly_chart(fig, use_container_width=True)


        with p1:
            st.markdown("### New York")
            # plotting_function(df_ny)
            df_ny_info = df_ny.groupby(['role'])['mean salary'].aggregate(
                ['count', 'mean', 'std', 'median']).sort_values(
                by='mean', ascending=False)
            st.dataframe(df_ny_info, use_container_width=True)
        with p2:
            st.markdown("### Texas")
            # plotting_function(df_tx)
            st.dataframe(
                df_tx.groupby(['role'])['mean salary'].aggregate(['count', 'mean', 'std', 'median']).sort_values(
                    by='mean',
                    ascending=False),
                use_container_width=True)
        with p3:
            st.markdown("### California")
            # plotting_function(df_ca)
            st.dataframe(
                df_ca.groupby(['role'])['mean salary'].aggregate(['count', 'mean', 'std', 'median']).sort_values(
                    by='mean',
                    ascending=False),
                use_container_width=True)

        st.markdown('''
        * More jobs found in TX and CA
        * NY and CA offer higher salaries''')

    with tab2:
        df_filtered_states = df_map

        data_states = df_filtered_states.groupby('states', as_index=False)[
            ['min salary', 'max salary', 'mean salary']].mean().sort_values(
            ['mean salary', 'min salary', 'max salary'], ascending=False)

        state_dict2 = {}
        c = 0
        for i in data_states['states']:
            i = i.replace(' ', '')
            state_dict2[i] = c
            c += 1

        choropleth1 = folium.Choropleth(geo_data='data/us-state-boundaries.geojson')
        for feature in choropleth1.geojson.data['features']:
            state_stusab = feature['properties']['stusab']
            state_name = feature['properties']['name']

            if state_stusab in state_dict2:
                data_states['states'] = data_states['states'].replace(" "+ state_stusab, state_name)


        map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, titles='CartoDB position')

        choropleth = folium.Choropleth(
            geo_data='data/us-state-boundaries.geojson',
            data=data_states,
            columns=('states', 'mean salary'),
            key_on='feature.properties.name',
            fill_color='YlGn',
            nan_fill_color="White",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Median Sales Price',
            highlight=True
        )

        choropleth.geojson.add_to(map)
        data_states = data_states.set_index('states')

        state_dict = {}
        c = 0
        for i in data_states.index:
            state_dict[i] = c
            c += 1

        for feature in choropleth.geojson.data['features']:
            state_name2 = feature['properties']['name']
            if state_name2 in state_dict:
                v = state_dict.get(state_name2)
                feature['properties']['min salary'] = 'min salary: ' + str(int(data_states['min salary'][v])) + " K"
                feature['properties']['max salary'] = 'max salary: ' + str(int(data_states['max salary'][v])) + " K"
                feature['properties']['mean salary'] = 'mean salary: ' + str(int(data_states['mean salary'][v])) + " K"
            else:
                feature['properties']['min salary'] = ''
                feature['properties']['max salary'] = ''
                feature['properties']['mean salary'] = ''


        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(['name', 'min salary', 'max salary', 'mean salary'], labels=False)
        )

        st_map = st_folium(map, width=700, height=450)

        st.success("Graphs generated successfully")

if selected == "Insight of DS/DA/BA By Company Size & Revenue":
    st.header("Insight of DS/DA/BA By Company Size & Revenue")
    df_company['Revenue'] = df_company['Revenue'].replace('Unknown / Non-Applicable', None)
    df_company['Revenue'] = df_company['Revenue'].str.replace('$', ' ')
    df_company['Revenue'] = df_company['Revenue'].str.replace('(USD)', ' ')
    df_company['Revenue'] = df_company['Revenue'].str.replace('(', ' ')
    df_company['Revenue'] = df_company['Revenue'].str.replace(')', ' ')
    df_company['Revenue'] = df_company['Revenue'].str.replace(' ', '')
    df_company['Revenue'] = df_company['Revenue'].str.replace('2to5billion', '2billionto5billion')
    df_company['Revenue'] = df_company['Revenue'].str.replace('1to2billion', '1billionto2billion')
    df_company['Revenue'] = df_company['Revenue'].str.replace('5to10billion', '5billionto10billion')
    df_company['Revenue'] = df_company['Revenue'].replace('10+billion', '10billionto11billion')
    df_company['Revenue'] = df_company['Revenue'].str.replace('Lessthan1million', '0millionto1million')
    df_company['Revenue'] = df_company['Revenue'].str.replace('million', ' ')
    df_company['Revenue'] = df_company['Revenue'].str.replace('billion', '000 ')
    df_company = df_company[df_company['Revenue'].isin(['100to500 ', '500 to1000 ', '10000 to11000 ', '25to50 ',
                                '5000 to10000 ', '5to10 ', '50to100 ', '1000 to2000 ',
                                '2000 to5000 ', '0 to1 ', '1to5 ', '10to25 '])]
    df_company = df_company[df_company['Size'].isin(['51 to 200 employees', '1001 to 5000 employees',
                             '501 to 1000 employees', '10000+ employees', '1 to 50 employees',
                             '201 to 500 employees', '5001 to 10000 employees'])]

    avg_revenues = ['0 to1 ', '1to5 ', '5to10 ', '10to25 ',
                    '25to50 ', '50to100 ', '100to500 ', '500 to1000 ',
                    '1000 to2000 ', '2000 to5000 ',
                    '5000 to10000 ', '10000 to11000 ']
    avg_sizes = ['1 to 50 employees',
                 '51 to 200 employees', '201 to 500 employees',
                 '501 to 1000 employees', '1001 to 5000 employees',
                 '5001 to 10000 employees', '10000+ employees']
    df_size_revenue = pd.DataFrame(np.zeros((len(avg_revenues), len(avg_sizes))), index=avg_revenues, columns=avg_sizes)
    for i in avg_revenues:
        for j in avg_sizes:
            df_size_revenue.at[i, j] = len(df_company[(df_company['Revenue'] == i) & (df_company['Size'] == j)])
    fig = px.imshow(df_size_revenue, text_auto=True,
                    labels=dict(x="Company Size", y="Millions of $", color="Count"),
                    aspect="auto")
    st.plotly_chart(fig)



    def generate_stack_bar(avg_revenues, col_name):
        df_revenues_DS = pd.DataFrame(
            np.zeros((len(avg_revenues), 3)),
            index=avg_revenues,
            columns=['DS', 'DA', 'BA'])
        for i in avg_revenues:
            for j in ['DS', 'DA', 'BA']:
                df_revenues_DS.at[i, j] = len(
                    df_company[(df_company[col_name] == i) & (df_company['role'] == j)]
                )

        ax = df_revenues_DS.plot.bar(stacked=True)
        plt.ylabel('Job Count')
        fig1 = ax.get_figure()
        st.pyplot(fig1, clear_figure=True)


    def generate_bar_charts(avg_revenues, col_name):
        df_revenues_DS = pd.DataFrame(
            np.zeros((len(avg_revenues), 3)),
            index=avg_revenues,
            columns=['min salary', 'max salary', 'mean salary'])
        for i in avg_revenues:
            df_revenues_DS.loc[i] = df_company[df_company[col_name] == i][['min salary', 'max salary', 'mean salary']].mean()
        # st.dataframe(df_revenues_DS)
        data_sector = df_revenues_DS
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=data_sector.index,
            y=data_sector['mean salary'],
            name='Mean Salary'
        ))
        fig.add_trace(go.Bar(
            x=data_sector.index,
            y=data_sector['min salary'],
            name='Minimum Salary'
        ))
        fig.add_trace(go.Bar(
            x=data_sector.index,
            y=data_sector['max salary'],
            name='Maximum Salary'
        ))
        st.plotly_chart(fig, use_container_width=True)


    def generate_df_salries(avg_revenues, col_name):
        df_revenues_DS = pd.DataFrame(
            np.zeros((len(avg_revenues), 3)),
            index=avg_revenues,
            columns=['min salary', 'max salary', 'mean salary'])
        for i in avg_revenues:
            df_revenues_DS.loc[i] = df_company[df_company[col_name] == i][['min salary', 'max salary', 'mean salary']].mean()
        st.dataframe(df_revenues_DS)


    c_rev, c_size = st.columns(2)
    with c_rev:
        st.markdown("Job Count by Company Revenue")
        generate_stack_bar(avg_revenues, "Revenue")
        generate_df_salries(avg_revenues, "Revenue")

    with c_size:
        st.markdown("Job Count by Company Size")
        generate_stack_bar(avg_sizes, "Size")
        generate_df_salries(avg_sizes, "Size")

    st.markdown("---")
    st.markdown("**Salaries by Company Revenue**")
    generate_bar_charts(avg_revenues, "Revenue")

    st.markdown("**Salaries by Company Size**")
    generate_bar_charts(avg_sizes, "Size")

    st.markdown("---")
    st.markdown('''
    * The higher the revenue, the bigger the company size.
    * More jobs can be found in really big corporations(10 billion+ in revenue and 10000+ employees).
    * Salaries about the same across companies of different revenues and sizes. Really big corporations(10 billion+ in revenue and 10000+ employees) offer more salaries.'''
                )



