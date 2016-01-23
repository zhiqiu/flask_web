import MySQLdb
import sys 

db = MySQLdb.connect(host="localhost",user="root",passwd="1340830",db="flask",charset="utf8" )
cursor = db.cursor()
sql = "select * from user"
cursor.execute(sql)
res = cursor.fetchall()

reload(sys)
sys.setdefaultencoding('utf-8')

for row in res:
    print row[0], isinstance(row[1],str), row[1].decode('utf-8')
