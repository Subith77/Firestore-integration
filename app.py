
from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore
import qrcode
import io
import base64

app = Flask(__name__)

# Initialize Firebase Admin SDK (replace with your JSON path)
cred = credentials.Certificate("F:/Firebase integration/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        mobile = request.form.get('mobile')

        # Save to Firestore
        doc_ref = db.collection('users').document()
        doc_ref.set({
            'name': name,
            'mobile': mobile
        })

        key = doc_ref.id

        # Generate QR code with Firestore document ID
        img = qrcode.make(key)
        buf = io.BytesIO()
        img.save(buf)
        buf.seek(0)

        # Convert QR code image to base64 string for embedding in HTML
        img_base64 = base64.b64encode(buf.read()).decode('ascii')

        return render_template('qr.html', qr_code=img_base64, key=key)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
