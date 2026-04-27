@echo off
echo Setting up Git repository for Portfolio Website...
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    echo Then run this script again.
    pause
    exit /b 1
)

echo Git is installed. Proceeding with setup...
echo.

REM Configure Git (update with your details)
echo Configuring Git user...
git config --global user.name "Vikramaraj M"
git config --global user.email "vhbrosis@gmail.com"

REM Initialize repository
echo Initializing Git repository...
git init

REM Add remote origin
echo Adding remote repository...
git remote add origin https://github.com/vikrammvr007/VikramWebsite.git

REM Add all files
echo Adding files to staging...
git add .

REM Create initial commit
echo Creating initial commit...
git commit -m "Initial commit: Complete portfolio website with admin panel"

REM Push to GitHub
echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo SUCCESS: Repository has been connected to GitHub!
echo Your code is now available at: https://github.com/vikrammvr007/VikramWebsite
echo.
pause