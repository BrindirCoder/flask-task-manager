from app import db
from datetime import datetime


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    category = db.Column(db.String(50))
    status = db.Column(db.String(10), default="pending")  # pending or done

    def __repr__(self):
        return f"<Task {self.title}>"
