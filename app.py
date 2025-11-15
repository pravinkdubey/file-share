from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
        return """
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <title>Send Data from iPhone to Windows</title>
            <style>
                :root{--bg:#f8fafc;--card:#ffffff;--accent:#007aff}
                html,body{height:100%;margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,'Helvetica Neue',Arial}
                body{background:var(--bg);display:flex;align-items:center;justify-content:center;padding:20px}
                .card{width:100%;max-width:540px;background:var(--card);border-radius:12px;box-shadow:0 6px 18px rgba(0,0,0,.06);padding:20px}
                h2{margin:0 0 12px 0;font-size:18px}
                p{margin:0 0 14px 0;color:#444}
                .file-label{display:block;padding:14px;border-radius:10px;border:2px dashed #e6e9ef;text-align:center;color:#666;background:#fafbff;margin-bottom:12px}
                .file-input{display:none}
                .btn{display:inline-block;background:var(--accent);color:#fff;padding:12px 16px;border-radius:10px;border:none;font-size:16px;text-align:center}
                .files-list{margin:8px 0 12px 0;font-size:14px;color:#333}
                .progress{height:10px;background:#e6e9ef;border-radius:8px;overflow:hidden}
                .progress > i{display:block;height:100%;background:linear-gradient(90deg,var(--accent),#0051a8);width:0}
                .status{font-size:13px;color:#555;margin-top:10px}
                @media (prefers-color-scheme:dark){:root{--bg:#0b1220;--card:#071022;color:#dbeafe}}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>Send Files from iPhone</h2>
                <p>Choose photos, videos, or files to upload to this Windows machine.</p>

                <form id="uploadForm">
                    <label class="file-label" for="fileInput">Tap to select files (or use Share → Safari → Files)</label>
                    <input id="fileInput" class="file-input" type="file" name="file" multiple accept="*/*">

                    <div class="files-list" id="filesList">No files selected</div>

                    <div class="progress" aria-hidden="true"><i id="progressBar"></i></div>
                    <div class="status" id="status"></div>

                    <div style="display:flex;gap:8px;margin-top:12px">
                        <button type="button" id="chooseBtn" class="btn">Choose Files</button>
                        <button type="submit" id="uploadBtn" class="btn" style="background:#22c55e">Upload</button>
                    </div>
                </form>
            </div>

            <script>
                const fileInput = document.getElementById('fileInput');
                const chooseBtn = document.getElementById('chooseBtn');
                const filesList = document.getElementById('filesList');
                const uploadForm = document.getElementById('uploadForm');
                const progressBar = document.getElementById('progressBar');
                const status = document.getElementById('status');

                chooseBtn.addEventListener('click', () => fileInput.click());

                fileInput.addEventListener('change', () => {
                    const files = Array.from(fileInput.files || []);
                    if (!files.length) { filesList.textContent = 'No files selected'; return }
                    filesList.innerHTML = files.map(f => `<div> • ${escapeHtml(f.name)} (${Math.round(f.size/1024)} KB)</div>`).join('');
                });

                uploadForm.addEventListener('submit', function(e){
                    e.preventDefault();
                    const files = Array.from(fileInput.files || []);
                    if (!files.length){ status.textContent='No files selected'; return }

                    const fd = new FormData();
                    files.forEach(f => fd.append('file', f));

                    const xhr = new XMLHttpRequest();
                    xhr.open('POST', '/upload');

                    xhr.upload.onprogress = function(ev){
                        if (!ev.lengthComputable) return;
                        const pct = Math.round((ev.loaded/ev.total)*100);
                        progressBar.style.width = pct + '%';
                        status.textContent = 'Uploading — ' + pct + '%';
                    };

                    xhr.onload = function(){
                        if (xhr.status >= 200 && xhr.status < 300){
                            try{ const j = JSON.parse(xhr.responseText); status.textContent = j.message || 'Upload complete'; filesList.innerHTML = (j.files||[]).map(n => `<div>✔ ${escapeHtml(n)}</div>`).join(''); }
                            catch(e){ status.textContent = 'Upload complete'; }
                            progressBar.style.width = '100%';
                        } else {
                            status.textContent = 'Upload failed: ' + xhr.status;
                        }
                    };

                    xhr.onerror = function(){ status.textContent = 'Network error during upload'; };
                    xhr.send(fd);
                });

                function escapeHtml(s){ return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) }
            </script>
        </body>
        </html>
        """

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("file")
    saved = []
    for file in files:
        if not file:
            continue
        filename = secure_filename(file.filename) or 'unnamed'
        dest = os.path.join(UPLOAD_FOLDER, filename)
        file.save(dest)
        saved.append(filename)
    return jsonify({"message": "Upload complete. Files saved.", "files": saved})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
