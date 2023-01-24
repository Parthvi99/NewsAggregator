from flask import Flask, render_template, request
from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import AddLinkForm

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
mysql = MySQL()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root: @localhost/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mykey'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'newsagg'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
ourdb = SQLAlchemy(app)
Migrate(app, ourdb)
conn = mysql.connect()
conn.commit()


@app.route('/')
def index():
    cursor = conn.cursor()


    cursor.execute("SELECT * from allcontent;")
    rows = cursor.fetchall()

    total_count = len(rows)
    return render_template("index.html",total_count=total_count,rows=rows)


@app.route('/form',methods = ['GET','POST'])
def addlinkform():
    form = AddLinkForm()
    print(form.hello())
    return render_template('addlinkform.jinja2', form=form)


@app.route('/link/add', methods=['POST'])
def add_link():
    form = AddLinkForm()
    link = request.form['link']
    # User input
    # Database connect
    # add link to db
    try:
        cursor = conn.cursor()
        query = f"Insert into mainrss(main_links) values(%s)"
        cursor.execute(query, link)
        conn.commit()

        return render_template(
            'addlinkform.jinja2',
            title='Add New RSS links',
            messages=['Link has been added'],
            form=form
        )

    except Exception as exception:
        return render_template(
            'addlinkform.jinja2',
            title='Add New RSS links',
            error=[exception],
            form=form
        )


if __name__ == '__main__':
    app.run(debug=True)


