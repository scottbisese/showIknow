from flask import Flask, render_template, request, redirect, url_for
# The below handles some deprecated dependencies in Python > 3.10 that Flask Navigation needs
import collections
collections.MutableSequence = collections.abc.MutableSequence
collections.Iterable = collections.abc.Iterable
from flask_navigation import Navigation
# Import Azure SQL helper code
from azuresqlconnector import *
  
app = Flask(__name__)

nav = Navigation(app)

# Initialize navigations
# Navigations have a label and a reference that ties to one of the functions below
nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Modal Example', 'modal'), 
    nav.Item('Form Example', 'form'),
    nav.Item('Display Table Example', 'table')
])

@app.route('/') 
def index():
    return render_template('form-example-home.html')

@app.route('/modal') 
def modal():
    return render_template('modal.html')

@app.route('/form') 
def form():
    return render_template('form.html')

# This function handles data entry from the form
@app.route('/form_submit', methods=['POST']) 
def form_submit():
    form_data1 = request.form['text1']
    form_data2 = request.form['text2']
    form_data3 = request.form['text3']

    print("Submitting data:")
    print('Text 1: ', form_data1)
    print('Text 2: ', form_data2)
    print('Text 3: ', form_data3)
    print(". . .")

    # Initialize SQL connection
    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()

    sql_query = f"""
        INSERT INTO FormExample.ExampleTable
        VALUES (
         '{form_data1}',
         '{form_data2}',
         '{form_data3}'
         );
        """

    cursor.execute(sql_query)

    print("Data submitted. . .")

    # IMPORTANT: The connection must commit the changes.
    conn.commit()

    print("Changes commited.")

    cursor.close()

    print("Redirecting. . .")

    # Redirect back to form page after the form is submitted
    return redirect(url_for('form'))

@app.route('/table') 
def table():

    # Initialize SQL connection
    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()

    sql_query = f"""
        SELECT * FROM FormExample.ExampleTable;
        """

    cursor.execute(sql_query)

    records = cursor.fetchall()

    cursor.close()

    return render_template('table.html', records=records)

if __name__ == '__main__': 
    app.run()