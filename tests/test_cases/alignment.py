query = """SELECT abc
           FROM   xyz
           WHERE  def = 'def'"""  # Q447
query = """SELECT abc
             FROM xyz
            WHERE def = 'def'
         ORDER BY abc"""
query = """SELECT abc
             FROM xyz
            WHERE def = 'def' AND feg = 'feg'"""  # Q447
query = """SELECT abc
             FROM xyz
  LEFT OUTER JOIN ijk ON abc.id = ijk.id"""
query = """SELECT abc
             FROM xyz
            WHERE def = 'def'
              AND feg = 'feg'
               OR ijk = 'ijk'"""
query = """INSERT INTO xyz (clm1, clm2)
                 VALUES (abc, def)"""  # Q447
query = """INSERT INTO xyz (clm1, clm2)
                VALUES (abc, def)
              RETURNING id"""  # Q447
query = """INSERT INTO xyz (clm1, clm2)
                VALUES (abc, def)"""
query = """INSERT INTO xyz (clm1, clm2)
                       SELECT abc
                       FROM def"""  # Q447
query = """SELECT abc
             FROM xyz
           JOIN   ghj ON jkl = def
            WHERE def = 'def'"""  # Q447
query = """SELECT abc,
def
             FROM xyz"""  # Q449
query = """SELECT abc,
                  def
             FROM xyz"""
query = """SELECT abc
             FROM xyz
            WHERE abc >= EXTRACT(abc FROM xyz.def)"""
