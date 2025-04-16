from flask import jsonify, render_template
from app import app
from app.connection.db import get_db_connection

# For Dashboard
@app.route('/get_latest_data', methods=['GET'])
def get_latest_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sensor ORDER BY timestamp DESC LIMIT 1')
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        data = {
            'varLuxLeft': row[1],
            'varLuxRight': row[2],
            'varPositionServo': row[3],
            'voltage': row[4],
            'current': row[5],
            'power': row[6],
            'energy_calc': row[7],
            'timestamp': row[8],
        }
        return jsonify(data)
    else:
        return jsonify([], 'No data found')
    
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('index.html')
# END: For Dashboard

# For historical data
@app.route('/get_historical_data', methods=['GET'])
def historical_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT varLuxLeft, varLuxRight, varPositionServo, voltage, current, power, energy_calc, timestamp FROM sensor ORDER BY timestamp DESC')
    row = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(row)
# END: For historical data