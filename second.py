import pymysql
import configparser
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twisted.enterprise import adbapi
from twisted.internet import reactor
#config = {'host':'127.0.0.1', 'user':'root', 'password':'', 'db':''}

def getDb(db):
    cf = configparser.ConfigParser()
    cf.read("my.conf")
    o1 = cf.items(db)
    conf = {}
    for x,y in o1:
        if x == 'port':
            y = int(y)
        conf[x] = y
    return conf

def db_func(plat):
    def outer(f):
        def inner(*args,**kwargs):
            config = getDb(plat)
            conn = pymysql.connect(**config)
            try:
                return f(conn, *args, **kwargs)
            finally:
                conn.close()
        return inner
    return outer

@db_func(plat = 'local')
def access_mysql(conn):
    
    #conn = pymysql.connect(**config)
 
    # cur = conn.cursor(pymysql.cursors.DictCursor)
 
    # cur.execute("SELECT * FROM member limit 10")

    # arr = cur.fetchall()
    # for val in arr:
    #     val['id'] *= 100
    # print(arr)
    # try:
    #     param = [(add1(i['id']), i['name'], i['email']) for i in arr]
    #     print(param)
    #     sql = 'INSERT IGNORE INTO member_test VALUES(%s,%s,%s)'  
    #     n=cur.executemany(sql,param)

    #     cur = conn.cursor()
    #     cur.execute('show databases')
    #     databases = cur.fetchall()
    #     dat = [i[0] for i in databases]
    #     print(tuple('laji')==('laji',))
    #     if ('laji',) not in databases:
    #         sql = 'create database laji'
    #         cur.execute(sql)

    #     conn.commit()
    # except Exception as e:
    #     conn.rollback()
    #     raise e
    # cur.close()
    # conn.close()

    with conn as db: 
        db.execute("SELECT id,email,title FROM magazine where id >= 70")
        arr = db.fetchall()
        idArr = []
        emailArr = []
        titleArr = []
        for id,email,title in arr:
            idArr.append(id)
            emailArr.append(email)
            print(title)
            titleArr.append(title)
        data = {"email":emailArr,"title":titleArr}
        df = pd.DataFrame(data,columns=['email','title'],index=idArr)
        print(df)
        # df.to_csv('foo.csv')
        # df.to_excel('foo.xlsx', sheet_name='Sheet1')

def sqlorm():
    engine = create_engine('mysql+pymysql://root:@localhost:3306/adnint?charset=utf8',echo=True)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    magazine = session.execute('SELECT id,email,title FROM magazine where id >= :id', {'id': 70})
    for mgz in magazine:
        print(mgz)

def querydb(tx,param):
    sql = "select * from magazine where id = %s" % (param)
    # sql = "insert into magazine (id) values (%s)" % (param)
    tx.execute(sql)
    return tx.fetchall()[0][1]

def add1(id):
    return int(id) + 1 


def twisted_demo():
    params = [1,2,4,7,9]
    for param in params:
        d = dbpool.runInteraction(querydb, param)  
        d.addCallback(lambda res: a.append(res))
    reactor.callLater(1, reactor.stop)
    # reactor.callLater(0, twisted_demo)
    reactor.run()

def getMagazine(id):
    return dbpool.runQuery("SELECT * FROM magazine WHERE id = %s", id)

def printResult(l):
    if l:
        print(l[0][0])
    else:
        print("No")

def ebPrintError(failure):
    import sys
    sys.stderr.write(str(failure))

def stop(_): reactor.stop()

def test():
    d = getMagazine("1")
    d.addCallback(lambda res: a.append(res))
    d.addCallback(stop)
    d.addErrback(ebPrintError)

if __name__== '__main__':
    # access_mysql()
    # sqlorm()
    a = []
    dbpool = adbapi.ConnectionPool(
                dbapiName ='pymysql',
                host ='127.0.0.1',
                db = '',
                user = 'root',
                passwd = '',
                charset = 'utf8',
                use_unicode = False
        )
    # twisted_demo()
    # print(a)
    reactor.callLater(0,test)
    reactor.run()
    print(a)