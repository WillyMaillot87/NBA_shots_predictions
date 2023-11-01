import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import plotly.express as px
import plotly.figure_factory as ff

title = "Exploratory data analysis"
sidebar_name = "Exploratory data analysis"


def run():

    
    # streamlit_NBA page - Presentation & datasets
    
    
    st.markdown(' ')
    st.markdown(' ')
    st.markdown(' ')
    
    
    
    # Introduction to the page
    st.markdown(''' Here are short excerpts from several datasets. The originals are the datasets we 
used to build our final dataset, which you can select from the dropdown box. 
Below that, you'll find a sample from our working dataframe, which we relied 
on for our machine learning models. 
This dataframe consists of shooting actions performed by the top 20 players of the
21st century (selected based on a score calculated from their career statistics + more than 5 years in the league).  
A list of features that make up this database is provided.

Then, you will have the opportunity to examine a variety of graphs that will
provide visual representations of our variables. These visualizations will enhance
your understanding of the characteristics and behaviors exhibited by the variables
in our dataset.
''')
    st.header("Datasets")
    st.markdown(' ')  
    
    st.markdown('<p style="color: #17408b; font-size: 27px; font-style: italic; font-weight: 600;">Originals and final</p>', unsafe_allow_html=True)
    dataset = st.selectbox('**Description & five random rows of each dataset (originals and final)**',('None', 'Shot Locations 1997 -2020', 'player_data', 'ranking', 'Seasons_Stats', 'Final dataframe'), key="intro_dataset_selectbox")
    
  

    # Inventory of Datasets
    if dataset == 'Shot Locations 1997 -2020':
        dataset = pd.read_csv("NBA Shot Locations 1997 - 2020.csv")
        description = '''This original dataset contains information on all shots taken in the NBA between 
1997 and 2020.  
4 729 512 rows / 22 columns.  
It contains the target variable: Shot Made Flag.'''
    elif dataset == "player_data":
        dataset = pd.read_csv("player_data.csv")
        description = '''Various information about players, like position, ...  
4550 rows / 8 columns'''
    elif dataset == "ranking":
        dataset = pd.read_csv("ranking.csv")
        description = '''Ranking of NBA given a day.  
210 342 rows / 13 columns.'''
    elif dataset == "Final dataframe":
        dataset = pd.read_csv("df.csv")
        dataset = dataset.drop(columns=dataset.columns[0])
        description = '''All the shots (missed or made) by the 20 best players othe 21st century.  
248 528 rows / 46 columns'''
    elif dataset == "Seasons_Stats":
        dataset = pd.read_csv("Seasons_Stats.csv")
        dataset = dataset.drop(columns=dataset.columns[0])
        description = '''Player statistics by year from 1950 to 2017.  
24 691 rows / 52 columns.'''
    elif dataset == "None":
        dataset = None

    if dataset is not None:
        st.markdown(description)
        st.dataframe(dataset.sample(n=5).reset_index(drop=True))
        
    st.markdown(' ')
    st.markdown(' ')
    
    
    
    # Dataframe for the modeling
    
    st.markdown('<p style="color: #17408b; font-size: 27px; font-style: italic; font-weight: 600;">Working Dataframe</p>', unsafe_allow_html=True)
    st.markdown('''All the shots (missed or made) by the 20 best players othe 21st century with only the features for the modeling.   
248 528 rows / 19 columns''')
        
    dataset = pd.read_csv("working_dataframe.csv")
    dataset = dataset.drop(columns=dataset.columns[0])
    st.dataframe(dataset.sample(n=5).reset_index(drop=True))
    
        # Features list of the working dataframe
    with st.expander("_**Click to see the list of features**_"):
        st.markdown('**Player Name**')
        st.markdown('**Period Grouped** : specifies the quarter time or overtime (OT)')
        st.markdown('**Total Seconds Remaining** : seconds remaining until the end of the match')
        st.markdown('**Shot Distance** : distance at which the shot was taken, measured in feet')
        st.markdown("**Action Type Grouped** : groups the type of action (Jump shot, Layup shot, Dunk shot, etc.) by the percentage of success, divided into 10% intervals")
        st.markdown("**on_fire** : player's increase in shooting percentage over x games with at least y shots")
        st.markdown('**Shot_Team** : home or away game')
        st.markdown('**Shot Type** : 2PT Field Goal or 3PT Field Goal')
        st.markdown('**X Location** : position (width of the court) where the shot was taken')
        st.markdown('**Y Location** : position (length of the court) where the shot was taken')
        st.markdown('**Season Type** : regular season or playoff game')
        st.markdown('**2PT Field Goal_accuracy** : 2PT percentage')
        st.markdown('**3PT Field Goal_accuracy** : 3PT percentage')
        st.markdown('**height**')
        st.markdown('**weight**')
        st.markdown('**age** : age at time of shooting')
        st.markdown('''**W_PCT** : winning percentage of the player's team over the season at the time of the match played''')
        st.markdown("**Shot Zone Range** : groups the variable 'Shot Distance' into 5 distance categories")
        st.markdown('**Shot Made Flag** : the target variable, indicates whether the shot is successful (1) or missed (0)')
        
    
       
       
        
        
        
        
        # streamlit_NBA page - Dataviz
    st.markdown(' ')
    st.markdown(' ')
    st.markdown(' ')
    st.markdown(' ')


    st.header("Data visualization")
    
    menu_viz = st.selectbox("**Select a graph :**",
                        (
    "Periods",
    "Remaining Minutes",
    "Remaining Seconds",
    "Action Type",
    "Shot Type",
    "Shot Zone Basic",
    "Shot Zone Area",
    "Shot Zone Range",
    "Shot Distance",
    "Game Date",
    "Season Type",
    "Home or Away Team",
    "Age",
    "Height",
    "Weight",
    "Position",
    "On Fire",
    "Correlation Matrix"
    ))



    # Load statistics of each NBA player from 1950 :
    df = pd.read_csv('df1.csv')



    ########## FIG 1 : PERIODS ##########

    # Separate into regular and over time shots
    df_regtime = df[df['Period'] <= 4].groupby(['Period']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_regtime["shot_acc"] = (df_regtime["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    fig1_1 = px.bar(x="Period",
                    y="shot_count",
                    color="shot_acc",
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots Regular Time and their accuracy (%)",
                    data_frame=df_regtime)


    # Plot the count of shots for over time
    df_overtime = df[df['Period'] > 4].groupby(['Period']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_overtime["shot_acc"] = (df_overtime["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    fig1_2 = px.bar(x="Period",
                    y="shot_count",
                    color="shot_acc",
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots Regular Time and their accuracy (%)",
                    data_frame=df_overtime)

    ########## FIG 2 : REMAINING MINUTES ##########

    df_minutes = df.groupby(['Minutes Remaining']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_minutes["shot_acc"] = (df_minutes["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    fig2 = px.bar(x="Minutes Remaining",
                    y="shot_count", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal, 
                    text="shot_acc", 
                    title="Shots per remaining minute and their accuracy (%)",
                    data_frame=df_minutes)

    ########### FIG 3 : Seconds Remaining ##########

    df_seconds_0 = df[(df['Minutes Remaining'] == 0) & (df['Shot Made Flag'] == 0)]['Seconds Remaining']
    df_seconds_1 = df[(df['Minutes Remaining'] == 0) & (df['Shot Made Flag'] == 1)]['Seconds Remaining']
    hist_data = [df_seconds_0, df_seconds_1]
    group_labels = ['Shots Missed', 'Shots Made']
    fig3 = ff.create_distplot(hist_data,
                                group_labels, 
                                bin_size=.75,
                                show_rug=False, 
                                show_hist = False)
    fig3.update_layout(title_text="KDE of Shots per remaining second of the last minute")

    ########## FIG 4 : Action Type ##########

    # Plot of the 70 categorical Action Type :
    df_70actions = df.groupby(['Action Type']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_70actions["shot_acc"] = (df_70actions["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    fig4_1 = px.bar(x="shot_count",
                    y="Action Type", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots per Action Type & their accuracy (%)",
                    orientation='h',
                    data_frame=df_70actions)
    fig4_1.update_layout(yaxis={'categoryorder': 'total ascending'}, height=1200)

    # Plot of the action types grouped v1
    df_action_v1 = df.groupby(['Action Type Grouped v1']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_action_v1["shot_acc"] = (df_action_v1["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    fig4_2 = px.bar(x="Action Type Grouped v1",
                    y="shot_count", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots per Action Type (1st version of grouping) and their accuracy (%)",
                    data_frame=df_action_v1)
    fig4_2.update_layout(xaxis={'categoryorder': 'total descending'})

    # Plot of the action types grouped
    df_action = df.groupby(['Action Type Grouped']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_action["shot_acc"] = (df_action["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    fig4_3 = px.bar(x="Action Type Grouped",
                    y="shot_count", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots per Action Type (grouped by accuracy) and their accuracy (%)",
                    data_frame=df_action)
    fig4_3.update_layout(xaxis={'categoryorder': 'total descending'})


    ########## FIG 5 : Shot Type ##########
    df_shottype = df.groupby(['Shot Type']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_shottype["shot_acc"] = (df_shottype["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    fig5 = px.bar(x="Shot Type",
                    y="shot_count", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots per Shot Type and their accuracy (%)",
                    data_frame=df_shottype)


    ########## FIG 6 : Shot Zone Basic ##########
    df_zonebasic = df.groupby(['Shot Zone Basic']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_zonebasic["shot_acc"] = (df_zonebasic["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    fig6 = px.bar(x="Shot Zone Basic",
                    y="shot_count", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots per Shot Type and their accuracy (%)",
                    data_frame=df_zonebasic)
    fig6.update_layout(xaxis={'categoryorder': 'total descending'})

    ########## FIG 7 : Shot Zone Area ##########
    df_zonearea = df.groupby(['Shot Zone Area']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_zonearea["shot_acc"] = (df_zonearea["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    fig7 = px.bar(x="Shot Zone Area",
                    y="shot_count", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots per Shot Type and their accuracy (%)",
                    data_frame=df_zonearea)
    fig7.update_layout(xaxis={'categoryorder': 'total descending'})


    ########## FIG 8 : Shot Zone Range ##########
    df_zonerange = df.groupby(['Shot Zone Range']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_zonerange["shot_acc"] = (df_zonerange["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    fig8 = px.bar(x="Shot Zone Range",
                    y="shot_count", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots per Shot Type and their accuracy (%)",
                    data_frame=df_zonerange)
    fig8.update_layout(xaxis={'categoryorder': 'total descending'})


    ########## FIG 9 : Shot Distance ##########

    df_distance_0 = df[df['Shot Made Flag'] == 0]['Shot Distance']
    df_distance_1 = df[df['Shot Made Flag'] == 1]['Shot Distance']
    hist_data = [df_distance_0, df_distance_1]
    group_labels = ['Shots Missed', 'Shots Made']
    fig9 = ff.create_distplot(hist_data,
                                group_labels, 
                                bin_size=.75,
                                show_rug=False, 
                                show_hist = False)
    fig9.update_layout(title_text="Number of Shots vs Shot Distance")
    fig9.add_vline(x=22, line_dash="dash", line_color="red")
    fig9.add_annotation(x=22, 
                        y=0.13,
                        text="3pt Line",
                        align="right",
                        showarrow=False,
                        font=dict(
                            family="Courier New, monospace",
                            size=18,
                            color="red"
                            )
                        )


    ########## FIG 10 : Game Date ##########

    df_month = df.groupby(['month']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_month["shot_acc"] = (df_month["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    df_month['month'].replace({1:"January",
                            2: "February",
                            3: "March",
                            4: "April",
                            5: "May",
                            6: "June",
                            10: "October",
                            11: "November",
                            12: "December"
                            }, inplace=True)
    fig10 = px.bar(x="month",
                    y="shot_count", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots per Month and their accuracy (%)",
                    data_frame=df_month)


    ########## FIG 11 : Season Type ##########
    df_season = df.groupby(['Season Type']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_season["shot_acc"] = (df_season["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    fig11 = px.bar(x="Season Type",
                    y="shot_count", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots per Season Type and their accuracy (%)",
                    data_frame=df_season)
    fig11.update_layout(xaxis={'categoryorder': 'total descending'})



    ########## FIG 12 : Home or Away Team ##########
    df_homeaway = df.groupby(['Shot_Team']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_homeaway["shot_acc"] = (df_homeaway["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    fig12 = px.bar(x="Shot_Team",
                    y="shot_count", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots per Season Type and their accuracy (%)",
                    data_frame=df_homeaway)


    ########## FIG 13 : Age ##########
    df_age = df.groupby(['age']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_age["shot_acc"] = (df_age["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)
    fig13 = px.bar(x="age",
                    y="shot_count", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots per age and their accuracy (%)",
                    data_frame=df_age)


    ########## FIG 14 : Height ##########
    df_height = df.groupby(['height']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_height["shot_acc"] = (df_height["shot_acc"]*100).round(2).apply('{:.1f}'.format).astype(float)
    fig14 = px.bar(x="height",
                    y="shot_count", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots per height and their accuracy (%)",
                    data_frame=df_height)

    ########## FIG 15 : Weight ##########
    df_weight_0 = df[df['Shot Made Flag'] == 0]['weight']
    df_weight_1 = df[df['Shot Made Flag'] == 1]['weight']
    hist_data = [df_weight_0, df_weight_1]
    group_labels = ['Shots Missed', 'Shots Made']
    fig15 = ff.create_distplot(hist_data,
                                group_labels, 
                                bin_size=.75,
                                show_rug=False, 
                                show_hist = False)
    fig15.update_layout(title_text="Number of Shots vs Weight")

    ########## FIG 16 : position ##########
    df_pos = df.groupby(['position']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_pos["shot_acc"] = (df_pos["shot_acc"]*100).round(2).apply('{:.1f}'.format).astype(float)
    fig16 = px.bar(x="position",
                    y="shot_count", 
                    color="shot_acc", 
                    color_continuous_scale=px.colors.sequential.Teal,
                    text="shot_acc",
                    title="Shots per Position and their accuracy (%)",
                    data_frame=df_pos)
    fig16.update_layout(xaxis={'categoryorder': 'total descending'})


    ########## FIG 17 : On Fire ##########
    df_onfire = df.groupby(['Player Name', 'on_fire']).agg(shot_acc = ('Shot Made Flag', 'mean'), shot_count = ('Shot Made Flag', 'count')).reset_index()
    df_onfire['on_fire'].replace([0, 1], ["no", "yes"], inplace=True)
    df_onfire["shot_acc"] = (df_onfire["shot_acc"]*100).round(2).apply('{:.2f}'.format).astype(float)

    fig17 = px.bar(x="Player Name", y="shot_count", color="on_fire", text="shot_acc", title="Shots per Player while On Fire and their accuracy (%)", data_frame=df_onfire)
    fig17.update_layout(xaxis={'categoryorder': 'total descending'})


    ########## FIG 18 : Correlation ##########

    # Création du dataset pour la corrélation
    dataset = df[['Period Grouped', 'Total Seconds Remaining', 'Shot Distance', 'Action Type Grouped', 'on_fire', 'Shot_Team', 'Shot Type', 'X Location', 'Y Location',
                    'Season Type', '2PT Field Goal_accuracy', '3PT Field Goal_accuracy', 'height', 'weight', 'age', 'W_PCT', 'Shot Made Flag']]


    le = preprocessing.LabelEncoder()

    categorical_cols = dataset.select_dtypes(include=['object']).columns

    for col in categorical_cols : 
        le.fit(dataset[col])
        dataset[col] = le.transform(dataset[col])

    corr_matrix = dataset.corr().round(2)

    # Création de la Heatmap

    fig18 = px.imshow(corr_matrix, text_auto=True, aspect="auto",color_continuous_scale=px.colors.sequential.RdBu, title="Feature correlation matrix")
    fig18.update_layout(height=600)

    # fig18 = plt.figure()
    # sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5, fmt = '.2f', center = 0)
    # plt.title('Feature correlation matrix')

    # Affichage en fonction de la sélection :

    if menu_viz == "Periods":
        tab1, tab2 = st.tabs(["Regular Time", "Over Time"])
        with tab1 :
            st.plotly_chart(fig1_1)
        with tab2 :
            st.plotly_chart(fig1_2)
        with st.container():
            st.markdown("""
            - The period appears to affect the shot accuracy
            - In regular time, as the periods advance, the number of shots and the shot accuracy decrease
            - In over time, the number of shots clearly decreases as there are not always overtimes played, but the accuracy remains relatively constant. Apart from period 8, but it is a very rare situation.
            - This variable could be grouped in 5 categories: P1, P2, P3, P4 and OT
            """)

    elif menu_viz == "Remaining Minutes":
        st.plotly_chart(fig2)
        with st.container():
            st.markdown("""
            - The remaining minutes appear to have a clear impact on the accuracy in the last minute.
            - From minutes 10 to 1, the number of shots taken and the accuracy remain relatively constant.
            - At minute 11, the number of shots is clearly lower and the accuracy gets a little bit reduced.
            - At minute 0, there is a clear increase in the number of shots and a drop in the accuracy
            - In this scenario this variable can be grouped into 2 categories: last minute shots and suring the period shots
            """)

    elif menu_viz == "Remaining Seconds":
        st.plotly_chart(fig3)
        with st.container():
            st.markdown("""
            - The remaining seconds of the last minute of the period has a clear impact on the shot accuracy
            - Blue line represents missed shots and orange line represent made shots
            - It is pretty clear that the number of shots has an exponential growth during the last 10 seconds while the accuracy clearly drops
            """)

    elif menu_viz == "Action Type":
        tab1, tab2, tab3 = st.tabs(["70 Action Types", "Grouped Types (1st version)", "Grouped types (final version)"])
        with tab1 :
            st.plotly_chart(fig4_1, height=1200)
        with tab2 :
            st.plotly_chart(fig4_2)
        with tab3 :
            st.plotly_chart(fig4_3)
        with st.container():
            st.markdown("""
            - The Action Type has an impact on the shot accuracy
            - The most common action type is Jump Shot and it shows the lower accuracy
            - Apart from Dunks, which accuracy is very high, the rest of action types accuracies oscillates around 50%, but Layups are more common than the rest
            """)

    elif menu_viz == "Shot Type":
        st.plotly_chart(fig5)
        with st.container():
            st.markdown("""
            - 2pt shots are more common and have higher accuracy than 3pt shots
            - Here it is important to check if there are no strange values regarding the Shot Type and the Shot Zone Range or the Shot Zone Basic.
            """)

    elif menu_viz == "Shot Zone Basic":
        st.plotly_chart(fig6)
        with st.container():
            st.markdown("""
            - Shot Zone Basic has an impact in the accuracy and number of shots
            - Restricted Area shots are very common and have a high accuracy but Mid Range shots, although they are common, their accuracy is low, as the rest of the shot zones
            - The accuracy of Backcourt shots is very low as they are far from the basket
            """)

    elif menu_viz == "Shot Zone Area":
        st.plotly_chart(fig7)
        with st.container():
            st.markdown("""
            - Shot Zone Area has an impact in the accuracy and number of shots
            - Most common shots come from Center Zone with a higher accuracy than all the rest.
            - The rest of the zones show a similar accuracy and numer of shots
            """)

    elif menu_viz == "Shot Zone Range":
        st.plotly_chart(fig8)
        with st.container():
            st.markdown("""
            - Shot Zone Range has an impact in the accuracy and number of shots
            - Most part of the shots come from Less then 8 ft and show the highest accuracy
            - A high number of 24 + ft shots are taken as they are 3 pointers
            """)

    elif menu_viz == "Shot Distance":
        st.plotly_chart(fig9)
        with st.container():
            st.markdown("""
            - This plot shows similar info than the precedent bar plot but with continous values
            - At short distances accuracy is high and it declines at long distances
            """)

    elif menu_viz == "Game Date":
        st.plotly_chart(fig10)
        with st.container():
            st.markdown("""
            - The month has not an impact on the shot accuracy, it remains around 45'%' always
            - The difference in the number of shots comes from the different number of games played at those months
            """)

    elif menu_viz == "Season Type":
        st.plotly_chart(fig11)
        with st.container():
            st.markdown("""
            - The accuracy is very close in both Season types
            - Of course there are less shots in Playoffs as there are less matches.
            """)

    elif menu_viz == "Home or Away Team":
        st.plotly_chart(fig12)
        with st.container():
            st.markdown("""
            - The away teams take more shots but their accuracy is a bit lower than the home teams
            """)

    elif menu_viz == "Age":
        st.plotly_chart(fig13)
        with st.container():
            st.markdown("""
            - As we look at the 20 best players in the league it seems that the age doesn't impact the accuracy a lot
            - After 36 the accuracy tends to decrease. 
            """)

    elif menu_viz == "Height":
        st.plotly_chart(fig14)
        with st.container():
            st.markdown("""
            - There is an increase in the accuracy of the shots when the player's height is above 6.67ft. This can be explained by the fact that taller players usually play close to the basket.
            """)

    elif menu_viz == "Weight":
        st.plotly_chart(fig15)
        with st.container():
            st.markdown("""
            - We see an increase in accuracy (the blue and orange curves overlap) as the player gets heavier. This can be explained by the fact that heavier players usually play close to the basket.
            """)

    elif menu_viz == "Position":
        st.plotly_chart(fig16)
        with st.container():
            st.markdown("""
            - Positions seems to have an impact on the accuracy. 
            - There is a difference of 8.5% accuracy between a Guard and a Center.
            """)

    elif menu_viz == "On Fire":
        st.plotly_chart(fig17, height=600)
        with st.container():
            st.markdown("""
            - A Player is set "On Fire" if he reach +5% accuracy for 3 matches in a row with minimum 5 shots attempted.  
            - It appears that 8.13% of games played are set 'on fire'.
            """)

    elif menu_viz == "Correlation Matrix":
        st.plotly_chart(fig18)


    ########### Personnalised Graphs ##################
    
    # numeric_cols = df.select_dtypes(exclude="object").columns.to_list()
    # categorical_cols = df.select_dtypes(include="object").columns.to_list()

    # with st.expander("Make your own graph"):
    #     col1, col2, col3 = st.columns([1, 1, 1])

    #     with col1 :
    #         var_x = st.selectbox("feature on the x-axis", numeric_cols)
    #     with col2 :
    #         var_y = st.selectbox("feature on the y-axis", numeric_cols)
    #     with col3 : 
    #         var_color = st.selectbox("feature on the y-axis", categorical_cols)

    #         figp = px.scatter(
    #             data_frame = df,
    #             x = var_x,
    #             y = var_y,
    #             color = var_color,
    #             title=str(var_y) + " VS " + str(var_x)
    #         )

    #         st.plotly_chart(figp)

