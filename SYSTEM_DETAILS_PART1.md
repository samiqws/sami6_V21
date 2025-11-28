# 📘 شرح تفصيلي - الجزء 1: مراقب الملفات وملفات الفخ

## 1️⃣ File Monitor (مراقب الملفات)

### الفئات الرئيسية

#### FileIntegrityMonitor
```python
class FileIntegrityMonitor:
    def __init__(self):
        self.file_hashes = {}       # تخزين hash لكل ملف
        self.file_metadata = {}      # معلومات إضافية
        self.monitored_paths = set() # المسارات المراقبة
```

**المهام الرئيسية:**

##### 1. حساب Hash (SHA-256)
```python
def calculate_hash(self, file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # قراءة الملف على دفعات 4KB لتوفير الذاكرة
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
```

**لماذا نستخدم Hash؟**
- لمقارنة محتوى الملف قبل وبعد
- إذا تغير hash = الملف تم تعديله
- برامج الفدية تشفر الملفات = hash يتغير

##### 2. حساب الإنتروبيا (Entropy)
```python
def calculate_entropy(self, file_path):
    # قراءة أول 1MB فقط للسرعة
    data = f.read(1024 * 1024)
    
    # حساب تكرار كل byte
    frequencies = [0] * 256  # 256 قيمة ممكنة للبايت
    for byte in data:
        frequencies[byte] += 1
    
    # حساب Shannon Entropy
    entropy = 0.0
    for freq in frequencies:
        if freq > 0:
            probability = freq / len(data)
            entropy -= probability * math.log2(probability)
    
    return entropy
```

**فهم الإنتروبيا:**
- **0.0 - 3.0**: ملف نصي عادي (تكرار عالي)
- **3.0 - 6.0**: ملفات عادية (Word, Excel)
- **6.0 - 7.0**: ملفات مضغوطة أو صور
- **> 7.0**: ملفات مشفرة! ⚠️ (عشوائية عالية جداً)

**مثال:**
- ملف نصي: "AAAA..." → entropy منخفض
- ملف مشفر: "X#9@!..." → entropy عالي (> 7.0)

##### 3. التحقق من السلامة
```python
def verify_integrity(self, file_path):
    # جلب hash القديم
    original_hash = self.file_hashes.get(file_path)
    
    # حساب hash الحالي
    current_hash = self.calculate_hash(file_path)
    current_entropy = self.calculate_entropy(file_path)
    
    # المقارنة
    hash_changed = (current_hash != original_hash)
    entropy_suspicious = (current_entropy > 7.0)
    
    return {
        "compromised": hash_changed,
        "entropy_suspicious": entropy_suspicious,
        "current_entropy": current_entropy
    }
```

---

#### RansomwareEventHandler
معالج أحداث نظام الملفات

```python
class RansomwareEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # ملف تم تعديله
        self._handle_event("modified", event.src_path)
    
    def on_created(self, event):
        # ملف جديد تم إنشاؤه
        self._handle_event("created", event.src_path)
    
    def on_deleted(self, event):
        # ملف تم حذفه
        self._handle_event("deleted", event.src_path)
    
    def on_moved(self, event):
        # ملف تم نقله/تغيير اسمه
        self._handle_event("moved", event.dest_path, event.src_path)
```

**دورة حياة الحدث:**
```
1. نظام الملفات → تغيير في ملف
2. watchdog → يكتشف التغيير
3. RansomwareEventHandler → on_modified()
4. _handle_event() → جمع المعلومات
5. verify_integrity() → فحص السلامة
6. callback() → إرسال للكاشف
```

---

#### FileSystemMonitor
المنسق الرئيسي للمراقبة

```python
class FileSystemMonitor:
    def __init__(self, protected_paths, callback):
        self.protected_paths = protected_paths  # المجلدات المحمية
        self.callback = callback                # دالة المعالجة
        self.observers = []                     # مراقبين
    
    def start(self):
        for path in self.protected_paths:
            observer = Observer()
            observer.schedule(
                self.event_handler,
                path,
                recursive=True  # مراقبة المجلدات الفرعية
            )
            observer.start()
            self.observers.append(observer)
```

