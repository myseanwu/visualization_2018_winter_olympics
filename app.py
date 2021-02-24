# Hsin-Yuan Wu
# si649f20 interactive vis

# imports we will use
import altair as alt
import pandas as pd
import streamlit as st

#Title
st.title('Tiny Norway Totally Dominating the Winter Olympics')
st.write("Individual vis by Hsin-Yuan Wu")

#Import data
DS = pd.read_csv('winter_history.csv') 
dt = pd.read_csv('total_winter_medals.csv') # side bar? total medals
human_dev = pd.read_csv('human.csv')


# dataframe
sports =DS.groupby(['Year','Country','Discipline']).count().reset_index()[['Year','Country','Discipline','Medal']]
top5 = ['NOR','GER','CAN','USA','NED']
sports_5 = sports[sports['Country'].isin(top5)]

# dataframe
country_short = ['NOR', 'GER','CAN','USA','NED', 'KOR','RUS','OAR',
                 'SUI','FRA','SWE','AUT','JPN','ITA','CHN','CZE','Finland',
                 'GBR','BLR','SVK','AUS','POL','SLO','ESP','NZL','HUN',
                 'UKR','BEL','KAZ','LAT','LIE']

## history medals
df_his=DS[DS['Country'].isin(country_short)]
df_point = df_his.groupby(['Year','Country']).count().reset_index()
top5_country = ['USA','CAN','NOR','GER','NED']
df_point_5 = df_point[df_point['Country'].isin(top5_country)]


## total medals so far
team = ['Austria','Canada','Germany','Norway','United States']
medals = [232,199,240,368,305]
dt_total=pd.DataFrame(zip(team,medals),columns=['team','medals'])


# dataframe of medals/disciplines
df_medal= DS[DS['Country'].isin(country_short)].groupby(['Year','Country','Medal']).count().reset_index()
df_medal.rename(columns={'Event':'Quantity'},inplace=True)


# df fro 2018
country = ['Norway','Germany','Canada','United States','Netherlands','South Korea',
            'Olympic Athletes from Russia','Switzerland','France','Sweden','Austria',
            'Japan','Italy','China','Czech Republic','Finland','Great Britain','Belarus',
            'Slovakia','Australia','Poland','Slovenia','Spain','New Zealand','Hungary',
            'Ukraine','Belgium','Kazakhstan','Latvia','Liechtenstein']

athletes = [109,156,225,241,34,122,168,166,106,116,105,124,120,80,93,100,58,33,56,50,62,71,13,21,19,33,22,46,34,3]
Gold = [14,14,11,9,8,5,2,5,5,7,5,4,3,1,2,1,1,2,1,0,1,0,0,0,1,1,0,0,0,0]

Silver = [14,10,8,8,6,8,6,6,4,6,3,5,2,6,2,1,0,1,2,2,0,1,0,0,0,0,1,0,0,0]
Bronze = [11,7,10,6,6,4,9,4,6,1,6,4,5,2,3,4,4,0,0,1,1,1,2,2,0,0,0,1,1,1]


d = {'country': country, 'athletes': athletes,'Gold': Gold, 'Silver': Silver, 'Bronze': Bronze}
df = pd.DataFrame(data=d)
df_melt = df.rename(columns={'Gold':'1.Gold','Silver':'2.Silver','Bronze':'3.Bronze'}).filter(['country','1.Gold','2.Silver','3.Bronze']).melt('country',var_name=['medals'])

# df_5 for HDI trends
country_5 = ['Norway','United States','Netherlands','Germany','Canada']
data = pd.read_csv('HDI.csv')
data_5 = data[data['Country'].isin(country_5)].iloc[:,1:]
df_5 = data_5.melt('Country',var_name=['year'])

################# Altair Charts ################
# altair_vis 1 (history)
country_options= list(df_point['Country'].unique())

# radio
# widget = alt.binding_radio(options=country_options,name='Select Country: ')

# drop down
widget = alt.binding_select(options=country_options,name='Select Country: ')

selectionEmoji = alt.selection_single(fields=['Country'],
                                       init={'Country':country_options[5]},
                                       bind=widget,
                                       name='Counry')
colorCondition = alt.condition(selectionEmoji,'Country',alt.value('white'))



selection1 = alt.selection_single(empty='none',on="mouseover",fields=['Country'],bind='legend')
condition1 = alt.condition(selection1,alt.value(1),alt.value(0.00001))

