import os
import subprocess
import psutil
import logging
from typing import List, Dict, Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class ContainmentEngine:
    """Automated containment and response actions"""
    
    def __init__(self, config: dict):
        self.config = config
        self.containment_config = config.get("containment", {})
        self.auto_contain = self.containment_config.get("auto_contain", False)
        self.containment_log = []
    
    async def execute_containment(self, incident_data: dict, auto: bool = False) -> dict:
        """
        Execute containment protocols based on incident severity.
        Returns summary of actions taken.
        """
        if auto and not self.auto_contain:
            logger.info("Auto-containment is disabled")
            return {"status": "skipped", "reason": "auto_contain_disabled"}
        
        actions_taken = []
        actions_failed = []
        
        threat_level = incident_data.get("threat_level", "low")
        process_info = incident_data.get("process", {})
        
        logger.warning(f"Initiating containment for {threat_level} threat")
        
        # 1. Kill suspicious process
        if self.containment_config.get("kill_process", True):
            result = await self.kill_process(process_info)
            if result["success"]:
                actions_taken.append(result)
            else:
                actions_failed.append(result)
        
        # 2. Isolate network (for high/critical threats)
        if threat_level in ["high", "critical"] and self.containment_config.get("isolate_network", True):
            result = await self.isolate_network()
            if result["success"]:
                actions_taken.append(result)
            else:
                actions_failed.append(result)
        
        # 3. Disable network drives
        if self.containment_config.get("disable_network_drives", True):
            result = await self.disable_network_drives()
            if result["success"]:
                actions_taken.append(result)
            else:
                actions_failed.append(result)
        
        # 4. Lock system (for high/critical threats if enabled)
        if threat_level in ["high", "critical"] and self.containment_config.get("lock_system", False):
            result = await self.lock_workstation()
            if result["success"]:
                actions_taken.append(result)
            else:
                actions_failed.append(result)
        
        summary = {
            "status": "completed",
            "actions_taken": actions_taken,
            "actions_failed": actions_failed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "auto_triggered": auto
        }
        
        self.containment_log.append(summary)
        return summary
    
    async def kill_process(self, process_info: dict) -> dict:
        """Terminate a suspicious process"""
        pid = process_info.get("pid", 0)
        process_name = process_info.get("name", "unknown")
        
        # Check if valid PID
        if pid <= 0:
            logger.warning(f"Invalid PID ({pid}) for process {process_name}")
            return {
                "action": "process_kill",
                "success": False,
                "error": "invalid_pid",
                "target": process_name,
                "message": "No valid process ID provided"
            }
        
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=5)
            
            logger.info(f"Terminated process: {process_name} (PID: {pid})")
            return {
                "action": "process_kill",
                "success": True,
                "target": process_name,
                "pid": pid,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except psutil.NoSuchProcess:
            return {
                "action": "process_kill",
                "success": False,
                "error": "process_not_found",
                "target": process_name
            }
        except psutil.AccessDenied:
            return {
                "action": "process_kill",
                "success": False,
                "error": "access_denied",
                "target": process_name,
                "message": "Requires administrator privileges"
            }
        except Exception as e:
            logger.error(f"Failed to kill process {process_name}: {e}")
            return {
                "action": "process_kill",
                "success": False,
                "error": str(e),
                "target": process_name
            }
    
    async def isolate_network(self) -> dict:
        """Disable network adapters to isolate the system"""
        try:
            # Windows command to disable network adapters
            cmd = 'powershell "Get-NetAdapter | Where-Object {$_.Status -eq \'Up\'} | Disable-NetAdapter -Confirm:$false"'
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.warning("Network adapters disabled - System isolated")
                return {
                    "action": "network_isolation",
                    "success": True,
                    "message": "All network adapters disabled",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            else:
                return {
                    "action": "network_isolation",
                    "success": False,
                    "error": result.stderr,
                    "message": "Requires administrator privileges"
                }
        except Exception as e:
            logger.error(f"Network isolation failed: {e}")
            return {
                "action": "network_isolation",
                "success": False,
                "error": str(e)
            }
    
    async def disable_network_drives(self) -> dict:
        """Disconnect all network drives"""
        try:
            # Windows command to disconnect network drives
            cmd = 'net use * /delete /yes'
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            logger.info("Network drives disconnected")
            return {
                "action": "disable_network_drives",
                "success": True,
                "message": "All network drives disconnected",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to disconnect network drives: {e}")
            return {
                "action": "disable_network_drives",
                "success": False,
                "error": str(e)
            }
    
    async def lock_workstation(self) -> dict:
        """Lock the workstation"""
        try:
            # Method 1: Try ctypes (more reliable)
            try:
                import ctypes
                result = ctypes.windll.user32.LockWorkStation()
                if result != 0:
                    logger.warning("Workstation locked via ctypes")
                    return {
                        "action": "lock_workstation",
                        "success": True,
                        "message": "Workstation locked",
                        "method": "ctypes",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
            except Exception as e:
                logger.warning(f"ctypes lock failed, trying subprocess: {e}")
            
            # Method 2: Fallback to subprocess
            subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'], timeout=5)
            
            logger.warning("Workstation locked via subprocess")
            return {
                "action": "lock_workstation",
                "success": True,
                "message": "Workstation locked",
                "method": "subprocess",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to lock workstation: {e}")
            return {
                "action": "lock_workstation",
                "success": False,
                "error": str(e),
                "message": "Lock failed - both methods unsuccessful"
            }
    
    async def restore_network(self) -> dict:
        """Re-enable network adapters"""
        try:
            cmd = 'powershell "Get-NetAdapter | Where-Object {$_.Status -eq \'Disabled\'} | Enable-NetAdapter -Confirm:$false"'
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info("Network adapters re-enabled")
                return {
                    "action": "restore_network",
                    "success": True,
                    "message": "Network adapters restored"
                }
            else:
                return {
                    "action": "restore_network",
                    "success": False,
                    "error": result.stderr
                }
        except Exception as e:
            return {
                "action": "restore_network",
                "success": False,
                "error": str(e)
            }
    
    def get_containment_history(self) -> List[dict]:
        """Get history of containment actions"""
        return self.containment_log
