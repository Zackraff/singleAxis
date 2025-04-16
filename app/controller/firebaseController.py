from firebase_admin import db
from app.connection.db import get_db_connection
from app import response
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

def sync_data_from_fb_to_postgres():
    try:
        print("Syncing data from Firebase to PostgreSQL...")
        ref = db.reference('/sensors')
        sensors_data = ref.get()

        print(sensors_data.items())

        if sensors_data:
            conn = get_db_connection()
            cursor = conn.cursor()

            timestamp = datetime.now()
            
            varLuxLeft = float(sensors_data.get("varLuxLeft", 0))
            varLuxRight = float(sensors_data.get("varLuxRight", 0))
            varPositionServo = int(sensors_data.get("varPositionServo", 0))
            voltage = float(sensors_data.get("voltage", 0))
            current = float(sensors_data.get("current", 0))
            power = float(sensors_data.get("power", 0))
            energy_calc = float(sensors_data.get("energy_calc", 0))
            timestamp = int(sensors_data.get("timestamp", 0))


            cursor.execute('''
                INSERT INTO sensor (varLuxLeft, varLuxRight, varPositionServo, voltage, current, power, energy_calc, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', (varLuxLeft, varLuxRight, varPositionServo, voltage, current, power, energy_calc, timestamp))
            
            conn.commit()
            cursor.close()
            conn.close()

            print(f'Data successfully synced to database at {timestamp}')
                
        else:
            print('No data retrieved from Firebase')
    except Exception as e:
        print(str(e))
        return response.badRequest([], str(e))

scheduler = BackgroundScheduler()
scheduler.add_job(sync_data_from_fb_to_postgres, 'interval', minutes=5)
scheduler.start()