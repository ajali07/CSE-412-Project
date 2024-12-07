from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv("config.env")  # Loading environmental variables

app = Flask(__name__)

# Setting database config, you can change the config.env file to fit your database
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Defining database models for Customer, Invoice, Line, Product, Vendor
class Customer(db.Model):
    __tablename__ = "CUSTOMER"
    CUS_CODE = db.Column(db.Integer, primary_key=True)
    CUS_LNAME = db.Column(db.String)
    CUS_FNAME = db.Column(db.String)
    CUS_INITIAL = db.Column(db.String)
    CUS_AREACODE = db.Column(db.String)
    CUS_PHONE = db.Column(db.String)
    CUS_BALANCE = db.Column(db.Float)

class Invoice(db.Model):
    __tablename__ = "INVOICE"
    INV_NUMBER = db.Column(db.Integer, primary_key=True)
    CUS_CODE = db.Column(db.Integer)
    INV_DATE = db.Column(db.String)

class Line(db.Model):
    __tablename__ = "LINE"
    INV_NUMBER = db.Column(db.Integer)
    LINE_NUMBER = db.Column(db.Integer, primary_key=True)
    P_CODE = db.Column(db.String)
    LINE_UNITS = db.Column(db.Integer)
    LINE_PRICE = db.Column(db.Float)

class Product(db.Model):
    __tablename__ = "PRODUCT"
    P_CODE = db.Column(db.String, primary_key=True)
    P_DESCRIPT = db.Column(db.String)
    P_INDATE = db.Column(db.String)
    P_QOH = db.Column(db.Integer)
    P_MIN = db.Column(db.Integer)
    P_PRICE = db.Column(db.Float)
    P_DISCOUNT = db.Column(db.Float)
    V_CODE = db.Column(db.Integer)

class Vendor(db.Model):
    __tablename__ = "VENDOR"
    V_CODE = db.Column(db.Integer, primary_key=True)
    V_NAME = db.Column(db.String)
    V_CONTACT = db.Column(db.String)
    V_AREACODE = db.Column(db.String)
    V_PHONE = db.Column(db.String)
    V_STATE = db.Column(db.String)
    V_ORDER = db.Column(db.Integer)

model_mapping = {
    'Customer': Customer,
    'Invoice': Invoice,
    'Line': Line,
    'Product': Product,
    'Vendor': Vendor
}

# Helper function to process query data
def process_data(query_result):
    data = [vars(obj) for obj in query_result]
    for d in data:
        d.pop('_sa_instance_state', None)  
    return data

#routing to currect pages
@app.route('/')
def home():
    return render_template('index.html', title="Home", data=[], columns=[])

@app.route('/advanced_search', methods=['POST'])
def advanced_search():
    table = request.form['table']
    attribute = request.form['attribute']
    search_term = request.form['search_term']

    model = model_mapping.get(table)
    if model is None:
        return "Error: Table not found", 404

    if hasattr(model, attribute):
        column = getattr(model, attribute)
        # Check if the column type is a string type; adjust if using different dialects or custom types
        if isinstance(column.type, db.String):
            results = db.session.query(model).filter(column.contains(search_term)).all()
        else:
            # For numerical columns, we cast them to text for 'LIKE' operation
            results = db.session.query(model).filter(db.cast(column, db.String).like(f'%{search_term}%')).all()
        
        processed_data = process_data(results)
        columns = [column.name for column in model.__table__.columns]

        return render_template(
            'index.html',
            title=f"Search Results for {table}",
            data=processed_data,
            columns=columns
        )
    else:
        return "Error: Attribute not found", 404

@app.route('/customer')
def view_customers():
    customers = Customer.query.all()
    processed_data = process_data(customers)
    return render_template(
        'index.html',
        title="Customers",
        data=processed_data,
        columns=["CUS_CODE", "CUS_LNAME", "CUS_FNAME", "CUS_INITIAL", "CUS_AREACODE", "CUS_PHONE", "CUS_BALANCE"]
    )

@app.route('/vendor')
def view_vendors():
    vendors = Vendor.query.all()
    processed_data = process_data(vendors)
    return render_template(
        'index.html',
        title="Vendors",
        data=processed_data,
        columns=["V_CODE", "V_NAME", "V_CONTACT", "V_AREACODE", "V_PHONE", "V_STATE", "V_ORDER"]
    )

@app.route('/line')
def view_lines():
    lines = Line.query.all()
    processed_data = process_data(lines)
    return render_template(
        'index.html',
        title="Lines",
        data=processed_data,
        columns=["INV_NUMBER", "LINE_NUMBER", "P_CODE", "LINE_UNITS", "LINE_PRICE"]
    )

@app.route('/invoices')
def view_invoices():
    invoices = Invoice.query.all()
    processed_data = process_data(invoices)
    return render_template(
        'index.html',
        title="Invoices",
        data=processed_data,
        columns=["INV_NUMBER", "CUS_CODE", "INV_DATE"]
    )

@app.route('/products')
def view_products():
    products = Product.query.all()
    processed_data = process_data(products)
    return render_template(
        'index.html',
        title="Products",
        data=processed_data,
        columns=["P_CODE", "P_DESCRIPT", "P_INDATE", "P_QOH", "P_MIN", "P_PRICE", "P_DISCOUNT", "V_CODE"]
    )

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)