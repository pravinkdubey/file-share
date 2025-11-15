# 📂 Flask File Upload App

A simple Python + Flask application that allows you to upload files from your **iPhone (or any device)** directly to your **Windows PC** over the same Wi-Fi/hotspot network. Uploaded files are instantly saved in the `uploads` folder on your PC.

---

## 🚀 Setup Instructions

### 1. Install Python (if not installed)
Download Python from the [official website](https://www.python.org/downloads/) and install it.  
Verify installation:

```bash
python --version
```

2. Install Flask
Install Flask using pip:
```
pip install flask
```

3. Run the Server on Windows
Run your Flask app:
python app.py
```
python app.py
```

You’ll see output similar to:
```
http://0.0.0.0:5000/
```

4. Get Your Windows PC IPv4 Address
Open Command Prompt (CMD) and run:
```
ipconfig
```

Look for:
```
IPv4 Address: 192.168.x.x
```

5. Connect from Phone
- Ensure your iPhone is connected to the same Wi-Fi/hotspot as your PC.
- Open Safari (or any browser).
- Enter:
```
http://192.168.x.x:5000
```



6. Upload Files
- You’ll see the upload page.
- Choose files → Upload → Files appear instantly in the uploads folder on Windows.

📂 Supported Data Types
✔ Photos
✔ Videos
✔ Documents
✔ Text files
✔ ZIPs
✔ Anything (as long as your iPhone/browser allows upload)
(Replace 192.168.x.x with your PC’s IPv4 address.)

⚡ Notes
- Both devices must be on the same network.
- Default port is 5000. You can change it in app.py if needed.
- Works with any device that supports browser-based file uploads.
