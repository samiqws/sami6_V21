# 📘 أمثلة الاستخدام - Usage Examples

## 🎛️ التحكم في أوضاع المراقبة

### عرض الأوضاع الحالية

**PowerShell:**
```powershell
curl http://localhost:8000/api/monitoring/modes
```

**الرد:**
```json
{
  "modes": {
    "user_files": true,
    "decoy_files": true,
    "system_files": false
  },
  "descriptions": {
    "user_files": "مراقبة ملفات المستخدم...",
    "decoy_files": "مراقبة ملفات الفخاخ...",
    "system_files": "مراقبة ملفات النظام..."
  }
}
```

---

### تعطيل مراقبة ملفات المستخدم

```powershell
curl -X POST "http://localhost:8000/api/monitoring/modes/set?mode=user_files&enabled=false"
```

---

### تفعيل مراقبة النظام فقط

```powershell
$modes = @{
    user_files = $false
    decoy_files = $false
    system_files = $true
} | ConvertTo-Json

curl -X POST "http://localhost:8000/api/monitoring/modes/update-all" `
  -H "Content-Type: application/json" `
  -d $modes
```

---

## 🔒 حماية الملفات

### عرض إحصائيات النسخ الاحتياطية

```powershell
curl http://localhost:8000/api/protection/stats
```

**الرد:**
```json
{
  "protected_files": 25,
  "total_backups": 120,
  "total_size_mb": 45.2
}
```

---

### استرجاع ملف محدد

```powershell
curl -X POST "http://localhost:8000/api/protection/restore?file_path=C:\Users\User\Documents\report.docx&version_index=-1"
```

---

### استرجاع جميع الملفات

```powershell
curl -X POST http://localhost:8000/api/protection/restore-all
```

---

## 💾 مراقبة الأقراص

### عرض الأقراص المتصلة

```powershell
curl http://localhost:8000/api/drives/list
```

**الرد:**
```json
{
  "drives": [
    {
      "path": "C:\\",
      "type": "Fixed",
      "monitored": false
    },
    {
      "path": "D:\\",
      "type": "USB/Removable",
      "monitored": true
    }
  ]
}
```

---

## 🎯 سيناريوهات الاستخدام

### السيناريو 1: حماية ملفات العمل فقط
```json
{
  "user_files": true,   // ملفات المستخدم
  "decoy_files": false, // بدون فخاخ
  "system_files": false // بدون نظام
}
```

### السيناريو 2: كشف مبكر بالفخاخ
```json
{
  "user_files": false,  // بدون مستخدم
  "decoy_files": true,  // فخاخ فقط
  "system_files": false
}
```

### السيناريو 3: مراقبة شاملة
```json
{
  "user_files": true,
  "decoy_files": true,
  "system_files": true  // تحذير: قد يبطئ النظام
}
```

---

## ⚡ نصائح الاستخدام

1. **للاستخدام اليومي**: فعّل User Files + Decoy Files
2. **للاختبار**: فعّل Decoy Files فقط
3. **للحماية القصوى**: فعّل الثلاثة (مع مراقبة الأداء)
4. **لتوفير الموارد**: فعّل User Files فقط

---

## 📊 مراقبة الحالة

### عرض حالة النظام
```powershell
curl http://localhost:8000/api/status
```

### عرض الإحصائيات
```powershell
curl http://localhost:8000/api/stats
```

### عرض الأحداث الأخيرة
```powershell
curl http://localhost:8000/api/events?limit=10
```
