# to run this website and watch for changes: 
# $ export FLASK_ENV=development; flask run


from flask import Flask, g, render_template, request
import sqlite3


app = Flask(__name__)

@app.route('/')
def main():

    return render_template('main.html')


@app.route('/submit/', methods=['POST', 'GET'])
def submit():

    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            insert_message(request)
            return render_template('submit.html', thanks = True)
        except:
            return render_template('submit.html', error = True)


@app.route('/view/')
def view():

    ran_messages = random_messages(5)

    return render_template('view.html', messages = ran_messages)



def get_message_db():

    if 'message_db' not in g:
        g.message_db = sqlite3.connect('messages_db.sqlite')
    
    cursor = g.message_db.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS messages(id INT, handle TEXT, message TEXT);')

    return g.message_db


def insert_message(request):

    db = get_message_db()
    cursor = db.cursor()

    message = request.form["message"]
    handle = request.form["handle"]

    row_num = cursor.execute("SELECT COUNT(*) FROM messages;").fetchone()[0]
    cursor.execute(f"""INSERT INTO messages (id, handle, message) VALUES ({row_num + 1}, "{handle}", "{message}");""")
    db.commit()

    db.close()


def random_messages(n):

    db = get_message_db()
    cursor = db.cursor()

    row_num = cursor.execute("SELECT COUNT(*) FROM messages;").fetchone()[0]
    
    # if the input number is more than the number of rows of data stored in the database
    # we will print all the data in the database
    if n > row_num:
        n = row_num

    ran_messages = []

    for i in range(n):
        ran_message = cursor.execute("SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT 1;").fetchone()
        ran_messages.append(ran_message)

    db.close()

    return ran_messages
    
