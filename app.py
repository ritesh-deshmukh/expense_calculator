import os
from flask import Flask, flash, request, redirect, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
import datetime
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/example_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

Session(app)

api = Api(app)


class Master(db.Model):
    __tablename__ = 'MASTER'
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(100), unique=True)
    uploaded_by = db.Column(db.String(100))
    file_name = db.Column(db.String(500))
    file_type = db.Column(db.String(500))
    creation_ts = db.Column(db.String(500))
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Master %r>' % self.asset_id

db.create_all()


class FileHandler(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            query = Master(
                asset_id=str(uuid.uuid4()),
                uploaded_by="example_name",
                file_name=file.filename,
                file_type="pdf",
                creation_ts=str(datetime.datetime.now()),
                status="processing"
            )
            db.session.add(query)
            db.session.commit()
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


api.add_resource(FileHandler, '/upload')

if __name__ == "__main__":
    app.secret_key = 'secret_key'
    app.run(debug=True)
