from flask import Flask, render_template, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return """
    <h2>Send Data from iPhone to Windows</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" multiple>
        <button type="submit">Upload</button>
    </form>
    """

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("file")
    for file in files:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return "<h3>Upload complete! Files saved in Windows folder.</h3>"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
