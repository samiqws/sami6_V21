"""
Monitoring Configuration Manager - مدير إعدادات المراقبة
يسمح للمستخدم باختيار نوع المراقبة
"""

import json
import os
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class MonitoringMode:
    """أنواع المراقبة المتاحة"""
    USER_FILES = "user_files"       # ملفات المستخدم
    DECOY_FILES = "decoy_files"     # ملفات الهني بوت (الفخاخ)
    SYSTEM_FILES = "system_files"   # ملفات النظام


class MonitoringConfig:
    """إدارة إعدادات المراقبة"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        logger.info(f"MonitoringConfig using: {self.config_path}")
        
        # Verify config file exists
        if not os.path.exists(self.config_path):
            logger.error(f"Config file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        self.config = self._load_config()
        self.monitoring_modes = self._get_monitoring_modes()
    
    def _load_config(self) -> dict:
        """تحميل ملف الإعدادات"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def _save_config(self):
        """حفظ ملف الإعدادات"""
        try:
            logger.info(f"Attempting to save config to: {self.config_path}")
            logger.info(f"Config file exists: {os.path.exists(self.config_path)}")
            logger.info(f"Config dir exists: {os.path.exists(os.path.dirname(self.config_path))}")
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration saved successfully to: {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save config to {self.config_path}: {e}")
            return False
    
    def _get_monitoring_modes(self) -> dict:
        """الحصول على أوضاع المراقبة الحالية"""
        return self.config.get("monitoring", {}).get("monitoring_mode", {
            "user_files": True,
            "decoy_files": True,
            "system_files": False
        })
    
    def is_user_files_enabled(self) -> bool:
        """هل مراقبة ملفات المستخدم مفعلة؟"""
        return self.monitoring_modes.get("user_files", True)
    
    def is_decoy_files_enabled(self) -> bool:
        """هل مراقبة ملفات الفخاخ مفعلة؟"""
        return self.monitoring_modes.get("decoy_files", True)
    
    def is_system_files_enabled(self) -> bool:
        """هل مراقبة ملفات النظام مفعلة؟"""
        return self.monitoring_modes.get("system_files", False)
    
    def set_monitoring_mode(self, mode: str, enabled: bool) -> bool:
        """تفعيل/تعطيل وضع مراقبة معين"""
        try:
            valid_modes = ["user_files", "decoy_files", "system_files"]
            
            if mode not in valid_modes:
                logger.error(f"Invalid monitoring mode: {mode}")
                return False
            
            # تحديث الإعدادات
            if "monitoring" not in self.config:
                self.config["monitoring"] = {}
            
            if "monitoring_mode" not in self.config["monitoring"]:
                self.config["monitoring"]["monitoring_mode"] = {}
            
            self.config["monitoring"]["monitoring_mode"][mode] = enabled
            
            # حفظ التغييرات
            save_success = self._save_config()
            
            if not save_success:
                logger.error(f"Failed to save configuration for mode '{mode}'")
                return False
            
            # تحديث الذاكرة المحلية
            self.monitoring_modes = self._get_monitoring_modes()
            
            logger.info(f"Monitoring mode '{mode}' set to {enabled}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set monitoring mode: {e}")
            return False
    
    def get_all_modes(self) -> dict:
        """الحصول على جميع أوضاع المراقبة"""
        return {
            "user_files": self.is_user_files_enabled(),
            "decoy_files": self.is_decoy_files_enabled(),
            "system_files": self.is_system_files_enabled()
        }
    
    def set_all_modes(self, modes: dict) -> bool:
        """تعيين جميع أوضاع المراقبة دفعة واحدة"""
        try:
            for mode, enabled in modes.items():
                if mode in ["user_files", "decoy_files", "system_files"]:
                    self.set_monitoring_mode(mode, enabled)
            return True
        except Exception as e:
            logger.error(f"Failed to set all modes: {e}")
            return False
    
    def get_description(self, mode: str) -> str:
        """الحصول على وصف لنوع المراقبة"""
        descriptions = {
            "user_files": "مراقبة ملفات المستخدم (المستندات، الصور، إلخ)",
            "decoy_files": "مراقبة ملفات الفخاخ (Honeypot) للكشف المبكر",
            "system_files": "مراقبة ملفات النظام (غير موصى به)"
        }
        return descriptions.get(mode, "Unknown mode")
