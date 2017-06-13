import MySQLdb
db = MySQLdb.connect("192.168.1.220","root","Asd@1234","ansible_tools" )
cursor = db.cursor()
cursor.execute("SELECT * from ansible_test")
data = cursor.fetchone()
print "Database version : %s " % data
db.close()