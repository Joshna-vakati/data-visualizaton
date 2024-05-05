
import plotly.graph_objects as go
import pandas as pd
 
 # Reading the data
df = pd.read_csv("Loksabha.csv")

df3=df.copy()


df = df[(df['state'] == 'Andhra Pradesh') & (df['year'] == 2009) ]

df1=df.copy()
df2=df.copy()


fig = go.Figure()

fig.add_trace(go.Bar(x=df['Pc_name'], 
                     y=df['electors'],
                     name = 'electors',
                     showlegend = True, 
                     text = df['electors']))

fig.add_trace(go.Scatter(x=df['Pc_name'], 
                         y=df['votes'],
                         mode ='lines',
                         name = 'votes', 
                         showlegend = True, 
                         text = df['votes']))

fig.update_layout(title='<b>Andhra Pradesh Electors vs Votes in 2009</b>',
                  plot_bgcolor = 'rgba(0,0,0,0)',
                  yaxis_title = 'Count',
                  xaxis_title = 'Place Name',
                  title_x =0.5
                  )

# Display the chart
fig.show()

# ********************************   CHART 2  ******************************


winning_party_count = df1.groupby(['year', 'Pc_name', 'party'])['party'].count().reset_index(name='wins')

winning_party = winning_party_count.loc[winning_party_count.groupby(['year', 'Pc_name'])['wins'].idxmax()]

# print(winning_party)

labels = winning_party['party']
values = winning_party['wins']

fig = go.Figure(data = [go.Pie(labels=labels, values = values)])
fig.update_layout(title = '<b>winning party Analysis in 2009</b>',
                  plot_bgcolor = 'rgba(0,0,0,0)',
                  title_x =0.5)
# Display the chart
fig.show()



# ********************************   CHART 3  ******************************


# Remove commas from 'votes' column
df2['votes'] = df2['votes'].str.replace(',', '')

# Convert 'votes' column to numeric
df2['votes'] = pd.to_numeric(df2['votes'], errors='coerce')

# Drop rows with NaN values in 'votes' column
df2.dropna(subset=['votes'], inplace=True)

party_votes = df2.groupby('party')['votes'].sum().reset_index()
party_votes = party_votes.sort_values(by='votes', ascending=False)
party_votes['cumulative_percentage'] = (party_votes['votes'].cumsum() / party_votes['votes'].sum()) * 100

# considering top 20 
party_votes=party_votes.head(20)

# Creating  Pareto chart 
fig = go.Figure()

fig.add_trace(go.Bar(x=party_votes['party'], 
                     y=party_votes['votes'], 
                     name='Votes', 
                     marker=dict(color='blue')))

fig.add_trace(go.Scatter(x=party_votes['party'], 
                         y=party_votes['cumulative_percentage'], 
                         mode='lines', 
                         name='Cumulative Percentage', 
                         yaxis='y2', 
                         marker=dict(color='red')))

# Update layout
fig.update_layout(title='<b>Pareto Chart - Party-wise Votes</b>',
                  xaxis=dict(title='Party'),
                  yaxis=dict(title='Votes'),
                  yaxis2=dict(title='Cumulative Percentage', 
                overlaying='y', 
                side='right', 
                range=[0, 100]
))

fig.show()


# ********************************   CHART 4  ******************************

parties_to_consider = ['Indian National Congress', 'Telugu Desam', 'Janta Party',
                       'Yuvajana Sramika Rythu Congress Party', 'Bharatiya Janta Party',
                       'All India Trinamool Congress', 'Nationalist Congress Party', 'Biju Janata Dal']

# Years to consider
years_to_consider = [1999, 2004, 2009, 2014, 2019]

# Filter DataFrame by parties and years
df_filtered = df3[df3['party'].isin(parties_to_consider) & df3['year'].isin(years_to_consider)]
# print(f'dfghjklknb id {df_filtered}')

# Group by year and party, and find the max votes
grouped = df_filtered.groupby(['year', 'party'])['votes'].max().reset_index()
# print(f'goiuytcvbn is {grouped}')

fig = go.Figure()

for party, party_df in grouped.groupby('party'):
    fig.add_trace(go.Bar(
        y=party_df['year'],
        x=party_df['votes'],
        name=party,
        orientation='h',  # Horizontal orientation
        marker=dict(line=dict(width=3)) 
    ))

# Update layout
fig.update_layout(
    barmode='stack',  # Stacked bar mode
    title={'text': '<b>Horizontal Stacked Bar Chart of Votes by Party for Specific Years (Max Value)</b>',
           'x': 0.5,  # Centered horizontally
           'xanchor': 'center'},
    xaxis_title='Max Votes',
    yaxis_title='Year',
    showlegend=True,
    plot_bgcolor='rgba(0,0,0,0)'
)

# Show the chart
fig.show()