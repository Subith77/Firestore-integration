import cv2
from pyzbar.pyzbar import decode
from google.cloud import firestore
import os

# --- Set up Firestore ---
# Make sure your Google service account JSON file is correctly placed and named
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "F:\Firebase integration\serviceAccountKey.json"
db = firestore.Client()

def fetch_details(doc_id):
    try:
        doc_ref = db.collection('users').document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            print("\n✅ Document Data:")
            for key, value in doc.to_dict().items():
                print(f"{key}: {value}")
        else:
            print("\n❌ No document found with ID:", doc_id)
    except Exception as e:
        print("\n🚫 Error fetching data:", e)

def read_qr_code():
    cap = cv2.VideoCapture(0)
    print("\n📸 Scanning for QR Code... (Press 'q' to quit)")

    while True:
        ret, frame = cap.read()
        for barcode in decode(frame):
            qr_data = barcode.data.decode('utf-8')
            print("\n🔍 QR Code Detected:", qr_data)
            cap.release()
            cv2.destroyAllWindows()
            return qr_data

        cv2.imshow('QR Code Scanner - Press q to exit', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

def main():
    print("\n🧠 Choose input method:")
    print("1. Scan QR Code")
    print("2. Enter ID manually")
    choice = input("Your choice (1 or 2): ").strip()

    if choice == '1':
        doc_id = read_qr_code()
        if doc_id:
            fetch_details(doc_id)
        else:
            print("⚠️ No QR Code detected.")
    elif choice == '2':
        doc_id = input("🔤 Enter Document ID: ").strip()
        fetch_details(doc_id)
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
