import sqlite3

class Persister:
    sqlite_db_file = 'hippo.sqlite'

    def __init__(self):
        self.conn = sqlite3.connect(self.sqlite_db_file)
        self.cur = self.conn.cursor()

        self.init_db()

    def init_db(self):
        init_sql = """
        CREATE TABLE if not exists items (
          id integer primary key autoincrement,
          desc text UNIQUE,
          last_reviewed int,
          ff real,
          int_step int,
          iri real);"""

        self.cur.executescript(init_sql)
        self.conn.commit()

    def add_item(self, item):
        sql = """INSERT INTO items (desc, last_reviewed, ff, int_step, iri)
                 VALUES (?, ?, ?, ?, ?)"""

        self.cur.execute(sql, (item['desc'], item['last_reviewed'], 
                        item['ff'], item['int_step'], item['iri']))

        self.conn.commit()
        return self.cur.lastrowid

    def change_item_desc(self, item_id, desc):
        sql = """UPDATE items SET desc=? WHERE id=?"""
        self.cur.execute(sql, (desc, item_id))
        self.conn.commit()

    # for changing iri/int_step/ff/last_reviewed
    def update_item(self, item):
        sql = """UPDATE items SET last_reviewed=?, iri=?, int_step=?, ff=? WHERE id=?"""
        self.cur.execute(sql, (item['last_reviewed'], item['iri'],
                               item['int_step'], item['ff'], item['id'])) 
        self.conn.commit()

    def remove_item(self, item_id):
        sql = """DELETE FROM items WHERE id=?"""
        self.cur.execute(sql, (item_id,))
        self.conn.commit()

    def get_items(self):
        sql = """SELECT id, desc, last_reviewed, ff, int_step, iri FROM items"""
        self.cur.execute(sql)
        self.conn.commit()

        items = []
        for row in self.cur.fetchall():
            items.append({
                'id': row[0],
                'desc': row[1],
                'last_reviewed': row[2],
                'ff': row[3],
                'int_step': row[4],
                'iri': row[5]
            })
        return items

