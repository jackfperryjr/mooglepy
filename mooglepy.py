import sqlite3 as sql
import requests
import pandas as pd
import matplotlib.pyplot as plot
import numpy as np
import os
from os import system, name 

# Setting some stuff to be used later (bad practice, I know).
api_data = requests.get("https://www.moogleapi.com/api/characters")
data_frame = pd.read_json(api_data.text)
origins = data_frame.origin.nunique()

def setup():
    # Function to build the directory to be used.
    desktop = os.path.expanduser("~/desktop")
    os.chdir(desktop)

    if not os.path.isdir('mooglepy'):
        os.makedirs('mooglepy')
        os.chdir('mooglepy')

def create_database():
    # Function to build the database.
    connect = sql.connect("mooglepy.db")
    # Dropping columns I won't use from the API data.
    data = data_frame.drop(['id', 'description', 'race', 'job', 'age', 'height', 'weight', 'picture'], axis=1)
    # Rearranging the order the columns are in.
    columns = data.columns.tolist()
    columns = columns[+1:] + columns[:+1]
    data = data[columns]
    # Splitting the data into male and female.
    data_male = data.query('gender=="Male"')
    data_female = data.query('gender=="Female"')
    # Dumping data into Sqlite database.
    data_male.to_sql('male', connect, if_exists='replace', index=False)
    data_female.to_sql('female', connect, if_exists='replace', index=False)
    connect.commit()
    connect.close()    

def get_origins():
    # Function to build a list of iteration titles.
    connect = sql.connect("mooglepy.db")
    cursor = connect.cursor()
    results = []
    cursor.execute('select origin from (select origin from male union all select origin from female) group by origin')
    result = cursor.fetchall()

    for row in result:
        results.append(row[0])
    
    connect.commit()
    connect.close()
    return results

def get_genders(table):
    # Function to build a list of total genders per iteration.
    connect = sql.connect("mooglepy.db")
    cursor = connect.cursor()
    cursor.execute('select count(origin) from ' + table + ' group by origin')
    result = cursor.fetchall()
    results = [x[0] for x in result]
    
    if table == 'female':
        results.insert(0,0)
        results[10] = results[9] + results[10]
        results[12:12] = [results[13]]

    if table == 'male':
        results[10:10] = [results[9]]
        results[13] = results[12] + results[13]
        
    connect.commit()
    connect.close()
    return results

def create_graph():
    # Function to graph data.
    males = get_genders('male')
    females = get_genders('female')
    fig, ax = plot.subplots()
    index = np.arange(0, origins)
    bar_width = 0.35
    opacity = 0.7
    # Defining the bar for males.
    male_bar = plot.bar(index, males, bar_width,
                      alpha=opacity,
                      color='blue',
                      label='Males')
    # Defining the bar for females.
    female_bar = plot.bar(index + bar_width, females, bar_width,
                     alpha=opacity,
                     color='pink',
                     label='Females')
    # Grabbing the origins to use for xticks.
    game_titles = get_origins()
    # Building the graph.
    plot.ylabel('Number of each')
    plot.title('Male and Female characters across Final Fantasy')
    plot.xticks(index + bar_width, game_titles, rotation='vertical')
    plot.style.use('seaborn-paper')
    plot.legend()
    plot.tight_layout()
    plot.show(block=False)
    # Making sure we're in the created directory.
    mooglepy = os.path.expanduser("~/desktop/mooglepy")
    os.chdir(mooglepy)
    # Saving the graph as a .png file.
    fig.savefig("mooglepy.png")

def clear_screen(): 
    # Function to clear the screen before output message.
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear')

def main():
    # Function to do all the stuff.
    setup()
    # Getting totals for genders.
    totals = data_frame['gender'].value_counts()
    total_males = str(totals[0])
    total_females = str(totals[1])
    total_unknown = str(totals[2])
    create_database()
    create_graph()

    # Output message once completed.
    clear_screen()
    print("*********************************************************************************\n")
    print("I'm looking at the ratio of male to female characters across the data I've \ncompiled.")
    print('There are a total of ' + total_males + ' male characters and ' + total_females + ' female characters.')
    print('Additionally, there are ' + total_unknown + ' unknown character genders across the Final Fantasy game \ndata I have collected.')
    print("\nYour mooglepy.db and mooglepy.png have been output to a directory on your desktop \ncalled mooglepy.")
    print("\n*********************************************************************************")

if __name__ == "__main__":
    main()