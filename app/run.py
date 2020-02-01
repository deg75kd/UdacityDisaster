import json
import plotly
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar, Pie, Scatter
from sklearn.externals import joblib
from sqlalchemy import create_engine


app = Flask(__name__)

def tokenize(text):
    """Tokenizes a text into words.

    Args:
        text: Text field to be tokenized

    Returns:
        List of the text's words in lowercase
    """

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('messages', engine)

# load model
model = joblib.load("../models/classifier.pkl")

# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    """Analyzes data and creates graphs
    
    Returns:
        Flask object for rendering graphs on webpage
    """
    
    # extract data for genre bar chart
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    
    # extract data for category bar chart
    df_cat = df.drop(['message', 'original', 'genre'], axis=1)
    cat_names = [col for col in df_cat.columns if col != 'id']
    df_cat = pd.melt(df_cat, id_vars=['id'], value_vars=cat_names)
    category_totals = df_cat.groupby('variable')['value'].sum()
    category_totals.sort_values(ascending=True, inplace=True)
    x_vals = category_totals.values.tolist()
    y_vals = category_totals.index.tolist()
    
    # extract data for graph of number of categories by messages
    df_message_cats = df_cat.groupby('id').sum()
    df_message_cats['count'] = 1
    df_message_cats = df_message_cats.groupby('value').sum()
    x_counts = df_message_cats.index.tolist()
    y_counts = df_message_cats['count'].values
    
    # create visuals
    graphs = [
        {
            'data': [
                Pie(
                    labels = genre_names,
                    values = genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        },
        {
            'data': [
                Bar(
                    x=x_vals,
                    y=y_vals,
                    orientation='h',
                    text=y_vals,
                    textposition='auto'
                )
            ],

            'layout': {
                'title': 'Distribution of Message Categories',
                'yaxis': {
#                    'ticks': "",
                    'showticklabels': False
                },
                'xaxis': {
                    'title': "Messages"
                },
                'autosize': False,
                'width': 500,
                'height': 1000,
                'showlegend': False
            }
        },
        {
            'data': [
                Scatter(
                    x = x_counts,
                    y = y_counts,
                    mode = 'lines+markers'
                )
            ],

            'layout': {
                'title': 'Distribution of Category Counts for Messages',
                'yaxis': {
                    'title': "Messages"
                },
                'xaxis': {
                    'title': "Number of Categories"
                }
            }
        }
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    """Processes search item from user

    Returns:
        Flask object for rendering results
    """

    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    """Runs web application"""
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()