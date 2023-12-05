import pandas as pd
import streamlit as st
import preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
user_menu=st.sidebar.radio(
                 'Select an option',
                 ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis'))

#st.dataframe(df)

if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select years",years)
    selected_country=st.sidebar.selectbox("Select Country", country)

    medal_tally=helper.fetch_medaltally(df,selected_year,selected_country)
    if selected_country=='Overall' and selected_year=='Overall':
        st.title('Overall Tally')
    if selected_year!='Overall' and selected_country=='Overall':
        st.title('Medal Tally in' +  " " +str(selected_year))
    if selected_year=='Overall' and selected_country!='Overall':
        st.title(str(selected_country)+" "+"Overall Performance")
    if selected_year!='Overall' and selected_country!='Overall':
        st.title(str(selected_country)+" "+"Performance in"+" "+str(selected_year) )
    st.table(medal_tally)


if user_menu=='Overall Analysis':
    editions=df['Year'].unique().shape[0] - 1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletics=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    st.title("Top Statistic")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Event")
        st.title(events)
    with col2:
        st.header("Athletics")
        st.title(athletics)
    with col3:
        st.header("Nations")
        st.title(nations)

    nations_over_time = helper.data_overtime(df,'region')
    fig = px.line(nations_over_time, x='Editions', y='region')
    st.title("Participating nation over the year")
    st.plotly_chart(fig)

    events_over_time = helper.data_overtime(df, 'Event')
    fig = px.line(events_over_time, x='Editions', y='Event')
    st.title("Events over the year")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_overtime(df, 'Name')
    fig = px.line(athlete_over_time, x='Editions', y='Name')
    st.title("Athlete over the year")
    st.plotly_chart(fig)

    st.title("No. of Event Over Time(Every Sports)")
    fig, ax = plt.subplots(figsize=(25, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title('Most Successfull Athlete')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox("Select a sport",sport_list)
    x = helper.most_scuccesful(df,selected_sport)
    st.table(x)

if user_menu=='Country-wise Analysis':

    st.sidebar.title("Country-wise Analysis")
    countries_list = df['region'].dropna().unique().tolist()
    countries_list.sort()
    selected_country = st.sidebar.selectbox("Select a Counry",countries_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country+" "+ "Medal tally over the years" )
    st.plotly_chart(fig)

    st.title(selected_country + " " + "Excel in the following Sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(25, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title(selected_country + " " + "Top 10 Athlete")
    top10df = helper.most_scuccesful_of_country(df,selected_country)
    st.table(top10df)

if user_menu == 'Athlete-wise Analysis' :
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelete_df[athelete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelete_df[athelete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_rug=False, show_hist=False)
    fig.update_layout(autosize=False,width=920,height=600)
    st.title("Age Distribution")
    st.plotly_chart(fig)

    x = []
    name = []
    for sport in famous_sports:
        temp_df = athelete_df[athelete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x,name,show_rug=False, show_hist=False)
    fig.update_layout(autosize=False, width=900, height=600)
    st.title("Age Distribution wrt Age (Gold Medalist)")
    st.plotly_chart(fig)












