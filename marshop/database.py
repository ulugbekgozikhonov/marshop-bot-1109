import sqlite3

con = sqlite3.connect("marshop.db")
cur = con.cursor()

# print(cur.execute("Select Count(*) from products ").fetchone())

# def connext():
#     con = sqlite3.connect("marshop.db")
#     cur = con.cursor()
#     return cur


# def create_tables():
#     cur = connext()
#     cur.execute("""CREATE TABLE IF NOT EXISTS users(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         chat_id INTEGER UNIQUE,
#         full_name VARCHAR(100) NOT NULL,
#         phone_number VARCHAR(13) UNIQUE
        
#         )""")
    
# def add_user(data: dict):
#     cur = connext()    
#     cur.execute("INSERT INTO users(chat_id,full_name,phone_number) VALUES(?,?,?)",
#                 (data.get('chat_id'),data.get('full_name'),data.get('phone_number')))
#     con.commit()

# def get_user_by_chat_id(chat_id: int):
#     con = sqlite3.connect("marshop.db")
#     cur = con.cursor()
#     try:
#         user = cur.execute("SELECT * FROM users WHERE chat_id=?",(chat_id,)).fetchone()
#         return user
#     except Exception as ex:
#         print("Error select user",ex)
#         return False


import sqlite3

class DatabaseManager:
    
    def __init__(self,db_name) -> None:
        self.db_name=db_name
        self.__con = sqlite3.connect(self.db_name)
        self.__cur = self.__con.cursor()
    
    
    def create_tables(self):
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            full_name VARCHAR(100) NOT NULL,
            phone_number VARCHAR(13) UNIQUE
            
        )""")

        self.__cur.execute("""CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            photo VARCHAR(255),
            count INTEGER,
            price FLOAT,
            description TEXT,
            chat_id INTEGER,
            status BOOLEAN DEFAULT(FALSE),
            FOREIGN KEY (chat_id) REFERENCES users(chat_id)
            
        )""")
    
    def add_user(self,data: dict):
        try:
            self.__cur.execute("INSERT INTO users(chat_id,full_name,phone_number) VALUES(?,?,?)",
                    (data.get('chat_id'),data.get('full_name'),data.get('phone_number')))
            self.__con.commit()
        except Exception as ex:
            print(ex)
            return False
    
    def get_user_by_chat_id(self,chat_id: int):
        try:
            user = self.__cur.execute("SELECT * FROM users WHERE chat_id=?",(chat_id,)).fetchone()
            return user
        except Exception as ex:
            print(ex)
            return False
    def create_prodcut(self,data: dict):
        try: 
            self.__cur.execute("INSERT INTO products(name, photo, price, count, description, chat_id) VALUES(?,?,?,?,?,?)",
            (data.get("name"), data.get("photo"), data.get("price"), data.get("count"), data.get("description"), data.get("chat_id")))
            self.__con.commit()
            return True
        except Exception as ex:
            print(ex)
            return False
        
    def get_products_by_chat_id(self, chat_id,limit,offset):
        try:
            return self.__cur.execute(f"SELECT * FROM products WHERE chat_id=? LIMIT {limit} OFFSET {offset} ", (chat_id, )).fetchall()
        except Exception as ex:
            print(ex)
            return False  
    
    def get_products_count_by_chat_id(self,chat_id):
        try:
            return self.__cur.execute(f"SELECT COUNT(*) FROM products WHERE chat_id=? ", (chat_id, )).fetchone()[0]
        except Exception as ex:
            print(ex)
            return False  

    def get_product_by_status(self):
        try:
            return self.__cur.execute("SELECT * FROM products WHERE status=?",(True,)).fetchall()
        except Exception as ex:
            print(ex)
            return False  
    def get_products_by_chat_id_and_name(self,chat_id,name):
        try:
            return self.__cur.execute("SELECT * FROM products WHERE chat_id=? and name=?",(chat_id,name)).fetchone()
        except Exception as ex:
            print(ex)
            return False  