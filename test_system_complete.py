"""
Complete System Test for Ransomware Defense System
Tests all major components and endpoints
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_test(name, status, details=""):
    symbol = f"{Colors.GREEN}✓{Colors.END}" if status else f"{Colors.RED}✗{Colors.END}"
    print(f"{symbol} {name:.<50} {status}")
    if details:
        print(f"  {Colors.YELLOW}{details}{Colors.END}")

def test_endpoint(name, url, method="GET", data=None):
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        success = response.status_code == 200
        result = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
        
        print_test(name, success, f"Status: {response.status_code}")
        return success, result
    except Exception as e:
        print_test(name, False, f"Error: {str(e)}")
        return False, None

def main():
    print(f"\n{Colors.BOLD}Ransomware Defense System - Complete Test Suite{Colors.END}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    total_tests = 0
    passed_tests = 0
    
    # ============================================================
    # 1. System Status Tests
    # ============================================================
    print_header("System Status & Health")
    
    success, status_data = test_endpoint("System Status", f"{BASE_URL}/api/status")
    total_tests += 1
    if success:
        passed_tests += 1
        print(f"   Monitoring: {status_data.get('monitoring')}")
        print(f"   Protected Paths: {status_data.get('protected_paths')}")
        print(f"   Decoy Files: {status_data.get('decoy_files')}")
        print(f"   Active Incidents: {status_data.get('active_incidents')}")
    
    # ============================================================
    # 2. Statistics Tests
    # ============================================================
    print_header("Statistics & Metrics")
    
    success, stats_data = test_endpoint("System Statistics", f"{BASE_URL}/api/stats")
    total_tests += 1
    if success:
        passed_tests += 1
        print(f"   Total Events: {stats_data.get('total_events')}")
        print(f"   Suspicious Events: {stats_data.get('suspicious_events')}")
        print(f"   Active Incidents: {stats_data.get('active_incidents')}")
        print(f"   Decoy Files: {stats_data.get('decoy_files')}")
    
    # ============================================================
    # 3. Decoy System Tests
    # ============================================================
    print_header("Decoy System (Honeypots)")
    
    success, decoys_data = test_endpoint("Decoy Files List", f"{BASE_URL}/api/decoys")
    total_tests += 1
    if success:
        passed_tests += 1
        decoy_count = decoys_data.get('total', 0)
        print(f"   Total Decoys: {decoy_count}")
        if decoy_count > 0:
            sample_decoys = decoys_data.get('decoys', [])[:3]
            print(f"   Sample Decoys:")
            for decoy in sample_decoys:
                print(f"     - {decoy.get('path')} ({decoy.get('type')})")
    
    # ============================================================
    # 4. Containment Settings Tests
    # ============================================================
    print_header("Containment Settings")
    
    success, settings_data = test_endpoint("Get Containment Settings", f"{BASE_URL}/api/settings/containment")
    total_tests += 1
    if success:
        passed_tests += 1
        print(f"   Auto Containment: {settings_data.get('auto_contain')}")
        print(f"   Kill Process: {settings_data.get('kill_process')}")
        print(f"   Isolate Network: {settings_data.get('isolate_network')}")
        print(f"   Disable Network Drives: {settings_data.get('disable_network_drives')}")
        print(f"   Lock System: {settings_data.get('lock_system')}")
    
    # Test updating settings (toggle auto_contain)
    current_auto_contain = settings_data.get('auto_contain', False) if settings_data else False
    new_value = not current_auto_contain
    
    success, update_result = test_endpoint(
        "Update Containment Settings",
        f"{BASE_URL}/api/settings/containment",
        method="POST",
        data={"auto_contain": new_value}
    )
    total_tests += 1
    if success:
        passed_tests += 1
        print(f"   Changed auto_contain: {current_auto_contain} → {new_value}")
    
    # Restore original value
    if success:
        test_endpoint(
            "Restore Original Settings",
            f"{BASE_URL}/api/settings/containment",
            method="POST",
            data={"auto_contain": current_auto_contain}
        )
    
    # ============================================================
    # 5. Incidents Tests
    # ============================================================
    print_header("Incident Management")
    
    success, incidents_data = test_endpoint("Get Incidents", f"{BASE_URL}/api/incidents?limit=10")
    total_tests += 1
    if success:
        passed_tests += 1
        incident_count = len(incidents_data) if isinstance(incidents_data, list) else 0
        print(f"   Total Incidents (Recent 10): {incident_count}")
        if incident_count > 0:
            print(f"   Recent Incidents:")
            for incident in incidents_data[:3]:
                print(f"     - ID: {incident.get('id')[:8]}... | Severity: {incident.get('severity')} | Status: {incident.get('status')}")
    
    # ============================================================
    # 6. Events Tests
    # ============================================================
    print_header("File System Events")
    
    success, events_data = test_endpoint("Get Events", f"{BASE_URL}/api/events?limit=10")
    total_tests += 1
    if success:
        passed_tests += 1
        event_count = len(events_data) if isinstance(events_data, list) else 0
        print(f"   Total Events (Recent 10): {event_count}")
        if event_count > 0:
            print(f"   Recent Events:")
            for event in events_data[:3]:
                print(f"     - Type: {event.get('type')} | Path: {event.get('path', 'N/A')[:50]}...")
    
    # ============================================================
    # 7. Alerts Tests
    # ============================================================
    print_header("Alert System")
    
    success, alerts_data = test_endpoint("Get All Alerts", f"{BASE_URL}/api/alerts?unacknowledged_only=false")
    total_tests += 1
    if success:
        passed_tests += 1
        alert_count = len(alerts_data) if isinstance(alerts_data, list) else 0
        print(f"   Total Alerts: {alert_count}")
        if alert_count > 0:
            print(f"   Recent Alerts:")
            for alert in alerts_data[:3]:
                print(f"     - Severity: {alert.get('severity')} | Type: {alert.get('type')}")
                print(f"       Message: {alert.get('message', 'N/A')[:60]}...")
    
    # ============================================================
    # 8. Frontend Tests
    # ============================================================
    print_header("Frontend & UI")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        success = response.status_code == 200 and 'text/html' in response.headers.get('content-type', '')
        print_test("Dashboard Root", success, f"Status: {response.status_code}")
        total_tests += 1
        if success:
            passed_tests += 1
    except Exception as e:
        print_test("Dashboard Root", False, f"Error: {str(e)}")
        total_tests += 1
    
    # ============================================================
    # Results Summary
    # ============================================================
    print_header("Test Results Summary")
    
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"   Total Tests: {total_tests}")
    print(f"   {Colors.GREEN}Passed: {passed_tests}{Colors.END}")
    print(f"   {Colors.RED}Failed: {total_tests - passed_tests}{Colors.END}")
    print(f"   Pass Rate: {pass_rate:.1f}%")
    
    if pass_rate == 100:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All tests passed! System is fully operational.{Colors.END}")
    elif pass_rate >= 80:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ Most tests passed. System is operational with minor issues.{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Multiple tests failed. System requires attention.{Colors.END}")
    
    print(f"\n{Colors.BOLD}Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Test failed with error: {str(e)}{Colors.END}")
