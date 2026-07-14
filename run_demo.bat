@echo off
echo =======================================================
echo Pillar A: Ingestion, Structural Parsing ^& Database Load
echo =======================================================
echo.

call venv\Scripts\python.exe src\ingestion\test_pipeline_e2e.py

echo.
echo =======================================================
echo Pipeline execution completed successfully.
echo =======================================================
pause
