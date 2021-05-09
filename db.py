from entity import Entity
from typing import List
import sqlite3


class DataBasePanic(Exception):
    def __str__(self):
        return "База даннных поламалася("


connection = sqlite3.connect("main.db")
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS t_ads (id text, url text, imgUrl text,'
               'title text, price text, priceCurrency text, lifeTime text, geo text)')
connection.commit()
connection.close()
del connection


def update_entities(entities: List[Entity]):
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    results = []
    for entity in entities:
        cursor.execute("SELECT * FROM t_ads WHERE id=?", (entity.id,))
        if cursor.fetchone():
            cursor.execute("UPDATE t_ads SET id=?,url=?,imgUrl=?,title=?,price=?,priceCurrency=?,lifeTime=?,geo=?"
                           " WHERE id='{}'".format(entity.id), entity.get_tuple())
            connection.commit()
        else:
            cursor.execute("INSERT INTO t_ads VALUES (?,?,?,?,?,?,?,?)", entity.get_tuple())
            connection.commit()
            results.append(entity)
    connection.close()
    return results
