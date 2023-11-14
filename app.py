from flask import Flask, render_template, request, redirect, url_for
# The below handles some deprecated dependencies in Python > 3.10 that Flask Navigation needs
import collections
collections.MutableSequence = collections.abc.MutableSequence
collections.Iterable = collections.abc.Iterable
from flask_navigation import Navigation
# Import Azure SQL helper code
from azuresqlconnector import *
import requests
  
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

    # Your existing SQL code
    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()

    # Update SQL query with extracted values
    sql_query = """
    INSERT INTO FormExample.ExampleTable (Sentence, Sentiment, Positive_score)
    VALUES (?, ?, ?);
    """

    # Assuming your table has three columns, modify the query accordingly
    cursor.execute(sql_query, form_data1, "Not Available", 0)
    print("Data submitted. . .")
    # IMPORTANT: The connection must commit the changes.
    conn.commit()
    print("Changes committed.")
    

    

    url = "https://langaisamueltrujillo.cognitiveservices.azure.com/language/:analyze-text?api-version=2023-04-15-preview"
    

    headers = {
        "Ocp-Apim-Subscription-Key": "9640d8a2503542daa89851a93feec843",
        "Content-Type": "application/json",
    }

    data = {
        "kind": "SentimentAnalysis",
        "parameters": {
            "modelVersion": "latest",
            "opinionMining": "True"
        },
        "analysisInput": {
            "documents": [
                {
                    "id": "1",
                    "language": "en",
                    "text": form_data1
                }
            ]
        }
    }
    response = requests.post(url, headers=headers, json=data)

    sentiment_result = "Not Available"
    sentence = "Not Available"
    positive_score = 0

    if response.status_code == 200:
        result = response.json()
        if 'results' in result and 'documents' in result['results'] and len(result['results']['documents']) > 0:
            document = result['results']['documents'][0]
            if 'sentiment' in document:
                sentiment_result = document['sentiment']
            if 'sentences' in document and len(document['sentences']) > 0:
                sentence = document['sentences'][0]['text']
            if 'confidenceScores' in document and 'positive' in document['confidenceScores']:
                positive_score = document['confidenceScores']['positive']

        cursor.execute(sql_query, sentence, sentiment_result, positive_score)
        conn.commit()
            
 
    else:
        print(f"Sentiment Analysis failed with status code {response.status_code}")
        print(f"Response content: {response.content}")

        # Add a return statement for the failed case
        return redirect(url_for('table'))

    cursor.close()
    # Redirect back to form page only if sentiment analysis is successful
    return redirect(url_for('table'))

@app.route('/table') 
def table():

    # Initialize SQL connection
    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()

    sql_query = f"""
        SELECT Sentence, Sentiment, Positive_score FROM FormExample.ExampleTable;
    """

    cursor.execute(sql_query)

    records = cursor.fetchall()

    cursor.close()

    return render_template('table.html', records=records)

if __name__ == '__main__': 
    app.run()
