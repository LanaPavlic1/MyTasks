from pony.orm import Database, Required, PrimaryKey
from datetime import datetime

db = Database()

class Task(db.Entity):
    id = PrimaryKey(int, auto=True)
    content = Required(str)
    deadline = Required(datetime, nullable=True)
    created_at = Required(datetime, default=datetime.utcnow)
    completed = Required(bool, default=False)

db.bind(provider='sqlite', filename='tasks.db', create_db=True)
db.generate_mapping(create_tables=True)
