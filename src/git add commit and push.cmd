@echo off
set /P CommentVar=Comment? 
cd C:\Code\expense_report
git add *
git commit -m "%CommentVar%"
git push
pause
ssh ymatia@192.168.0.28 ./redeploy_expense_report.sh
