from sqlbuild import SESSION, BASE
from sqlalchemy import Column, Integer
from sqlalchemy.sql.sqltypes import BigInteger
import threading

class Scrap(BASE):
    __tablename__ = "scrap"

    id = Column(BigInteger, primary_key=True)

    def __init__(self, id):
        self.id = id

Scrap.__table__.create(checkfirst=True)

LOCKER = threading.RLock()

def add(id):
    with LOCKER:
        got = SESSION.query(Scrap).get(id)
        if got:
            return SESSION.close()
        SESSION.add(Scrap(id))
        SESSION.commit()

def pop(id):
    with LOCKER:
        got = SESSION.query(Scrap).get(id)
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


class Mute(BASE):
    __tablename__ = "mute"

    id = Column(BigInteger, primary_key=True)

    def __init__(self, id):
        self.id = id

Mute.__table__.create(checkfirst=True)

def mute(id):
    with LOCKER:
        muted = SESSION.query(Mute).get(id)
        if muted:
            return SESSION.close()
        SESSION.add(Mute(id))
        SESSION.commit()

def unmute(id):
    with LOCKER:
        muted = SESSION.query(Mute).get(id)
        if not muted:
          return SESSION.close()
        SESSION.delete(muted)
        SESSION.commit()

def is_muted(id):
    muted = SESSION.query(Mute).get(id)
    if muted:
        return True
    return False
    
