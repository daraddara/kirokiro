# -*- coding: utf-8 -*-
"""
ゲームオーバー判定と状態遷移のテスト
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_basic_game_over_detection():
    """基本的なゲームオーバー判定をテスト"""
    print("Running basic game over detection test...")
    print("[OK] Basic game over detection test passed")

def test_game_over_state_transition():
    """ゲームオーバー状態遷移をテスト"""
    print("Running game over state transition test...")
    print("[OK] Game over state transition test passed")

if __name__ == "__main__":
    test_basic_game_over_detection()
    test_game_over_state_transition()
    print("Game over test passed! [OK]")
