# Disaster Response Pipeline

## Table of Contents

* [Summary](#summary)
* [File Descriptions](#file-descriptions)
* [Prerequisites](#prerequisites)
* [Running the Code](#running-the-code)
* [Results](#results)
* [Built With](#built-with)
* [License](#license)

## Summary

The goal of this project is to classify Tweets sent during a disaster to determine if they are relevant.  It consists of three steps.  The first step is to perform an ETL on data from two csv files and save the results to a SQLite database.  In the second step we create a machine learning model, evaluate it and save the final product as a pickle file.  All of this is finally brought together in a Web page that displays some data analysis of the existing data and can classify new messages entered into a search box.

## File Descriptions

* app/run.py - Runs the web application
* app/templates/go.html - Web page called when a search is executed
* app/templates/master.html - Home web page; also performs some data analysis
* data/DisasterResponse.db - SQLite database created in ETL process; output of process_data.py
* data/disaster_categories.csv - Training data of categories
* data/disaster_messages.csv - Training data of messages
* data/process_data.py - Python script that performs ETL
* models/classifier.pkl - Pickle file; output of train_classifier.py
* models/train_classifier.py - Trains and tests classification model

## Prerequisites

Flask 0.12.4
gunicorn 19.9.0
itsdangerous 0.24
Jinja2 2.10
json
nltk 3.2.5
numpy 1.12.1
pandas 0.23.3
pickle 0.7.4
plotly 2.0.15
python 3.6
scikit-learn 0.19.1
SQLAlchemy 1.2.18
SQLite3

## Running the Code

First, you have to execute the ETL pipeline that cleans data and stores it in a SQLite database.
```
python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db
```

Next, you have to run the machine learning pipeline that trains the classifier and saves it as a pickle file.
```
python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl
```

Finally, to start the web application, run this.
```
python run.py
```

## Results

Over half of the messages are catgorized as "related", while just shy of half fall into the genre of news.  With the categories, each message can be classified into multiple categories.  If we then look at the number of categories each message falls into, there is an almost logarithmic decline.  Most messages don't fit into any category, and very few fit into more than ten.  There is a massive drop-off at two categories.  Based on the rest of the graph, this might deserve more investigation.

As for the classification model, testing reveals the average f1-score of most categories to be at 0.9 or higher.

## Built With

* [Bootstrap](https://getbootstrap.com/docs/4.0/getting-started/introduction/#starter-template) - The web framework used
* [Plotly](https://cdn.plot.ly/plotly-latest.min.js) - API for generating graphs

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)