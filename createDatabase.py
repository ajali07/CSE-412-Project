import psycopg2

#connect to postgres
conn = psycopg2.connect(
   database="postgres", user='postgres', password='sql', host='192.168.56.101', port= '5432'
)
conn.autocommit = True

# Open a cursor to perform database operations
cur = conn.cursor()

#Preparing query to create a database
cur.execute("DROP DATABASE IF EXISTS test412")
sql = '''CREATE database test412'''

#Creating the database and connect
cur.execute(sql)
cur = conn.close()

conn = psycopg2.connect(
   database="test412", user='postgres', password='sql', host='192.168.56.101', port= '5432'
)

conn.autocommit = True
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS CUSTOMER")
cur.execute("DROP TABLE IF EXISTS INVOICE")
cur.execute("DROP TABLE IF EXISTS LINE")
cur.execute("DROP TABLE IF EXISTS PRODUCT")
cur.execute("DROP TABLE IF EXISTS VENDOR")


sql = ''' 
    CREATE TABLE CUSTOMER (
    CUS_CODE INT PRIMARY KEY,
    CUS_LNAME VARCHAR(100),
    CUS_FNAME VARCHAR(100),
    CUS_INITIAL CHAR(100),
    CUS_AREACODE VARCHAR(50),
    CUS_PHONE VARCHAR(50),
    CUS_BALANCE FLOAT
    );

    CREATE TABLE INVOICE (
    INV_NUMBER INT PRIMARY KEY,
    CUS_CODE INT,
    INV_DATE DATE
    );

    CREATE TABLE LINE (
    LINE_NUMBER INT,
    INV_NUMBER INT,    
    P_CODE VARCHAR(100),
    LINE_UNITS FLOAT,
    LINE_PRICE FLOAT
    );

    CREATE TABLE PRODUCT (
    P_CODE VARCHAR(100) PRIMARY KEY,
    P_DESCRIPT VARCHAR(255),
    P_INDATE DATE,
    P_QOH INT,
    P_MIN INT,
    P_PRICE FLOAT,
    P_DISCOUNT FLOAT,
    V_CODE INT
    );

    CREATE TABLE VENDOR(
    V_CODE INT PRIMARY KEY,
    V_NAME VARCHAR(30),
    V_AREACODE VARCHAR(20),
    V_CONTACT VARCHAR(20),
    V_PHONE VARCHAR(20),
    V_STATE VARCHAR(20),
    V_ORDER VARCHAR(20)
    );

    '''

cur.execute(sql)

# load in file data
with open('data/CUSTOMER.csv', 'r') as file1:
    cur.copy_expert("COPY CUSTOMER FROM STDIN WITH CSV HEADER", file1)

with open('data/INVOICE.csv', 'r') as file2:
    cur.copy_expert("COPY INVOICE FROM STDIN WITH CSV HEADER", file2)

with open('data/LINE.csv', 'r') as file3:
    cur.copy_expert("COPY LINE FROM STDIN WITH CSV HEADER", file3)
    
with open('data/PRODUCT.csv', 'r') as file4:
    cur.copy_expert("COPY PRODUCT FROM STDIN WITH CSV HEADER", file4)
    
with open('data/VENDOR.csv', 'r') as file5:
    cur.copy_expert("COPY VENDOR FROM STDIN WITH CSV HEADER", file5)


conn.close()
