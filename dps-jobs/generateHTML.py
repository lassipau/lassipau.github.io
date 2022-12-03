import sqlite3
from sqlite3 import Error
from datetime import date


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)



def create_position(conn, position):
    """
    Create a new position
    :param conn:
    :param position:
    :return:
    """

    sql = ''' INSERT INTO positions(PositionType,University,UniversityLink,Department,DepartmentLink,DeadlineText,DeadlineDate,Description,ContactInfo,AnnouncementLink,AnnouncementDate)
              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, position)
    conn.commit()

    return cur.lastrowid
def write_position_html(row,f):
    """ 
    Write the html source code for a single position
    :param row: The record for one position, a tuple
    :param f: The open file stream
    :return:
    """

    f.write("<p>\n")
    #f.write("Type: " + row[0] +" <br>\n")
    #f.write("University: " + row[1] +" <br>\n")

    f.write("<b>ID:</b> DPS-Job-%s<br>\n" % row[11]) 
    f.write("<b>Position:</b> %s <br>\n" % row[0])
    f.write("<b>University:</b> <a href=\"%s\">%s</a><br>\n" % (row[1],row[2]))
    f.write("<b>Department:</b> <a href=\"%s\">%s</a><br>\n" % (row[3],row[4]))
    f.write("<b>Deadline:</b> %s <br>\n" % row[5])
    f.write("<b>Description:</b> %s <br>\n" % row[7])
    f.write("<b>Contact:</b> %s <br>\n" % row[8])
    f.write("<b>Announcement:</b> <a href=\"%s\">Application information</a><br>\n" % row[9])
    #<b>Position:</b> Professor <br>
    #<b>University:</b> <a href="https://tuni.fi">TAU</a><br>
    #<b>Department:</b> Mathematics <br>
    #<b>Deadline:</b> October 1st, 2022<br>
    #<b>Description:</b> lorem ipsum ...<br>
    #<b>Contact:</b> <br>
    #<b>Web-link:</b> <a href="https://tuni.fi"</a>Call text</a><br>
    #</p>


    #f.write("Type: %s <br>\n University: %s <br>\n" % (row[0],row[1]))
    # f.write("University: " + row[1] +" <br>\n")

    f.write("<br>\n")

    f.write("</p>\n\n")

def write_all_positions(conn,f):
    """
    Query all rows in the positions table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    today = str(date.today())
    # today = '2022-11-01' # For debugging  

    f.write("<h2>[UNDER CONSTRUCTION - TESTING PHASE]</h2>\n\n")

    f.write("<h2>Open Positions</h2>\n\n")

    cur.execute("SELECT * FROM positions WHERE DeadlineDate >= '%s' ORDER BY PosID DESC" % today)

    rows = cur.fetchall()


    for row in rows:
        print(row[0])
        write_position_html(row,f)

    f.write("<h2>Past Positions</h2>\n\n")

    cur.execute("SELECT * FROM positions WHERE DeadlineDate < '%s' ORDER BY PosID DESC" % today)

    rows = cur.fetchall()

    for row in rows:
        print(row[0])
        write_position_html(row,f)

def main():
    database = "dps-jobs.db"

    sql_create_positions_table = """ CREATE TABLE IF NOT EXISTS positions (
                                    PositionType text,
                                    University text,
                                    UniversityLink text,
                                    Department text,
                                    DepartmentLink text,
                                    DeadlineText text,
                                    DeadlineDate text,
                                    Description text,
                                    ContactInfo text,
                                    AnnouncementLink text,
                                    AnnouncementDate text,
                                    PosID integer PRIMARY KEY
                                    ); """

    # create a database connection
    conn = create_connection(database)
    # create_table(conn, sql_create_positions_table)
    f = open("positions.html","w")
    with conn:
        # create a new position
    #    position = ('Professor', 'TAU', 'https://tuni.fi', 'Mathematics', 'https://math.tuni.fi', 'End of October 2022', '2022-10-31', 'A very good position indeed...', 'Lassi Paunonen', 'https://sysgrouptampere.wordpress.com', '2022-10-17');
    #    position_id = create_position(conn, position)
        # f.write("Positions<br>\n") 
        # f.write("<a href=\"https://sysgrouptampere.wordpress.com\">Homepage</a>\n") 

        write_all_positions(conn,f)

    f.close()


    filenames = ['positions_page_beginning.html', 'positions.html', 'positions_page_end.html']
    with open('index.html', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(infile.read())


if __name__ == '__main__':
    main()
