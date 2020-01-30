import sys
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    # load csv files
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    # merge dataframes
    df_merge = pd.merge(messages, categories, on='id')
    
    return df_merge

def clean_data(df):
    # split categories into separate columns
    df_cat = df['categories'].str.split(';', expand=True)
    row = df_cat.head(1)
    category_colnames = row.apply(lambda x: x.str[:-2]).values[0]
    df_cat.columns = category_colnames
    # convert category values to numbers
    for column in category_colnames:
        df_cat[column] = pd.to_numeric(df_cat[column].str[-1:])
    # replace original categories column with new columns
    df = df.drop('categories', axis=1)
    df = pd.merge(df, df_cat, left_index=True, right_index=True)
    # drop duplicates
    df = df.drop_duplicates()
	
    return df

def save_data(df, database_filename):
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('messages', engine, index=False)
    return None

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()