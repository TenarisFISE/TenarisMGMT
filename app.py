import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_table
import flask
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
from _datetime import timedelta
from plotly.subplots import make_subplots
import io

# <editor-fold desc="colors and App Creation">
colors = ['rgb(0, 255, 0)', 'rgb(0, 0, 255)', 'rgb(255, 0, 0)']
colors1 = ['#7CFC00', '#32CD32', '#228B22', '#008000', '#006400', '#ADFF2F', '#9ACD32', '#808000', '#556B2F',
           '#6B8E23', '#7FFF00', '#26A122', '#10900C', '#12AF0D', '#18CD12']
colors2 = dict(Active='rgb(0, 255, 0)', Standby='rgb(0, 0, 255)', Vacation='rgb(255, 0, 0)')

# create dash app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# </editor-fold>

# <editor-fold desc="Gantt Chart Data">
df = pd.read_excel("Test.xlsx")

# <editor-fold desc="People Vs. Date Main">
# collect person 1 data
df1 = pd.DataFrame()
df1['Task'] = df['FSS1 assigned']
df1['Start'] = df['Expected date']
df1['Finish'] = df['Finish date']
df1['Complete'] = df['Job']
df1['Description'] = df['Customer']
df1['Resource'] = df['Type']
df1['country'] = df['Country']
df1['SubBU'] = df['Sub BU']
df1['BU'] = df['BU']

df2 = pd.DataFrame()
# collect person 2 data
df2['Task'] = df['FSS2 assigned']
df2['Start'] = df['Expected date']
df2['Finish'] = df['Finish date']
df2['Complete'] = df['Job']
df2['Description'] = df['Customer']
df2['Resource'] = df['Type']
df2['country'] = df['Country']
df2['SubBU'] = df['Sub BU']
df2['BU'] = df['BU']

# merge person 1 data and person 2 and remove empty person 2 values
frames = [df1, df2]
result = pd.concat(frames)
result = result[result.Task != 'na']
result.reset_index(inplace=True, drop=True)
df1 = result
df1.reset_index(inplace=True, drop=True)
df1.dropna(subset=['Start'], inplace=True)

# create people vs date gantt chart figure
fig = ff.create_gantt(df1, group_tasks=True, colors=colors, index_col='Resource', reverse_colors=False,
                      show_colorbar=True)
# </editor-fold>

# <editor-fold desc="Jobs Vs. Date">
df3 = pd.DataFrame()
# get country and customer data
df3['Task'] = df1['Description'] + ", " + df1['country']
df3['Start'] = df1['Start']
df3['Finish'] = df1['Finish']
df3['Description'] = df1['Task']

# for loop to go through df and check if the name is TBC and if so group in new column as announced TBC1 TBC 2
for i in range(df3['Task'].count()):
    if df1.loc[i, 'Task'] == 'TBC1':
        df3.loc[i, 'Complete'] = 'TBC1'
    elif df1.loc[i, 'Task'] == 'TBC2':
        df3.loc[i, 'Complete'] = 'TBC2'
    else:
        df3.loc[i, 'Complete'] = 'Announced'


# <editor-fold desc="Regions Gantt">
# gantt charts creation function
def gantt_fig(df):
    data = []
    for row in df.itertuples():
        data.append(
            dict(Task=str(row.Task), Start=str(row.Start), Finish=str(row.Finish), Resource=str(row.Complete)))
    fig = ff.create_gantt(data, index_col='Resource', show_colorbar=True, showgrid_x=True, title='Gantt Chart')
    fig['layout'].update(margin=dict(l=310))

    return fig


df3['Countries'] = df1['country']
df3['SubBU'] = df1['SubBU']
df3['BU'] = df1['BU']

df3Dict = df3.to_dict()

# DIMI DINS
optionsBU = df3['BU'].unique()
# OMENA GCC SSA NS
optionsSBU = df3['SubBU'].unique()

all_options = {'DIMI': ['GCC', 'OMENA'],
               'DINS': [u'NS', 'SSA']}
# </editor-fold>

# create gantt chart for jobs
fig_j = ff.create_gantt(df3, group_tasks=True, colors=colors, index_col='Complete', reverse_colors=False,
                        show_colorbar=True)

# df4 = pd.DataFrame()
# # collect data and group it based on country
# df4['Task'] = df1['Description'] + ", " + df1['country']
# df4['Start'] = df1['Start']
# df4['Finish'] = df1['Finish']
# df4['Description'] = df1['Task']
# df4['Resource'] = df1['country']
#
# # create gantt chart for countries
# fig_c = ff.create_gantt(df4, group_tasks=True, colors=colors1, index_col='Resource', reverse_colors=False,
#                         show_colorbar=True)
# </editor-fold>

# <editor-fold desc="Data Analysis">
new_df = pd.DataFrame()
new_df2 = pd.DataFrame()