# selection_zoom=alt.selection_interval(bind='scales',encodings=['y']) #,encodings=['x']


points = alt.Chart(df_point).mark_circle(color='grey').encode(
    alt.X('Year:N'),
    alt.Y('Medal:Q', title=None,axis=alt.Axis(orient='right',grid=False)),
    # alt.Color('Country:N',legend=alt.Legend(orient='left')),
    
)

line= alt.Chart(df_point).mark_line().encode(
     alt.X('Year:N'),
    alt.Y('Medal:Q'),
).add_selection(selectionEmoji
).encode(
    color=colorCondition
).transform_filter(
    selectionEmoji
)

point2 = alt.Chart(df_medal).mark_circle().transform_joinaggregate(        #calculate the mean budget
    total='sum(Sport)',
    groupby=['Year','Country']
).encode(
    alt.X('Year:N'),
    alt.Y('Quantity:Q',title='Medal quantity'),
    alt.Color('Medal:N',#scale=alt.Scale(scheme='magma')
                scale=alt.Scale(
                            domain=['Bronze', 'Gold','Silver'],
                            range=['#B07822', '#FFFF66','#D8D8D8'])),
    alt.Size('Quantity:Q',legend=alt.Legend(title="Quantity"))
).add_selection(selectionEmoji
).transform_filter(
    selectionEmoji
).properties(width=200, height=100 #
).encode(tooltip=['Quantity:Q','Country'])

history_line_inter = (points+line).encode(tooltip=['Medal:Q','Country']
                            ).properties(#title='How many medals did these countries win in the past? (total)',
                                        width=300, height=200 
                                        )
#.configure_view(strokeWidth=0)

inter_1 = (history_line_inter | point2).resolve_scale(
    color='independent'
)#.properties(title='How many medals did these countries win in the past? (total)')

# total medals

team = ['Austria','Canada','Germany','Norway','United States']
medals = [232,199,240,368,305]
dt=pd.DataFrame(zip(team,medals),columns=['team','medals'])

total_medals = alt.Chart(dt, title='Total winter Olympics medals').mark_bar(color='#cf71af').encode(
    alt.X('team:N',sort=alt.SortField('medals:Q',order='descending'),title=None),
    alt.Y('medals:Q',title=None)
).configure_title(fontSize=18,anchor='start').configure_axis(grid=False).configure_view(strokeWidth=0)


### Sports/disciplines ###
## vis 2 
selection4 = alt.selection_single(fields=['Country'],on='mouseover',bind='legend')
condition4 = alt.condition(selection4,alt.value(100),alt.value(20))
condition5 = alt.condition(selection4,alt.value(1),alt.value(0.05))

all_points_in= alt.Chart(sports_5,title='').mark_circle(
     opacity=0.8,
    stroke='black',
    strokeWidth=0.1
).encode(
    alt.X('Year:O',title=None),   # , axis=alt.Axis(labelAngle=0)
    alt.Y('Discipline:N',title=None),
    alt.Color('Country:N'),
    alt.Size('Medal:Q',)  # scale=alt.Scale(range=[10, 40])
).add_selection(selection4).encode(
    opacity=condition5)


line_5 = alt.Chart(sports_5).mark_rect().transform_filter(
    alt.datum.Country == 'NOR'
).encode(
    alt.X('Year:O',title='Norway won'),alt.Y('Discipline:N',title=None),color='Medal:Q'
).properties(width=350)


text = line_5.mark_text(baseline='middle').encode(
    text='Medal:Q',
        color=alt.condition(
        alt.datum.Medal > 5,
        alt.value('black'),
        alt.value('grey')
    )
)

#horizontal line
select_vline = alt.selection_single(encodings=['y'],empty='none',on="mouseover",nearest=True)
condition_hover_line = alt.condition(select_vline,alt.value(1),alt.value(0.00001))

vline = alt.Chart(sports_5).mark_bar(filled=False, color="darkblue",opacity = 0,strokeWidth=1.5
                                     ).encode(
    y='Discipline:N',  
).add_selection(
    select_vline
).encode(
    opacity=condition_hover_line,
#     tooltip=['Discipline:N']
)

NOR_hm = (line_5 + text + vline)


line_5_us = alt.Chart(sports_5).mark_rect().transform_filter(
    alt.datum.Country == 'USA'
).encode(
    alt.X('Year:O',title='USA won'),alt.Y('Discipline:N',title=None,axis=None),
    alt.Color('Medal:Q',scale=alt.Scale(scheme='blues'))
).properties(width=350)

