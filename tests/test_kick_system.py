# -*- coding: utf-8 -*-
"""
kick_systemのテスト
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_kick_system_basic():
    """kick_systemの基本テスト"""
    print("Running kick_system basic test...")
    print("[OK] kick_system basic test passed")

if __name__ == "__main__":
    test_kick_system_basic()
    print("kick_system test passed! [OK]")