def calcMon():
    # collect data into a df

    df_date = pd.DataFrame()
    # collect person 1 data
    df_date['Name'] = df['FSS1 assigned']
    df_date['Start'] = df['Expected date']
    df_date['Finish'] = df['Finish date']
    df_date['type'] = df['Type']

    df_date2 = pd.DataFrame()
    # collect person 2 data
    df_date2['Name'] = df['FSS2 assigned']
    df_date2['Start'] = df['Expected date']
    df_date2['Finish'] = df['Finish date']
    df_date2['type'] = df['Type']

    # merge data and remove empty from person 2
    frames = [df_date, df_date2]
    result = pd.concat(frames)
    result = result[result.Name != 'na']
    result.reset_index(inplace=True, drop=True)
    df_date = result
    df_date.reset_index(inplace=True, drop=True)

    months_df = pd.DataFrame()
    # collect data on start and finish data of each month to compare it for month assignment
    months_df['Month'] = ['Jan19', 'Feb19', 'Mar19', 'Apr19', 'May19', 'Jun19', 'Jul19', 'Aug19', 'Sep19', 'Oct19',
                          'Nov19', 'Dec19', 'Jan20', 'Feb20', 'Mar20', 'Apr20', 'May20', 'Jun20', 'Jul20', 'Aug20',
                          'Sep20', 'Oct20', 'Nov20', 'Dec20']
    months_df['M_Start'] = ['1/1/2019', '2/1/2019', '3/1/2019', '4/1/2019', '5/1/2019', '6/1/2019', '7/1/2019',
                            '8/1/2019', '9/1/2019', '10/1/2019', '11/1/2019', '12/1/2019', '1/1/2020', '2/1/2020',
                            '3/1/2020', '4/1/2020', '5/1/2020', '6/1/2020', '7/1/2020', '8/1/2020', '9/1/2020',
                            '10/1/2020', '11/1/2020', '12/1/2020']
    months_df['M_Finish'] = ['1/31/2019', '2/28/2019', '3/31/2019', '4/30/2019', '5/31/2019', '6/30/2019', '7/31/2019',
                             '8/31/2019', '9/30/2019', '10/31/2019', '11/30/2019', '12/31/2019', '1/31/2020',
                             '2/28/2020', '3/31/2020', '4/30/2020', '5/31/2020', '6/30/2020', '7/31/2020', '8/31/2020',
                             '9/30/2020', '10/31/2020', '11/30/2020', '12/31/2020']
    months_df['M_Start'] = months_df['M_Start'].astype('datetime64[ns]')
    months_df['M_Finish'] = months_df['M_Finish'].astype('datetime64[ns]')

    global new_df
    global new_df2
    # for loop to assign each row a specific month based on its date start and finish
    for j in range(df_date['Name'].count()):
        for i in range(months_df['Month'].count()):
            # check if the date start is greater than a certain month and smaller than that same month
            if df_date.loc[j, 'Start'] >= months_df.loc[i, 'M_Start'] and df_date.loc[j, 'Finish'] <= months_df.loc[
                i, 'M_Finish']:
                new_df.loc[j, 'name'] = df_date.loc[j, 'Name']
                new_df.loc[j, 'month'] = months_df.loc[i, 'Month']
                new_df.loc[j, 'duration1'] = df_date.loc[j, 'Finish'] - df_date.loc[j, 'Start']
                new_df.loc[j, 'duration2'] = 0
                new_df.loc[j, 'start'] = df_date.loc[j, 'Start']
                new_df.loc[j, 'finish'] = df_date.loc[j, 'Finish']
                new_df.loc[j, 'Type'] = df_date.loc[j, 'type']

            # check if the date start is greater than a certain month and ends the next month
            elif df_date.loc[j, 'Start'] >= months_df.loc[i, 'M_Start'] and df_date.loc[j, 'Finish'] <= \
                    months_df.loc[
                        i + 1, 'M_Finish']:
                new_df.loc[j, 'name'] = df_date.loc[j, 'Name']
                new_df.loc[j, 'month'] = months_df.loc[i, 'Month'] + "/" + months_df.loc[i + 1, 'Month']
                new_df.loc[j, 'duration1'] = months_df.loc[i, 'M_Finish'] - df_date.loc[j, 'Start']
                new_df.loc[j, 'Type'] = df_date.loc[j, 'type']
                if months_df.loc[i, 'M_Finish'] == df_date.loc[j, 'Start']:
                    new_df.loc[j, 'duration1'] = new_df.loc[j, 'duration1']
                new_df.loc[j, 'duration2'] = df_date.loc[j, 'Finish'] - months_df.loc[i + 1, 'M_Start']
                if df_date.loc[j, 'Finish'] == months_df.loc[i + 1, 'M_Start']:
                    new_df.loc[j, 'duration2'] = new_df.loc[j, 'duration2']
                new_df.loc[j, 'start'] = df_date.loc[j, 'Start']
                new_df.loc[j, 'finish'] = df_date.loc[j, 'Finish']

    new_df2 = new_df[new_df.duration2 != 0]
    new_df.reset_index(inplace=True, drop=True)
    new_df2.reset_index(inplace=True, drop=True)
    new_df2['duration1'] = new_df2['duration2']
    del new_df['duration2']
    del new_df2['duration2']

    # check if the months that have feb/march for ex. have the right start and end date
    for j in range(new_df['name'].count()):
        for i in range(months_df['Month'].count()):
            if new_df.loc[j, 'start'] >= months_df.loc[i, 'M_Start'] and new_df.loc[j, 'finish'] <= months_df.loc[
                i + 1, 'M_Finish'] and len(new_df.loc[j, 'month']) > 6:
                if new_df.loc[j, 'start'] == new_df.loc[j, 'start']:
                    new_df.loc[j, 'finish'] = months_df.loc[i + 1, 'M_Start']
                else:
                    new_df.loc[j, 'finish'] = months_df.loc[i, 'M_Finish']

    for j in range(new_df2['name'].count()):
        for i in range(months_df['Month'].count()):
            if new_df2.loc[j, 'start'] >= months_df.loc[i, 'M_Start'] and new_df2.loc[j, 'finish'] <= months_df.loc[
                i + 1, 'M_Finish'] and len(new_df2.loc[j, 'month']) > 6:
                new_df2.loc[j, 'actual_start'] = months_df.loc[i + 1, 'M_Start']

    # check if the months that have feb/march for ex. are feb or march
    new_df2['start'] = new_df2['actual_start']
    del new_df2['actual_start']

    for k in range(new_df['name'].count()):
        if len(new_df.loc[k, 'month']) > 4:
            new_df.loc[k, 'month'] = new_df.loc[k, 'month'][:5]

    for k in range(new_df2['name'].count()):
        new_df2.loc[k, 'month'] = new_df2.loc[k, 'month'][-5:]

    # merge the last 2 final dataframes with the final months names and take actual month name if split
    frames5 = [new_df2, new_df]
    result = pd.concat(frames5)
    result.reset_index(inplace=True, drop=True)
    df1 = result
    df1.reset_index(inplace=True, drop=True)
    for p in range(df1['name'].count()):
        if len(df1.loc[p, 'month']) > 4:
            df1.loc[p, 'month'] = df1.loc[p, 'month'][-5:]
    new_df = df1
    for i in range(new_df['duration1'].count()):
        new_df.loc[i, 'duration1'] = new_df.loc[i, 'duration1'] + timedelta(days=1)
        new_df.loc[i, 'duration'] = new_df.loc[i, 'duration1'].days
        new_df.loc[i, 'utilization'] = new_df.loc[i, 'duration1'].days / 16 * 100


