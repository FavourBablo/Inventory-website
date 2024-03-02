from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
import models
from app import app

admin_page = Blueprint('admin_page', __name__, template_folder='templates/admin')

# let us add an app route for admin index page that requires login to access
@admin_page.route("/admin/")
def admin():
    if not logged_in():
        return redirect(url_for('login', next='/admin/'))
    # username in session and user has admin role, continue
    return render_template('index.html', title="ADMIN", information="Here you can administer products, services, etc. Click on what you would like to do")

@admin_page.route("/admin/create-all-tables/")
def create_all_tables():
    # if not logged_in():
    #    return redirect(url_for('login', next='/admin/'))

    # The SQLAlchemy function below does not allow change of schema. To allow schema change, use Flask-Migrate instead
    try:
        with app.app_context():
            models.db.create_all()
    except Exception as e:
        return 'Tables not created. Reason: {}'.format(e.__cause__)

    return 'Tables successfully created!'


@admin_page.route("/admin/products/")
def products():
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))
    # username in session, continue
    # get our registered products from the database
    with app.app_context():
        products = models.Product.query.all()
    # check whether when products route was called using redirect, information was passed. If not passed, use default message  'Here you can administer products'
    information = request.args.get('information', 'Here you can administer products')
    # check whether when products route was called using redirect, css was passed. If not passed, use default css  'normal'
    css = request.args.get('css', 'normal')
    return render_template('products.html', title="ADMINISTER PRODUCTS", information=information, css=css, products=products)



@admin_page.route("/admin/products/process-product-add/", methods=['POST','GET'])
def process_product_add():
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))
    # username in session, continue

    if request.method != 'POST':

        # return to products.html page containing add form. Only POST method is allowed
        error = 'Please use the form to add new products'
        return render_template('products.html', title="ADMINISTER PRODUCTS", information=error, css="error")

    # No problem so far, get the request object and the parameters sent.
    name = request.form['name']
    code = request.form['code']
    description = request.form['description']
    price_per_unit = request.form['price_per_unit']
    product_inception_date = request.form['product_inception_date']


    # let us write to the database
    try:
        with app.app_context():
            product = models.Product(name=name, code=code, description=description, price_per_unit=price_per_unit,product_inception_date=product_inception_date)
            models.db.session.add(product)
            models.db.session.commit()

    except Exception as e:
        error = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('products.html', title="ADMINISTER PRODUCTS", information=error, css="error")

    # no error, proceed
    return redirect(url_for('admin_page.products', information="Add successful", css="success"))

@admin_page.route("/admin/products/edit/<int:orderid>/", methods=['POST','GET'])
def product_edit(orderid):
    # check database for the product to edit
    with app.app_context():
        product = models.Product.query.filter_by(orderid=orderid).first()
        # send to the edit form
        return render_template('product-edit.html', product=product)


@admin_page.route("/admin/products/process-product-edit/<int:orderid>/", methods=['POST', 'GET'])
def process_product_edit(orderid):
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))
    # username in session and admin role, continue

    if request.method != 'POST':

        # redirect to signup form. Only POST method is allowed
        error = 'Please use the form to edit products'
        return render_template('products.html', title="ADMINISTER PRODUCTS", information=error, css="error")

    # No problem so far, get the request object and the parameters sent.
    name = request.form['name']
    code = request.form['code']
    description = request.form['description']
    price_per_unit = request.form['price_per_unit']
    product_inception_date = request.form['product_inception_date']


    # let's update the database
    try:
        with app.app_context():
            # Get the existing data from database as object
            product = models.Product.query.filter_by(orderid=orderid).first()
            # Update the fields
            product.name = name
            product.code = code
            product.description = description
            product.price_per_unit = price_per_unit
            product.product_inception_date = product_inception_date
            # commit
            models.db.session.commit()

    except Exception as e:
        error = 'Could not update product. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.products', information="Update not successful", css="error"))

    return redirect(url_for('admin_page.products', information="Update successful", css="success"))

