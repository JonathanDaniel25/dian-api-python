from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from db import meta, engine

users = Table("users", meta, 
    Column("id", Integer, primary_key=True), 
    Column("name", String(75)), 
    Column("email", String(100)),
    Column("password", String(255))
)

meta.create_all(engine)