import psycopg2 as pg


def get_connection():
    # conn = pg.connect(database = "testdb", 
    #     user = "postgres", password = "test", 
    #     host = "127.0.0.1", port = "5432")
    conn = pg.connect(
        database='d1vg1p6775ts33',
        user='kxriveycfvembv',
        password='f6aac0667840144279ff257db494bd660830897ba735f504d4239d10a2619ae7',
        host='ec2-54-83-58-222.compute-1.amazonaws.com',
        port=5432)
    return conn


def create_db():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE UserTable
        (USERID       TEXT    UNIQUE    NOT Null,
         NAME           TEXT    NOT NULL,
         EMAIL            TEXT     NOT NULL,
         PASSWORD        TEXT,
         MOBILE          TEXT UNIQUE    NOT Null,
         REG          TEXT UNIQUE    NOT Null,
         NT         INT    NOT Null,
         IMG      TEXT UNIQUE    NOT Null
         );''')
        print "Table created successfully"
        connection.commit()
        connection.close()
    except Exception as error:
        print(error)
        return error


def filter_user_data(USER):
    connection = get_connection()
    cursor = connection.cursor()
    fetch_db = """SELECT USERID,NAME,EMAIL,PASSWORD,MOBILE,REG,NT,IMG from UserTable where USERID='%s'"""
    fetch_db = fetch_db % (USER)
    cursor.execute(fetch_db)
    rows = cursor.fetchall()
    for row in rows:
        print "User ID = ", row[0]
        print "Your Name = ", row[1]
        print "Registered Name = ", row[2]
        print "Password = ", row[3], "\n"
    print "Operation done successfully"
    cursor.close()
    return rows[0]


def insert_db(USER, NAME, EMAIL, PASSWORDV,MOBILE,REG,NT,IMG):
    connection = get_connection()
    cursor = connection.cursor()
    print "cur is created"
    print(str(USER), str(NAME), str(EMAIL), str(PASSWORDV), str(MOBILE), str(REG), int(NT), str(IMG))
    query = """INSERT INTO UserTable (USERID,NAME,EMAIL,PASSWORD,MOBILE,REG,NT,IMG) VALUES('%s', '%s', '%s', '%s','%s','%s', '%d', '%s');"""
    query = query % (str(USER), str(NAME), str(EMAIL), str(PASSWORDV), str(MOBILE), str(REG), int(NT), str(IMG))
    print query
    cursor.execute(query)
    connection.commit()
    print "Records created successfully"
    connection.close()


def user_alreadyexits(USER, NAME, EMAIL, PASSWORDV,MOBILE,REG,NT,IMG):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT USERID from UserTable where USERID='%s';"""
    query = query % (USER, )
    cursor.execute(query)
    rows = cursor.fetchall()
    print rows
    try:
        if (len(rows) == 0):
            insert_db(USER, NAME, EMAIL, PASSWORDV,MOBILE,REG,NT,IMG)
        else:
            return 1
    except Exception as error:
        return error
    connection.close()


def authenticate(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT USERID, PASSWORD from UserTable where USERID='%s' and PASSWORD='%s';"""
    query = query % (username, password)
    cursor.execute(query)
    rows = cursor.fetchall()
    print rows
    try:
        if (rows[0][0] == username) and (rows[0][1] == password):
            return 1
        else:
            return 0
    except Exception as error:
        return error
    connection.close()
