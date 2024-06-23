import csv
import json

# Function to convert CSV to JSON with consistent casing and trimmed spaces
def csv_to_json(csv_file_path):
    data = []
    with open(csv_file_path, mode='r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            processed_row = {key.strip().lower(): value.strip() for key, value in row.items()}
            data.append(processed_row)
    return json.dumps(data, indent=4)

# Function to embed JSON data into HTML
def embed_json_in_html(json_data, html_file_path):
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV Data Display</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css">
    <style>
        #search-result {{
            margin-top: 20px;
        }}
    </style>
</head>
<body>

<h1>CSV Data Display</h1>

<div>
    <label for="search-input">Enter Search Values (comma separated):</label>
    <input type="text" id="search-input">
    <button onclick="searchData()">Search</button>
</div>

<div id="search-result">
    <!-- Search results will be displayed here -->
</div>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
<script>
    // Embedded JSON data
    const data = {json_data};

    // Function to search data based on input
    function searchData() {{
        const input = document.getElementById('search-input').value;
        const searchValues = input.split(',').map(value => value.trim().toLowerCase());
        const keys = Object.keys(data[0]);

        // Find the column to search in (first column)
        const searchColumn = keys[0];

        const results = data.filter(item => searchValues.some(value => (item[searchColumn] || "").toString().toLowerCase().includes(value)));

        const resultDiv = document.getElementById('search-result');
        resultDiv.innerHTML = ''; // Clear previous results

        if (results.length > 0) {{
            const table = document.createElement('table');
            table.id = 'result-table';
            table.className = 'display';
            const thead = document.createElement('thead');
            const tbody = document.createElement('tbody');
            const headerRow = document.createElement('tr');

            // Create table header
            keys.forEach(key => {{
                const th = document.createElement('th');
                th.textContent = key;
                headerRow.appendChild(th);
            }});
            thead.appendChild(headerRow);
            table.appendChild(thead);

            // Create table body
            results.forEach(result => {{
                const dataRow = document.createElement('tr');
                keys.forEach(key => {{
                    const td = document.createElement('td');
                    td.textContent = result[key];
                    dataRow.appendChild(td);
                }});
                tbody.appendChild(dataRow);
            }});
            table.appendChild(tbody);

            resultDiv.appendChild(table);

            // Initialize DataTable
            $('#result-table').DataTable();
        }} else {{
            resultDiv.textContent = 'No matching data found.';
        }}
    }}

    // Add event listener to trigger search on Enter key press
    document.getElementById('search-input').addEventListener('keyup', function(event) {{
        if (event.key === 'Enter') {{
            searchData();
        }}
    }});
</script>

</body>
</html>
    """

    # Insert the JSON data into the HTML template
    html_content = html_template.format(json_data=json_data)

    # Write the HTML content to the specified file
    with open(html_file_path, 'w') as html_file:
        html_file.write(html_content)

# Example usage
csv_file_path = 'data.csv'  # Path to your CSV file
html_file_path = 'output.html'  # Path to your output HTML file

# Convert CSV to JSON
json_data = csv_to_json(csv_file_path)

# Embed JSON data into HTML
embed_json_in_html(json_data, html_file_path)

