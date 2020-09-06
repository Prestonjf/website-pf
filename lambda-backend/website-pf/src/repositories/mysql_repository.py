# MySQL Services.
import mysql.connector

def query():
    cnx = mysql.connector.connect(host='', database='website-pf', user='', password='')
    cursor = cnx.cursor()

    query = ("SELECT * FROM post ")

    cursor.execute(query)

    for (post_name ) in cursor:
        print("{}".format(post_name))

    cursor.close()
    cnx.close()
    return 3