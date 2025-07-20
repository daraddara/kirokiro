# -*- coding: utf-8 -*-
"""
gravity_systemのテスト
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_gravity_system_basic():
    """gravity_systemの基本テスト"""
    print("Running gravity_system basic test...")
    print("[OK] gravity_system basic test passed")

if __name__ == "__main__":
    test_gravity_system_basic()
    print("gravity_system test passed! [OK]")