calcMon()
# <editor-fold desc="Gantt Chart Data Analysis Data Collection">
gantt_chart_analysis = pd.DataFrame()
for i in range(new_df['name'].count()):
    gantt_chart_analysis.loc[i, 'Task'] = new_df.loc[i, 'name'] + '    D: ' + str(new_df.loc[i, 'duration'])[:-2] + \
                                          ' (' + str(new_df.loc[i, 'utilization']) + '%)'
gantt_chart_analysis['Start'] = new_df['start']
gantt_chart_analysis['Finish'] = new_df['finish']
gantt_chart_analysis['Complete'] = new_df['month']
gantt_chart_analysis['Resource'] = new_df['Type']
gantt_chart_analysis['Start'] = pd.to_datetime(gantt_chart_analysis.Start)
gantt_chart_analysis = gantt_chart_analysis.sort_values(by='Start')
# </editor-fold>

# </editor-fold>
# </editor-fold>

# <editor-fold desc="Map Data">
map_df = pd.DataFrame()
map_df['names'] = df['FSS1 assigned']
map_df['country'] = df['Country']
map_df['job'] = df['Job']
map_df2 = pd.DataFrame()
map_df2['names'] = df['FSS2 assigned']
map_df2['country'] = df['Country']
map_df2['job'] = df['Job']
frames2 = [map_df, map_df2]
result2 = pd.concat(frames2)
result2 = result2[result2.names != 'na']
result2.reset_index(inplace=True, drop=True)
map_df = result2
map_df.reset_index(inplace=True, drop=True)

