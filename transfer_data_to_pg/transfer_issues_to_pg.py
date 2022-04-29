import sys
import transfer_utils


def createTable_Issues(pgcur):
    if transfer_utils.isTableExists(pgcur, "issues"):
        pgcur.execute("DROP TABLE issues")
        print("'issues' table droped")

    pgcur.execute("""CREATE TABLE issues (
                        issue_id integer,
                        project_id integer,
                        tracker_id integer,
                        status_id integer,
                        priority_id integer,
                        author_id integer,
                        assigned_to_id integer,
                        subject character varying,
                        done_ratio numeric,
                        estimated_hours numeric,
                        created_on date,
                        closed_on date )
                   """)
    print("'issues' table created")

def migrate(pgcur, mysqlcur):
    createTable_Issues(pgcur)

    mysqlcur.execute("select count(0) from issues")
    issues_count = mysqlcur.fetchone()["count(0)"]

    print("moving 'issues':")
    sys.stdout.write("\r%d%%" % 0)
    sys.stdout.flush()

    mysqlcur.execute("select * from issues order by id desc")

    i = 0
    for row in mysqlcur:
        i += 1
        if i%1000 == 0:
            sys.stdout.write("\r%d%%" % int(i/issues_count*100))
            sys.stdout.flush()

        pgcur.execute("""INSERT INTO issues(
                             issue_id,
                             project_id,
                             tracker_id,
                             status_id,
                             priority_id,
                             author_id,
                             assigned_to_id,
                             subject,
                             done_ratio,
                             estimated_hours,
                             created_on,
                             closed_on )
                             values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                             (row["id"], row["project_id"], row["tracker_id"], None, None, row["author_id"],
                              row["assigned_to_id"], row["subject"], 0.0, row["estimated_hours"],
                              row["created_on"], row["closed_on"],))

    sys.stdout.write("\r100%")
    sys.stdout.flush()

    print()
    print( str(issues_count) + " issues was moved to postgresq")
