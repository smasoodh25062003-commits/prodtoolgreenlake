@echo off
cd /d "c:\Users\hussasye\Downloads\GreenLake"

echo Adding all changes...
git add -A

echo.
if "%~1"=="" (
  set "msg=Update %date% %time%"
) else (
  set "msg=%~*"
)
echo Committing: %msg%
git commit -m "%msg%"

if errorlevel 1 (
  echo No changes to commit, or nothing new.
) else (
  echo.
  echo Pushing to GitHub...
  git push origin master
)

echo.
pause
