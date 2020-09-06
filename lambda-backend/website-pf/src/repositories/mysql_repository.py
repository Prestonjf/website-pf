# MySQL Services
import mysql.connector

def query():
    cnx = mysql.connector.connect(host='ip-172-31-88-223.ec2.internal', database='website-pf', user='website-pf-user', password='Web21!epfW')
    cursor = cnx.cursor()

    query = ("SELECT * FROM post ")

    cursor.execute(query)

    for (post_name ) in cursor:
        print("{}".format(post_name))

    cursor.close()
    cnx.close()
    return 3