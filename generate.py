import csv
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import re

# Function to convert CSV to JSON with consistent casing and trimmed spaces
def csv_to_json(csv_file_path):
    def clean_value(value):
        if value is None:
            return ""
        # Remove surrounding quotes if present
        value = re.sub(r'^"|"$', '', value.strip())
        return value

    data = []
    with open(csv_file_path, mode='r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            processed_row = {
                re.sub(r'^"|"$', '', key.strip().lower() if key else key): clean_value(value)
                for key, value in row.items()
            }
            data.append(processed_row)
    return json.dumps(data, indent=4)

# Function to ensure the key is 16, 24, or 32 bytes long
def adjust_key_length(key, length=32):
    if len(key) > length:
        return key[:length]
    return key.ljust(length)

# Function to encrypt JSON data
def encrypt_data(data, key):
    key = adjust_key_length(key).encode('utf-8')  # Adjust key length and convert to bytes
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return json.dumps({'iv': iv, 'ciphertext': ct})

# Function to embed encrypted JSON data into HTML
def embed_encrypted_data_in_html(encrypted_data, html_file_path):
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV Data Display</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css">
    <link rel="stylesheet" href="styles.css">
    <link rel="icon" href="logo.ico" type="image/x-icon">
</head>
<body>

<h1>CSV Data Display</h1>

<div class="container">
    <div class="input-group">
        <input type="password" id="key-input" placeholder="Enter decryption key">
        <button onclick="decryptData()">Decrypt</button>
    </div>

    <div id="search-section" style="display:none;">
        <div class="input-group">
            <input type="text" id="search-input" placeholder="Enter Search Values (comma separated)">
            <button onclick="searchData()">Search</button>
        </div>
        <div id="search-result">
            <!-- Search results will be displayed here -->
        </div>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
<script>
    // Encrypted JSON data
    const encryptedData = {encrypted_data};

    // Function to decrypt data
    function decryptData() {{
        const key = document.getElementById('key-input').value;
        try {{
            const decryptedData = JSON.parse(decrypt(encryptedData, key));
            window.data = decryptedData; // Set the decrypted data globally
            document.getElementById('search-section').style.display = 'block';
        }} catch (e) {{
            alert('Invalid key or data could not be decrypted.');
        }}
    }}

    // Decrypt function
    function decrypt(encrypted, key) {{
        const parsedData = JSON.parse(encrypted);
        const iv = CryptoJS.enc.Base64.parse(parsedData.iv);
        const ciphertext = CryptoJS.enc.Base64.parse(parsedData.ciphertext);
        const decrypted = CryptoJS.AES.decrypt({{
            ciphertext: ciphertext
        }}, CryptoJS.enc.Utf8.parse(key.padEnd(32)), {{
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        }});
        return decrypted.toString(CryptoJS.enc.Utf8);
    }}

    // Function to search data based on input
    function searchData() {{
        const input = document.getElementById('search-input').value;
        const searchValues = input.split(',').map(value => value.trim().toLowerCase());
        const keys = Object.keys(window.data[0]);

        // Find the column to search in (first column)
        const searchColumn = keys[0];

        const results = window.data.filter(item => searchValues.some(value => (item[searchColumn] || "").toString().toLowerCase().includes(value)));

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
                    td.setAttribute('data-label', key);
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

    // Add event listener to trigger decryption on Enter key press
    document.getElementById('key-input').addEventListener('keyup', function(event) {{
        if (event.key === 'Enter') {{
            decryptData();
        }}
    }});

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

    # Insert the encrypted JSON data into the HTML template
    html_content = html_template.format(encrypted_data=json.dumps(encrypted_data))

    # Write the HTML content to the specified file
    with open(html_file_path, 'w') as html_file:
        html_file.write(html_content)

# Example usage
csv_file_path = 'data.csv'  # Path to your CSV file
html_file_path = 'index.html'  # Path to your output HTML file
encryption_key = 'your-encryption-key'  # Must be 16, 24, or 32 bytes long

# Convert CSV to JSON
json_data = csv_to_json(csv_file_path)

# Encrypt JSON data
encrypted_data = encrypt_data(json_data, encryption_key)

# Embed encrypted JSON data into HTML
embed_encrypted_data_in_html(encrypted_data, html_file_path)

