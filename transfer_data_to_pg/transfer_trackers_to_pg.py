import transfer_utils

def createTable_Trackers(pgcur):
    if transfer_utils.isTableExists(pgcur, "trackers"):
        pgcur.execute("DROP TABLE trackers")
        print("'trackers' table droped")

    pgcur.execute("""CREATE TABLE trackers (
                        id integer,
                        name character varying )
                   """)
    print("'trackers' table created")

def migrate(pgcur, mysqlcur):
    createTable_Trackers(pgcur)

    mysqlcur.execute("select * from trackers")

    for row in mysqlcur:
        pgcur.execute("""INSERT INTO trackers(id, name) values(%s, %s)""", (row["id"], row["name"],))

    print("all trackers were moved to postgresq")
