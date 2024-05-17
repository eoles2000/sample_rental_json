# Considerations

This markdown file outlines some considerations for the `process_json_pandas.py` script, including scheduling, potential future iterations, and assumptions about the JSON files.

## Scheduling the Script

### Windows (Task Scheduler)
- **Step 1**: Open Task Scheduler.
- **Step 2**: Create a task, specifying the Python executable and the script path as the action.
- **Step 3**: Set up triggers to define when the task should run, such as daily, weekly, or monthly.

### Unix-like Systems (Cron Job)
- **Step 1**: Open the terminal and type `crontab -e`.
- **Step 2**: Add a new line with the schedule and command to run the script.
- **Step 3**: Save the changes and exit the editor.

## Future Iterations
- **Logging Improvements**: Enhance logging with more detailed information, including debugging messages and error handling.
- **Performance Optimization**: Explore ways to optimize script performance, especially for large JSON files or databases.
- **Duplicate Checks**: Add checks for duplicate START and END sessions_ids.
- **User Interaction**: Implement command-line options for more user interaction, such as specifying output formats (such as parquet) or filtering criteria.
- **Unit Testing**: Implement unit tests that can be ran in an automated fashion so we know if changes to the script are working as designed.

## Assumptions about JSON Files
- **Schema Consistency**: Assumes that JSON files adhere to a consistent schema defined by the script.
- **Data Quality**: Assumes that JSON files contain valid and clean data without major inconsistencies or errors.
- **Timestamp Format**: Assumes that timestamps in the JSON files are in a compatible format with Pandas' `Timestamp` data type.