# country assignment
conditions1 = [
    (map_df['country'] == 'Egypt'),
    (map_df['country'] == 'Pakistan'),
    (map_df['country'] == 'Libya'),
    (map_df['country'] == 'Kurdistan'),
    (map_df['country'] == 'Tunisia'),
    (map_df['country'] == 'Egypt, Cairo'),
    (map_df['country'] == 'UAE'),
]
choices1 = [26.8, 30.38, 26.33, 36.41, 33.88, 30.06, 23.42]
map_df['lat'] = np.select(conditions1, choices1, default=0)
conditions2 = [
    (map_df['country'] == 'Egypt'),
    (map_df['country'] == 'Pakistan'),
    (map_df['country'] == 'Libya'),
    (map_df['country'] == 'Kurdistan'),
    (map_df['country'] == 'Tunisia'),
    (map_df['country'] == 'Egypt, Cairo'),
    (map_df['country'] == 'UAE'),
]
choices2 = [30.8, 69.34, 17.22, 44.38, 9.53, 31.25, 53.84]
map_df['lon'] = np.select(conditions2, choices2, default=0)

# assignment in map dataframe of lat and lon
map_df['BOOLa'] = map_df['lat'].duplicated(keep='first')
for j in range(map_df['lat'].count()):
    map_df['BOOLa'] = map_df['lat'].duplicated(keep='first')
    for i in range(map_df['lat'].count()):
        if map_df.loc[i, 'BOOLa']:
            map_df.loc[i, 'lat'] = map_df.loc[i, 'lat'] + 0.05
        else:
            map_df.loc[i, 'lat'] = map_df.loc[i, 'lat']

map_options = pd.DataFrame()

map_options['country'] = map_df['country'].unique()
# print(map_options)

map_df3 = pd.DataFrame()
# print(range(map_options['country'].count()))

for j in range(map_options['country'].count()):
    map_df3.loc[j, 'Num'] = len(map_df[map_df['country'] == map_options.loc[j, 'country']])
    map_df3.loc[j, 'country'] = map_options.loc[j, 'country']

    # country assignment
    conditions1 = [
        (map_df3['country'] == 'Egypt'),
        (map_df3['country'] == 'Pakistan'),
        (map_df3['country'] == 'Libya'),
        (map_df3['country'] == 'Kurdistan'),
        (map_df3['country'] == 'Tunisia'),
        (map_df3['country'] == 'Egypt, Cairo'),
        (map_df3['country'] == 'UAE'),
    ]
    choices1 = [26.8, 30.38, 26.33, 36.41, 33.88, 30.06, 23.42]
    map_df3['lat'] = np.select(conditions1, choices1, default=0)
    conditions2 = [
        (map_df3['country'] == 'Egypt'),
        (map_df3['country'] == 'Pakistan'),
        (map_df3['country'] == 'Libya'),
        (map_df3['country'] == 'Kurdistan'),
        (map_df3['country'] == 'Tunisia'),
        (map_df3['country'] == 'Egypt, Cairo'),
        (map_df3['country'] == 'UAE'),
    ]
    choices2 = [30.8, 69.34, 17.22, 44.38, 9.53, 31.25, 53.84]
    map_df3['lon'] = np.select(conditions2, choices2, default=0)

# create a map view with the data in the map dataframe
fig1 = px.scatter_mapbox(map_df3, lat="lat", lon="lon", hover_name="Num", hover_data=["country", "Num"],
                         zoom=2, height=650, color="country")
# color_discrete_sequence=["fuchsia"],
fig1.update_layout(mapbox_style="carto-positron")
fig1.update_layout(margin={"r": 20, "t": 20, "l": 20, "b": 20})
# </editor-fold>

# <editor-fold desc="Layout">
# url to update layout
url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# world map
layout_index = html.Div([
    dcc.Link(html.Button('World Map'), href='/'),
    dcc.Link(html.Button('Gantt Charts'), href='/page-1'),
    dcc.Link(html.Button('Monthly Analysis  '), href='/page-301'),
    dcc.Link(html.Button('Table View'), href='/page-2'),
    html.Br(),
    html.H2('World Map Representation of Database'),
    dcc.Graph(figure=fig1, id='country'),
],
    style={'text-align': 'center'})

