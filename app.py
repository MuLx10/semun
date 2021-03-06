from flask import Flask, redirect, render_template, request, url_for, flash, session
from db import db
import os
app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
# some issue
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

target = os.path.join(APP_ROOT, 'static/images/')
if not os.path.exists(target):
    os.mkdir(target)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/create_db')
def create_db():
    db.create_db()
    return "created"


@app.route('/logina', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        value = db.authenticate(
            request.form['username'],
            request.form['password'])
        if (value == 1):
            print "login Succesful"
            session['name'] = request.form['username']
            user_data = session['name']
            print user_data
            data = db.filter_user_data(user_data)
            print(data,'fetched')
            data = map(str,list(data))
            print(len(data),data)
            return render_template(
                'index.html',
                 data = data)
        else:
            error = 'Invalid username or password \
            Please try again!'
            return render_template('login.html', error=error, session=session)
    return render_template('login.html')


@app.route('/reg?is%2')
def registration():
    return render_template('registration.html')


@app.route("/registform", methods=['POST'])
def register():

    f = request.files['file']
    name = f.filename
    if '.jpg' in name or '.jpeg' in name or '.png' in name:
        xt = '.'+name.split('.')[-1]
        name = request.form['field1']+':'+request.form['field3']+xt
        f.save("/".join([target,name ]))
    else:
        flash('ERROR! PLEASE ENTER CORRECT FORMAT (jpg,png)')
        return redirect(url_for('registration'))
        
    data = db.user_alreadyexits(request.form['field3'],
                                request.form['field1'],
                                request.form['field2'],
                                request.form['field4'],
                                request.form['field6'],
                                request.form['field8'],
                                request.form['field9'],
                                name
                                )
    if (data == 1) :
        flash('ERROR! PLEASE ENTER SOMETHING OR CHECK YOUR USER')
        return redirect(url_for('registration'))

    '''
    USERID,NAME,EMAIL,PASSWORD,MOBILE,REG,NT,IMG
    Name    : {{ data[1]}}<br/>
    Email   : {{ data[2]}}<br/>
    Mobile: {{ data[4]}}<br/>
    Registration type: {{ data[5]}}<br/>
    No of Tickets:{{ data[6]}}<br/></p>
    '''
    data = [request.form['field3'],
            request.form['field1'],
            request.form['field2'],
            request.form['field4'],
            request.form['field6'],
            request.form['field8'],
            request.form['field9'],
            name]
    data = map(str,data)
    flash('You were successfull')
    return render_template(
                'index.html',
                 data = data)
    return redirect(url_for('registration'))




@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/clearsession')
def clearsession():
    session.clear()
    return redirect(url_for('logina'))



@app.route('/logina')
def logina():
    return render_template('login.html')


@app.route('/add')
def add():
    return render_template('add_catagories.html')


@app.route("/catagory", methods=['POST'])
def catagory():
    error = None
    if 'name' in session:
        data_catagory = db.catagory_alreadyexits(session['name'],
                                                 request.form['field7'],
                                                 request.form['field8'],
                                                 request.form['field9'])
        if (data_catagory == 1):
            flash('ERROR! CATAGORY ALREADY SATISFIED OR SOMETHING WENT WRONG PLEASE CHECK NEXT MESSAGE TO CONFIRM')
        else:
            flash(data_catagory)
            user_data = session['name']
            print user_data
            data = db.filter_user_data(user_data)
            print type(data), data, len(data)
            data_user_get = db.filter_user_chart(user_data)
            graph_data = []
            for elem in data_user_get:
                cat = elem[0]
                exp = elem[1]
                li = [cat, int(exp)]
                graph_data.append(li)
            graph_data.insert(0, ['Category', 'Expenses'])
            print "Graph data ", graph_data
            return render_template(
                'index.html',
                error=error,
                data=data,
                data_chart=graph_data)
        flash('REQUEST PERFORMED!')
        return redirect(url_for('add'))
    else:
        flash(
            'Please Login to Perform Action'
        )
        return redirect(url_for('logina'))


@app.route('/asd')
def data_user():
    error = None
    data = None
    if 'name' in session:
        user_data = session['name']
        print user_data
        data = db.filter_user_data(user_data)
        print type(data), data, len(data)
        return render_template('index.html', error=error, data=data)
    else:
        flash('ERROR: Please Login to Preform this actions')
        return redirect(url_for('logina'))


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8080"),
            debug= True
    )
