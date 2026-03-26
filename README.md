# lamp-monitor — LAMP Stack + Node-RED + Grafana 실시간 모니터링

Python으로 가상 센서 데이터를 생성하여 MySQL에 저장하고,
**Node-RED**와 **Grafana** 두 가지 방식으로 실시간 모니터링하는 프로젝트입니다.

## 빠른 시작

```bash
# 1. DB 초기화
mysql -u root < db_setup.sql

# 2. Python 인젝터 실행
pip install mysql-connector-python
python3 injector.py

# 3. Node-RED 대시보드
#    http://localhost:1880/ui

# 4. Grafana 대시보드
#    http://localhost:3000
```

## 상세 내용

→ [project.md](project.md) 참고
