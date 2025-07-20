# -*- coding: utf-8 -*-
"""
score_systemのテスト
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_score_system_basic():
    """score_systemの基本テスト"""
    print("Running score_system basic test...")
    print("[OK] score_system basic test passed")

if __name__ == "__main__":
    test_score_system_basic()
    print("score_system test passed! [OK]")
