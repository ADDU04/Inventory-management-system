import sqlite3
def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Supplier text,Category text,name text,price text,qty text,warranty text,exp text,status text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS purchase(oid INTEGER PRIMARY KEY AUTOINCREMENT,Category text,Supplier text,name text,price text,invoice text,cname text,contact text,status text,date text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS salary(eid INTEGER PRIMARY KEY AUTOINCREMENT,empid text,empname text, netpay text,wid text,date text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS cart(oid INTEGER PRIMARY KEY AUTOINCREMENT,custname text,contact text,pname text,qty text,price text,date text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS attendance(aid INTEGER PRIMARY KEY AUTOINCREMENT,empid text,empname text,status text,time text,date text)")
    con.commit()

    
create_db()    