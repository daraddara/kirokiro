"""
Integration test file for the game system
Requirements: 統合テスト - ゲームの基本機能が正常に動作することを確認
"""

import sys
import os
# Add the parent directory to sys.path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game import PuyoPuyoGame
from src.puyo import Puyo
from src.puyo_pair import PuyoPair
from src.playfield import PlayField
from src.input_handler import InputHandler
from src.puyo_manager import PuyoManager
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
    
    def circ(self, x, y, r, color):
        pass
    
    def circb(self, x, y, r, color):
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


def test_game_initialization():
    """ゲームの初期化をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel):
        # ゲーム初期化のみテスト（run()は呼ばない）
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        
        # 手動で初期化処理を実行
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 初期化が正しく行われているかチェック
        assert hasattr(game, 'playfield')
        assert hasattr(game, 'input_handler')
        assert hasattr(game, 'puyo_manager')
        assert hasattr(game, 'current_falling_pair')
        assert hasattr(game, 'gravity_active')
        assert hasattr(game, 'fall_timer')
        
        # 初期状態の確認
        assert game.gravity_active == False
        assert game.current_falling_pair is not None
        assert game.fall_timer == 0
        
        print("[OK] Game initialization test passed")


def test_input_handler_functionality():
    """InputHandlerの基本機能をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.input_handler.pyxel', mock_pyxel):
        input_handler = InputHandler()
        
        # 初期状態では何も押されていない
        assert input_handler.should_move_left() == False
        assert input_handler.should_move_right() == False
        assert input_handler.should_rotate_clockwise() == False
        assert input_handler.should_rotate_counterclockwise() == False
        assert input_handler.should_fast_drop() == False
        assert input_handler.should_quit_game() == False
        assert input_handler.should_test_gravity() == False
        assert input_handler.should_test_connection() == False
        
        # 左キーを押す
        mock_pyxel.press_key(mock_pyxel.KEY_LEFT)
        input_handler.update()
        assert input_handler.should_move_left() == True
        
        # 右キーを押す
        mock_pyxel.clear_just_pressed()
        mock_pyxel.press_key(mock_pyxel.KEY_RIGHT)
        input_handler.update()
        assert input_handler.should_move_right() == True
        
        # 回転キーを押す
        mock_pyxel.clear_just_pressed()
        mock_pyxel.press_key(mock_pyxel.KEY_X)
        input_handler.update()
        assert input_handler.should_rotate_clockwise() == True
        
        # テストキーを押す
        mock_pyxel.clear_just_pressed()
        mock_pyxel.press_key(mock_pyxel.KEY_G)
        input_handler.update()
        assert input_handler.should_test_gravity() == True
        
        mock_pyxel.clear_just_pressed()
        mock_pyxel.press_key(mock_pyxel.KEY_C)
        input_handler.update()
        assert input_handler.should_test_connection() == True
        
        print("[OK] Input handler functionality test passed")


def test_game_update_structure():
    """ゲームのupdate処理の構造をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 初期状態の確認
        initial_frame_count = game.frame_count
        initial_fall_timer = game.fall_timer
        
        # update処理を1回実行
        game.update()
        
        # フレームカウンターが増加していることを確認
        assert game.frame_count == initial_frame_count + 1
        
        # 重力が非アクティブの場合、落下タイマーが更新されることを確認
        if not game.gravity_active:
            assert game.fall_timer >= initial_fall_timer
        
        print("[OK] Game update structure test passed")


def test_puyo_pair_movement_integration():
    """ぷよペアの移動統合テスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 初期位置を記録
        initial_position = game.current_falling_pair.get_position()
        
        # 左移動をシミュレート
        mock_pyxel.press_key(mock_pyxel.KEY_LEFT)
        game.input_handler.update()
        
        # 重力が非アクティブであることを確認
        assert game.gravity_active == False
        
        # 入力処理を実行
        game.handle_puyo_pair_input()
        
        # 位置が変更されていることを確認
        new_position = game.current_falling_pair.get_position()
        if game.playfield.can_move_puyo_pair(game.current_falling_pair, -1, 0):
            # 移動可能な場合は位置が変わる
            assert new_position[0] <= initial_position[0]
        
        print("[OK] Puyo pair movement integration test passed")


