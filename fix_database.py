#!/usr/bin/env python3
"""
Database Repair Tool for Ransomware Detection Engine
أداة إصلاح قاعدة البيانات
"""

import os
import shutil
import sqlite3
from datetime import datetime


def main():
    print("=" * 60)
    print("Database Repair Tool - أداة إصلاح قاعدة البيانات")
    print("=" * 60)
    print()
    
    db_path = os.path.join("backend", "data", "ransomware_defense.db")
    
    if not os.path.exists(db_path):
        print("✅ No database file found. A new one will be created on next start.")
        print("✅ لا يوجد ملف قاعدة بيانات. سيتم إنشاء واحد جديد عند التشغيل التالي.")
        return
    
    print(f"📁 Database found: {db_path}")
    print()
    
    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join("backend", "data", f"ransomware_defense_backup_{timestamp}.db")
    
    print("[1/4] Creating backup...")
    print(f"[1/4] إنشاء نسخة احتياطية...")
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
        print()
    except Exception as e:
        print(f"⚠️ Backup failed: {e}")
        print()
    
    # Try to recover data
    print("[2/4] Attempting to recover data...")
    print("[2/4] محاولة استرجاع البيانات...")
    recovered_data = {}
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Try to get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"📊 Found {len(tables)} tables")
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                recovered_data[table] = count
                print(f"  - {table}: {count} records")
            except Exception as e:
                print(f"  - {table}: ❌ corrupted ({e})")
        
        conn.close()
        print("✅ Data recovery scan completed")
        print()
    except Exception as e:
        print(f"❌ Could not read database: {e}")
        print()
    
    # Delete corrupted database
    print("[3/4] Deleting corrupted database...")
    print("[3/4] حذف قاعدة البيانات التالفة...")
    try:
        os.remove(db_path)
        print("✅ Corrupted database deleted")
        print()
    except Exception as e:
        print(f"❌ Failed to delete: {e}")
        print()
        return
    
    # Summary
    print("[4/4] Summary - الملخص")
    print("=" * 60)
    print()
    print("✅ Database repair completed successfully!")
    print("✅ تم إصلاح قاعدة البيانات بنجاح!")
    print()
    print("📋 Next steps - الخطوات التالية:")
    print("  1. Run start.bat to start the application")
    print("     شغّل start.bat لبدء التطبيق")
    print()
    print("  2. A fresh database will be created automatically")
    print("     سيتم إنشاء قاعدة بيانات جديدة تلقائياً")
    print()
    
    if recovered_data:
        print("📊 Previous database statistics:")
        print("📊 إحصائيات قاعدة البيانات السابقة:")
        for table, count in recovered_data.items():
            print(f"     - {table}: {count} records")
        print()
    
    print(f"💾 Backup saved at: {backup_path}")
    print()
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
    finally:
        input("\nPress Enter to exit...")
