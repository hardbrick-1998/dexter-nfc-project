from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app) # Mengizinkan website mengirim data ke server ini

DB_FILE = 'stok_flowmeter.csv'

# Bikin file CSV otomatis kalau belum ada
if not os.path.exists(DB_FILE):
    with open(DB_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Waktu_Scan', 'RFID_ID', 'Status', 'Lokasi'])
    print(f"[*] File database {DB_FILE} dibuat.")

@app.route('/api/scan', methods=['POST'])
def receive_scan():
    data = request.json
    tag_id = data.get('tag_id')
    
    if not tag_id:
        return jsonify({"error": "ID Tag tidak ditemukan"}), 400

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Terscan di Lapangan"
    lokasi = "Pitstop MACO"
    
    # Simpan ke CSV
    with open(DB_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, tag_id, status, lokasi])
        
    print(f"\n[+] DATA MASUK: {tag_id} pada {timestamp}")
    
    return jsonify({
        "status": "success", 
        "message": f"Data {tag_id} tersimpan!"
    }), 200

if __name__ == '__main__':
    print("=== SERVER DEXTER MENYALA ===")
    print("Menunggu data dari HP...")
    app.run(host='0.0.0.0', port=5000)