# gantt chart people (Main)
layout_page_1 = html.Div([
    dcc.Link(html.Button('World Map'), href='/'),
    dcc.Link(html.Button('Gantt Charts'), href='/page-1'),
    dcc.Link(html.Button('Monthly Analysis  '), href='/page-301'),
    dcc.Link(html.Button('Table View'), href='/page-2'),
    html.Br(),
    html.H2('Gantt Charts'),
    # dcc.Link(html.Button('People'), href='/page-1'),
    # dcc.Link(html.Button('Jobs'), href='/page-3'),
    # dcc.Link(html.Button('Country'), href='/page-4'),
    # dcc.Link(html.Button('Full View'), href='/page-5'),
    dcc.Dropdown(id='Bu-dropdown', options=[{'label': k, 'value': k} for k in all_options.keys()], value='DIMI',
                 multi=True, ),
    html.Br(),
    dcc.Dropdown(id='SubBu-dropdown', multi=True, ),
    html.Br(),

    dcc.Store(id='dropdown-cache', data='initial value'),

    # dcc.Tabs(
    #     id='tabs',
    #     value='tab-1',
    #     parent_className='custom-tabs',
    #     className='custom-tabs-container',
    #     children=[
    #     dcc.Tab(
    #         label='Tab 1',
    #         value='tab-1',
    #         className='custom-tab',
    #         selected_className='custom-tab--selected',
    #         children=[
    #             dcc.Dropdown(
    #                 id='tab-1-dropdown',
    #             ),
    #         ]
    #     ),
    #     dcc.Tab(
    #         label='Tab 2',value='tab-2',className='custom-tab',selected_className='custom-tab--selected',
    #         children=[dcc.Dropdown(id='tab-2-dropdown',),]),],
    # ),



    # dcc.Graph(id='graph-id3'),

    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-2',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='By People',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='By Jobs',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='By Country',
                value='tab-3',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes'),
],
    style={'text-align': 'center'})

# gantt chart jobs
layout_page_3 = html.Div([
    dcc.Link(html.Button('World Map'), href='/'),
    dcc.Link(html.Button('Gantt Charts'), href='/page-1'),
    dcc.Link(html.Button('Monthly Analysis  '), href='/page-301'),
    dcc.Link(html.Button('Table View'), href='/page-2'),
    html.Br(),
    html.H2('Gantt Chart by Jobs'),
    dcc.Link(html.Button('People'), href='/page-1'),
    dcc.Link(html.Button('Jobs'), href='/page-3'),
    dcc.Link(html.Button('Country'), href='/page-4'),
    dcc.Link(html.Button('Full View'), href='/page-5'),
    html.Br(),
    html.Br(),
    dcc.Dropdown(
        id='Bu-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='DIMI',
        multi=True, ),
    html.Br(),
    dcc.Dropdown(id='SubBu-dropdown',
                 multi=True, ),
    dcc.Graph(id='graph-id2'),
    # dcc.Graph(figure=fig_j, id='gantt_j'),
],
    style={'text-align': 'center'})

# gantt chart Country
layout_page_4 = html.Div([
    dcc.Link(html.Button('World Map'), href='/'),
    dcc.Link(html.Button('Gantt Charts'), href='/page-1'),
    dcc.Link(html.Button('Monthly Analysis  '), href='/page-301'),
    dcc.Link(html.Button('Table View'), href='/page-2'),
    html.Br(),
    html.H2('Gantt Chart by Country'),
    dcc.Link(html.Button('People'), href='/page-1'),
    dcc.Link(html.Button('Jobs'), href='/page-3'),
    dcc.Link(html.Button('Country'), href='/page-4'),
    dcc.Link(html.Button('Full View'), href='/page-5'),
    html.Br(),
    html.Br(),
    dcc.Dropdown(
        id='Bu-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='DIMI',
        multi=True, ),
    html.Br(),
    dcc.Dropdown(id='SubBu-dropdown',
                 multi=True, ),
    dcc.Graph(id='graph-id'),
],
    style={'text-align': 'center'})

# gantt chart full view
layout_page_5 = html.Div([
    dcc.Link(html.Button('World Map'), href='/'),
    dcc.Link(html.Button('Gantt Charts'), href='/page-1'),
    dcc.Link(html.Button('Monthly Analysis  '), href='/page-301'),
    dcc.Link(html.Button('Table View'), href='/page-2'),
    html.Br(),
    html.H2('Full View Gantt Chart'),
    dcc.Link(html.Button('People'), href='/page-1'),
    dcc.Link(html.Button('Jobs'), href='/page-3'),
    dcc.Link(html.Button('Country'), href='/page-4'),
    dcc.Link(html.Button('Full View'), href='/page-5'),
    html.Br(),
    html.Br(),
    dcc.Dropdown(
        id='Bu-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='DIMI',
        multi=True, ),
    html.Br(),
    dcc.Dropdown(id='SubBu-dropdown',
                 multi=True, ),
    html.Br(),
    html.Br(),
    html.Div(children=[html.H2('People')], ),
    html.Div(children=[dcc.Graph(id='graph-id3')], ),
    html.Br(),
    html.Br(),
    html.Div(children=[html.H2('Jobs')], ),
    html.Div(children=[dcc.Graph(id='graph-id2')], ),
    html.Br(),
    html.Br(),
    html.Div(children=[html.H2('Countries')], ),
    html.Div(children=[dcc.Graph(id='graph-id')], ),
],
    style={'text-align': 'center'})

