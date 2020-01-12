query = """select clmn
             FROM tbl"""  # Q440
query = """SELECT clmn
             FROM tbl"""
query = "insert INTO tbl values vl"  # Q440
query = "INSERT INTO tbl VALUES vl"
query = "delete from tbl"  # Q440
query = "DELETE FROM tbl"
query = "update tbl set clmn = x"  # Q440
query = "UPDATE tbl SET clmn = x"
qyart = "UPDATE tbl SET EXTRACT(abc from xyz)"  # Q440
