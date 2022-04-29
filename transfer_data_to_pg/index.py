import os
from dotenv import load_dotenv
import psycopg2
import pymysql
from pymysql.cursors import DictCursor
import transfer_issues_to_pg
import transfer_time_entries_to_pg

if __name__ == "__main__":
    load_dotenv(dotenv_path="./credentials/redmine_mysql.env")

    pgconn = psycopg2.connect(dbname='durationsdb', user='pguser', password='pgpass', host='localhost')
    pgcur = pgconn.cursor()
    
    mysqlconn = pymysql.connect(
        host='192.168.222.48', port=3306,
        user=os.environ.get('redmine_mysql_user'), password=os.environ.get('redmine_mysql_password'),
        db='redmine',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    mysqlcur = mysqlconn.cursor()

    transfer_issues_to_pg.migrate(pgcur, mysqlcur)
    pgconn.commit()

    transfer_time_entries_to_pg.migrate(pgcur, mysqlconn)
    pgconn.commit()

    pgcur.close()
    pgconn.close()
    mysqlcur.close()
    mysqlconn.close()
