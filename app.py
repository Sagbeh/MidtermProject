from flask import Flask, render_template, request, session, redirect, url_for, escape, flash
from Forms import *
from DB import *


app = Flask(__name__)

#home page that redirects user to login page if not currently logged in
@app.route('/')
def index():
    #if user is in session, they can go to place order
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    # if not, the user must log in
    return redirect(url_for('login'))
# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # create the database
    createDB()

    error = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        # get the user's login credentials from the fields in the login page
        username_form  = request.form['username']
        password_form  = request.form['password']
        sqlite_file = 'Freehugs.db'  # name of the sqlite database file
        # Connecting to the database
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        sqlUser = "SELECT COUNT(1) FROM CUSTOMERS WHERE userName = ?;"
        argUser = ([username_form])
        c.execute(sqlUser, argUser) # CHECKS IF USERNAME EXISTS
        if c.fetchone()[0]:
            sqlPass = "SELECT password FROM CUSTOMERS WHERE userName = ?;"
            argPass = ([username_form])
            c.execute(sqlPass, argPass) # Get password
            for row in c.fetchall():
                if password_form == row[0]: # if password in customers table matches the form, user is logged in...
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential" # otherwise, login denied
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error)

app.secret_key = 'something secretive' # secret key for session

#logout link function
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

# registration page for user
@app.route('/registration', methods=['POST', 'GET'])
def register():
    #create new registration form
    form = RegistrationForm()

    if request.method == 'POST':
        # store user inputs as variables for the customers table insert
        user = request.form['user']
        password = request.form['password']
        fName = request.form['fName']
        lName = request.form['lName']
        add = request.form['add']
        add2 = request.form['add2']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        phone = request.form['phone']
        #call function to insert record and return insert status
        msg = registerUser(user, password, fName, lName,add, add2, city, state, zip, phone)
        #present user feedback regarding user creation
        return render_template("result.html", msg=msg)
    elif request.method == 'GET':
        #send user to registration page with registration form
        return render_template('registration.html', form= form)

# User order page
@app.route('/order', methods=['POST', 'GET'])
def orderHug():
    # call order form
    form = OrderForm()

    if request.method == 'POST':
        # store user input as variables for order table insert
        type = request.form['type']
        duration = request.form['duration']
        pat = request.form['pat']
        sway = request.form['sway']
        lift = request.form['lift']
        user = session['username'] # get username from session
        cid = getCID(user) #function uses username to retrieve cid of the user
        # create new order
        msg = createOrder(cid, type, duration, pat, sway, lift)
        return render_template('success.html', msg = msg)
    elif request.method == 'GET':
        return render_template('order.html', form=form)


# admin page to view all customers
@app.route('/list')
def list():
    # call db method to return customer records
    rows = displayCustomers()
    # display records in table on list page
    return render_template("list.html", rows=rows)
# admin page to view all orders
@app.route('/orderlist')
def orderlist():
    # call db method to return order records
    rows = displayOrders()
    return render_template("orderlist.html", rows=rows)
# admin home page
@app.route('/adminindex')
def adminIndex():
   return render_template('adminindex.html')
# admin login page
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminLogin():
    error = None

    if request.method == 'POST':
        # admin can set password here
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'admin':
            error = 'Invalid username or password. Please try again!'
        else:
            flash('You were successfully logged in')
            # successful login goes to admin page
            return redirect(url_for('adminIndex'))
    return render_template('adminlogin.html', error=error)
# admin page to view open orders
@app.route('/openorders')
def openorders():

    rows = displayOpenOrders()
    return render_template("openorders.html", rows=rows)
# admin page to view closed orders
@app.route('/closedorders')
def closedorders():

    rows = displayClosedOrders()
    return render_template("closedorders.html", rows=rows)
# admin page to close orders
@app.route('/closeorders', methods=['POST', 'GET'])
def closeorders():

    # displays the open orders
    rows = displayOpenOrders()
    # call the closed order form
    form = CloseOrderForm()

    if request.method == 'POST':
        # get the order id from user input
        oid = request.form['oid']
        # db method to update the orders table
        msg = closeOrders(oid)
        return render_template('adminsuccess.html', msg=msg)
    elif request.method == 'GET':
        return render_template('closeorders.html', form=form, rows = rows)
# admin page to delete a customer
@app.route('/deletecustomer', methods=['POST', 'GET'])
def deletecustomer():

    # display all customers
    rows = displayCustomers()
    form = DeleteCustomerForm()

    if request.method == 'POST':
        # get customer id from delete customer form
        cid = request.form['cid']
        # call db method to delete the customer
        msg = deleteCustomer(cid)
        return render_template('adminsuccess.html', msg=msg)
    elif request.method == 'GET':
        return render_template('deletecustomer.html', form=form, rows = rows)
# admin page to search for one customer
@app.route('/searchcustomer', methods=['POST', 'GET'])
def searchcustomer():
    # create the search customer form
    form = SearchCustomerForm()

    if request.method == 'POST':
        # get the customer id from user input in the form
        cid = request.form['cid']
        # call db method to search for customer via cid
        rows = searchCustomer(cid)
        return render_template('list.html', rows= rows)
    elif request.method == 'GET':
        return render_template('searchcustomer.html', form=form)
# run the application
if __name__ == '__main__':
    app.run(debug=True)