**مثال على الاستخدام:**
```python
protected_paths = [
    "C:\\Users\\Public\\Documents",
    "C:\\Important\\Files"
]

monitor = FileSystemMonitor(protected_paths, handle_file_event)
monitor.start()

# الآن يراقب جميع الملفات في هذه المجلدات!
```

---

## 2️⃣ Decoy Manager (مدير ملفات الفخ)

### ما هي ملفات الفخ؟
ملفات **وهمية** تبدو مهمة لبرامج الفدية، لكنها **فخ للكشف المبكر**!

### الفلسفة
برامج الفدية تشفر **كل الملفات** بدون تمييز. إذا لمست ملف فخ → **كشف فوري**!

### التنفيذ

#### إنشاء ملفات الفخ
```python
class DecoyFileManager:
    def create_decoy_files(self, count=50):
        created_decoys = []
        
        for i in range(count):
            # اختيار نوع عشوائي
            file_type = random.choice(["pdf", "docx", "xlsx", "jpg", "txt"])
            
            # اسم واقعي
            filename = f"Financial_Report_{random.randint(1000, 9999)}.{file_type}"
            
            # محتوى واقعي
            content = self._generate_decoy_content(file_type)
            
            # حفظ الملف
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # حساب hash للتحقق لاحقاً
            file_hash = hashlib.sha256(content).hexdigest()
            
            # تسجيل في السجل
            self.decoy_registry[file_path] = {
                "hash": file_hash,
                "type": file_type,
                "created_at": datetime.now()
            }
```

#### محتوى واقعي للملفات
```python
def _generate_decoy_content(self, file_type):
    if file_type == "txt":
        # ملف نصي يبدو مهم
        content = """
        CONFIDENTIAL DOCUMENT
        Financial Records 2024
        Employee Database
        Password List: admin123, backup456...
        """
        return content.encode('utf-8')
    
    elif file_type == "pdf":
        # هيكل PDF بسيط صحيح
        pdf = b"%PDF-1.4\n..."
        return pdf
    
    elif file_type == "jpg":
        # header JPEG صحيح
        jpg_header = b'\xFF\xD8\xFF\xE0...'
        return jpg_header + os.urandom(2048)
```

**لماذا محتوى واقعي؟**
- برامج الفدية الذكية قد تتحقق من نوع الملف
- محتوى واقعي = أصعب للكشف أنه فخ

#### التحقق من ملفات الفخ
```python
def verify_decoy(self, file_path):
    if file_path not in self.decoy_registry:
        return {"is_decoy": False}
    
    original_hash = self.decoy_registry[file_path]["hash"]
    
    # هل تم حذف الملف؟
    if not os.path.exists(file_path):
        return {
            "is_decoy": True,
            "compromised": True,
            "reason": "deleted"  # ⚠️ إنذار!
        }
    
    # حساب hash الحالي
    with open(file_path, 'rb') as f:
        current_hash = hashlib.sha256(f.read()).hexdigest()
    
    # هل تم تعديل الملف؟
    if current_hash != original_hash:
        return {
            "is_decoy": True,
            "compromised": True,
            "reason": "modified"  # ⚠️ تنبيه فوري!
        }
    
    return {"is_decoy": True, "compromised": False}
```

### أمثلة على أسماء ملفات الفخ
```
Financial_Report_2024.xlsx
Confidential_Data_5839.pdf
Password_List_7291.txt
Client_Database_3847.docx
Backup_Keys_9201.zip
```

**لماذا هذه الأسماء؟**
- تجذب انتباه برامج الفدية
- تبدو ملفات مهمة ومربحة للمهاجم
- توفر **كشف مبكر** قبل تشفير الملفات الحقيقية

