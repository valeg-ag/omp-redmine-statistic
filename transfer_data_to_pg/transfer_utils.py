

def isTableExists(pgcur, tableName):
    pgcur.execute("""SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                         WHERE table_schema = 'public'
                           AND table_name   = %(table)s)
                  """, {"table": tableName})

    records = pgcur.fetchall()
    return records[0][0]
