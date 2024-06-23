# CSV to JSON and HTML Converter

This project converts CSV data to JSON format and embeds it into an HTML file for display. The HTML file uses DataTables for better data presentation and includes a search feature. The script ensures consistent casing and trimmed spaces, removing any extra quotes from the CSV data.

## Features

- Convert CSV data to JSON with consistent formatting.
- Embed JSON data into an HTML file.
- Display data using DataTables with search functionality.
- Styled using external CSS with SFU colors.

## Prerequisites

- Python 3.x
- Required Python libraries: `csv`, `json`, `re`

## Usage

1. Place your CSV file in the same directory as the script or specify the path to your CSV file.
2. Run the Python script to generate the HTML file.
3. Open the generated HTML file in a web browser to view the data.

### Example Usage

```python
# Example usage
csv_file_path = 'data.csv'  # Path to your CSV file
html_file_path = 'index.html'  # Path to your output HTML file

# Convert CSV to JSON
json_data = csv_to_json(csv_file_path)

# Embed JSON data into HTML
embed_json_in_html(json_data, html_file_path)
```

### Instructions:

1. Save the provided text as `README.md`.
2. Ensure you have the `generate.py` script and `styles.css` file in your project directory.
3. Download sample CSV files from [JBurkardt's website](https://people.sc.fsu.edu/~jburkardt/data/csv/csv.html) and place them in your project directory for testing.

This README file provides comprehensive instructions for using the project, including acknowledgments and references.

### Sample CSV Files

You can find sample CSV files for testing at [JBurkardt's website](https://people.sc.fsu.edu/~jburkardt/data/csv/csv.html).

## Files

- `generate.py`: The main Python script to convert CSV to JSON and generate the HTML file.
- `styles.css`: The CSS file for styling the HTML output.
- `data.csv`: Sample CSV file (not included, please download from the link above).

## Acknowledgements

This project was developed with the assistance of GPT, provided by OpenAI, and uses sample CSV data from [JBurkardt's website](https://people.sc.fsu.edu/~jburkardt/data/csv/csv.html).

## License

This project is licensed under the MIT License. See the LICENSE file for details.

<pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span></span></div></div></pre>
