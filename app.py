import time
import json
import sqlite3

import smbus2
import bme280

address = 0x76
bus = smbus2.SMBus(1)
calibration_params = bme280.load_calibration_params(bus, address)

conn = sqlite3.connect('/var/db/bme240.db')

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS data (
                   d_sec INTEGER PRIMARY KEY AUTOINCREMENT,
                   deg_c REAL NOT NULL,
                   press REAL NOT NULL,
                   rel_h REAL NOT NULL
               );""")

while True:
    try:
        sample = bme280.sample(bus, address, calibration_params)
        data = {
            "d_sec": int(time.time()),
            "deg_c": sample.temperature,
            "press": sample.pressure,
            "rel_h": sample.humidity,
        }
        message = json.dumps(data, separators=(',', ':'))
        print(message)
        cur.execute("INSERT INTO data VALUES(:d_sec, :deg_c, :press, :rel_h);", data)
        conn.commit()
        time.sleep(5)
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as ex:
        print("Unknown Error")
        print(ex)
        break
                                                                                                                                             39,9          Bot
