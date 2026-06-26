@echo off
set /P CommentVar=Comment? 
cd C:\Code\expense_report
git add *
git commit -m "%CommentVar%"
git push