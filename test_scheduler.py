import schedule
import sqlite3
import pandas as pd
import gzip
import csv
from datetime import datetime


def job():

    csv_name = 'db' + datetime.today().strftime('%Y-%m-%d')
    txt_name = 'db' + datetime.today().strftime('%Y-%m-%d')
    conn = sqlite3.connect('test.db', isolation_level=None,
                           detect_types=sqlite3.PARSE_COLNAMES)
    db_df = pd.read_sql_query("SELECT * FROM mock_data", conn)
    db_df.to_csv('csv/' + csv_name + '.csv', index=False)

    with open(txt_name + '.txt', "w") as my_output_file:
        with open('csv/' + csv_name + '.csv', "r") as my_input_file:
            [my_output_file.write(" ".join(row)+'\n')
             for row in csv.reader(my_input_file)]
        my_output_file.close()

    with open(txt_name + '.txt', 'rb') as orig_file:
        with gzip.open(txt_name + ".txt.gz", 'wb') as zipped_file:
            zipped_file.writelines(orig_file)


schedule.every(10).seconds.do(job)
while True:
    schedule.run_pending()
# ini semua ntar dimasukin ke sebuah function trus dijalanin sebagai sebuah job dengan interval berapa menit
