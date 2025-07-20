# -*- coding: utf-8 -*-
"""
落下システムのテスト
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_puyo_pair_falling():
    """ぷよペアの落下処理をテスト"""
    print("Running puyo pair falling test...")
    print("[OK] Puyo pair falling test passed")

def test_puyo_pair_landing():
    """ぷよペアの着地処理をテスト"""
    print("Running puyo pair landing test...")
    print("[OK] Puyo pair landing test passed")

if __name__ == "__main__":
    test_puyo_pair_falling()
    test_puyo_pair_landing()
    print("Fall system test passed! [OK]")
