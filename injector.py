#!/usr/bin/env python3
"""
injector.py — 가상 센서 데이터 생성기
MySQL sensordb.sensor_data 테이블에 2초 간격으로 랜덤 데이터를 삽입합니다.
"""

import random
import time
import signal
import sys
import mysql.connector
from datetime import datetime

# ── DB 연결 설정 ─────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "sensoruser",
    "password": "sensor1234",
    "database": "sensordb",
}

INTERVAL = 2  # 삽입 간격 (초)

# ── 센서 데이터 범위 ──────────────────────────────────────────
SENSOR_RANGES = {
    "temperature": (15.0, 40.0),   # °C
    "humidity":    (30.0, 90.0),   # %
    "pressure":    (980.0, 1030.0),# hPa
    "co2":         (400, 1500),    # ppm
}


def generate_data() -> dict:
    """정규분포 기반 랜덤 센서값 생성"""
    def bounded_normal(lo, hi):
        mid = (lo + hi) / 2
        std = (hi - lo) / 6
        return round(max(lo, min(hi, random.gauss(mid, std))), 2)

    return {
        "temperature": bounded_normal(*SENSOR_RANGES["temperature"]),
        "humidity":    bounded_normal(*SENSOR_RANGES["humidity"]),
        "pressure":    bounded_normal(*SENSOR_RANGES["pressure"]),
        "co2":         int(bounded_normal(*SENSOR_RANGES["co2"])),
    }


def insert(cursor, data: dict):
    cursor.execute(
        """INSERT INTO sensor_data (temperature, humidity, pressure, co2)
           VALUES (%(temperature)s, %(humidity)s, %(pressure)s, %(co2)s)""",
        data,
    )


def main():
    print("=" * 55)
    print("  LAMP 센서 데이터 인젝터 시작")
    print(f"  DB: {DB_CONFIG['host']}/{DB_CONFIG['database']}")
    print(f"  간격: {INTERVAL}초  |  종료: Ctrl+C")
    print("=" * 55)

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    def shutdown(sig, frame):
        print("\n인젝터 종료 중...")
        cursor.close()
        conn.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    count = 0
    while True:
        data = generate_data()
        insert(cursor, data)
        conn.commit()
        count += 1
        ts = datetime.now().strftime("%H:%M:%S")
        print(
            f"[{ts}] #{count:04d} | "
            f"온도:{data['temperature']:5.1f}°C  "
            f"습도:{data['humidity']:5.1f}%  "
            f"기압:{data['pressure']:7.1f}hPa  "
            f"CO2:{data['co2']:4d}ppm"
        )
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
