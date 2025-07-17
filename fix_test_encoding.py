"""
Fix encoding issues in test files by replacing Unicode checkmarks with ASCII text
"""

import os
import re

def fix_test_file(filename):
    """テストファイルのUnicode文字を修正"""
    if not os.path.exists(filename):
        print(f"File {filename} not found, skipping...")
        return
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ✓ を [OK] に置換
        content = content.replace('✓', '[OK]')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed encoding in {filename}")
        
    except Exception as e:
        print(f"Error fixing {filename}: {e}")

def main():
    """全てのテストファイルを修正"""
    test_files = [
        "test_puyo.py",
        "test_fall_system.py", 
        "test_gravity_system.py",
        "test_kick_system.py",
        "test_connection_system.py",
        "test_game_integration.py"
    ]
    
    print("Fixing encoding issues in test files...")
    
    for test_file in test_files:
        fix_test_file(test_file)
    
    print("Encoding fix complete!")

if __name__ == "__main__":
    main()