# models.py
from peewee import *
import datetime

db = SqliteDatabase('football.db')

class Match(Model):
    datums = CharField()
    turnirs = CharField()
    vieta = CharField()
    pretinieks = CharField()
    rezultats = CharField()
    vartu_guveji = CharField(null=True)
    goli_par = IntegerField(default=0)
    goli_pret = IntegerField(default=0)
    iznākums = CharField(null=True)  # uzvara/neizšķirts/zaudējums
    
    class Meta:
        database = db

def initialize_db():
    db.connect()
    db.create_tables([Match], safe=True)
    return db