@admin_page.route("/admin/products/delete/<int:orderid>/", methods=['POST', 'GET'])
def product_delete(orderid):
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))
    # username in session and admin role, continue

    # No problem so far
    # let's update the database
    try:
        with app.app_context():
        # Get the existing data from database as object
         product = models.Product.query.filter_by(orderid=orderid).first()
        # Delete the record
         models.db.session.delete(product)
        # commit
         models.db.session.commit()

    except Exception as e:
        error = 'Could not delete product. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.products', information="Delete not successful", css="error"))

    return redirect(url_for('admin_page.products', information="Delete successful", css="success"))

@admin_page.route("/admin/order/")
def order():
    if not logged_in():
        return redirect(url_for('login', next='/admin/order/'))
    # username in session, continue
    # get our registered order from the database
    with app.app_context():
        order = models.Order.query.all()
    # check whether when products route was called using redirect, information was passed. If not passed, use default message  'Here you can administer order'
    information = request.args.get('information', 'Here you can administer order')
    # check whether when order route was called using redirect, css was passed. If not passed, use default css  'normal'
    css = request.args.get('css', 'normal')
    return render_template('order.html', title="ADMINISTER ORDER", information=information, css=css, orders=order)



@admin_page.route("/admin/order/process-order-add/", methods=['POST','GET'])
def process_order_add():
    if not logged_in():
        return redirect(url_for('login', next='/admin/order/'))
    # username in session, continue

    if request.method != 'POST':

        # return to order.html page containing add form. Only POST method is allowed
        error = 'Please use the form to add new order'
        return render_template('order.html', title="ADMINISTER ORDER", information=error, css="error")

    # No problem so far, get the request object and the parameters sent.
    order_id = request.form['order_id']
    product_name = request.form['product_name']
    quantity = request.form['quantity']
    customer_id = request.form['customer_id']


    # let's write to the database
    try:
        with app.app_context():
            order = models.Order(order_id=order_id,product_name=product_name, quantity=quantity, customer_id=customer_id)
            models.db.session.add(order)
            models.db.session.commit()

    except Exception as e:
        error = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('order.html', title="ADMINISTER ORDER", information=error, css="error")

    # no error, continue
    return redirect(url_for('admin_page.order', information="Add successful", css="success"))

@admin_page.route("/admin/order/edit/<int:order_id>/", methods=['POST','GET'])
def order_edit(order_id):
    # check database for the product to edit
    with app.app_context():
        order = models.Order.query.filter_by(order_id=order_id).first()
        # send to the edit form
        return render_template('order-edit.html', order=order)


@admin_page.route("/admin/order/process-order-edit/<int:order_id>/", methods=['POST', 'GET'])
def process_order_edit(order_id):
    if not logged_in():
        return redirect(url_for('login', next='/admin/order/'))
    # username in session and admin role, continue

    if request.method != 'POST':
        # redirect to signup form. Only POST method is allowed
        error = 'Please use the form to edit order'
        return render_template('order.html', title="ADMINISTER ORDER", information=error, css="error")
    # No problem so far, get the request object and the parameters sent.
    product_name = request.form['product_name']
    quantity = request.form['quantity']
    customer_id = request.form['customer_id']
    # let's update the database
    try:
        with app.app_context():
            # Get the existing data from database as object
            order = models.Order.query.filter_by(order_id=order_id).first()
            # Update the fields
            order.order_id = order_id
            order.product_name = product_name
            order.quantity = quantity
            order.customer_id= customer_id
            # commit
            models.db.session.commit()

    except Exception as e:
        error = 'Could not update order. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.order', information=error, css="error"))

    return redirect(url_for('admin_page.order', information="Update successful", css="success"))

@admin_page.route("/admin/order/delete/<int:order_id>/", methods=['POST', 'GET'])
def order_delete(order_id):
    if not logged_in():
        return redirect(url_for('login', next='/admin/order/'))
    # username in session and admin role, continue

    # No problem so far
    # let's update the database
    try:
        with app.app_context():
        # Get the existing data from database as object
         order = models.Order.query.filter_by(order_id=order_id).first()
        # Delete the record
         models.db.session.delete(order)
        # commit
         models.db.session.commit()

    except Exception as e:
        error = 'Could not delete order. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.order', information="Delete not successful", css="error"))

    return redirect(url_for('admin_page.order', information="Delete successful", css="success"))

