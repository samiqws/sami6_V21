# 🔧 Troubleshooting Guide - دليل حل المشاكل

## ❌ "Failed to update settings" Error

### Problem:
When clicking monitoring mode toggles, you get an error: "Failed to update settings"

### Possible Causes & Solutions:

#### 1️⃣ **Config File Permissions**

**Symptom:** Cannot save changes to `config/settings.json`

**Solution:**
```bash
# Check file permissions
# Right-click config/settings.json → Properties → Security
# Make sure your user has "Write" permission

# Or run the application as Administrator
```

#### 2️⃣ **Config File Doesn't Exist**

**Symptom:** Error log shows "File not found"

**Solution:**
```bash
# Make sure config/settings.json exists
# If not, copy from config/settings.json.example
# Or run install.bat again
```

#### 3️⃣ **Invalid JSON Format**

**Symptom:** Error parsing config file

**Solution:**
```bash
# Validate your config/settings.json at jsonlint.com
# Or restore from backup
```

#### 4️⃣ **Backend Not Running**

**Symptom:** Network error or connection refused

**Solution:**
```bash
# Make sure backend is running:
start.bat

# Check if server is responding:
curl http://localhost:8000/api/status
```

---

## 🔍 Debug Steps:

### 1. Check Backend Logs
```bash
# Look in the terminal running start.bat
# Search for errors like:
# - "Failed to save config"
# - "Permission denied"
# - "Invalid monitoring mode"
```

### 2. Check Browser Console
```bash
# Open browser DevTools (F12)
# Go to Console tab
# Look for errors when clicking toggle
```

### 3. Test API Directly
```powershell
# Test getting modes
curl http://localhost:8000/api/monitoring/modes

# Test setting a mode
curl -X POST "http://localhost:8000/api/monitoring/modes/set?mode=user_files&enabled=true"
```

---

## ✅ Quick Fixes:

### Fix 1: Reset Config File
```bash
# Backup current config
copy config\settings.json config\settings.json.backup

# Restore default (if you have it)
copy config\settings.json.default config\settings.json

# Or manually add monitoring_mode section:
```

```json
{
  "monitoring": {
    "monitoring_mode": {
      "user_files": true,
      "decoy_files": true,
      "system_files": false
    }
  }
}
```

### Fix 2: Run as Administrator
```bash
# Right-click start.bat → Run as Administrator
```

### Fix 3: Check File Lock
```bash
# Make sure no other program is using settings.json
# Close any text editors that have it open
```

---

## 📝 Enable Debug Logging:

### Backend (main.py):
```python
# Set logging level to DEBUG
logging.basicConfig(level=logging.DEBUG)
```

### Frontend (Console):
```javascript
// Enable verbose logging
localStorage.setItem('debug', 'true');
```

---

## 🆘 Still Not Working?

### Collect Debug Information:

1. **Backend logs** from terminal
2. **Browser console** errors (F12 → Console)
3. **Network tab** in DevTools (check API calls)
4. **Config file** contents (config/settings.json)

### Manual Workaround:

Edit `config/settings.json` directly:
```json
{
  "monitoring": {
    "monitoring_mode": {
      "user_files": true,
      "decoy_files": false,
      "system_files": false
    }
  }
}
```

Then restart:
```bash
# Stop with Ctrl+C
# Start again
start.bat
```

---

## 🎯 Common Error Messages:

| Error | Cause | Solution |
|-------|-------|----------|
| "Failed to update settings" | Permission issue | Run as admin |
| "Invalid monitoring mode" | Wrong parameter | Check mode name |
| "Configuration saved successfully" | Success! | No action needed |
| "Failed to save config" | File lock/permission | Close editors, check permissions |
| "Network error" | Backend offline | Start backend with start.bat |

---

## ✨ Prevention Tips:

1. ✅ Always run `start.bat` as Administrator
2. ✅ Don't edit `settings.json` while system is running
3. ✅ Keep backup of `settings.json`
4. ✅ Validate JSON before saving
5. ✅ Check logs regularly

---

## 📞 Need More Help?

Check these files:
- `logs/ransomware_defense.log` - System logs
- `QUICK_START_GUIDE.md` - Setup instructions
- `FIXES_APPLIED.md` - Recent fixes
