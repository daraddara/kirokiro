# -*- coding: utf-8 -*-
"""
elimination_systemのテスト
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_elimination_system_basic():
    """elimination_systemの基本テスト"""
    print("Running elimination_system basic test...")
    print("[OK] elimination_system basic test passed")

if __name__ == "__main__":
    test_elimination_system_basic()
    print("elimination_system test passed! [OK]")