@admin_page.route("/admin/customer/")
def customer():
    if not logged_in():
        return redirect(url_for('login', next='/admin/customer/'))
    # username in session, continue
    # get our registered order from the database
    with app.app_context():
        customer = models.Customer.query.all()
    # check whether when products route was called using redirect, information was passed. If not passed, use default message  'Here you can administer order'
    information = request.args.get('information', 'Here you can register customer')
    # check whether when order route was called using redirect, css was passed. If not passed, use default css  'normal'
    css = request.args.get('css', 'normal')
    return render_template('customer.html', title="REGISTER CUSTOMER", information=information, css=css, customers=customer)



@admin_page.route("/admin/customer/process-customer-add/", methods=['POST','GET'])
def process_customer_add():
    if not logged_in():
        return redirect(url_for('login', next='/admin/customer/'))
    # username in session, continue

    if request.method != 'POST':

        # return to order.html page containing add form. Only POST method is allowed
        error = 'Please use the form to add new customer'
        return render_template('customer.html', title="REGISTER CUSTOMER", information=error, css="error")

    # No problem so far, get the request object and the parameters sent.
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    # let's write to the database
    try:
        with app.app_context():
            customer = models.Customer(first_name=first_name, last_name=last_name, email=email)
            models.db.session.add(customer)
            models.db.session.commit()

    except Exception as e:
        import traceback
        traceback.print_exc()
        error = 'Could not submit. The error message is {}'.format(str(e))
        return render_template('customer.html', title="REGISTER ORDER", information=error, css="error")
    # no error, continue
    return redirect(url_for('admin_page.customer', information="Add successful", css="success"))

@admin_page.route("/admin/customer/edit/<int:customer_id>/", methods=['POST','GET'])
def customer_edit(customer_id):
    # check database for the product to edit
    with app.app_context():
        customer = models.Customer.query.filter_by(customer_id=customer_id).first()
        # send to the edit form
        return render_template('customer-edit.html', customer=customer)


@admin_page.route("/admin/customer/process-customer-edit/<int:customer_id>/", methods=['POST', 'GET'])
def process_customer_edit(customer_id):
    if not logged_in():
        return redirect(url_for('login', next='/admin/customer/'))
    # username in session and admin role, continue

    if request.method != 'POST':
        # redirect to signup form. Only POST method is allowed
        error = 'Please use the form to edit order'
        return render_template('customer.html', title="REGISTER CUSTOMER", information=error, css="error")
    # No problem so far, get the request object and the parameters sent.
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']


    # let's update the database
    try:
        with app.app_context():
            # Get the existing data from database as object
            customer = models.Customer.query.filter_by(customer_id=customer_id).first()
            # Update the fields
            customer.first_name = first_name
            customer.last_name = last_name
            customer.email = email
            # commit
            models.db.session.commit()


    except Exception as e:
        error = 'Could not update customer. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.customer', information=error, css="error"))

    return redirect(url_for('admin_page.customer', information="Update successful", css="success"))

@admin_page.route("/admin/customer/delete/<int:customer_id>/", methods=['POST', 'GET'])
def customer_delete(customer_id):
    if not logged_in():
        return redirect(url_for('login', next='/admin/customer/'))
    # username in session and admin role, continue

    # No problem so far
    # let's update the database
    try:
        with app.app_context():
        # Get the existing data from database as object
         customer = models.Customer.query.filter_by(customer_id=customer_id).first()
        # Delete the record
         models.db.session.delete(customer)
        # commit
         models.db.session.commit()

    except Exception as e:
        error = 'Could not delete customer. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.customer', information="Delete not successful", css="error"))

    return redirect(url_for('admin_page.customer', information="Delete successful", css="success"))

def logged_in():
    if 'username' not in session or 'admin' not in session['userroles']:
        return False
    else:
        return True
