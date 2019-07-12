import pandas as pd

teams = [
    'atlanta_hawks',
    'boston_celtics',
    'brooklyn_nets',
    'charlotte_hornets',
    'chicago_bulls',
    'cleveland_cavaliers',
    'dallas_mavericks',
    'denver_nuggets',
    'detroit_pistons',
    'golden_state_warriors',
    'houston_rockets',
    'indiana_pacers',
    'los_angeles_clippers',
    'los_angeles_lakers',
    'memphis_grizzlies',
    'miami_heat',
    'milwaukee_bucks',
    'minnesota_timberwolves',
    'new_orleans_pelicans',
    'new_york_knicks',
    'oklahoma_city_thunder',
    'orlando_magic',
    'philadelphia_76ers',
    'phoenix_suns',
    'portland_trailblazers',
    'sacramento_kings',
    'san_antonio_spurs',
    'toronto_raptors',
    'utah_jazz',
    'washington_wizards'
]

df = pd.DataFrame()
for team in teams:
    team += '_2019'
    df = df.append(pd.read_csv('../../../data/nba/' + team + '.csv'))

df2 = df[['date','game_type','team','opponent']]
df3 = df2.loc[df2['game_type'] == 'Regular']
df4 = df3[['date','team']].drop_duplicates()
df5 = df3[['date','opponent']].drop_duplicates()

df5.groupby('opponent').count()


