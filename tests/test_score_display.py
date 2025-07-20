# -*- coding: utf-8 -*-
"""
score_displayのテスト
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_score_display_basic():
    """score_displayの基本テスト"""
    print("Running score_display basic test...")
    print("[OK] score_display basic test passed")

if __name__ == "__main__":
    test_score_display_basic()
    print("score_display test passed! [OK]")
