# JSON Processing Script

## Overview
This script processes a JSON file containing rental data, validates it against a predefined schema, stores it in an in-memory SQLite database, performs SQL queries to summarize the data, and optionally displays the results to the console.

## Setup
1. **Install Python**: Make sure you have Python installed on your system. You can download it from [here](https://www.python.org/downloads/).

2. **Install Required Libraries**: Install the required Python libraries using pip:
   ```
   pip install -r requirements.txt
   ```

3. **Clone Repository**: Clone this repository to your local machine:
   ```
   git clone <repository-url>
   ```

## Usage
Run the script with the following command:
```
python json_processing.py --path <path-to-json-file> [--display]
```

- `--path`: Specify the path to the JSON file containing rental data.
- `--display`: (Optional) Display the summarized results to the console.

### Examples
1. **Process JSON file and display results to console**:
   ```
   python json_processing.py --path data.json --display
   ```

2. **Process JSON file without displaying results to console**:
   ```
   python json_processing.py --path data.json
   ```

## Libraries Used
- [pandas](https://pandas.pydata.org/): Used for data manipulation and analysis.
- [pandera](https://pandera.readthedocs.io/en/stable/): Used for data validation.
- [tabulate](https://pypi.org/project/tabulate/): Used for tabular data display.
- [termcolor](https://pypi.org/project/termcolor/): Used for colored text output.

