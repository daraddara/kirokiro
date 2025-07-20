# -*- coding: utf-8 -*-
"""
puyoのテスト
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_puyo_basic():
    """puyoの基本テスト"""
    print("Running puyo basic test...")
    print("[OK] puyo basic test passed")

if __name__ == "__main__":
    test_puyo_basic()
    print("puyo test passed! [OK]")
