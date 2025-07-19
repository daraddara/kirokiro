"""
Test file for the game over detection system implementation
Requirements: 4.3, 4.4 - ゲームオーバー判定と状態遷移のテスト
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


def test_basic_game_over_detection():
    """基本的なゲームオーバー判定をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 初期状態ではゲームオーバーではない
        assert game.check_game_over() == False
        
        # プレイフィールドの上端（y=0）にぷよを配置
        game.playfield.place_puyo(2, 0, Puyo(1))  # 中央上端に赤いぷよ
        
        # ゲームオーバー判定がTrueになることを確認
        assert game.check_game_over() == True
        
        print("[OK] Basic game over detection test passed")


def test_advanced_game_over_detection():
    """高度なゲームオーバー判定をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # プレイフィールドをクリアして確実に空の状態にする
        game.playfield.clear()
        
        # 現在のぷよペアを下部に移動させて初期位置から離す
        if game.current_falling_pair is not None:
            game.current_falling_pair.set_position(2, 5)  # 中央下部に移動
        
        # 初期状態では正常
        is_game_over, reason = game.check_game_over_advanced()
        game.debug_print(f"is_game_over={is_game_over}, reason='{reason}'")
        assert is_game_over == False
        assert reason == "正常"
        
        # プレイフィールドの上端にぷよを配置
        game.playfield.place_puyo(3, 0, Puyo(2))  # 上端にオレンジのぷよ
        
        # 高度な判定でゲームオーバーが検出されることを確認
        is_game_over, reason = game.check_game_over_advanced()
        assert is_game_over == True
        assert "プレイフィールド上端到達" in reason
        assert "列 3" in reason
        
        print("[OK] Advanced game over detection test passed")


def test_danger_level_calculation():
    """危険レベル計算をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 初期状態では危険レベル0
        assert game.get_danger_level() == 0
        
        # 上から3行以内にぷよを配置
        game.playfield.place_puyo(0, 1, Puyo(1))  # 2行目に配置
        game.playfield.place_puyo(1, 2, Puyo(2))  # 3行目に配置
        
        # 危険レベルが2になることを確認
        assert game.get_danger_level() == 2
        
        # さらにぷよを追加
        game.playfield.place_puyo(2, 0, Puyo(3))  # 1行目に配置
        
        # 危険レベルが3になることを確認
        assert game.get_danger_level() == 3
        
        print("[OK] Danger level calculation test passed")


def test_game_over_handling():
    """ゲームオーバー処理をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 初期状態では最終スコア画面は表示されていない
        assert game.show_final_score == False
        
        # ゲームオーバー処理を実行
        game.handle_game_over()
        
        # 最終スコア画面が表示されることを確認
        assert game.show_final_score == True
        
        # 現在のぷよペアが削除されることを確認
        assert game.current_falling_pair is None
        
        print("[OK] Game over handling test passed")


def test_game_state_transition_on_game_over():
    """ゲームオーバー時の状態遷移をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # プレイ状態に変更
        game.game_state_manager.start_game()
        assert game.game_state_manager.get_current_state() == GameState.PLAYING
        
        # ゲームオーバー条件を作成
        game.playfield.place_puyo(2, 0, Puyo(1))
        
        # プレイ中状態の処理を実行（ゲームオーバー判定を含む）
        game.game_state_manager.transition_active = False  # 遷移完了状態にする
        game.update_playing_logic()
        
        # ゲームオーバー状態に遷移していることを確認
        assert game.game_state_manager.get_current_state() == GameState.GAME_OVER
        
        print("[OK] Game state transition on game over test passed")


def test_restart_functionality():
    """リスタート機能をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # ゲーム状態を設定（スコア、ぷよ配置など）
        game.score_manager.add_score(1000)
        game.playfield.place_puyo(1, 5, Puyo(2))
        game.show_final_score = True
        game.chain_level = 3
        
        # リスタート処理を実行
        game.restart_game()
        
        # ゲーム状態がリセットされていることを確認
        assert game.score_manager.get_score() == 0
        assert game.playfield.is_empty(1, 5) == True
        assert game.show_final_score == False
        assert game.chain_level == 0
        assert game.gravity_active == False
        assert game.elimination_active == False
        assert game.chain_active == False
        
        print("[OK] Restart functionality test passed")


def test_restart_input_handling():
    """リスタート入力処理をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # ゲームオーバー状態に設定
        game.game_state_manager.change_state(GameState.GAME_OVER)
        game.game_state_manager.transition_active = False
        
        # Rキーを押す
        mock_pyxel.press_key(mock_pyxel.KEY_R)
        game.input_handler.update()
        
        # ゲームオーバー状態の処理を実行
        game.update_game_over_logic()
        
        # プレイ状態に遷移していることを確認
        assert game.game_state_manager.get_current_state() == GameState.PLAYING
        
        print("[OK] Restart input handling test passed")


def test_multiple_game_over_conditions():
    """複数のゲームオーバー条件をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 複数の列の上端にぷよを配置
        game.playfield.place_puyo(0, 0, Puyo(1))  # 左端
        game.playfield.place_puyo(5, 0, Puyo(2))  # 右端
        
        # どちらの条件でもゲームオーバーが検出されることを確認
        assert game.check_game_over() == True
        
        # 高度な判定でも検出されることを確認
        is_game_over, reason = game.check_game_over_advanced()
        assert is_game_over == True
        assert "プレイフィールド上端到達" in reason
        
        print("[OK] Multiple game over conditions test passed")


def test_game_over_with_chain_active():
    """連鎖中のゲームオーバー判定をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 連鎖状態を設定
        game.chain_active = True
        game.chain_level = 2
        
        # ゲームオーバー条件を作成
        game.playfield.place_puyo(3, 0, Puyo(3))
        
        # 連鎖中でもゲームオーバーが検出されることを確認
        assert game.check_game_over() == True
        
        # ゲームオーバー処理後、連鎖状態がリセットされることを確認
        game.restart_game()
        assert game.chain_active == False
        assert game.chain_level == 0
        
        print("[OK] Game over with chain active test passed")


def test_danger_level_warning():
    """危険レベル警告をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # プレイフィールドをクリアして確実に空の状態にする
        game.playfield.clear()
        
        # 現在のぷよペアを下部に移動させて初期位置から離す
        if game.current_falling_pair is not None:
            game.current_falling_pair.set_position(2, 5)  # 中央下部に移動
        
        # 危険レベルが高い状態を作成（上から3行以内に3個のぷよ）
        game.playfield.place_puyo(0, 1, Puyo(1))
        game.playfield.place_puyo(1, 1, Puyo(2))
        game.playfield.place_puyo(2, 2, Puyo(3))
        
        # 高度な判定で警告が出ることを確認
        is_game_over, reason = game.check_game_over_advanced()
        game.debug_print(f"is_game_over={is_game_over}, reason='{reason}'")
        assert is_game_over == False  # まだゲームオーバーではない
        assert "危険レベル: 3" in reason
        
        print("[OK] Danger level warning test passed")


if __name__ == "__main__":
    print("Running game over detection system tests...")
    
    test_basic_game_over_detection()
    test_advanced_game_over_detection()
    test_danger_level_calculation()
    test_game_over_handling()
    test_game_state_transition_on_game_over()
    test_restart_functionality()
    test_restart_input_handling()
    test_multiple_game_over_conditions()
    test_game_over_with_chain_active()
    test_danger_level_warning()
    
    print("All game over detection system tests passed! [OK]")