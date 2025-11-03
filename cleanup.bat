@echo off
echo ========================================
echo   CLEANUP SCRIPT - RFQ Automation
echo ========================================
echo.
echo This will move old files to archive folder
echo.
pause

echo.
echo Creating archive folders...
if not exist archive mkdir archive
if not exist archive\old_dashboards mkdir archive\old_dashboards
if not exist archive\old_backend mkdir archive\old_backend
if not exist archive\old_docs mkdir archive\old_docs

echo.
echo Moving old dashboard files...
if exist app_demo.py move app_demo.py archive\old_dashboards\
if exist streamlit_app.py move streamlit_app.py archive\old_dashboards\
if exist streamlit_flowchart_app.py move streamlit_flowchart_app.py archive\old_dashboards\
if exist nicegui_app.py move nicegui_app.py archive\old_dashboards\

echo.
echo Moving old backend files...
if exist main_with_sse.py move main_with_sse.py archive\old_backend\
if exist sse_server.py move sse_server.py archive\old_backend\

echo.
echo Moving old documentation...
if exist DEMO_QUICK_START.md move DEMO_QUICK_START.md archive\old_docs\
if exist FIXES_APPLIED.md move FIXES_APPLIED.md archive\old_docs\
if exist FLOWCHART_DEMO_README.md move FLOWCHART_DEMO_README.md archive\old_docs\
if exist THREADING_FIX.md move THREADING_FIX.md archive\old_docs\
if exist VISUAL_FEEDBACK_ADDED.md move VISUAL_FEEDBACK_ADDED.md archive\old_docs\
if exist WHATS_NEW.md move WHATS_NEW.md archive\old_docs\
if exist WORKING_SOLUTION.md move WORKING_SOLUTION.md archive\old_docs\
if exist todo_list.md move todo_list.md archive\old_docs\

echo.
echo Moving extra launchers...
if exist start_flowchart_demo.py move start_flowchart_demo.py archive\old_docs\
if exist run_flowchart.bat move run_flowchart.bat archive\old_docs\

echo.
echo Deleting temporary files...
if exist temp_*.txt del temp_*.txt
if exist processed_email_ids.txt del processed_email_ids.txt
if exist last_processed.txt del last_processed.txt

echo.
echo ========================================
echo   CLEANUP COMPLETE!
echo ========================================
echo.
echo Cleaned files are in 'archive' folder
echo.
echo Next steps:
echo 1. Review archive folder
echo 2. Test: streamlit run flowchart_demo.py
echo 3. Commit changes to Git
echo.
pause
