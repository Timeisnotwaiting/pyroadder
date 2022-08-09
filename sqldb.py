from sqlbuild import SESSION, BASE
from sqlalchemy import Column, Integer
import threading

class Scrap(BASE):
    __tablename__ = "scrap"

    id = Column(Integer, primary_key=True)

    def __init__(self, id):
        self.id = id

Scrap.__table__.create(checkfirst=True)

LOCKER = threading.RLock()

def add(id):
    with LOCKER:
        got = SESSION.query(Scrap).get(a)
        if not got:
            adder = Scrap(a)
            SESSION.add(adder)
            SESSION.commit()
        else:
            SESSION.close()

def pop(id):
    with LOCKER:
        got = SESSION.query(Scrap).get(a)
        if got:
            SESSION.delete(got)
            SESSION.commit()
        else:
            SESSION.close()

def getdb():
    all = SESSION.query(Scrap).all()
    DB = []
    for db in all:
        DB.append(db.id)
    return DB
