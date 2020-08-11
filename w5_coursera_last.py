"""
Project for Week 4 of "Python Data Analysis".
Processing CSV files with baseball stastics.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import numpy as np
##
## Provided code from Week 3 Project
##

info = {"masterfile": "Master_2016.csv",   # Name of Master CSV file
                    "battingfile": "Batting_2016.csv", # Name of Batting CSV file
                    "separator": ",",                  # Separator character in CSV files
                    "quote": '"',                      # Quote character in CSV files
                    "playerid": "playerID",            # Player ID field name
                    "firstname": "nameFirst",          # First name field name
                    "lastname": "nameLast",            # Last name field name
                    "yearid": "yearID",                # Year field name
                    "atbats": "AB",                    # At bats field name
                    "hits": "H",                       # Hits field name
                    "doubles": "2B",                   # Doubles field name
                    "triples": "3B",                   # Triples field name
                    "homeruns": "HR",                  # Home runs field name
                    "walks": "BB",                     # Walks field name
                    "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]}

def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    table = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            table.append(row)
    return table


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table

##
## Provided formulas for common batting statistics
##

# Typical cutoff used for official statistics
MINIMUM_AB = 500

def batting_average(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the batting average as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return hits / at_bats
    else:
        return 0

def onbase_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the on-base percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    walks = float(batting_stats[info["walks"]])
    if at_bats >= MINIMUM_AB:
        return (hits + walks) / (at_bats + walks)
    else:
        return 0

def slugging_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the slugging percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    doubles = float(batting_stats[info["doubles"]])
    triples = float(batting_stats[info["triples"]])
    home_runs = float(batting_stats[info["homeruns"]])
    singles = hits - doubles - triples - home_runs
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return (singles + 2 * doubles + 3 * triples + 4 * home_runs) / at_bats
    else:
        return 0


##
## Part 1: Functions to compute top batting statistics by year
##

def filter_by_year(statistics, year, yearid):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      year       - Year to filter by
      yearid     - Year ID field in statistics
    Outputs:
      Returns a list of batting statistics dictionaries that
      are from the input year.
    """
    out=[]
    for i in range(len(statistics)):
        if statistics[i][yearid] == str(year): out.append(statistics[i])

    return out

filename = 'batting1.csv'
keyfield = 'year'
separator = ','
quote = '"'
statistics = read_csv_as_list_dict(filename, separator, quote)

year = 2020
out1 = filter_by_year(statistics, year, 'year')


def top_player_ids(info, statistics, formula, numplayers):
    """
    Inputs:
      info       - Baseball data information dictionary
      statistics - List of batting statistics dictionaries
      formula    - function that takes an info dictionary and a
                   batting statistics dictionary as input and
                   computes a compound statistic
      numplayers - Number of top players to return
    Outputs:
      Returns a list of tuples, player ID and compound statistic
      computed by formula, of the top numplayers players sorted in
      decreasing order of the computed statistic.
    """
    
    # np.nan
    # np.zeros로 preallocation
    # np.argsort로 sorting
    # list(dictype.keys())
    # np.argsort(career.values())[::-1]
    # compute_top_stats_career는 모든 데이터의 합으로 정의하겠음
    
    score = np.zeros(len(statistics)) * np.nan
    for i in range(len(statistics)):
        score[i] = (formula(info, statistics[i]))
    
    rix = np.argsort(score)[::-1][:numplayers]
    out = []
    for i in rix:
        out.append((statistics[i]['playerID'], score[i]))
    
    return out

info = info

filename = 'batting2.csv'
keyfield = 'year'
separator = ','
quote = '"'
statistics = read_csv_as_list_dict(filename, separator, quote)

formula = slugging_percentage
numplayers = 2

top_player_ids(info, statistics, formula, numplayers)

def lookup_player_names(info, top_ids_and_stats):
    """
    Inputs:
      info              - Baseball data information dictionary
      top_ids_and_stats - list of tuples containing player IDs and
                          computed statistics
    Outputs:
      List of strings of the form "x.xxx --- FirstName LastName",
      where "x.xxx" is a string conversion of the float stat in
      the input and "FirstName LastName" is the name of the player
      corresponding to the player ID in the input.
    """
    out = None
    for i in range(len(top_ids_and_stats)):
        msid = top_ids_and_stats[i][0]
        score_tmp = top_ids_and_stats[i][1]
        for j in range(len(master)):
            if master[j]['playerID'] == msid:
                out = str(round(score_tmp,3)) + ' --- ' + \
                master[j]['nameFirst'] + ' ' + master[j]['nameLast']
                break

    return out

filename = 'batting2.csv'
keyfield = 'year'
separator = ','
quote = '"'
statistics = read_csv_as_list_dict(filename, separator, quote)
formula = slugging_percentage
numplayers = 2
top_ids_and_stats = top_player_ids(info, statistics, formula, numplayers)

filename = 'master2.csv'
keyfield = 'year'
separator = ','
quote = '"'
master = read_csv_as_list_dict(filename, separator, quote)

lookup_player_names(info, top_ids_and_stats)

