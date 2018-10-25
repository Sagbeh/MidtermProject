from flask_wtf import Form
from wtforms import SubmitField,SelectField, IntegerField, StringField, PasswordField, validators, ValidationError
# create the registration form
class RegistrationForm(Form):
    # all fields required except for address 2
    user = StringField("Username", [validators.DataRequired("Please enter a username.")])
    password = PasswordField("Password", [validators.DataRequired("Please enter a password.")])
    fName = StringField("First Name", [validators.DataRequired("Please enter your first name.")])
    lName = StringField("Last Name", [validators.DataRequired("Please enter your last name.")])
    add = StringField("Address", [validators.DataRequired("Please enter your address.")])
    add2 = StringField("Address 2 (optional)")
    city = StringField("City", [validators.DataRequired("Please enter your city.")])
    state = SelectField("State", choices = [("AL","AL"), ("AK","AK"), ("AZ","AZ"), ("AR","AR"), ("CA","CA"), ("CO","CO"), ("CT","CT"), ("DC","DC"), ("DE","DE"), ("FL","FL"), ("GA","GA"),
          ("HI","HI"), ("ID","ID"), ("IL","IL"), ("IN","IN"), ("IA","IA"), ("KS","KS"), ("KY","KY"), ("LA","LA"), ("ME","ME"), ("MD","MD"),
          ("MA","MA"), ("MI","MI"), ("MN","MN"), ("MS","MS"), ("MO","MO"), ("MT","MT"), ("NE","NE"), ("NV","NV"), ("NH","NH"), ("NJ","NJ"),
          ("NM","NM"), ("NY","NY"), ("NC","NC"), ("ND","ND"), ("OH","OH"), ("OK","OK"), ("OR","OR"), ("PA","PA"), ("RI","RI"), ("SC","SC"),
          ("SD","SD"), ("TN","TN"), ("TX","TX"), ("UT","UT"), ("VT","VT"), ("VA","VA"), ("WA","WA"), ("WV","WV"), ("WI","WI"), ("WY", "WY")])
    zip = StringField("Zipcode", [validators.DataRequired("Please enter your name.")])
    phone = StringField("Contact Number", [validators.DataRequired("Please enter your contact number.")])
    submit = SubmitField("Send")
# create the order form
class OrderForm(Form):
    # all fields are dropdowns
    type = SelectField("Hug Type", choices=[('The Standard', 'The Standard'), ('Bear Hug', 'Bear Hug'), ('Half Hug', 'Half Hug'), ('Bro Hug', 'Bro Hug'), ('Flying Hug', 'Flying Hug')])
    duration = SelectField('Hug Duration', choices=[('2', '2 seconds'), ('3', '3 seconds'), ('5', '5 seconds')])
    pat = SelectField("Pats", choices= [('None', 'None'), ('2', 2), ('3', 3)])
    sway = SelectField("Sway", choices=[('Yes', 'Yes'), ('No','No')])
    lift = SelectField("Lift", choices=[('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField("Send")
# create the close order form
class CloseOrderForm(Form):

    oid = IntegerField("Order ID: ", [validators.required("Value must be an integer.")])
    submit = SubmitField("Submit")
# create the delete customer form
class DeleteCustomerForm(Form):

    cid = IntegerField("Customer ID: ", [validators.required("Value must be an integer.")])
    submit = SubmitField("Submit")
# create the search customer form
class SearchCustomerForm(Form):

    cid = IntegerField("Customer ID: ", [validators.required("Value must be an integer.")])
    submit = SubmitField("Submit")
