# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

"""
Project for Week 4 of "Python Data Analysis".
Processing CSV files with baseball stastics.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""
import csv

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
##
## Provided code from Week 3 Project
##

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
#csv파일 열어서 table에 list형식으로 저장

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
    yearlist = []
    for playerstat in statistics :
        if playerstat[yearid] == str(year) :
            yearlist.append(playerstat)
        else :
            pass
            
    return yearlist


#filename = 'batting1.csv'
#separator = ','
#quote = '"'
#statistics = read_csv_as_list_dict(filename, separator, quote)
#year = 2020
#print (filter_by_year(statistics, year, 'year'))

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

    idxscore = {}
    for i in range(len(statistics)) :
        idxscore[formula(info, statistics[i])] = i

#점수 값을 키로, 순서를 값으로 하는 dic생성
    score = []
    for i in range(len(statistics)) :
        score.append(formula(info, statistics[i]))
    score.sort(reverse=True)

#모든 선수들의 점수를 score에 넣고 정렬
    numscore = []
    for i in range(len(score)) :
        numscore.append(score[i])
        if i == numplayers - 1 :
            break
        else :
            pass

#numplayers숫자만큼 numscore에 상위권 선수들만의 점수 넣음
    playerscore = []
    for i in range(len(numscore)) :
        playerids = statistics[idxscore[numscore[i]]]['playerID']
        playerscore.append((playerids, score[i]))

    return playerscore

# In[]
info = info

filename = 'batting2.csv'
separator = ','
quote = '"'
statistics = read_csv_as_list_dict(filename, separator, quote)

formula = slugging_percentage
numplayers = 10

#print (top_player_ids(info, statistics, formula, numplayers))

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
    statname = []
    for idstat in top_ids_and_stats:
        for i in range(len(master)):
            if master[i][info['playerid']] == idstat[0]:
                statname.append(str(round(idstat[1],3)) + " --- " + master[i][info['firstname']] + " " + master[i][info['firstname']])
                break
            else :
                pass

    return statname

filename = 'batting2.csv'
separator = ','
quote = '"'
statistics = read_csv_as_list_dict(filename, separator, quote)
formula = slugging_percentage
numplayers = 10
top_ids_and_stats = top_player_ids(info, statistics, formula, numplayers)

filename = 'master2.csv'
separator = ','
quote = '"'
master = read_csv_as_list_dict(filename, separator, quote)

#print (lookup_player_names(info, top_ids_and_stats))

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

    yearplayer = []

    for i in range(len(statistics)):
        if statistics[i]['yearID'] == str(year):
            yearplayer.append(statistics[i])
        else:
            pass
    yearID = top_player_ids(info, yearplayer, formula, numplayers)
    out = lookup_player_names(info, yearID)
    
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
#print (compute_top_stats_year(info, formula, numplayers, year))
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

    nested = {}
    for i in range(len(statistics)):
            
        if statistics[i]['playerID'] in nested:
            for n in range(len(fields)):
                nested[statistics[i]['playerID']][fields[n]] += int(statistics[i][fields[n]])
        else:
            nested[statistics[i]['playerID']] = {}
            for n in range(len(fields)):
                nested[statistics[i]['playerID']][fields[n]] = int(statistics[i][fields[n]])
    return nested

filename = 'batting2.csv'
playerid = 'playerID'
separator = ','
quote = "'"
statistics = read_csv_as_list_dict(filename, separator, quote)
fields = ['G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO'] 

#print (aggregate_by_player_id(statistics, playerid, fields))
                       
def compute_top_stats_career(info, formula, numplayers):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
    """
    statistics
    playerid = info['playerid']
    fields
    nested = aggregate_by_player_id(statistics, playerid, fields)
    playerlist = []
    for key in aggregate_by_player_id(statistics, playerid, fields).keys():
        playerlist.append(key)
    playerstatlist = []

    print ("")

        
    for i in range(len(nested)):
        playercareer = {}     
        playercareer['playerID'] = playerlist[i]
        playercareer.update(nested[playerlist[i]])
        playerstatlist.append(playercareer)

    out = lookup_player_names(info, top_player_ids(info, playerstatlist, formula, numplayers))
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
    baseballdatainfo = info

    print("Top 5 batting averages in 2005")
    top_batting_average_2005 = compute_top_stats_year(baseballdatainfo, batting_average, 5, 2005)
    for player in top_batting_average_2005:    
        print(player)
    print("")

    print("Top 5 batting averages in 2003")
    top_batting_average_2003 = compute_top_stats_year(baseballdatainfo, batting_average, 5, 2003)
    for player in top_batting_average_2003:
        print(player)
    print("")
        
    print("Top 5 on-base percentage in 2006")
    top_onbase_2006 = compute_top_stats_year(baseballdatainfo, onbase_percentage, 5, 2006)
    for player in top_onbase_2006:
        print(player)
    print("")
            
    print("Top 5 slugging percentage in 2005")
    top_slugging_2005 = compute_top_stats_year(baseballdatainfo, slugging_percentage, 5, 2005)
    for player in top_slugging_2005:
        print(player)
    print("")
                
    # You can also use lambdas for the formula
    #  This one computes onbase plus slugging percentage
    print("Top 2 OPS in 2006")
    top_ops_2006 = compute_top_stats_year(baseballdatainfo,
                                          lambda info, stats: (onbase_percentage(info, stats) + slugging_percentage(info, stats)),
                                          2, 2006)
    for player in top_ops_2006:
        print(player)
    print("")

    print("Top 10 career batting averages")
    top_batting_average_career = compute_top_stats_career(baseballdatainfo, batting_average, 10)
    for player in top_batting_average_career:
        print(player)
    print("")
        

