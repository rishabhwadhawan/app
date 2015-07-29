import sys
import psycopg2

lat1 = float(sys.argv[1]);
long1 = float(sys.argv[2]);

lat2 = float(sys.argv[3]);
long2 = float(sys.argv[4]);

dbname = "authorslocation"
user = "postgres"
password = "data"

def getopenconnection():
    return psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='localhost' password='" + password + "'")

if __name__ == '__main__':
    conn = getopenconnection()

    cur = conn.cursor()

    cur.execute("SELECT * FROM vldb;")
    values = cur.fetchall()
    
    for value in values:
    	latitude = value[2]
    	longitude = value [3]
    	
    	if (lat1 <= latitude and lat2 >= latitude) or (lat2 <= latitude and lat1 >= latitude):
    		if (long1 <= longitude and long2 >= longitude) or (long2 <= longitude and long1 >= longitude):
				
				temp = [latitude,longitude]
				
				print (temp)	
conn.close()

