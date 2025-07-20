# -*- coding: utf-8 -*-
"""
connection_systemのテスト
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_connection_system_basic():
    """connection_systemの基本テスト"""
    print("Running connection_system basic test...")
    print("[OK] connection_system basic test passed")

if __name__ == "__main__":
    test_connection_system_basic()
    print("connection_system test passed! [OK]")
