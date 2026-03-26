-- DB 및 테이블 초기화
CREATE DATABASE IF NOT EXISTS sensordb;
CREATE USER IF NOT EXISTS 'sensoruser'@'localhost' IDENTIFIED BY 'sensor1234';
GRANT ALL PRIVILEGES ON sensordb.* TO 'sensoruser'@'localhost';
FLUSH PRIVILEGES;

USE sensordb;

CREATE TABLE IF NOT EXISTS sensor_data (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT        NOT NULL COMMENT '온도 (°C)',
    humidity    FLOAT        NOT NULL COMMENT '습도 (%)',
    pressure    FLOAT        NOT NULL COMMENT '기압 (hPa)',
    co2         INT          NOT NULL COMMENT 'CO2 (ppm)',
    created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SELECT 'DB 및 테이블 설정 완료!' AS result;
