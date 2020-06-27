tbl = "tbl"
query = f"SELECT ca,cb FROM {tbl}"  # Q443
query = f"""SELECT abc
            FROM   {tbl}
            WHERE  def = 'def'"""  # Q447
query = f"""SELECT abc
              FROM {tbl}
             WHERE def = 'def'"""
