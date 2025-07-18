"""
Test file for the restart functionality
"""

import sys
import os
# Add the parent directory to sys.path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game import PuyoPuyoGame
from src.puyo import Puyo
from src.game_state import GameState
import unittest.mock as mock


class MockPyxel:
    """Pyxelのモック - テスト用"""
    
    def __init__(self):
        self.keys_pressed = set()
        self.keys_just_pressed = set()
        self.quit_called = False
        self.init_called = False
        self.run_called = False
        
        # Pyxelの定数をモック
        self.KEY_LEFT = 'LEFT'
        self.KEY_RIGHT = 'RIGHT'
        self.KEY_UP = 'UP'
        self.KEY_DOWN = 'DOWN'
        self.KEY_X = 'X'
        self.KEY_Z = 'Z'
        self.KEY_Q = 'Q'
        self.KEY_ESCAPE = 'ESCAPE'
        self.KEY_G = 'G'
        self.KEY_C = 'C'
        self.KEY_E = 'E'
        self.KEY_A = 'A'
        self.KEY_R = 'R'
    
    def init(self, width, height, title):
        self.init_called = True
        self.width = width
        self.height = height
        self.title = title
    
    def run(self, update_func, draw_func):
        self.run_called = True
        self.update_func = update_func
        self.draw_func = draw_func
    
    def btn(self, key):
        return key in self.keys_pressed
    
    def btnp(self, key):
        return key in self.keys_just_pressed
    
    def quit(self):
        self.quit_called = True
    
    def cls(self, color):
        pass
    
    def text(self, x, y, text, color):
        pass
    
    def rect(self, x, y, w, h, color):
        pass
    
    def rectb(self, x, y, w, h, color):
        pass
    
    def press_key(self, key):
        """テスト用: キーを押す"""
        self.keys_just_pressed.add(key)
        self.keys_pressed.add(key)
    
    def release_key(self, key):
        """テスト用: キーを離す"""
        self.keys_just_pressed.discard(key)
        self.keys_pressed.discard(key)
    
    def clear_just_pressed(self):
        """テスト用: フレーム終了時の処理"""
        self.keys_just_pressed.clear()


def test_restart_from_game_over():
    """ゲームオーバーからのリスタートをテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # プレイ状態に遷移
        game.game_state_manager.start_game()
        assert game.game_state_manager.get_current_state() == GameState.PLAYING
        
        # ゲームオーバー状態を作成
        game.playfield.place_puyo(2, 0, Puyo(1))  # 上端にぷよを配置
        
        # 更新処理を実行してゲームオーバーを検出
        game.update()
        
        # 現在の状態を確認
        current_state = game.game_state_manager.get_current_state()
        print(f"Current state after update: {current_state}")
        
        # ゲームオーバー判定を直接実行
        is_game_over = game.check_game_over()
        print(f"Is game over: {is_game_over}")
        
        # 高度なゲームオーバー判定を実行
        is_game_over_adv, reason = game.check_game_over_advanced()
        print(f"Is game over (advanced): {is_game_over_adv}, Reason: {reason}")
        
        # 手動でゲームオーバー処理を実行
        game.handle_game_over("テスト用ゲームオーバー")
        
        # 遷移状態をリセット
        game.game_state_manager.transition_active = False
        
        # 遷移可能かどうかをチェック
        can_transition = game.game_state_manager.can_transition_to(GameState.GAME_OVER)
        print(f"Can transition to GAME_OVER: {can_transition}")
        
        # 手動で状態を変更
        result = game.game_state_manager.end_game()
        print(f"End game result: {result}")
        
        # 現在の状態を確認
        current_state = game.game_state_manager.get_current_state()
        print(f"Current state after end_game: {current_state}")
        
        # 強制的にゲームオーバー状態に変更
        game.game_state_manager.change_state(GameState.GAME_OVER)
        
        # ゲームオーバー状態に遷移していることを確認
        assert game.game_state_manager.get_current_state() == GameState.GAME_OVER
        
        # 遷移状態をリセット
        game.game_state_manager.transition_active = False
        
        # 遷移可能かどうかをチェック
        can_transition = game.game_state_manager.can_transition_to(GameState.PLAYING)
        print(f"Can transition to PLAYING: {can_transition}")
        
        # リスタート
        mock_pyxel.press_key(mock_pyxel.KEY_R)
        game.input_handler.update()
        
        # リスタートキーが検出されることを確認
        should_restart = game.input_handler.should_restart_game()
        print(f"Should restart: {should_restart}")
        
        # ゲームオーバー状態の更新処理を実行
        game.update_game_over_logic()
        
        # 現在の状態を確認
        current_state = game.game_state_manager.get_current_state()
        print(f"Current state after restart: {current_state}")
        
        # 遷移状態を確認
        is_in_transition = game.game_state_manager.is_in_transition()
        print(f"Is in transition: {is_in_transition}")
        
        # 遷移が完了するまで更新
        for _ in range(10):
            game.game_state_manager.update()
        
        # 最終的な状態を確認
        final_state = game.game_state_manager.get_current_state()
        print(f"Final state after updates: {final_state}")


if __name__ == "__main__":
    print("Running restart test...")
    test_restart_from_game_over()
    print("Restart test completed")