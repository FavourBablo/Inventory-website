# import Flask class, render_template function
from flask import Flask, render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # create a flask app named app
# let us prepare for database access using SQLAlchemy
# specify our database config url
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # this is added to avoid the warning message FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
# associate our Flask app object with SQLAlchemy, creating a new object named db. Our ORM models will inherit this db object
db = SQLAlchemy(app)

# """ app.app_context().push()


# with app.app_context():
#     db.create_all() """

# import the models
import models

# register admin_page blueprint
from admin import admin_page

app.register_blueprint(admin_page)


@app.route("/")
def home():
    return render_template('home.html', title="HOME")


@app.route("/products-and-services/")
def products_and_services():
    return render_template('products-and-services.html', title="PRODUCTS AND SERVICES")


@app.route("/about-us/")
def about_us():
    return render_template('about-us.html', title="ABOUT US")


# Let us track session across requests. We can for example use it to know if there is somebody logged in
# session helps us to track cookies in a more secured way also. You need to import it
# to use session your flask app needs a secret key.
# You can use the following command to generate a not-easy-to-guess secret key: python -c 'import os; print(os.urandom(24))'
app.secret_key = b'\xdf\x9c9\\\x99\xe7\x17\xbf\x17\x08m5`\x89~\xda\xe2\xb5(\xe9\xc0\xe24\x8b'


@app.route("/login/")
def login():
    # save off in session where we should go after login process. Session survives across requests.
    session['next_url'] = request.args.get('next', '/')  # get the next or use default '/' URL after login
    return render_template('login.html', title="SIGN IN", information="Enter login details")


@app.route("/process-login/", methods=['POST'])
def process_login():
    # Get the request object and the parameters sent.
    email = request.form['email']
    password = request.form['password']

    # call our custom defined function to authenticate user
    if (authenticateUser(email, password)):
        session['username'] = email
        session['userroles'] = ['admin']  # just hardcoding a list of roles for the sake of illustration. This should be read from database.
        return redirect(url_for('admin_page.admin'))
    else:
        error = 'Invalid user or password'
        return render_template('login.html', title="SIGN IN", information=error)


def authenticateUser(email, password):
    try:
        # First check to see if the user with the email can be found
        user = models.User.query.filter_by(email=email).first()
        # Return true if user is found and password is correct; else return false.
        # Notice that we are using the check_password() function defined in the User class
        # to check password which was stored in hash form.
        if user and user.check_password(password):  # return True only if both are true.
            return True
        else:
            return False
    except Exception as e:
        error = "An unexpected error occurred while processing your request." + str(e)
        return error


# Flask can also help up handle errors e.g. 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page-not-found.html'), 404


@app.route("/logout/")
def logout():
    session.pop('username', None)  # remove the item with key called username from the session
    session.pop('userroles', None)  # remove the item with key called userroles from the session
    return redirect(url_for('home'))


@app.route("/signup/")
def signup():
    return render_template('signup.html', title="SIGN UP", information="Use the form displayed to register")


@app.route("/process-signup/", methods=['POST'])
def process_signup():
    # Let's  get the request object and the parameters sent.

    firstname = request.form['firstname']
    lastname = request.form['lastname']
    othernames = request.form['othernames']
    email = request.form['email']
    password = request.form['password']

    # let save them to the database. Of course, is better to store password in a hash form.
    # You also need to confirm that there is no duplicate entry.

    # let's write to the database
    try:
        with app.app_context():
            user = models.User(firstname=firstname, lastname=lastname, othernames=othernames, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

    except Exception as e:
        information = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('signup.html', title="SIGN-UP", information=information)

    # Let us prepare feedback information
    information = 'User by name {}  {} successfully added. The login name is the email address {}.'.format(firstname,
                                                                                                           lastname,
                                                                                                           email)

    return render_template('signup.html', title="SIGN-UP", information=information)


def logged_in():
    if 'username' not in session:
        return False
    else:
        return True


@app.route("/no-anonymity-here/")
def no_anonymity_here():
    if not logged_in():
        return redirect(url_for('login', next='/no-anonymity-here/'))

    # username in session, continue
    return '''
    You have successfully entered a non-anonymous zone. Your are logged in as {}.
    <a href="/">Click here to go to the Home page</a>
    '''.format(session['username'])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)