"""
Test file for the chain system implementation
Requirements: 3.4 - 連鎖判定の実装のテスト
"""

import sys
import os
# Add the parent directory to sys.path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.puyo import Puyo
from src.playfield import PlayField
from src.game import PuyoPuyoGame
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


def test_chain_initialization():
    """連鎖システムの初期化をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 連鎖システムの初期状態を確認
        assert game.chain_level == 0
        assert game.chain_active == False
        assert game.total_chain_score == 0
        
        print("[OK] Chain initialization test passed")


def test_chain_start():
    """連鎖開始のテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # プレイフィールドをクリア
        game.playfield.clear()
        
        # 消去可能なぷよを配置（4つの赤いぷよ）
        test_positions = [(0, 8), (0, 9), (1, 8), (1, 9)]
        for x, y in test_positions:
            game.playfield.place_puyo(x, y, Puyo(1))  # 赤いぷよ
        
        # 消去処理を開始
        game.start_elimination_process()
        
        # 連鎖が開始されていることを確認
        assert game.chain_active == True
        assert game.chain_level == 1
        assert game.elimination_active == True
        
        print("[OK] Chain start test passed")


def test_chain_continuation():
    """連鎖継続のテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # プレイフィールドをクリア
        game.playfield.clear()
        
        # 連鎖を手動で開始状態にする
        game.chain_active = True
        game.chain_level = 1
        
        # 新たな消去可能なぷよを配置
        test_positions = [(2, 8), (2, 9), (3, 8), (3, 9)]
        for x, y in test_positions:
            game.playfield.place_puyo(x, y, Puyo(2))  # オレンジのぷよ
        
        # 消去処理を開始（連鎖継続）
        game.start_elimination_process()
        
        # 連鎖レベルが増加していることを確認
        assert game.chain_active == True
        assert game.chain_level == 2
        assert game.elimination_active == True
        
        print("[OK] Chain continuation test passed")


def test_chain_end():
    """連鎖終了のテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 連鎖を手動で開始状態にする
        game.chain_active = True
        game.chain_level = 3
        game.total_chain_score = 1000
        
        # 連鎖を終了
        game.end_chain()
        
        # 連鎖状態がリセットされていることを確認
        assert game.chain_active == False
        assert game.chain_level == 0
        assert game.total_chain_score == 0
        
        print("[OK] Chain end test passed")


def test_chain_elimination_check():
    """連鎖消去判定のテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # プレイフィールドをクリア
        game.playfield.clear()
        
        # 連鎖状態を設定
        game.chain_active = True
        game.chain_level = 1
        
        # 消去可能なぷよがない状態で連鎖判定
        game.check_for_chain_elimination()
        
        # 連鎖が終了していることを確認
        assert game.chain_active == False
        assert game.chain_level == 0
        
        print("[OK] Chain elimination check test passed")


def test_chain_with_gravity():
    """重力処理と連鎖の統合テスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # プレイフィールドをクリア
        game.playfield.clear()
        
        # 連鎖を発生させる配置を作成
        # 底に4つの赤いぷよ
        bottom_positions = [(0, 10), (0, 11), (1, 10), (1, 11)]
        for x, y in bottom_positions:
            game.playfield.place_puyo(x, y, Puyo(1))  # 赤いぷよ
        
        # 上に4つの青いぷよ（重力で落下後に連鎖を形成）
        top_positions = [(0, 8), (0, 9), (1, 8), (1, 9)]
        for x, y in top_positions:
            game.playfield.place_puyo(x, y, Puyo(4))  # 青いぷよ
        
        # 消去処理を開始
        game.start_elimination_process()
        
        # 連鎖が開始されていることを確認
        assert game.chain_active == True
        assert game.chain_level == 1
        
        print("[OK] Chain with gravity integration test passed")


def test_no_chain_when_no_elimination():
    """消去がない場合は連鎖が開始されないことをテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # プレイフィールドをクリア
        game.playfield.clear()
        
        # 消去不可能なぷよを配置（3つだけ）
        test_positions = [(0, 9), (0, 10), (0, 11)]
        for x, y in test_positions:
            game.playfield.place_puyo(x, y, Puyo(1))  # 赤いぷよ
        
        # 消去処理を開始
        game.start_elimination_process()
        
        # 連鎖が開始されていないことを確認
        assert game.chain_active == False
        assert game.chain_level == 0
        assert game.elimination_active == False
        
        print("[OK] No chain when no elimination test passed")


def test_chain_level_increment():
    """連鎖レベルの増加をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # プレイフィールドをクリア
        game.playfield.clear()
        
        # 最初の連鎖を開始
        test_positions = [(0, 8), (0, 9), (1, 8), (1, 9)]
        for x, y in test_positions:
            game.playfield.place_puyo(x, y, Puyo(1))  # 赤いぷよ
        
        game.start_elimination_process()
        assert game.chain_active == True
        assert game.chain_level == 1
        
        # 連鎖継続をテスト
        game.playfield.clear()
        test_positions = [(2, 8), (2, 9), (3, 8), (3, 9)]
        for x, y in test_positions:
            game.playfield.place_puyo(x, y, Puyo(2))  # オレンジのぷよ
        
        game.start_elimination_process()
        assert game.chain_active == True
        assert game.chain_level == 2
        
        # 連鎖終了をテスト
        game.playfield.clear()
        game.start_elimination_process()  # 消去可能なぷよがない
        assert game.chain_active == False
        assert game.chain_level == 0
        
        print("[OK] Chain level increment test passed")


if __name__ == "__main__":
    print("Running chain system tests...")
    
    test_chain_initialization()
    test_chain_start()
    test_chain_continuation()
    test_chain_end()
    test_chain_elimination_check()
    test_chain_with_gravity()
    test_no_chain_when_no_elimination()
    test_chain_level_increment()
    
    print("All chain system tests passed! [OK]")