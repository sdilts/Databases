#!/usr/bin/python3
import sqlite3, sys
from enum import Enum
from pathlib import PurePath

def map_lines(filename, func):
    with open(filename, 'r') as f:
        header = f.readline()
        for line in f:
            func(line.strip())

def parse_string(iterator):
    accumulator = []
    ret_list = []
    cur = next(iterator)
    while(cur != '"'):
        if cur == "\\":
            accumulator.append(next(iterator))
        else:
            accumulator.append(cur)
        cur = next(iterator)
    return "".join(accumulator)

def parse_list(string):
    accumulator = []
    ret_list = []
    iterator = iter(string)
    cur = next(iterator, None)
    while(cur != None):
        if cur == ',':
            ret_list.append("".join(accumulator))
            accumulator.clear()
        elif cur == '"':
            accumulator.clear()
            ret_list.append(parse_string(iterator))
            # read the comma that is theoretically after the string:
            tmp = next(iterator,None)
            while(tmp != ',' and tmp != None):
                tmp = next(iterator,None)
        else:
            accumulator.append(cur)
        cur = next(iterator,None)

    ret_list.append("".join(accumulator))
    return ret_list

def to_number(value, func):
    if value == '':
        return None
    else:
        return func(value)

def extract_values(string):
    columns = parse_list(string)
    column_dict = dict()
    column_dict['rank'] = int(columns[0])
    column_dict['title'] = columns[1]
    column_dict['Genre'] = parse_list(columns[2])
    column_dict['description'] = columns[3]
    column_dict['Director'] = columns[4]
    column_dict['actors'] = parse_list(columns[5])
    column_dict['year'] = to_number(columns[6], int)
    column_dict['runtime'] = to_number(columns[7], int)
    column_dict['rating'] = to_number(columns[8], float)
    column_dict['votes'] = to_number(columns[9], int)
    column_dict['revenue'] = to_number(columns[10], float)
    column_dict['metaScore'] = to_number(columns[11], float)
    return column_dict


def get_rows(cursor):
    desc = cursor.description
    column_names = [col[0] for col in desc]
    return [dict(zip(column_names, row))
            for row in cursor.fetchall()]

def get_title_info(movie_dict, cursor):
    cursor.execute("SELECT * FROM Title WHERE OriginalTitle = :title and MediaType = 'movie' and StartYear = :year and RunTime = :runtime",
                   movie_dict)
    rows = get_rows(cursor)
    assert(len(rows) == 1 or len(rows) == 0)
    if len(rows) == 0:
        return None
    else:
        return rows[0]

def update_info(title_info, columns, cursor):
    # update the title:
    cursor.execute("UPDATE Title SET Description=? WHERE TitleID = ?",
                   (columns['description'],title_info['TitleID']))
    cursor.execute("UPDATE Rating SET MetaScore=? and Revenue=? WHERE TitleID = ?",
                   (columns['metaScore'], columns['revenue'], title_info['TitleID']))

def add_info(columns, cursor):
    cursor.execute("INSERT INTO Title (RunTime, OriginalTitle, StartYear, MediaType) VALUES (:runtime, :title, :year, 'movie')", columns)
    cursor.connection.commit()
    title_info = get_title_info(columns, cursor)
    assert(title_info != None)
    cursor.execute("INSERT INTO Rating (:title :rating :votes :metaScore :revenue)",
                   columns)


jobs = [("IMDB-Movie-Data.csv", insert_line)]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error: please specify the data directory and the path to the db file.")
        print("\tUsage: import-db.py data-dir db-file-path")
        exit()

    import_file_path = PurePath(sys.argv[1])
    db_file = PurePath(sys.argv[2])

    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()

    def insert_line(line):
        columns = extract_values(line)
        print(columns['rank'])
        title_info = get_title_info(columns,cursor)
        if title_info == None:
            add_info(columns, cursor)
        # else:
        #     update_info(title_info,columns, cursor)
        conn.commit()

    for filename, func in jobs:
        map_lines(import_file_path / filename, func)
