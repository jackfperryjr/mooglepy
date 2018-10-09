import sqlite3 as sql
import requests
import pandas as pd
import matplotlib.pyplot as plot
import numpy as np
import os
from os import system, name 

api_data = requests.get("https://www.moogleapi.com/api/characters")
data_frame = pd.read_json(api_data.text)
origins = data_frame.origin.nunique()

def setup():
    desktop = os.path.expanduser("~/desktop")
    os.chdir(desktop)
    
    if not os.path.isdir('mooglepy'):
        os.makedirs('mooglepy')
        os.chdir('mooglepy')

def create_database():
    connect = sql.connect("mooglepy.db")
    data = data_frame.drop(['id', 'description', 'race', 'job', 'age', 'height', 'weight', 'picture'], axis=1)
    
    columns = data.columns.tolist()
    columns = columns[+1:] + columns[:+1]

    data = data[columns]
    data_male = data.query('gender=="Male"')
    data_female = data.query('gender=="Female"')

    data_male.to_sql('male', connect, if_exists='replace', index=False)
    data_female.to_sql('female', connect, if_exists='replace', index=False)
    
    connect.commit()
    connect.close()    

def get_origins():
    connect = sql.connect("mooglepy.db")
    cursor = connect.cursor()
    results = []
    cursor.execute('select origin from (select origin from male union all select origin from female) group by origin')
    result = cursor.fetchall()

    for row in result:
        results.append(row[0])
    
    connect.commit()
    connect.close() 
#     print(results)
    return results

def get_males():
    connect = sql.connect("mooglepy.db")
    cursor = connect.cursor()
    results = []
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 01"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 02"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 03"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 04"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 05"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 06"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 07"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 08"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 09"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 10"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 10-2" or origin="Final Fantasy 10"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 12"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 13"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 13-2" or origin="Final Fantasy 13"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from male where origin="Final Fantasy 15"')
    result = cursor.fetchone()
    results.extend(result)   
    
    connect.commit()
    connect.close() 
#     print(results)
    return results

def get_females():
    connect = sql.connect("mooglepy.db")
    cursor = connect.cursor()
    results = []
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 01"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 02"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 03"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 04"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 05"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 06"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 07"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 08"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 09"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 10"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 10-2" or origin="Final Fantasy 10"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 12"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 13"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 13-2" or origin="Final Fantasy 13"')
    result = cursor.fetchone()
    results.extend(result)
    
    cursor.execute('select count(*) from female where origin="Final Fantasy 15"')
    result = cursor.fetchone()
    results.extend(result)    
    
    connect.commit()
    connect.close() 
#     print(results)
    return results

def create_graph():
    males = get_males()
    females = get_females()

    fig, ax = plot.subplots()
    index = np.arange(0, origins)
    bar_width = 0.35
    opacity = 0.7

    male_bar = plot.bar(index, males, bar_width,
                      alpha=opacity,
                      color='blue',
                      label='Males')

    female_bar = plot.bar(index + bar_width, females, bar_width,
                     alpha=opacity,
                     color='pink',
                     label='Females')

    game_titles = get_origins()
    
    plot.ylabel('Number of each')
    plot.title('Male and Female characters across Final Fantasy')
    plot.xticks(index + bar_width, game_titles, rotation='vertical')
    plot.style.use('seaborn-paper')
    plot.legend()
    plot.tight_layout()
    plot.show(block=False)
    mooglepy = os.path.expanduser("~/desktop/mooglepy")
    os.chdir(mooglepy)
    fig.savefig("mooglepy.png")

def clear_screen(): 
    if name == 'nt': 
        _ = system('cls') 
  
    else: 
        _ = system('clear')

def main():
    setup()
    
    totals = data_frame['gender'].value_counts()
#     print('Males: ' + str(totals[0]))
#     print('Females: ' + str(totals[1]))
#     print('Unknown: ' + str(totals[2]))
    total_males = str(totals[0])
    total_females = str(totals[1])
    total_unknown = str(totals[2])
    create_database()
    create_graph()
    clear_screen()
    print("\n")
    print("Final Fantasy began back in 1987 and grown and expanded across many iterations and spinoffs. This data comes from my own API and is incomplete.")
    print("But I'm looking at the ratio of male to female characters across the data I've compiled.")
    print('There are a total of ' + total_males + ' male characters and ' + total_females + ' female characters.')
    print('Additionally, there are ' + total_unknown + ' unknown character genders across the Final Fantasy game data I have collected.')
    print("\nYour mooglepy.db and mooglepy.png have been output to a directory on your desktop called mooglepy.")
    print("\n")

if __name__ == "__main__":
    main()
