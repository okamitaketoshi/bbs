class database():
    def __init__(self, path):
        self.path = path
        self.create()
 
    def create(self):
        conn = sqlite3.connect(self.path, isolation_level='EXCLUSIVE')
        try:
            conn.execute("create table if not exists entry (id integer primary key, message text, date real);")
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.close()
 
    def post(self, message):
        conn = sqlite3.connect(self.path, isolation_level='DEFERRED')
        try:
            conn.execute("insert into entry(message, date) values(?, ?);", (message, time.time()))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.close()
 
    def get(self):
        result = []
        conn = sqlite3.connect(self.path)
        try:
            result = [x for x in conn.execute("select id, message, date from entry;")]
        finally:
            conn.close()
 
        return result