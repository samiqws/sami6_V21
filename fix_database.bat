@echo off
chcp 65001 >nul
echo ============================================================
echo Fix Corrupted Database - إصلاح قاعدة البيانات التالفة
echo ============================================================
echo.

echo This script will:
echo - Backup the corrupted database
echo - Delete the corrupted database
echo - Recreate a fresh database
echo.
echo سيقوم هذا السكريبت بـ:
echo - أخذ نسخة احتياطية من قاعدة البيانات التالفة
echo - حذف قاعدة البيانات التالفة
echo - إنشاء قاعدة بيانات جديدة
echo.

set DB_PATH=backend\data\ransomware_defense.db
set BACKUP_PATH=backend\data\ransomware_defense_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%.db
set BACKUP_PATH=%BACKUP_PATH: =0%

pause

echo.
echo [1/3] Checking if database exists...
if exist "%DB_PATH%" (
    echo [OK] Database found: %DB_PATH%
    
    echo.
    echo [2/3] Creating backup...
    copy "%DB_PATH%" "%BACKUP_PATH%"
    if %errorLevel% == 0 (
        echo [OK] Backup created: %BACKUP_PATH%
    ) else (
        echo [WARNING] Could not create backup
    )
    
    echo.
    echo [3/3] Deleting corrupted database...
    del "%DB_PATH%"
    if %errorLevel% == 0 (
        echo [OK] Corrupted database deleted
    ) else (
        echo [ERROR] Could not delete database
        pause
        exit /b 1
    )
) else (
    echo [INFO] Database file not found, nothing to delete
)

echo.
echo ============================================================
echo Database repair completed!
echo قاعدة البيانات تم إصلاحها!
echo ============================================================
echo.
echo The application will create a new database on next start.
echo سيتم إنشاء قاعدة بيانات جديدة عند التشغيل التالي.
echo.
echo Next step: Run start.bat to start the application
echo الخطوة التالية: شغّل start.bat لبدء التطبيق
echo.

pause
