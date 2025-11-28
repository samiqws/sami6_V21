# 🔧 Database Repair Guide - دليل إصلاح قاعدة البيانات

## 🔴 المشكلة | The Problem

```
sqlalchemy.exc.DatabaseError: (sqlite3.DatabaseError) database disk image is malformed
```

قاعدة بيانات SQLite تالفة ويجب إصلاحها أو إعادة إنشائها.

The SQLite database is corrupted and needs to be repaired or recreated.

---

## ✅ الحلول | Solutions

### الحل 1: استخدام سكريبت الإصلاح التلقائي (موصى به)
### Solution 1: Use Automatic Repair Script (Recommended)

#### الخطوات | Steps:

1. **أوقف تشغيل التطبيق إذا كان يعمل**
   
   Stop the application if it's running (Press Ctrl+C in the terminal)

2. **شغّل سكريبت الإصلاح**
   
   Run the repair script:

   **Option A - Batch Script:**
   ```bash
   fix_database.bat
   ```

   **Option B - Python Script (More detailed):**
   ```bash
   python fix_database.py
   ```

3. **أعد تشغيل التطبيق**
   
   Restart the application:
   ```bash
   start.bat
   ```

---

### الحل 2: الإصلاح اليدوي
### Solution 2: Manual Repair

#### الخطوات | Steps:

1. **أوقف التطبيق**
   
   Stop the application

2. **انتقل إلى مجلد البيانات**
   
   Navigate to the data folder:
   ```bash
   cd backend\data
   ```

3. **احتفظ بنسخة احتياطية (اختياري)**
   
   Backup the corrupted database (optional):
   ```bash
   copy ransomware_defense.db ransomware_defense_backup.db
   ```

4. **احذف قاعدة البيانات التالفة**
   
   Delete the corrupted database:
   ```bash
   del ransomware_defense.db
   ```

5. **ارجع للمجلد الرئيسي**
   
   Return to main folder:
   ```bash
   cd ..\..
   ```

6. **أعد تشغيل التطبيق**
   
   Restart the application:
   ```bash
   start.bat
   ```

   سيتم إنشاء قاعدة بيانات جديدة تلقائياً
   
   A fresh database will be created automatically

---

## 🛡️ منع تكرار المشكلة | Preventing Future Corruption

### الأسباب الشائعة للتلف:
### Common Causes of Corruption:

1. **إيقاف مفاجئ للتطبيق**
   - Abruptly closing the application (Ctrl+C during database write)
   - حاول دائماً إيقاف التطبيق بشكل طبيعي

2. **مشاكل في القرص الصلب**
   - Hard disk errors or full disk
   - تأكد من وجود مساحة كافية

3. **عدة عمليات تصل لقاعدة البيانات**
   - Multiple processes accessing the database
   - شغّل نسخة واحدة فقط من التطبيق

### نصائح الوقاية:
### Prevention Tips:

1. **نسخ احتياطية منتظمة**
   
   Regular backups:
   ```bash
   # Create a backup manually
   copy backend\data\ransomware_defense.db backend\data\backup_YYYYMMDD.db
   ```

2. **إيقاف صحيح للتطبيق**
   
   Proper shutdown:
   - استخدم Ctrl+C وانتظر رسالة "Shutting down"
   - Wait for "Shutting down" message before closing

3. **راقب مساحة القرص**
   
   Monitor disk space:
   - تأكد من وجود مساحة كافية على القرص
   - Ensure sufficient disk space

---

## 📊 ماذا يحدث عند إعادة الإنشاء؟
## What Happens When Recreating?

عند حذف قاعدة البيانات وإعادة تشغيل التطبيق:

When you delete the database and restart the application:

- ✅ سيتم إنشاء قاعدة بيانات جديدة تلقائياً
  - A fresh database will be created automatically

- ⚠️ ستفقد البيانات التالية:
  - You will lose the following data:
  - التنبيهات القديمة (Old alerts)
  - سجل الأحداث (Event history)
  - الحوادث المسجلة (Recorded incidents)
  - إحصائيات النظام (System statistics)

- ✅ سيبقى كما هو:
  - Will remain unchanged:
  - الإعدادات (Settings in config/settings.json)
  - ملفات الفخ (Decoy files)
  - المراقبة الفورية (Real-time monitoring)

---

## 🆘 المساعدة الإضافية | Additional Help

إذا استمرت المشكلة:

If the problem persists:

1. تحقق من سجلات التطبيق
   
   Check application logs:
   ```
   logs\ransomware_defense.log
   ```

2. تأكد من الصلاحيات
   
   Verify permissions:
   - تشغيل كمسؤول (Run as Administrator)
   - صلاحيات الكتابة على المجلد (Write permissions on folder)

3. تحقق من مساحة القرص
   
   Check disk space:
   ```bash
   dir backend\data
   ```

4. أعد تشغيل الحاسوب
   
   Restart your computer

---

## 📝 ملاحظات | Notes

- النسخ الاحتياطية محفوظة في: `backend\data\`
  
  Backups are saved in: `backend\data\`

- يمكنك حذف النسخ الاحتياطية القديمة يدوياً
  
  You can manually delete old backups

- قاعدة البيانات الجديدة ستبدأ فارغة
  
  The new database will start empty

---

**✅ نجاح الإصلاح يعني أن التطبيق سيعمل بشكل طبيعي**

**✅ Successful repair means the application will work normally**