text_us = line_5_us.mark_text(baseline='middle').encode(
    text='Medal:Q',
        color=alt.condition(
        alt.datum.Medal > 5,
        alt.value('black'),
        alt.value('grey')
    )
)
US_hm = (line_5_us + text_us + vline)

hmap = (NOR_hm|US_hm).resolve_scale(y='shared'
    ).properties(title='Compare Norway and USA'
    ).configure_title(fontSize=18,anchor='middle') # fontsize



# combined with interactive >>> remove
point_sport = alt.Chart(sports_5,title='Which sports are they good at?').mark_bar().transform_joinaggregate(        #calculate the mean budget
    total='sum(Medal)',
    groupby=['Year','Discipline','Country']
).encode(
    alt.X('Year:N'),
    alt.Y('total:Q'),
    alt.Color('Discipline:N')#,scale=alt.Scale(scheme='magma')),
#     alt.Size('total:Q')
).add_selection(selection4
).transform_filter(
    selection4
)

inter_2=(all_points_in & point_sport).resolve_scale(
    color='independent', size='independent'
).configure_view(strokeWidth=0)


### Human development ###
# human vis 
## selcet
selection_c = alt.selection_multi(empty='none',fields=['Country'])
color_c = alt.condition(selection_c,
                   alt.value('steelblue'),
                   alt.value('lightgray') # WANT THIS TO BE %50 OPACITY
)

dev = alt.Chart(human_dev).mark_bar(color='#f3f3b0',).encode(
    alt.Y('Country:N',axis=None,sort=alt.SortField(field="index", order='descending'),title=None),
    alt.X('index:Q',axis=None,scale=alt.Scale(domain=[0.880,0.960]), 
    title="index: include factors such as a long and healthy life, the ability to acquire knowledge, and a decent standard of living."),
    )

dev_1 = alt.Chart(human_dev).mark_bar(color='lightblue',).encode(
    alt.Y('Country:N',axis=None,sort=alt.SortField(field="index", order='descending'),title=None),
    alt.X('index:Q',axis=None,scale=alt.Scale(domain=[0.880,0.960])
         ),
).add_selection(
 selection_c
).encode(color=color_c)

text = dev.mark_text(
    align='left',
    baseline='middle', 
    fontStyle='italic'
).encode(
    text=alt.Text('index:N',format=".3f"),
    x=alt.value(0) ,
).properties(width=20)

country_name = dev.mark_text(
    align='right',
    baseline='middle', 
    dx=20,
    fontSize=12,
    color='#3230c0',
    fontStyle='bold'
).encode(
    text=alt.Text('Country:N'),
    x=alt.value(0) ,
).properties(width=20)

human_dev =(country_name|text|dev+dev_1).configure_view(strokeWidth=0
                                            ).configure_concat(spacing=10
                                            #).properties(title='Society development matters?! Human Development Index'
                                            )#.configure_title(fontSize=40,anchor='middle')


### total medals ###
# vis 4
total = alt.Chart(dt_total, title='Total winter Olympics medals'
).mark_bar(color='#cf71af').encode(
    alt.X('team:N',sort=alt.SortField('medals',order='descending'),title=None),
    alt.Y('medals:Q',title=None),
    color=alt.condition(
        alt.datum.team == 'Norway',  # If the year is 1810 this test returns True,
        alt.value('black'),     # which sets the bar orange.
        alt.value('grey') 
    )
).configure_view(strokeWidth=0).configure_axis(
    grid=False
).configure_title(fontSize=24,anchor='start').properties(width=500,height=300)

### history ###3
points = alt.Chart(df_point_5).mark_circle().encode(
    alt.X('Year:N'),
    alt.Y('Medal:Q', title=None,axis=alt.Axis(orient='right',grid=False)),
    alt.Color(
                'Country:N',legend=alt.Legend(orient='left'),
                scale=alt.Scale(
                            domain=['CAN','GER' ,'NED','NOR','USA'],
                            range=['black','#21618C', 'grey','darkblue','blue']) #FFCC99
             )
)

line_NOR= alt.Chart(df_point_5).mark_line(color='darkblue').transform_filter(
    alt.datum.Country == 'NOR'
).encode(
     alt.X('Year:N'),
    alt.Y('Medal:Q'),
)

