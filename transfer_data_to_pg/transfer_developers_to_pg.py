import transfer_utils

def createTable_Developers(pgcur):
    if transfer_utils.isTableExists(pgcur, "developers"):
        pgcur.execute("DROP TABLE developers")
        print("'developers' table droped")

    pgcur.execute("""CREATE TABLE developers (
                        id integer,
                        login character varying,
                        firstname character varying,
                        lastname character varying )
                   """)
    print("'developers' table created")

def migrate(pgcur, mysqlcur):
    createTable_Developers(pgcur)

    allDevelopers = [(12, "AVS"),
        (23,"SSB"),
        (26, "GDY"),
        (27, "DVU"),
        (29, "SPS"),
        (31, "KOV"),
        (38, "PMG"),
        (39, "GVI"),
        (52, "DMY"),
        (57, "DAP"),
        (96, "KOM"),
        (105, "PVI"),
        (109, "KSA"),
        (112, "FPA"),
        (119, "KPA"),
        (123, "SAV"),
        (125, "ASP"),
        (126, "BEA"),
        (131, "CHIG"),
        (135, "REI"),
        (134, "KAD"),
        (140, "BIV"),
        (146, "MID"),
        (149, "GIY"),
        (167, "SDS"),
        (174, "ADP"),
    ]

    for dev in allDevelopers:
        firstname = None
        lastname = None
        
        mysqlcur.execute("select id, login, firstname, lastname from users where id = %s", dev[0])
        redmineUser = mysqlcur.fetchone()
        if redmineUser:
            firstname = redmineUser["firstname"]
            lastname = redmineUser["lastname"]

        pgcur.execute("""INSERT INTO developers(id, login, firstname, lastname) values(%s, %s, %s, %s)""", (dev[0], dev[1], firstname, lastname))

    print("all developers were moved to postgresq")
