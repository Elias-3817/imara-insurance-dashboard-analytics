@echo off
cd /d %~dp0\Python_Scripts
python .\02_New_entry_data_generator.py || exit /b
python .\03_monitoring_alert_system.py || exit /b