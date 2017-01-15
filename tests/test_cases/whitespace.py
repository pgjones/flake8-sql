query = "SELECT ca,cb FROM tbl"  # Q443
query = "SELECT ca ,cb FROM tbl"  # Q443
query = "SELECT ca, cb FROM tbl"
query = "SELECT ca FROM tbl WHERE ca= 'b'"  # Q444
query = "SELECT ca FROM tbl WHERE ca ='b'"  # Q444
query = "SELECT ca FROM tbl WHERE ca = 'b'"
query = "SELECT ca FROM tbl WHERE ca != 'b'"
