@echo off
echo ==========================================
echo   SatelliteEye Deployment Script
echo ==========================================
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Training...
echo (You can skip this if the model is already trained)
python src/train.py
echo.
echo Starting Web Server...
python app.py
pause