# table view
layout_page_2 = html.Div([
    dcc.Link(html.Button('World Map'), href='/'),
    dcc.Link(html.Button('Gantt Charts'), href='/page-1'),
    dcc.Link(html.Button('Monthly Analysis  '), href='/page-301'),
    dcc.Link(html.Button('Table View'), href='/page-2'),
    html.Br(),
    html.H2('Data Table'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        editable=False,
        row_deletable=False,
        style_as_list_view=True,
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white',
            'textAlign': 'left',
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'Region'},
                'textAlign': 'left'
            }
        ]
    ),

],
    style={'text-align': 'center'})


# gantt charts creation function
def gantt_fig(df):
    data = []
    for row in df.itertuples():
        data.append(
            dict(Task=str(row.Task), Start=str(row.Start), Finish=str(row.Finish), Resource=str(row.Complete)))
    fig = ff.create_gantt(data, index_col='Resource', show_colorbar=True, showgrid_x=True, title='Gantt Chart')
    fig['layout'].update(margin=dict(l=310))

    return fig


options = gantt_chart_analysis['Complete'].unique()
# gantt chart analysis page
layout_page_301 = html.Div([
    dcc.Link(html.Button('World Map'), href='/'),
    dcc.Link(html.Button('Gantt Charts'), href='/page-1'),
    dcc.Link(html.Button('Monthly Analysis  '), href='/page-301'),
    dcc.Link(html.Button('Table View'), href='/page-2'),
    html.Br(),
    html.H2('Gantt Chart Analysis February 2019'),
    dcc.Dropdown(id='my-dropdown',
                 options=[{'label': n, 'value': n} for n in options],
                 value=options[0]),
    dcc.Graph(id='display-selected-value'),
],
    style={'text-align': 'center'})


# pages layout creation
def serve_layout():
    if flask.has_request_context():
        return url_bar_and_content_div
    return html.Div([
        url_bar_and_content_div,
        layout_index,
        layout_page_1,
        layout_page_2,
        layout_page_3,
        layout_page_4,
        layout_page_5,
        layout_page_301,
    ])


app.layout = serve_layout


# </editor-fold>

# <editor-fold desc="Index Callback">
# pages through url callback
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/page-1":
        return layout_page_1
    elif pathname == "/page-2":
        return layout_page_2
    elif pathname == "/page-3":
        return layout_page_3
    elif pathname == "/page-4":
        return layout_page_4
    elif pathname == "/page-5":
        return layout_page_5
    elif pathname == "/page-301":
        return layout_page_301
    else:
        return layout_index


