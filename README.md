# Sensor Project

## Struktur Folder
- `publisher/`: Script Python untuk publish data dummy ke MQTT
- `backend/`: Flask app untuk subscribe MQTT dan simpan ke MySQL
- `frontend/`: HTML + Chart.js untuk menampilkan data sensor

## Langkah Menjalankan
1. Jalankan MQTTBox sebagai broker di `localhost:1883`
2. Jalankan `publish_data.py` untuk mengirim data dummy
3. Jalankan `app.py` untuk memulai Flask server
4. Buka `index.html` di browser untuk melihat grafik

## Struktur Database MySQL
```sql
CREATE DATABASE sensor_db;

USE sensor_db;

CREATE TABLE sensor_data (
    id INT PRIMARY KEY,
    sensor_type VARCHAR(50),
    value FLOAT,
    timestamp DATETIME
);
