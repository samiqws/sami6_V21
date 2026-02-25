import logging
import os
from typing import List, Dict, Optional
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import asyncio

logger = logging.getLogger(__name__)


class RansomwareDetector:
    """Advanced ransomware detection engine with multiple heuristics"""
    
    def __init__(self, config: dict, decoy_manager):
        self.config = config
        self.decoy_manager = decoy_manager
        
        # Detection thresholds
        self.entropy_threshold = config.get("detection", {}).get("entropy_threshold", 7.0)
        self.rapid_change_threshold = config.get("detection", {}).get("rapid_change_threshold", 50)
        self.extension_change_threshold = config.get("detection", {}).get("extension_change_threshold", 10)
        
        # Tracking structures
        self.file_modifications = defaultdict(list)
        self.process_activity = defaultdict(int)
        self.extension_changes = defaultdict(int)
        self.suspicious_processes = set()
        
        # Detection window (5 minutes)
        self.detection_window = timedelta(minutes=5)
    
    async def analyze_event(self, event_data: dict) -> dict:
        """
        Analyze a file system event for ransomware indicators.
        Returns detection result with threat assessment.
        """
        try:
            file_path = event_data.get("path")
            event_type = event_data.get("type")
            timestamp = event_data.get("timestamp", datetime.now(timezone.utc))
            process_info = event_data.get("process", {})
            integrity_info = event_data.get("integrity", {})
            
            process_name = process_info.get("name", "unknown")
            process_pid = process_info.get("pid", 0)
            # Use combined ID for accurate tracking
            process_id = f"{process_name}:{process_pid}"

            detection_result = {
                "suspicious": False,
                "threat_level": "none",
                "confidence": 0.0,
                "indicators": [],
                "recommended_action": "monitor"
            }
            
            indicators = []
            threat_score = 0
            
            # 1. Check if decoy file was accessed
            decoy_check = self.decoy_manager.verify_decoy(file_path)
            if decoy_check.get("is_decoy") and decoy_check.get("compromised"):
                indicators.append("decoy_file_compromised")
                threat_score += 50
                logger.warning(f"DECOY FILE COMPROMISED: {file_path} by {process_id}")
            
            # 2. Check entropy (encryption indicator)
            if integrity_info:
                current_entropy = integrity_info.get("current_entropy", 0)
                if current_entropy and current_entropy > self.entropy_threshold:
                    indicators.append("high_entropy")
                    threat_score += 30
            
            # 3. Check for extension changes
            if integrity_info and integrity_info.get("extension_changed"):
                indicators.append("extension_changed")
                threat_score += 20
                self.extension_changes[process_id] += 1
            
            # 4. Track rapid file modifications
            
            # Skip tracking for our own process
            if process_name.lower() in ["python.exe", "pythonw.exe"]:
                # Check if it's the monitoring script itself
                process_exe = process_info.get("exe", "")
                if "sami6" in process_exe.lower() or "backend" in process_exe.lower():
                    # Don't track our own file operations
                    return detection_result
            
            self.file_modifications[process_id].append(timestamp)
            
            # Clean old entries
            cutoff_time = timestamp - self.detection_window
            self.file_modifications[process_id] = [
                t for t in self.file_modifications[process_id] if t > cutoff_time
            ]
            
            modification_rate = len(self.file_modifications[process_id])
            if modification_rate > self.rapid_change_threshold:
                indicators.append("rapid_file_modifications")
                threat_score += 40
                logger.warning(f"Rapid modifications detected: {process_id} - {modification_rate} files")
            
            # 5. Check for mass extension changes
            if self.extension_changes[process_id] > self.extension_change_threshold:
                indicators.append("mass_extension_changes")
                threat_score += 35
            
            # 6. Check for suspicious file patterns
            if any(ext in file_path.lower() for ext in self.config.get("detection", {}).get("suspicious_extensions", [])):
                indicators.append("suspicious_extension")
                threat_score += 25
            
            # Determine threat level
            if threat_score >= 70:
                detection_result["threat_level"] = "critical"
                detection_result["recommended_action"] = "contain"
                logger.critical(f"[CRITICAL THREAT] Score: {threat_score} | File: {file_path} | Process: {process_name} | Indicators: {indicators}")
            elif threat_score >= 50:
                detection_result["threat_level"] = "high"
                detection_result["recommended_action"] = "alert"
                logger.error(f"[HIGH THREAT] Score: {threat_score} | File: {file_path} | Process: {process_name} | Indicators: {indicators}")
            elif threat_score >= 30:
                detection_result["threat_level"] = "medium"
                detection_result["recommended_action"] = "monitor"
                logger.warning(f"[MEDIUM THREAT] Score: {threat_score} | File: {file_path} | Process: {process_name} | Indicators: {indicators}")
            elif threat_score >= 15:
                detection_result["threat_level"] = "low"
                detection_result["recommended_action"] = "log"
                logger.info(f"[LOW THREAT] Score: {threat_score} | File: {file_path}")
            
            detection_result["suspicious"] = threat_score >= 30
            detection_result["confidence"] = min(threat_score / 100.0, 1.0)
            detection_result["indicators"] = indicators
            detection_result["threat_score"] = threat_score
            detection_result["process"] = process_info
            
            # Log all detections for debugging
            if threat_score > 0:
                logger.info(f"Detection analysis - File: {os.path.basename(file_path)} | Score: {threat_score} | Indicators: {indicators}")
            
            return detection_result
        
        except Exception as e:
            logger.error(f"Error analyzing event: {e}")
            # Return safe default result
            return {
                "suspicious": False,
                "threat_level": "none",
                "confidence": 0.0,
                "indicators": [],
                "recommended_action": "monitor"
            }
    
    def get_suspicious_processes(self) -> List[dict]:
        """Get list of processes with suspicious activity"""
        suspicious = []
        
        for process_id, count in self.extension_changes.items():
            if count > self.extension_change_threshold:
                suspicious.append({
                    "process": process_id,
                    "extension_changes": count,
                    "file_modifications": len(self.file_modifications.get(process_id, []))
                })
        
        return suspicious
    
    def reset_tracking(self):
        """Reset all tracking data"""
        self.file_modifications.clear()
        self.process_activity.clear()
        self.extension_changes.clear()
        self.suspicious_processes.clear()
        logger.info("Detection tracking data reset")
