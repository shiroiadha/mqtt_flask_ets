# app.py
from flask import Flask, jsonify, render_template
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import ssl
import threading
import time
from db_config import get_db_connection  # <-- gunakan fungsi dari file eksternal

app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")

# --- Konfigurasi HiveMQ Cloud ---
BROKER = "368d64a62a274d43965439d61347be40.s1.eu.hivemq.cloud"   # Ganti sesuai broker kamu
PORT = 8883
USERNAME = "mas_admin_1"
PASSWORD = "ATMIN_anjas123"
CLIENT_ID = "Atmin_MQTT-1"
TOPIC = "esp32/sensor"

# ======================================================
# ================   MQTT HANDLER   =====================
# ======================================================

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Terhubung ke HiveMQ Cloud broker!")
        client.subscribe(TOPIC)
    else:
        print(f"⚠️ Gagal konek ke broker, code={rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        print("📩 Data diterima:", data)

        # Pastikan payload memiliki format JSON seperti:
        # { "suhu": 26.5, "humidity": 55.1, "lux": 6.7, "tds": 800 }

        suhu = data.get("suhu")
        humidity = data.get("humidity")
        lux = data.get("lux")

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO data_sensor (suhu, humidity, lux, tds)
            VALUES (%s, %s, %s, %s)
        """, (suhu, humidity, lux))
        db.commit()
        cursor.close()
        db.close()

        print(f"✅ Data disimpan: T={suhu}, H={humidity}, lux={lux}")

    except Exception as e:
        print("⚠️ Error pada parsing atau penyimpanan:", e)


# ======================================================
# ================   MQTT THREAD   ======================
# ======================================================

def mqtt_thread():
    client = mqtt.Client(client_id=CLIENT_ID, clean_session=True)
    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)

    client.on_connect = on_connect
    client.on_message = on_message

    while True:
        try:
            client.connect(BROKER, PORT)
            client.loop_forever()
        except Exception as e:
            print("⚠️ MQTT terputus, mencoba ulang 5 detik:", e)
            time.sleep(5)

# Jalankan thread MQTT di background
threading.Thread(target=mqtt_thread, daemon=True).start()


# ======================================================
# ================   FLASK ROUTES   =====================
# ======================================================

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/data')
def get_all_data():
    """Ambil semua data dari DB"""
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM data_sensor ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(rows)

@app.route('/data/latest')
def get_latest_data():
    """Ambil 50 data terakhir"""
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM data_sensor ORDER BY timestamp DESC LIMIT 50")
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    rows.reverse()
    return jsonify(rows)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)