__author__='Sam'
# Imports sqlite3 library for database use
import sqlite3

# Define createDB function
def createDB():
        # Connect to the database file
        conn = sqlite3.connect('Freehugs.db')

        print("\nOpened database successfully\n")

        while True:
                try:
                        # Query to create the Customers table
                        conn.execute('CREATE TABLE CUSTOMERS \
                                     (customerID INTEGER PRIMARY KEY NOT NULL, \
                                     userName TEXT NOT NULL, \
                                     password TEXT NOT NULL, \
                                     firstName TEXT NOT NULL, \
                                     lastName TEXT NOT NULL, \
                                     address1 TEXT NOT NULL, \
                                     address2 TEXT, \
                                     zipcode TEXT NOT NULL, \
                                     city TEXT NOT NULL, \
                                     state TEXT NOT NULL, \
                                     phoneNumber TEXT NOT NULL);')
                # Catch sqlite error if query is executed and table already exists
                except sqlite3.OperationalError:
                        print("\nTable already exists\n")
                else:
                        print("Table created successfully\n")
                        # Closing the connection to the database file

                break

        while True:
                try:
                        # Query to create the Orders table
                        conn.execute("CREATE TABLE ORDERS \
                                     (orderID INTEGER PRIMARY KEY NOT NULL, \
                                     customerID INTEGER, \
                                     hugType TEXT NOT NULL, \
                                     hugDuration REAL NOT NULL, \
                                     pat TEXT NOT NULL, \
                                     sway TEXT NOT NULL, \
                                     lift TEXT NOT NULL, \
                                     orderComplete TEXT NOT NULL);")
                # Catch sqlite error if query is executed and table already exists
                except sqlite3.OperationalError:
                        print("\nTable already exists\n")
                else:
                        print("Table created successfully\n")
                        # Closing the connection to the database file

                break

        conn.close()
# function to obtain cid value
def getCID(user):
    sqlite_file = 'FreeHugs.db'  # name of the sqlite database file
    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)

    c = conn.cursor()
    sql = ("SELECT customerID FROM CUSTOMERS WHERE userName = ?;")
    arg = user
    #fetch one row of data
    row = c.execute(sql, [arg]).fetchone()
    # retreive the element for the first value in the row
    cid = row[0]
    conn.commit()
    conn.close()

    # return the value
    return cid

# function to insert order into orders table
def createOrder(cid, hType, hDuration, hPat, hSway, hLift):
    try:
        sqlite_file = 'Freehugs.db'  # name of the sqlite database file
        # Connecting to the database
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        sql = "INSERT INTO ORDERS (customerID, hugType, hugDuration, pat, sway, lift, orderComplete) \
                                         VALUES (?, ?, ?, ?, ?, ?, ?)"
        arg = (cid, hType, hDuration, hPat, hSway, hLift, 'No')
        # Executes the insert
        c.execute(sql, arg)
        conn.commit()

    except:
        conn.rollback()
        msg = "error creating order"
        return msg
    finally:
        msg = "Order created successfully!"
        conn.close()
        print('\norder created successfully\n')
        return msg
# function to insert record into customers table
def registerUser(user, password, fName, lName, add, add2, city, state, zip, phone):

    try:
        sqlite_file = 'Freehugs.db'  # name of the sqlite database file
        # Connecting to the database
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        sql = "INSERT INTO CUSTOMERS (userName, password, firstName, lastName, address1, address2, city, state, zipcode, phoneNumber) \
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        arg = (user, password, fName, lName, add, add2, city, state, zip, phone)
        # Executes the insert
        c.execute(sql, arg)
        conn.commit()

    except:
        conn.rollback()
        msg = "error in insert operation"
        return msg
    finally:
        msg = "Registration successful!"
        conn.close()
        print('\nRecord updated successfully\n')
        return msg
# function to select all records in customers table
def displayCustomers():
    sqlite_file = 'FreeHugs.db'  # name of the sqlite database file
    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    conn.row_factory = sqlite3.Row

    c = conn.cursor()
    c.execute("SELECT * FROM CUSTOMERS")
    conn.commit()

    result = c.fetchall()
    conn.close()

    return result


# function to select all orders from orders table
def displayOrders():
    sqlite_file = 'FreeHugs.db'  # name of the sqlite database file
    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    conn.row_factory = sqlite3.Row

    c = conn.cursor()
    c.execute("SELECT * FROM ORDERS")
    conn.commit()

    result = c.fetchall()
    conn.close()

    return result
# function to select all open orders from orders table
def displayOpenOrders():
    sqlite_file = 'FreeHugs.db'  # name of the sqlite database file
    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    conn.row_factory = sqlite3.Row

    c = conn.cursor()
    sql = "SELECT * FROM ORDERS WHERE orderComplete = ?;"
    arg = 'No'
    c.execute(sql, [arg])
    conn.commit()

    result = c.fetchall()
    conn.close()

    return result
# function to select all closed orders from the orders table
def displayClosedOrders():
    sqlite_file = 'FreeHugs.db'  # name of the sqlite database file
    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    conn.row_factory = sqlite3.Row

    c = conn.cursor()
    sql = "SELECT * FROM ORDERS WHERE orderComplete = ?;"
    arg = 'Yes'
    c.execute(sql, [arg])
    conn.commit()

    result = c.fetchall()
    conn.close()

    return result
# function to update the orders table
def closeOrders(oid):
    try:
        sqlite_file = 'FreeHugs.db'  # name of the sqlite database file
        # Connecting to the database file
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        sql = "UPDATE ORDERS SET orderComplete = ? WHERE orderID = ?;"
        arg = ('Yes', oid)
        c.execute(sql, arg)
        conn.commit()
    except:
        conn.rollback()
        msg = "Order ID doesn't exist"
        return msg
    finally:
        msg = "Order updated successfully!"
        conn.close()
        print('\nOrder updated successfully\n')
        return msg
# function to delete a record from the customers table
def deleteCustomer(cid):

    try:
        sqlite_file = 'FreeHugs.db'  # name of the sqlite database file
        # Connecting to the database file
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        sql = "DELETE FROM CUSTOMERS WHERE customerID = ?;"
        arg = (cid)
        c.execute(sql, arg)
        conn.commit()
    except:
        conn.rollback()
        msg = "Customer ID doesn't exist"
        return msg
    finally:
        msg = "Customer deleted successfully!"
        conn.close()
        print('\nCustomer deleted successfully\n')
        return msg
# function to search for a customer in the customers table
def searchCustomer(cid):

    sqlite_file = 'FreeHugs.db'  # name of the sqlite database file
    #  Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    sql = "SELECT * FROM CUSTOMERS WHERE customerID = ?;"
    arg = (cid)
    c.execute(sql, arg)
    conn.commit()

    result = c.fetchall()
    conn.close()

    return result
