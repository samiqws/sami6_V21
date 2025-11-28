"""
Test script to verify ransomware detection system
WARNING: This creates and modifies test files only
"""

import os
import time
import random
import string

def create_test_directory():
    """Create test directory"""
    test_dir = "C:\\Users\\Public\\Documents\\TestArea"
    os.makedirs(test_dir, exist_ok=True)
    print(f"✓ Created test directory: {test_dir}")
    return test_dir

def test_normal_operations(test_dir):
    """Test normal file operations"""
    print("\n[TEST 1] Normal file operations...")
    
    # Create some files
    for i in range(5):
        file_path = os.path.join(test_dir, f"normal_file_{i}.txt")
        with open(file_path, 'w') as f:
            f.write(f"Normal content {i}\n")
        time.sleep(0.5)
    
    print("✓ Created 5 normal files")

def test_rapid_modifications(test_dir):
    """Simulate rapid file modifications (suspicious)"""
    print("\n[TEST 2] Rapid file modifications (should trigger alert)...")
    
    for i in range(60):
        file_path = os.path.join(test_dir, f"rapid_test_{i}.txt")
        with open(file_path, 'w') as f:
            f.write(''.join(random.choices(string.ascii_letters, k=100)))
    
    print("✓ Created 60 files rapidly")

def test_extension_changes(test_dir):
    """Simulate extension changes (suspicious)"""
    print("\n[TEST 3] Extension changes (should trigger alert)...")
    
    files = []
    for i in range(15):
        file_path = os.path.join(test_dir, f"document_{i}.txt")
        with open(file_path, 'w') as f:
            f.write("Original content")
        files.append(file_path)
    
    time.sleep(1)
    
    # Change extensions
    for file_path in files:
        new_path = file_path.replace('.txt', '.encrypted')
        os.rename(file_path, new_path)
    
    print("✓ Changed 15 file extensions")

def cleanup(test_dir):
    """Clean up test files"""
    print("\n[CLEANUP] Removing test files...")
    try:
        for file in os.listdir(test_dir):
            file_path = os.path.join(test_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("✓ Cleanup complete")
    except Exception as e:
        print(f"Cleanup error: {e}")

def main():
    print("=" * 60)
    print("Ransomware Detection System - Test Suite")
    print("=" * 60)
    
    print("\nThis script will test the detection system.")
    print("Make sure the detection engine is running!")
    
    input("\nPress Enter to start tests...")
    
    test_dir = create_test_directory()
    
    try:
        test_normal_operations(test_dir)
        time.sleep(2)
        
        test_rapid_modifications(test_dir)
        time.sleep(2)
        
        test_extension_changes(test_dir)
        
        print("\n" + "=" * 60)
        print("Tests completed!")
        print("Check the dashboard for detection results")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nTests interrupted")
    finally:
        cleanup_input = input("\nClean up test files? (y/n): ")
        if cleanup_input.lower() == 'y':
            cleanup(test_dir)

if __name__ == "__main__":
    main()