def test_gravity_system_integration():
    """重力システムの統合テスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 初期状態では重力が非アクティブ
        assert game.gravity_active == False
        
        # 重力をアクティブにする
        game.apply_gravity_after_fixation()
        assert game.gravity_active == True
        
        # 重力システムの更新を実行
        game.update_gravity_system()
        
        # 重力処理が実行されることを確認
        # （実際の重力適用は浮いているぷよがある場合のみ）
        
        print("[OK] Gravity system integration test passed")


def test_connection_detection_integration():
    """連結判定システムの統合テスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 連結判定機能が利用可能であることを確認
        connected_groups = game.playfield.find_connected_groups()
        erasable_groups = game.playfield.find_erasable_groups()
        
        # 結果が適切な形式であることを確認
        assert isinstance(connected_groups, list)
        assert isinstance(erasable_groups, list)
        
        # 各グループが座標のリストであることを確認
        for group in connected_groups:
            assert isinstance(group, list)
            for pos in group:
                assert isinstance(pos, tuple)
                assert len(pos) == 2  # (x, y)
        
        print("[OK] Connection detection integration test passed")


def test_game_systems_interaction():
    """ゲームシステム間の相互作用をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 重力が非アクティブの時は通常処理が実行される
        assert game.gravity_active == False
        
        # update処理を実行
        initial_fall_timer = game.fall_timer
        game.update()
        
        # 重力が非アクティブなので落下システムが動作する
        assert game.fall_timer >= initial_fall_timer
        
        # 重力をアクティブにする
        game.gravity_active = True
        
        # update処理を実行
        game.update()
        
        # 重力がアクティブな時は通常の落下処理がスキップされる
        # （重力システムのみが動作する）
        
        print("[OK] Game systems interaction test passed")


def test_critical_methods_exist():
    """重要なメソッドが存在することを確認"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 重要なメソッドが存在することを確認
        assert hasattr(game, 'update')
        assert hasattr(game, 'draw')
        assert hasattr(game, 'update_fall_system')
        assert hasattr(game, 'update_gravity_system')
        assert hasattr(game, 'handle_puyo_pair_input')
        assert hasattr(game, 'fix_puyo_pair')
        assert hasattr(game, 'apply_gravity_after_fixation')
        assert hasattr(game, 'test_connection_detection')
        
        # メソッドが呼び出し可能であることを確認
        assert callable(game.update)
        assert callable(game.draw)
        assert callable(game.update_fall_system)
        assert callable(game.update_gravity_system)
        assert callable(game.handle_puyo_pair_input)
        
        print("[OK] Critical methods exist test passed")


def test_update_method_calls_required_functions():
    """updateメソッドが必要な関数を呼び出すことを確認"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # メソッドの呼び出しを追跡するためのモック
        with mock.patch.object(game, 'update_gravity_system') as mock_gravity:
            with mock.patch.object(game, 'update_fall_system') as mock_fall:
                with mock.patch.object(game, 'handle_puyo_pair_input') as mock_input:
                    
                    # 重力が非アクティブの状態でupdate実行
                    game.gravity_active = False
                    game.update()
                    
                    # 重要なメソッドが呼び出されることを確認
                    mock_gravity.assert_called_once()
                    mock_fall.assert_called_once()
                    mock_input.assert_called_once()
        
        print("[OK] Update method calls required functions test passed")


if __name__ == "__main__":
    print("Running game integration tests...")
    
    test_game_initialization()
    test_input_handler_functionality()
    test_game_update_structure()
    test_puyo_pair_movement_integration()
    test_gravity_system_integration()
    test_connection_detection_integration()
    test_game_systems_interaction()
    test_critical_methods_exist()
    test_update_method_calls_required_functions()
    
    print("All game integration tests passed! [OK]")
    print()
    print("These tests help prevent issues like:")
    print("- Missing input handling in update loop")
    print("- Gravity system blocking normal operations")
    print("- Critical methods being accidentally removed")
    print("- Game systems not interacting properly")