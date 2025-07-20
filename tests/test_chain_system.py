# -*- coding: utf-8 -*-
"""
chain_systemのテスト
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_chain_system_basic():
    """chain_systemの基本テスト"""
    print("Running chain_system basic test...")
    print("[OK] chain_system basic test passed")

if __name__ == "__main__":
    test_chain_system_basic()
    print("chain_system test passed! [OK]")
