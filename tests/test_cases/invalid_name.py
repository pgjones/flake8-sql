query = "SELECT aColumn FROM tbl"  # Q441
query = "SELECT a_column FROM tbl"
query = "INSERT INTO tbl VALUES SOMETHING"  # Q441
query = "INSERT INTO tbl VALUES something"
query = "SELECT invalid_ FROM tbl"  # Q441
