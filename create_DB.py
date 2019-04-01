from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/example_db'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Master(db.Model):
    __tablename__ = 'MASTER'
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(100))
    uploaded_by = db.Column(db.String(100))
    file_name = db.Column(db.String(500))
    file_type = db.Column(db.String(10))
    creation_ts = db.Column(db.DATETIME)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


if __name__ == "__main__":
    pass