# Make sure the following call to test_baseball_statistics is
# commented out when submitting to OwlTest/CourseraTest.

#test_baseball_statistics()
# In[]
yearid = 'yearID'

filename = 'batting2.csv'
separator = ','
quote = "'"
statistics = read_csv_as_list_dict(filename, separator, quote)

filename = 'master2.csv'
separator = ','
quote = "'"
master = read_csv_as_list_dict(filename, separator, quote)

test_baseball_statistics()


# In[]

yearid = 'yearID'

filename = 'batting3.csv'
separator = ','
quote = '"'
statistics = read_csv_as_list_dict(filename, separator, quote)

filename = 'master3.csv'
separator = ','
quote = '"'
master = read_csv_as_list_dict(filename, separator, quote)

test_baseball_statistics()


# In[]
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

    yearplayer = []

    for i in range(len(statistics)):
        if statistics[i][info['yearid']] == str(year):
            yearplayer.append(statistics[i])
        else:
            pass
    yearID = top_player_ids(info, yearplayer, formula, numplayers)
    out = lookup_player_names(info, yearID)
    
    return out

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
    
    print('eeee')
    print(playerid, fields)

    nested = {}
    for i in range(len(statistics)):
            
        if statistics[i][info['playerid']] in nested:
            for n in range(len(fields)):
                nested[statistics[i][info['playerid']]][fields[n]] += int(statistics[i][fields[n]])
        else:
            nested[statistics[i][info['playerid']]] = {}
            for n in range(len(fields)):
                nested[statistics[i][info['playerid']]][fields[n]] = int(statistics[i][fields[n]])
    return nested


info = {"masterfile": "Master_2016.csv",   # Name of Master CSV file
                        "battingfile": "Batting_2016.csv", # Name of Batting CSV file
                        "separator": ",",                  # Separator character in CSV files
                        "quote": '"',                      # Quote character in CSV files
                        "playerid": "player",            # Player ID field name
                        "firstname": "firstname",          # First name field name
                        "lastname": "lastname",            # Last name field name
                        "yearid": "year",                # Year field name
                        "atbats": "atbats",                    # At bats field name
                        "hits": "hits",                       # Hits field name
                        "doubles": "2B",                   # Doubles field name
                        "triples": "3B",                   # Triples field name
                        "homeruns": "HR",                  # Home runs field name
                        "walks": "BB",                     # Walks field name
                        "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]}



filename = 'batting1.csv'
separator = ','
quote = '"'
statistics = read_csv_as_list_dict(filename, separator, quote)

filename = 'master1.csv'
separator = ','
quote = '"'
master = read_csv_as_list_dict(filename, separator, quote)

fields = ['atbats', 'hits'] 
test_baseball_statistics()