line_USA = alt.Chart(df_point_5).mark_line(color='blue').transform_filter(
    alt.datum.Country == 'USA'
).encode(
     alt.X('Year:N'),
    alt.Y('Medal:Q',),
)

history_line = (points+line_NOR+line_USA).encode(tooltip=['Medal:Q','Country']
                                                ).properties(
                                                    title='Norway vs USA'
                                                ).configure_view(strokeWidth=0
                                                ).configure_title(fontSize=24,anchor='middle', dy=-50)




### 2018 ###
selection_bar1 = alt.selection_single(empty='none',on="mouseover")
condition_hover_bar1 = alt.condition(selection_bar1,alt.value(1),alt.value(0.9))

bars_2018 = alt.Chart(df_melt
).mark_bar().encode(
        y=alt.Y('country:N', sort='-x',title=None),
        x=alt.X('value:Q',title=None,axis=alt.Axis(orient='top',grid=False)),
        color=alt.Color('medals:N',sort=['Gold','Silver','Bronze'],scale=alt.Scale(scheme='blues')
                       ,legend=alt.Legend(orient='left')
                       )
).add_selection(
    selection_bar1
).encode(
    opacity=condition_hover_bar1,
    tooltip=['medals:N','value:Q','country:N']

).configure_view(strokeWidth=0).properties(width=600)

## HDI trend line
selection_line = alt.selection_single(empty='none',on="mouseover",fields=['Country'],bind='legend')
lineCondition = alt.condition(selection_line, alt.value(4),alt.value(2))

HDI_trend = alt.Chart(df_5).mark_line().transform_filter(
    alt.datum.year > 1999
).encode(
    alt.X('year:O'),
    alt.Y('value:Q',scale=alt.Scale(domain=[0.85,0.96])),
    alt.Color('Country:N',
#              scale=alt.Scale(
#                             domain=['CAN','GER' ,'NED','NOR','USA'],
#                             range=['black','steelblue', 'grey','darkblue','blue'])
             )
).add_selection(
    selection_line
).encode(
    size=lineCondition,
)

### compare top 5 in sport diciplines
## NOR
line_5 = alt.Chart(sports_5).mark_rect().transform_filter(
    alt.datum.Country == 'NOR'
).encode(
    alt.X('Year:O',title='Norway won'),alt.Y('Discipline:N',title=None),color='Medal:Q'
).properties(width=250,height=150)

text = line_5.mark_text(baseline='middle').encode(
    text='Medal:Q',
        color=alt.condition(
        alt.datum.Medal > 5,
        alt.value('black'),
        alt.value('grey')
    )
)

#horizontal line
select_vline = alt.selection_single(encodings=['y'],empty='none',on="mouseover",nearest=True)
condition_hover_line = alt.condition(select_vline,alt.value(1),alt.value(0.00001))

vline = alt.Chart(sports_5).mark_bar(filled=False, color="darkblue",opacity = 0,strokeWidth=1.5
                                     ).encode(
    y='Discipline:N',  
).add_selection(
    select_vline
).encode(
    opacity=condition_hover_line,
#     tooltip=['Discipline:N']
)

NOR_hm = (line_5 + text + vline)#.add_selection(selection_hp).encode(opacity=condition_hp)

## US
line_5_us = alt.Chart(sports_5).mark_rect().transform_filter(
    alt.datum.Country == 'USA'
).encode(
    alt.X('Year:O',title='USA won'),alt.Y('Discipline:N',title=None,axis=None),
    alt.Color('Medal:Q',scale=alt.Scale(scheme='blues'))
).properties(width=250,height=150)

text_us = line_5_us.mark_text(baseline='middle').encode(
    text='Medal:Q',
        color=alt.condition(
        alt.datum.Medal > 5,
        alt.value('black'),
        alt.value('grey')
    )
)

US_hm = (line_5_us + text_us + vline)#.add_selection(selection_hp).encode(opacity=condition_hp)

## CAN
line_5_CA = alt.Chart(sports_5).mark_rect().transform_filter(
    alt.datum.Country == 'CAN'
).encode(
    alt.X('Year:O',title='Canada won'),alt.Y('Discipline:N',title=None),
    alt.Color('Medal:Q',scale=alt.Scale(scheme='blues'))
).properties(width=250,height=150)

