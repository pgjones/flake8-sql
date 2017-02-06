query = """INSERT INTO tbl (clm1, clm2)
                VALUES (val1, val2),
                       (val3, val4); SELECT clm
                                       FROM tbl;"""  # Q446
query = """INSERT INTO tbl (clm1, clm2)
                VALUES (val1, val2),
                       (val3, val4);
                SELECT clm
                  FROM tbl;"""