def compute_top_stats_year(info, formula, numplayers, year):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
      year        - Year to filter by
    Outputs:
      Returns a list of strings for the top numplayers in the given year
      according to the given formula.
    """
    statistics_filtered = filter_by_year(statistics, year, yearid)
    out = top_player_ids(info, statistics_filtered, formula, numplayers)
    
    # return이 탑 플레이어의 뭘 달라는건지? ID만 달라는것 같은데 걍 tuple로 둠.
    
    return out

filename = 'batting3.csv'
keyfield = 'playerID'
separator = ','
quote = '"'
statistics = read_csv_as_list_dict(filename, separator, quote)

yearid = 'yearID'

filename = 'master3.csv'
keyfield = 'year'
separator = ','
quote = '"'
master = read_csv_as_list_dict(filename, separator, quote)

formula = onbase_percentage
numplayers = 10
year = 2004
compute_top_stats_year(info, formula, numplayers, year)

##
## Part 2: Functions to compute top batting statistics by career
##

def aggregate_by_player_id(statistics, playerid, fields):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      playerid   - Player ID field name
      fields     - List of fields to aggregate
    Output:
      Returns a nested dictionary whose keys are player IDs and whose values
      are dictionaries of aggregated stats.  Only the fields from the fields
      input will be aggregated in the aggregated stats dictionaries.
    """
    out = {}
    for i in range(len(statistics)):
        row = statistics[i]
        mskeys = list(row.keys())
        nest = []
        for j in range(len(mskeys)):
            if mskeys[j] in fields:
                nest.append({mskeys[j] : row[mskeys[j]]})
            
        out[row[playerid]] = nest
    
    return out # nested dictionary가 정확히 list에 들어간 dict을 말하는건지는 잘 모르겠네요.

filename = 'batting4.csv'
playerid = 'playerID'
separator = ';'
quote = "'"
statistics = read_csv_as_list_dict(filename, separator, quote)

fields = ['teamID', 'G', 'AB', 'R', 'H', '3B'] 

aggregate_by_player_id(statistics, playerid, fields)


def compute_top_stats_career(info, formula, numplayers):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
    """
    playerid
    statistics
    
    career = {}
    for i in range(len(statistics)):
        value = formula(info, statistics[i])
        msid = statistics[i][playerid]
        
        if msid in list(career.keys()):
            career[msid] = career[msid] + value
        elif not(msid in list(career.keys())):
            career[msid] = value
            
    rix = np.argsort(list(career.values()))[::-1][:numplayers]
    
    out = []
    for i in rix: 
        out.append(list(career.keys())[i])
    return out


##
## Provided testing code
##

def test_baseball_statistics():
    """
    Simple testing code.
    """

    #
    # Dictionary containing information needed to access baseball statistics
    # This information is all tied to the format and contents of the CSV files
    #
    baseballdatainfo = {"masterfile": "Master_2016.csv",   # Name of Master CSV file
                        "battingfile": "Batting_2016.csv", # Name of Batting CSV file
                        "separator": ",",                  # Separator character in CSV files
                        "quote": '"',                      # Quote character in CSV files
                        "playerid": "playerID",            # Player ID field name
                        "firstname": "nameFirst",          # First name field name
                        "lastname": "nameLast",            # Last name field name
                        "yearid": "yearID",                # Year field name
                        "atbats": "AB",                    # At bats field name
                        "hits": "H",                       # Hits field name
                        "doubles": "2B",                   # Doubles field name
                        "triples": "3B",                   # Triples field name
                        "homeruns": "HR",                  # Home runs field name
                        "walks": "BB",                     # Walks field name
                        "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]}

    print("Top 5 batting averages in 1923")
    top_batting_average_1923 = compute_top_stats_year(baseballdatainfo, batting_average, 5, 1923)
    for player in top_batting_average_1923:
        print(player)
    print("")

    print("Top 10 batting averages in 2010")
    top_batting_average_2010 = compute_top_stats_year(baseballdatainfo, batting_average, 10, 2010)
    for player in top_batting_average_2010:
        print(player)
    print("")

    print("Top 10 on-base percentage in 2010")
    top_onbase_2010 = compute_top_stats_year(baseballdatainfo, onbase_percentage, 10, 2010)
    for player in top_onbase_2010:
        print(player)
    print("")

    print("Top 10 slugging percentage in 2010")
    top_slugging_2010 = compute_top_stats_year(baseballdatainfo, slugging_percentage, 10, 2010)
    for player in top_slugging_2010:
        print(player)
    print("")

    # You can also use lambdas for the formula
    #  This one computes onbase plus slugging percentage
    print("Top 10 OPS in 2010")
    top_ops_2010 = compute_top_stats_year(baseballdatainfo, \
                                          lambda info, stats: (onbase_percentage(info, stats) + slugging_percentage(info, stats)),
                                          10, 2010)
    for player in top_ops_2010:
        print(player)
    print("")

    print("Top 20 career batting averages")
    top_batting_average_career = compute_top_stats_career(baseballdatainfo, batting_average, 20)
    for player in top_batting_average_career:
        print(player)
    print("")


# Make sure the following call to test_baseball_statistics is
# commented out when submitting to OwlTest/CourseraTest.

yearid = 'yearID'

filename = 'Batting.csv'
separator = ','
quote = "'"
statistics = read_csv_as_list_dict(filename, separator, quote)

filename = 'Master.csv'
separator = ','
quote = "'"
master = read_csv_as_list_dict(filename, separator, quote)
test_baseball_statistics()
















    
    
