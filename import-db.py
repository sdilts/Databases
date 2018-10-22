#!/usr/bin/python3

import sqlite3, sys
from enum import Enum
from pathlib import PurePath

class DBType(Enum):
    integer = 1
    text = 2
    boolean = 3
    enumeration = 4
    key = 5
    values = 6
    real = 7

def convert_string(string, strtype):
    if string == '\\N':
        return None
    elif strtype == DBType.integer:
        return int(string)
    elif strtype == DBType.text:
        return string
    elif strtype == DBType.boolean:
        return string == '1'
    elif strtype == DBType.enumeration:
        return string
    elif strtype == DBType.key:
        # each key has a two char prefix:
        return int(string[2:])
    elif strtype == DBType.values:
        return string.split(',')
    elif strtype == DBType.real:
        return float(string)
    else:
        raise ValueError("Unknown DBType")

def get_index(arr, index):
    if len(arr) > index+1:
        return arr[index]
    else:
        return None

def define_column_reader(header,type_dict):
    def read_func(line):
        line_dict = dict()
        values = line.strip().split('\t')
        assert(len(values) == len(header))
        for colname,value in zip(header, values):
            line_dict[colname] = convert_string(value,type_dict[colname])
        return line_dict

    return read_func

type_dict = dict()
# title table:
type_dict['tconst'] = DBType.key
type_dict['titleType'] =  DBType.enumeration
type_dict['primaryTitle'] =   DBType.text
type_dict['originalTitle'] =  DBType.text
type_dict['isAdult'] =  DBType.boolean
type_dict['startYear'] =  DBType.text
type_dict['endYear'] =  DBType.text
type_dict['runtimeMinutes'] =  DBType.integer
type_dict['genres'] =  DBType.values
# person table:
type_dict['nconst'] = DBType.key
type_dict['primaryName'] = DBType.text
type_dict['birthYear'] = DBType.text
type_dict['deathYear'] = DBType.text
type_dict['primaryProfession'] = DBType.values
type_dict['knownForTitles'] = DBType.values
# new from title.crew.tsv
type_dict['directors'] = DBType.values
type_dict['writers'] = DBType.values
# new from title.episodes.tsv
type_dict['parentTconst'] = DBType.key
type_dict['seasonNumber'] = DBType.integer
type_dict['episodeNumber'] = DBType.integer
# new from akas.tsv
type_dict['titleId'] = DBType.key
type_dict['ordering'] = DBType.integer
type_dict['title'] = DBType.text
type_dict['region'] = DBType.text
type_dict['language'] = DBType.text
type_dict['types'] = DBType.values
type_dict['attributes'] = DBType.values
type_dict['isOriginalTitle'] = DBType.boolean
# new from title.principals.tsv
type_dict['category'] = DBType.text
type_dict['job'] = DBType.text
type_dict['characters'] = DBType.text
# new from title.ratings.tsv:
type_dict['averageRating'] = DBType.real
type_dict['numVotes'] = DBType.integer

def map_lines(file_name, insert_func):
    with open(file_name, 'r') as f:
        header = f.readline().strip().split('\t')
        row_reader = define_column_reader(header, type_dict)
        counter = 0
        for line in f:
            line_dict = row_reader(line)
            insert_func(line_dict)

def read_title(file_name, cursor):
    def insert_func(line_dict):
        cursor.execute("INSERT INTO Title (TitleID, RunTime, OriginalTitle, StartYear, EndYear, MediaType) VALUES (:tconst, :runtimeMinutes, :primaryTitle, :startYear, :endYear, :titleType)",
                       line_dict)
        if line_dict['genres'] != None:
            for genre in line_dict['genres']:
                cursor.execute("INSERT INTO TitleGenre VALUES (?, ?)", (line_dict['tconst'], genre))
    map_lines(file_name, insert_func)

def read_person(file_name, cursor):
    def insert_func(line_dict):
        profs = line_dict['primaryProfession']
        line_dict['prim1'] = profs[0]
        line_dict['prim2'] = get_index(profs, 1)
        line_dict['prim3'] = get_index(profs, 2)
        cursor.execute("INSERT INTO Person VALUES (:nconst, :primaryName, :birthYear, :deathYear, :prim1, :prim2, :prim3)",
                       line_dict)
        if line_dict['knownForTitles'] != None:
            personID = line_dict['nconst']
            for title in line_dict['knownForTitles']:
                cursor.execute("INSERT INTO KnownFor VALUES (?, ?)", (title,personID))

    map_lines(file_name, insert_func)

def read_crew(file_name, cursor):
    def insert(line_dict):
        titleID = line_dict['tconst']
        if line_dict['writers'] != None:
            for writer in line_dict['writers']:
                cursor.execute("INSERT INTO Wrote VALUES (?, ?)", (titleID, writer))
        if line_dict['directors'] != None:
            for director in line_dict['directors']:
                cursor.execute("INSERT INTO Directed VALUES (?, ?)",(titleID, director))
    map_lines(file_name, insert)

def read_episode(file_name, cursor):
    def insert(line_dict):
        cursor.execute("INSERT INTO EpisodeOf VALUES (:tconst, :parentTconst, :seasonNumber, :episodeNumber)",
                       line_dict)
    map_lines(file_name, insert)

def read_akas(file_name, cursor):
    def insert(line_dict):
        cursor.execute("INSERT INTO RegionInfo VALUES  (:titleId, :ordering, :region, :title, :language, :isOriginalTitle)",
                       line_dict)
    map_lines(file_name, insert)

def read_principals(file_name, cursor):
    def insert(line_dict):
        cursor.execute("INSERT INTO PrincipalIn VALUES (:tconst, :nconst, :ordering, :category, :job, :characters)",
                       line_dict)
    map_lines(file_name, insert)

def read_rating(file_name, cursor):
    def insert(line_dict):
        cursor.execute("INSERT INTO Rating (TitleID, AverageRating, VoteCount) VALUES (:tconst, :averageRating, :numVotes)",
                       line_dict)
    map_lines(file_name, insert)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error: please specify the data directory and the path to the db file.")
        print("\tUsage: import-db.py data-dir db-file-path")
        exit()

    import_file_path = PurePath(sys.argv[1])
    db_file_path = PurePath(sys.argv[2])

    conn = sqlite3.connect('imbd.db')
    cursor = conn.cursor()

    print("Loading data from title.basics.tsv")
    read_title(import_file_path / "title.basics.tsv", cursor)
    print("Loading data from name.basics.tsv")
    read_person(import_file_path / "name.basics.tsv", cursor)
    print("Loading data from title.crew.tsv")
    read_crew(import_file_path / "title.crew.tsv", cursor)
    print("Loading data from title.episode.tsv")
    read_episode(import_file_path / "title.episode.tsv", cursor)
    print("Loading data from title.akas.tsv")
    read_akas(import_file_path / "title.akas.tsv", cursor)
    print("Loading data from title.principals.tsv")
    read_principals(import_file_path / "title.principals.tsv", cursor)
    print("Loading data from title.ratings.tsv")
    read_rating(import_file_path / "title.principals.tsv", cusor)
    conn.commit()
