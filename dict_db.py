"""
数据访问对象
向数据库发送指定的增删改查的请求
"""
import pymysql
import hashlib

salt=b"qwerdf"#加盐

#密码散裂化处理
def hash_password(password):
    hash=hashlib.md5(salt)
    hash.update(password.encode())
    return  hash.hexdigest()#获取散裂化后的十六进制密码


class Database:
    def __init__(self,host="127.0.0.1",port=3306,
                        user="root",password="123456",
                        database="dict",charset="utf8"):
        #连接数据库
        self.db=pymysql.connect(host=host,port=port,
                        user=user,password=password,
                        database=database,charset=charset)
        #建立游标对象，去执行sql语句的对象
        self.cur=self.db.cursor()

    def close(self):
        self.cur.close()
        self.db.close()

    def register(self,username,password):
        """
        1.判断user表中是否存在注册的用户名
            -存在返回false
            -不存在继续第二步
        2.将该用户信息存入user表中
        :return:
        """
        sql="select * from user where username='%s'"% username
        self.cur.execute(sql)
        result=self.cur.fetchone()
        if result:
            return False
        password=hash_password(password)#将密码进行散裂化处理
        try:
            sql="insert into user(username,password) values(%s,%s)"
            self.cur.execute(sql,[username,password])
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    def login(self, username, password):
        """
        select * from user where username='nfx' and
            password = '123456';   ????
        :param username:
        :param password:
        :return:
        """
        password = hash_password(password)  # md5散列处理
        sql = "SELECT * FROM user WHERE username = %s and password = %s;"
        self.cur.execute(sql, [username, password])  # 执行sql语句
        result = self.cur.fetchone()  # 获取查询结果
        if result:  # 如果有返回值，则表示登陆成功
            return True
        else:
            return False

    def query(self, word):
        sql = "SELECT mean FROM words WHERE word='%s'" % word
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            # 返回的是单词的解释 mean
            return result[0]
    def insert_history(self,username,word):
        #当用户查询完单词后执行此方法
        sql="insert into history(username,word) values (%s,%s);"
        try:
            self.cur.execute(sql,[username,word])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
    def select_history(self,username):
        sql="SELECT username, word, time " \
        "FROM history " \
        "WHERE username = '%s' " \
        "ORDER BY time DESC " \
        "LIMIT 5" % username
        self.cur.execute(sql)
        return self.cur.fetchall()