text_CA = line_5_CA.mark_text(baseline='middle').encode(
    text='Medal:Q',
        color=alt.condition(
        alt.datum.Medal > 5,
        alt.value('black'),
        alt.value('grey')
    )
)

CA_hm = (line_5_CA + text_CA + vline)#.add_selection(selection_hp).encode(opacity=condition_hp)

# GER
line_5_GER = alt.Chart(sports_5).mark_rect().transform_filter(
    alt.datum.Country == 'GER'
).encode(
    alt.X('Year:O',title='Germany won'),alt.Y('Discipline:N',title=None,axis=None),
    alt.Color('Medal:Q',scale=alt.Scale(scheme='blues'))
).properties(width=250,height=150)

text_GER = line_5_GER.mark_text(baseline='middle').encode(
    text='Medal:Q',
        color=alt.condition(
        alt.datum.Medal > 5,
        alt.value('black'),
        alt.value('grey')
    )
)

GER_hm = (line_5_GER + text_GER + vline)#.add_selection(selection_hp).encode(opacity=condition_hp)

# NED
line_5_NED = alt.Chart(sports_5).mark_rect().transform_filter(
    alt.datum.Country == 'NED'
).encode(
    alt.X('Year:O',title='Netherlands won'),alt.Y('Discipline:N',title=None),
    alt.Color('Medal:Q',scale=alt.Scale(scheme='blues'))
).properties(width=250,height=150)

text_NED = line_5_NED.mark_text(baseline='middle').encode(
    text='Medal:Q',
        color=alt.condition(
        alt.datum.Medal > 5,
        alt.value('black'),
        alt.value('grey')
    )
)

NED_hm = (line_5_NED + text_NED + vline)#.add_selection(selection_hp).encode(opacity=condition_hp)

T = (NOR_hm | US_hm) & (CA_hm  | GER_hm) & NED_hm 

T_5 = T.resolve_scale(y='shared'
    ).configure_title(fontSize=24,anchor='middle').configure_concat(spacing=10)





############# streamlit #####################

## columns
# col1, col2 = st.beta_columns([2, 3])
# col1.subheader("Total")
# col1.write(total)
# col2.subheader("2018 winter")
# col2.write(bars_2018)

st.header('2018 Winter Olympics')
st.write(bars_2018)

# st.write('Not only in 2018, Norway won the most in total!')

# total medals
st.markdown("<h3 style='text-align: left; color: steelblue;'>Not only in 2018, Norway won the most in total!</h3>", 
                unsafe_allow_html=True)

with st.beta_expander("👉 In history, top 5 countries who won the most medals"):
    st.write(total)

st.header('How many medals did these countries win in the past?')
st.write(history_line)
st.markdown("<h3 style='text-align: left; color: steelblue;'>Not just luckily, 2018 is not the first time Norway won more medals than the US did.</h3>",
                unsafe_allow_html=True)

with st.beta_expander("👉 How many medals in the past they won?"):
    st.header("How many medals in the past they won?")
    st.write(inter_1)


# comapere discipline
st.header('Expertise sports')

st.write(hmap)
st.markdown("<h3 style='text-align: left; color: steelblue;'>USA won most of the medals from Ice Hockey most of the time, while Norway from Cross Country Skiing. They are not overlapping expertises too much.</h3>", 
                unsafe_allow_html=True)

with st.beta_expander("👉 What sports are the other top 5 countries good at?"):
    # st.write(inter_2)
    st.write(T_5)

st.header('Society development matters?!')
# st.write("Index factors including:\na long and healthy life,\nthe ability to acquire knowledge,\nand a decent standard of living\nyear: 2018")

st.markdown("<p style='text-align: left; color: grey;font-style:italic'>Index factors including: a long and healthy life, the ability to acquire knowledge, and a decent standard of living (year: 2018)</p>", 
                unsafe_allow_html=True)

st.write(human_dev)

# top 5 HDI tred
with st.beta_expander("👉 HDI of Top 5 countries since 2000"):
    st.write(HDI_trend)
    st.write('Norway is always ahead of other countries!!')

st.markdown("<h3 style='text-align: left; color: steelblue;'>Among 2018 top 5 countries, Human development index are all good. Does that mean highly developed countries have better sports development?!</h3>", 
                unsafe_allow_html=True)
st.markdown("<h3 style='text-align: left; color: steelblue;'>Is this also a hint that we could investigate Norway's development policy?</h3>", 
                unsafe_allow_html=True)


