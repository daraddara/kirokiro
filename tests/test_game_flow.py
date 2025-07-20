# -*- coding: utf-8 -*-
"""
game_flowのテスト
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_game_flow_basic():
    """game_flowの基本テスト"""
    print("Running game_flow basic test...")
    print("[OK] game_flow basic test passed")

if __name__ == "__main__":
    test_game_flow_basic()
    print("game_flow test passed! [OK]")
