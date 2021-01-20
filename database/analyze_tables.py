#!/usr/local/bin/python3.6
import os
import time 
import subprocess
from mysql.connector import connect, Error 

# ------------------------------------
# Analyze and Optimize tables MySQL.
#

Host_DB='localhost'
DB_name=''
User='root'
Password=''

connection = connect(host='localhost', database='',user='root',password='')

cursor = connection.cursor()
records = "show tables;"
cursor.execute(records)
tables = cursor.fetchall()

def analyze_optimize(sw):
    start_time = time.strftime('%Y_%m_%d-%H:%M:%S')

    cwd = os.getcwd()
    log_name = 'analyze_optimize_tables.txt'
    file_log = cwd + "/" + log_name

    os.system('echo "%s tables ... starting: %s " > %s ' % (sw,start_time,file_log))
    os.system('printf "\n" >> %s ' % file_log)

    for table in tables:
        table = ''.join(table)
        os.system('mysql -u%s -p%s %s -e " %s table %s ;  " >> %s   ' %(User,Password,DB_name,sw,table,file_log))
        os.system('printf "\n" >> %s ' % file_log)
        time.sleep(1)

    os.system('printf "\n" >> %s ' % file_log)
    end_time = time.strftime('%Y_%m_%d-%H:%M:%S')
    os.system('echo "%s tables ... Ending: %s " >> %s ' % (sw,end_time,file_log))


if __name__ == "__main__":
    i = int(input("""
    Please input 1 or 2 for starting script ...
    1) Analyze.
    2) Optimize. 
    """))

    if i == 1:
        analyze_optimize(sw='analyze')
        cursor.close()
        connection.close()
    elif i == 2:
        analyze_optimize(sw='optimize')
        cursor.close()
        connection.close()
    else:
        print("Just input 1 or 2 ")
        cursor.close()
        connection.close()
        exit

