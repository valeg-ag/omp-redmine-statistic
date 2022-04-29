import sys
import re
import transfer_utils


def createTable_Issues(pgcur):
    if transfer_utils.isTableExists(pgcur, "time_entries"):
        pgcur.execute("DROP TABLE time_entries")
        print("'time_entries' table droped")

    pgcur.execute("""CREATE TABLE time_entries (
                        time_entry_id integer,
                        issue_id integer,
                        project_id integer,
                        user_id integer,
                        activity_id integer,
                        spent_on date,
                        hours numeric,
                        auto_cherry_pick integer,
                        manual_cherry_pick integer )
                   """)
    print("'time_entries' table created")

def migrate(pgcur, mysqlconn):
    createTable_Issues(pgcur)

    mysql_time_entries_cur = mysqlconn.cursor()
    mysql_revision_cur = mysqlconn.cursor()

    print("moving 'time_entries':")
    sys.stdout.write("\r%d%%" % 0)
    sys.stdout.flush()

    mysql_time_entries_cur.execute("select count(0) from time_entries")
    time_entries_count = mysql_time_entries_cur.fetchone()["count(0)"]

    mysql_revision_cur.execute("SELECT * FROM changesets")

    revision_comments = {}
    for row in mysql_revision_cur:
        revision_comments[row["revision"]] = row["comments"]

    mysql_time_entries_cur.execute("select * from time_entries order by id desc")

    i = 0
    for row in mysql_time_entries_cur:
        i += 1
        if i%1000 == 0:
            sys.stdout.write("\r%d%%" % int(i/time_entries_count*100))
            sys.stdout.flush()

        auto_cherry_pick = False
        manual_cherry_pick = False

        revisions = re.findall(r'commit:omp_git\|(\w+)', row["comments"])
        if len(revisions) > 0:
            if revisions[0] in revision_comments:
                rev_comment = revision_comments[revisions[0]]

                auto_cherry_pick = len(re.findall(r'\[int\] *[Дд]окрутка +в +(\w+) *\[/int\]', rev_comment)) > 0
                if not auto_cherry_pick:
                    manual_cherry_pick = len(re.findall(r'\[int\] *[Рр]учная *[Дд]окрутка +в +(\w+) *\[/int\]', rev_comment)) > 0

        pgcur.execute("""INSERT INTO time_entries(
                             time_entry_id,
                             issue_id,
                             project_id,
                             user_id,
                             activity_id,
                             spent_on,
                             hours,
                             auto_cherry_pick,
                             manual_cherry_pick )
                             values(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                             (row["id"], row["issue_id"], row["project_id"], row["user_id"], row["activity_id"],
                              row["spent_on"], row["hours"],
                              1 if auto_cherry_pick else 0,
                              1 if manual_cherry_pick else 0,))

    sys.stdout.write("\r100%")
    sys.stdout.flush()

    print()
    print( str(time_entries_count) + " time entries was moved to postgresq")

    mysql_time_entries_cur.close()
    mysql_revision_cur.close()
