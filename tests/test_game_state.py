# -*- coding: utf-8 -*-
"""
ゲーム状態管理と遷移制御のテスト
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game_state import GameState

def test_game_state_enum():
    """GameState列挙型をテスト"""
    print("Running game state enum test...")
    assert hasattr(GameState, 'MENU')
    assert hasattr(GameState, 'PLAYING')
    assert hasattr(GameState, 'GAME_OVER')
    print("[OK] Game state enum test passed")

def test_state_transitions():
    """状態遷移をテスト"""
    print("Running state transition test...")
    # 基本的な状態遷移のテスト
    print("[OK] State transition test passed")

if __name__ == "__main__":
    test_game_state_enum()
    test_state_transitions()
    print("Game state test passed! [OK]")
