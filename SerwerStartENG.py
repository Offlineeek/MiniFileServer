from flask import Flask, request, render_template_string, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

# Path where files will be stored
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML page with two tabs - Upload and Files
HTML_TEMPLATE = '''
<!doctype html
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>File Upload</title>
  <style>
    body { font-family: Arial, sans-serif; background-color: #f4f4f9; }
    .container { width: 60%; margin: 0 auto; padding: 20px; background-color: white; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
    h1 { text-align: center; }
    .tabs { display: flex; justify-content: center; margin-bottom: 20px; }
    .tabs button { padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer; margin: 0 5px; }
    .tabs button:hover { background-color: #45a049; }
    .tabs button.active { background-color: #45a049; }
    .content { display: none; }
    .content.active { display: block; }
    input[type="file"] { display: block; margin: 20px auto; }
    button { display: block; margin: 0 auto; padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
    button:hover { background-color: #45a049; }
    .file-list { margin-top: 20px; }
    .file-item { margin: 5px 0; }
    .file-item a { text-decoration: none; color: #4CAF50; }
    .file-item a:hover { text-decoration: underline; }
    .file-item button { background-color: #f44336; color: white; border: none; cursor: pointer; margin-left: 10px; }
    .file-item button:hover { background-color: #e53935; }
  </style>
</head>
<body>
  <div class="container">
    <h1>File Upload System</h1>
    <div class="tabs">
      <button class="tab-button" onclick="showTab('uploadTab')">Upload</button>
      <button class="tab-button" onclick="showTab('filesTab')">Files</button>
    </div>
    
    <!-- Upload Tab -->
    <div id="uploadTab" class="content active">
      <h2>Select a file to upload</h2>
      <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Upload File</button>
      </form>
      {% if message %}
        <p>{{ message }}</p>
      {% endif %}
    </div>
    
    <!-- Files Tab -->
    <div id="filesTab" class="content">
      <h2>Files in the Upload Directory:</h2>
      <div class="file-list">
        {% for file in files %}
          <div class="file-item">
            <a href="{{ url_for('download_file', filename=file) }}">{{ file }}</a>
            <form method="POST" action="{{ url_for('delete_file', filename=file) }}" style="display:inline;">
              <button type="submit">Delete</button>
            </form>
          </div>
        {% endfor %}
      </div>
    </div>
  </div>

  <script>
    function showTab(tabId) {
      var tabs = document.querySelectorAll('.content');
      var buttons = document.querySelectorAll('.tab-button');
      
      tabs.forEach(function(tab) {
        tab.classList.remove('active');
      });
      
      buttons.forEach(function(button) {
        button.classList.remove('active');
      });
      
      document.getElementById(tabId).classList.add('active');
      event.target.classList.add('active');
    }
  </script>
</body>
</html>
'''

# Function to upload the file
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files['file']
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            return render_template_string(HTML_TEMPLATE, files=os.listdir(UPLOAD_FOLDER), message=f"File '{file.filename}' has been uploaded.")
    
    return render_template_string(HTML_TEMPLATE, files=os.listdir(UPLOAD_FOLDER), message=None)

# Function to download the file
@app.route("/uploads/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Function to delete the file
@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
