import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
st.set_page_config(page_title="DS/DA/BS Salary Dashboard")
df=pd.read_csv('data/cleaned_data.csv')

st.sidebar.header("Please Filter here:")
states=st.sidebar.multiselect("Select the State",options=df['states'].unique(),
default=df['states'].unique())
roles=st.sidebar.multiselect("Select the role",options=df['role'].unique(),
default=df['role'].unique())
sectors=st.sidebar.multiselect("Select the Sector",options=df['Sector'].unique(),
default=['Information Technology',
                 'Business Services', 'Finance','Biotech & Pharmaceuticals', 'Health Care'])

df_selection=df.query("states==@states & role==@roles & Sector==@sectors")
# st.dataframe(df_selection)

st.title("DS/DA/BS Salary Dashboard")
col1,col2=st.columns(2)
col1.metric("Mean salary(K $)",value=round(df_selection['mean salary'].mean(),2),delta=None)
col2.metric("Job Count",value=df_selection['role'].count())

st.markdown("---")
df_states_count=pd.DataFrame(
        np.zeros((len(states),len(roles))),
        index=states,
        columns=roles)

for i in states:
    for j in roles:
        df_states_count.at[i,j]=len(
            df_selection[(df_selection['states']==i) & (df_selection['role']==j)]
        )

col1,col2=st.columns(2)

with col1:
    # st.dataframe(df_states_count)
    st.markdown('Job Count in States')
    df_states_count['job count']=df_states_count.sum(axis=1)
    df_states_count.sort_values(by='job count', ascending=False,inplace=True)
    df_states_count.drop(['job count'],axis=1,inplace=True)

    ax=df_states_count.head().plot.bar(stacked=True)
    # plt.xlabel('State')
    plt.ylabel('Job Count')
    # plt.title('Top States for DS/DA/BA')
    fig1=ax.get_figure()
    st.pyplot(fig1,clear_figure=True)
with col2:
    st.markdown("Job Count by Sector")
    df_sector_count=df_selection.groupby('Sector')['role'].count()
    df_sector_count.sort_values(ascending=False,inplace=True)
    ax1=df_sector_count.head().plot.barh()
    # plt.ylabel("Sector")
    plt.xlabel("Job Count")
    fig=ax1.get_figure()
    st.pyplot(fig,clear_figure=True)

data_states=df_selection.groupby('states')[['min salary','max salary','mean salary']].mean().sort_values(['mean salary','min salary','max salary'],ascending=False).head()
fig = go.Figure()
fig.update_layout(
autosize=True,
width=800,
height=500)

fig.add_trace(go.Bar(
x = data_states.index,
y = data_states['mean salary'],
name = 'Mean Salary'
))

fig.add_trace(go.Bar(
x = data_states.index,
y = data_states['min salary'],
name = 'Minimum Salary'
))

fig.add_trace(go.Bar(
x = data_states.index,
y = data_states['max salary'],
name = 'Maximum Salary'
))

fig.update_layout(title = 'Salaries in States', barmode = 'group')
st.plotly_chart(fig, use_container_width=True)

data_sector=df_selection.groupby('Sector')[['min salary','max salary','mean salary']].mean().sort_values(['mean salary','min salary','max salary'],ascending=False)
fig = go.Figure()
fig.add_trace(go.Bar(
x = data_sector.index,
y = data_sector['mean salary'],
name = 'Mean Salary'
))
fig.add_trace(go.Bar(
x = data_sector.index,
y = data_sector['min salary'],
name = 'Minimum Salary'
))
fig.add_trace(go.Bar(
x = data_sector.index,
y = data_sector['max salary'],
name = 'Maximum Salary'
))

fig.update_layout(title = 'Salaries in Different Sectors', barmode = 'group')
st.plotly_chart(fig, use_container_width=True)

col3,col4=st.columns(2)
with col3:
    st.dataframe(data_states)
with col4:
    st.dataframe(data_sector)