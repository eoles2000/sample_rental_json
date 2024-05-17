"""
File: json_processing.py
Author: Brian Allen
Version: 1.0
Description: This script processes a JSON file containing rental data, validates it against a predefined schema, stores it in an in-memory SQLite database, performs SQL queries to summarize the data, and optionally displays the results to the console.

Example 1:
python json_processing.py --path data.json --display
    - Process the JSON file "data.json" and display the summarized results to the console.

Example 2:
python json_processing.py --path data.json
    - Process the JSON file "data.json" without displaying the results to the console.
"""
import argparse
import pandas as pd
import pandera as pa
import sqlite3
from tabulate import tabulate
from termcolor import colored
import logging

# Set up logging configuration
logging.basicConfig(filename='json_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
display_console = True

def process_json(json_file_path):
    try:
        logging.info("Loading JSON file into a pandas DataFrame...")
        # Load JSON file into a pandas DataFrame
        df = pd.read_json(json_file_path)

        logging.info("Defining DataFrame schema for validation...")
        # Define our Schema so we can validate it
        schema = pa.DataFrameSchema({
            "type": pa.Column(pa.String,checks=[pa.Check.isin(["START","END"])],nullable=False),
            "id": pa.Column(pa.String,checks=[pa.Check.str_startswith("ABC")],nullable=False),
            "timestamp": pa.Column(pa.Timestamp, nullable=False),
            "comments": pa.Column(pa.String, nullable=True)
        })
        
        # Validate the data and capture validation errors
        schema.validate(df, lazy=True)

        logging.info("Connecting to in-memory SQLite database...")        
        #Connect to in memory sqlite
        #Not a fan of SQLite, but it is built into python and works fine for this. Would prefer a real database though
        conn = sqlite3.connect(':memory:')
        
        logging.info("Writing dataframe into a table...")
        #Write dataframe into a table
        df.to_sql('rentals',conn, index=False)
       
        my_summary_query = '''
        SELECT start_rentals.id as session_id,
               start_rentals.timestamp as start_time,
               end_rentals.timestamp as end_time,
               (strftime('%s', end_rentals.timestamp) - strftime('%s', start_rentals.timestamp)) / 3600 AS session_duration,
               CASE WHEN ((strftime('%s', end_rentals.timestamp) - strftime('%s', start_rentals.timestamp)) / 3600) > 24 THEN 1 ELSE 0 END AS rental_late,
               CASE WHEN length(end_rentals.comments) > 0 THEN 1 ELSE 0 END as rental_damaged
        FROM rentals as start_rentals
        INNER JOIN rentals as end_rentals ON start_rentals.id = end_rentals.id
        WHERE start_rentals.type = 'START'
        AND end_rentals.type = 'END'
        '''
     
        my_unreturned_query = '''
        SELECT start_rentals.id as session_id,
               start_rentals.timestamp as start_time,
               start_rentals.comments
        FROM rentals as start_rentals
        LEFT JOIN rentals as end_rentals ON start_rentals.id = end_rentals.id and end_rentals.type= 'END'
        WHERE start_rentals.type = 'START'
        and end_rentals.id IS NULL
        '''

        my_missing_start_query = '''
        SELECT end_rentals.id as session_id,
               end_rentals.timestamp as end_time,
               end_rentals.comments
        FROM rentals as end_rentals
        LEFT JOIN rentals as start_rentals ON end_rentals.id = start_rentals.id AND start_rentals.type = 'START'
        WHERE end_rentals.type = 'END'
        and start_rentals.id IS NULL
        '''

        logging.info("Executing queries and fetching data...")
        df_summary = pd.read_sql_query(my_summary_query, conn)
        df_unreturned = pd.read_sql_query(my_unreturned_query, conn)
        df_missing_start = pd.read_sql_query(my_missing_start_query, conn)

        logging.info("Closing database connection...")
        conn.close()

        # Display the records and write to disk
        if df_summary.empty == False:
            print_table(df_summary,"Summary","green")
        if df_unreturned.empty == False:
            print_table(df_unreturned,"Unreturned","yellow")
        if df_missing_start.empty == False:
            print_table(df_missing_start,"Missing Starts","magenta")
        
    except FileNotFoundError:
        logging.error("Error: File not found.")
        print(colored("Error: File not found.","red"))
    except ValueError:
        logging.error("Error: Invalid JSON format.")
        print(colored("Error: Invalid JSON format.","red"))
    except pa.errors.SchemaErrors as exc:
        # If there are schema errors, display them nicely in a DataFrame
        error_df = pd.DataFrame(exc.failure_cases)
        logging.error("Schema validation failed. Errors:")
        logging.error(error_df)
        print_table(error_df,"Errors","red")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(colored("An unknown error occurred, please see the log","red"))
        
def print_table(df,title_name,title_color):
    logging.info("Displaying " + title_name + " table...")
    #write to csv file
    df.to_csv(r'./output_csv/output_' + title_name + '.txt', header='keys', index=None, sep=' ', mode='a')
    #display to the console
    if display_console:
        print(colored(tabulate([title_name]),title_color))
        print(colored(tabulate(df,headers="keys",tablefmt="pretty"),title_color))
    
def main(args):
    global display_console
    if args.display:
        display_console = True
    else:
        display_console = False
    # Process the file and provide summarized data
    process_json(args.path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='JSON Processing Arguments')
    parser.add_argument('--path',
                        required=True,
                        help='Location of the JSON file')
    parser.add_argument('--display',
                        action="store_true",
                        help='Display the results to console')
    args = parser.parse_args()
    main(args)