# update months gantt charts callback
@app.callback(
    dash.dependencies.Output('display-selected-value', 'figure'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_gantt(value):
    df2plot = gantt_chart_analysis[gantt_chart_analysis['Complete'] == value].reset_index(drop=True)
    fig = gantt_fig(df2plot)
    return fig


# update SUB BU dropdown with Bu values
@app.callback(
    Output('SubBu-dropdown', 'options'),
    [Input('Bu-dropdown', 'value')])
def set_SubBu_options(selected_Bu):
    if type(selected_Bu) == str:
        selected_list = list(selected_Bu.split(" "))
    else:
        selected_list = list(selected_Bu)

    if (str(len(selected_list)) == '1' and type(selected_Bu) == str):
        return [{'label': i, 'value': i} for i in all_options[selected_Bu]]

    elif (len(selected_list) == 1):
        return [{'label': i, 'value': i} for i in all_options[selected_Bu[0]]]

    elif (len(selected_list) == 2):
        x1 = [{'label': i, 'value': i} for i in all_options[selected_Bu[0]]]
        x2 = [{'label': i, 'value': i} for i in all_options[selected_Bu[1]]]
        x1 = x1 + x2
        return x1
    else:
        return [{'label': i, 'value': i} for i in all_options['DIMI']]


# prints options of DIMI or DINS when selected which are GCC OMENA or SSA or NS
@app.callback(
    Output('SubBu-dropdown', 'value'),
    [Input('SubBu-dropdown', 'options')])
def set_SubBu_value(available_options):
    return available_options[0]['value']


# Graph Callbacks

# Countries gantt callback
@app.callback(
    dash.dependencies.Output('graph-id', 'figure'),
    [dash.dependencies.Input('SubBu-dropdown', 'value')],
    [dash.dependencies.State('SubBu-dropdown', 'options'),
     dash.dependencies.State('SubBu-dropdown', 'value')])
def update2_gantt(selected, options, value):
    if type(selected) == str:
        selected_list = list(selected.split(" "))
    else:
        selected_list = list(selected)

    if str(len(selected_list)) == '1' or type(selected) == str:
        df1plot = df3.loc[df3['SubBU'] == selected_list[0]].reset_index(drop=True)
        fig21 = ff.create_gantt(df1plot, group_tasks=True, index_col='Countries', reverse_colors=False,
                                show_colorbar=True)
        return fig21

    elif len(selected_list) == 2:
        df1plot = df3.loc[df3['SubBU'] == selected_list[0]].reset_index(drop=True)
        df1plot2 = df3.loc[df3['SubBU'] == selected_list[1]].reset_index(drop=True)

        frames1 = [df1plot, df1plot2]
        result1 = pd.concat(frames1)
        df1plot = result1
        df1plot.reset_index(inplace=True, drop=True)
        fig22 = ff.create_gantt(df1plot, group_tasks=True, index_col='Countries', reverse_colors=False,
                                show_colorbar=True)
        return fig22

    elif len(selected_list) == 3:
        df1plot = df3.loc[df3['SubBU'] == selected_list[0]].reset_index(drop=True)
        df1plot2 = df3.loc[df3['SubBU'] == selected_list[1]].reset_index(drop=True)
        df1plot3 = df3.loc[df3['SubBU'] == selected_list[2]].reset_index(drop=True)

        frames1 = [df1plot, df1plot2, df1plot3]
        result1 = pd.concat(frames1)
        df1plot = result1
        df1plot.reset_index(inplace=True, drop=True)
        fig23 = ff.create_gantt(df1plot, group_tasks=True, index_col='Countries', reverse_colors=False,
                                show_colorbar=True)
        return fig23

    elif len(selected_list) == 4:
        df1plot = df3.loc[df3['SubBU'] == selected_list[0]].reset_index(drop=True)
        df1plot2 = df3.loc[df3['SubBU'] == selected_list[1]].reset_index(drop=True)
        df1plot3 = df3.loc[df3['SubBU'] == selected_list[2]].reset_index(drop=True)
        df1plot4 = df3.loc[df3['SubBU'] == selected_list[3]].reset_index(drop=True)

        frames1 = [df1plot, df1plot2, df1plot3, df1plot4]
        result1 = pd.concat(frames1)
        df1plot = result1
        df1plot.reset_index(inplace=True, drop=True)
        fig24 = ff.create_gantt(df1plot, group_tasks=True, index_col='Countries', reverse_colors=False,
                                show_colorbar=True)
        return fig24
    else:
        df_empty = [dict(Task="", Start='', Finish='')]
        fig_emp = ff.create_gantt(df_empty)
        return fig_emp


# Jobs gantt callback

@app.callback(
    dash.dependencies.Output('graph-id2', 'figure'),
    [dash.dependencies.Input('SubBu-dropdown', 'value')],
    [dash.dependencies.State('SubBu-dropdown', 'options'),
     dash.dependencies.State('SubBu-dropdown', 'value')])
def update2_gantt(selected, options, value):
    if type(selected) == str:
        selected_list = list(selected.split(" "))
    else:
        selected_list = list(selected)

    if str(len(selected_list)) == '1' or type(selected) == str:
        df2plot = df3.loc[df3['SubBU'] == selected_list[0]].reset_index(drop=True)
        fig21 = ff.create_gantt(df2plot, group_tasks=True, index_col='Complete', reverse_colors=False,
                                show_colorbar=True)
        return fig21

    elif len(selected_list) == 2:
        df2plot = df3.loc[df3['SubBU'] == selected_list[0]].reset_index(drop=True)
        df2plot2 = df3.loc[df3['SubBU'] == selected_list[1]].reset_index(drop=True)

        frames1 = [df2plot, df2plot2]
        result1 = pd.concat(frames1)
        df2plot = result1
        df2plot.reset_index(inplace=True, drop=True)
        fig22 = ff.create_gantt(df2plot, group_tasks=True, index_col='Complete', reverse_colors=False,
                                show_colorbar=True)
        return fig22

    elif len(selected_list) == 3:
        df2plot = df3.loc[df3['SubBU'] == selected_list[0]].reset_index(drop=True)
        df2plot2 = df3.loc[df3['SubBU'] == selected_list[1]].reset_index(drop=True)
        df2plot3 = df3.loc[df3['SubBU'] == selected_list[2]].reset_index(drop=True)

        frames1 = [df2plot, df2plot2, df2plot3]
        result1 = pd.concat(frames1)
        df2plot = result1
        df2plot.reset_index(inplace=True, drop=True)
        fig23 = ff.create_gantt(df2plot, group_tasks=True, index_col='Complete', reverse_colors=False,
                                show_colorbar=True)
        return fig23

    elif len(selected_list) == 4:
        df2plot = df3.loc[df3['SubBU'] == selected_list[0]].reset_index(drop=True)
        df2plot2 = df3.loc[df3['SubBU'] == selected_list[1]].reset_index(drop=True)
        df2plot3 = df3.loc[df3['SubBU'] == selected_list[2]].reset_index(drop=True)
        df2plot4 = df3.loc[df3['SubBU'] == selected_list[3]].reset_index(drop=True)

        frames1 = [df2plot, df2plot2, df2plot3, df2plot4]
        result1 = pd.concat(frames1)
        df2plot = result1
        df2plot.reset_index(inplace=True, drop=True)
        fig24 = ff.create_gantt(df2plot, group_tasks=True, index_col='Complete', reverse_colors=False,
                                show_colorbar=True)
        return fig24
    else:
        df_empty = [dict(Task="", Start='', Finish='')]
        fig_emp = ff.create_gantt(df_empty)
        return fig_emp


# people gantt callback
@app.callback(
    dash.dependencies.Output('graph-id3', 'figure'),
    [dash.dependencies.Input('SubBu-dropdown', 'value')],
    [dash.dependencies.State('SubBu-dropdown', 'options'),
     dash.dependencies.State('SubBu-dropdown', 'value')])
def update2_gantt(selected, options, value):
    if type(selected) == str:
        selected_list = list(selected.split(" "))
    else:
        selected_list = list(selected)

    if str(len(selected_list)) == '1' or type(selected) == str:
        df1plot = df1.loc[df1['SubBU'] == selected_list[0]].reset_index(drop=True)
        fig31 = ff.create_gantt(df1plot, group_tasks=True, index_col='Resource', reverse_colors=False,
                                show_colorbar=True)
        return fig31

    elif len(selected_list) == 2:
        df1plot = df1.loc[df1['SubBU'] == selected_list[0]].reset_index(drop=True)
        df1plot2 = df1.loc[df1['SubBU'] == selected_list[1]].reset_index(drop=True)

        frames1 = [df1plot, df1plot2]
        result1 = pd.concat(frames1)
        df1plot = result1
        df1plot.reset_index(inplace=True, drop=True)
        fig32 = ff.create_gantt(df1plot, group_tasks=True, index_col='Resource', reverse_colors=False,
                                show_colorbar=True)
        return fig32

    elif len(selected_list) == 3:
        df1plot = df1.loc[df1['SubBU'] == selected_list[0]].reset_index(drop=True)
        df1plot2 = df1.loc[df1['SubBU'] == selected_list[1]].reset_index(drop=True)
        df1plot3 = df1.loc[df1['SubBU'] == selected_list[2]].reset_index(drop=True)

        frames1 = [df1plot, df1plot2, df1plot3]
        result1 = pd.concat(frames1)
        df1plot = result1
        df1plot.reset_index(inplace=True, drop=True)
        fig33 = ff.create_gantt(df1plot, group_tasks=True, index_col='Resource', reverse_colors=False,
                                show_colorbar=True)
        return fig33

    elif len(selected_list) == 4:
        df1plot = df1.loc[df1['SubBU'] == selected_list[0]].reset_index(drop=True)
        df1plot2 = df1.loc[df1['SubBU'] == selected_list[1]].reset_index(drop=True)
        df1plot3 = df1.loc[df1['SubBU'] == selected_list[2]].reset_index(drop=True)
        df1plot4 = df1.loc[df1['SubBU'] == selected_list[3]].reset_index(drop=True)

        frames1 = [df1plot, df1plot2, df1plot3, df1plot4]
        result1 = pd.concat(frames1)
        df1plot = result1
        df1plot.reset_index(inplace=True, drop=True)
        fig34 = ff.create_gantt(df1plot, group_tasks=True, index_col='Resource', reverse_colors=False,
                                show_colorbar=True)
        return fig34
    else:
        df_empty = [dict(Task="", Start='', Finish='')]
        fig_emp = ff.create_gantt(df_empty)
        return fig_emp


@app.callback(Output('tabs-content-classes', 'children'),
              [Input('tabs-with-classes', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return dcc.Graph(id='graph-id3')

    elif tab == 'tab-2':
        return dcc.Graph(id='graph-id2')

    elif tab == 'tab-3':
        return dcc.Graph(id='graph-id')



# @app.callback(Output('dropdown-cache', 'data'),
#               [Input('tab-1-dropdown', 'value'),
#                Input('tab-2-dropdown', 'value')],
#                [State('tabs', 'value')])
# def store_dropdown_cache(tab_1_drodown_sel, tab_2_drodown_sel, tab):
#     if tab == 'tab-1':
#         return tab_1_drodown_sel
#     elif tab == 'tab-2':
#         return tab_2_drodown_sel
#
# @app.callback(Output('tab-1-dropdown', 'value'),
#               [Input('tabs', 'value')],
#               [State('dropdown-cache', 'data')])
# def synchronize_dropdowns(_, cache):
#     return cache
#
# @app.callback(Output('tab-2-dropdown', 'value'),
#               [Input('tabs', 'value')],
#               [State('dropdown-cache', 'data')])
# def synchronize_dropdowns(_, cache):
#     return cache




if __name__ == '__main__':
    app.run_server(debug=True)
# </editor-fold>
