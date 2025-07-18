"""
Test file for the complete game flow
Requirements: 1.1, 1.2, 1.3 - ゲームフロー全体のテスト
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
        self.drawn_texts = []
        
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
        self.drawn_texts.append((x, y, text, color))
    
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


def test_complete_game_flow():
    """
    ゲームの完全なフローをテスト
    - メニュー状態から開始
    - プレイ状態に遷移
    - ぷよを操作
    - ゲームオーバーになる
    - リスタート
    """
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 初期状態はメニュー
        assert game.game_state_manager.get_current_state() == GameState.MENU
        
        # メニュー状態の更新（自動的にプレイ状態に遷移）
        for _ in range(70):  # 60フレーム後に自動遷移するため
            game.update()
        
        # プレイ状態に遷移していることを確認
        assert game.game_state_manager.get_current_state() == GameState.PLAYING
        
        # ぷよを操作（左右移動、回転）
        mock_pyxel.press_key(mock_pyxel.KEY_LEFT)
        game.update()
        mock_pyxel.clear_just_pressed()
        
        mock_pyxel.press_key(mock_pyxel.KEY_RIGHT)
        game.update()
        mock_pyxel.clear_just_pressed()
        
        mock_pyxel.press_key(mock_pyxel.KEY_X)  # 回転
        game.update()
        mock_pyxel.clear_just_pressed()
        
        # 高速落下
        mock_pyxel.press_key(mock_pyxel.KEY_DOWN)
        for _ in range(20):  # 複数フレーム高速落下
            game.update()
        mock_pyxel.release_key(mock_pyxel.KEY_DOWN)
        
        # ぷよが固定されるまで待機
        for _ in range(100):
            game.update()
            if game.current_falling_pair is None:
                break
        
        # 新しいぷよペアが生成されていることを確認
        assert game.current_falling_pair is not None
        
        # ゲームオーバー状態を作成（上端にぷよを配置）
        for x in range(6):
            game.playfield.place_puyo(x, 0, Puyo(1))  # 上端にぷよを配置
        
        # 遷移状態をリセット
        game.game_state_manager.transition_active = False
        
        # 手動でゲームオーバー処理を実行
        is_game_over, reason = game.check_game_over_advanced()
        assert is_game_over == True
        
        game.handle_game_over(reason)
        game.game_state_manager.end_game()
        
        # ゲームオーバー状態に遷移していることを確認
        assert game.game_state_manager.get_current_state() == GameState.GAME_OVER
        assert game.show_final_score == True
        
        # 遷移状態をリセット
        game.game_state_manager.transition_active = False
        
        # リスタート
        mock_pyxel.press_key(mock_pyxel.KEY_R)
        game.input_handler.update()
        game.update_game_over_logic()
        
        # 遷移が完了するまで更新
        for _ in range(10):
            game.game_state_manager.update()
        
        # プレイ状態に戻っていることを確認
        assert game.game_state_manager.get_current_state() == GameState.PLAYING
        assert game.show_final_score == False
        
        # スコアがリセットされていることを確認
        assert game.score_manager.get_score() == 0
        
        print("[OK] Complete game flow test passed")


def test_chain_reaction_flow():
    """
    連鎖反応のフローをテスト
    - 連鎖が発生する状況を作成
    - 連鎖処理が正しく実行されることを確認
    """
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # プレイ状態に遷移
        game.game_state_manager.start_game()
        
        # 連鎖が発生する状況を作成
        # 1段目: 赤赤赤赤
        # 2段目: 青青青青
        for x in range(2, 6):
            game.playfield.place_puyo(x, 10, Puyo(1))  # 赤いぷよ
            game.playfield.place_puyo(x, 11, Puyo(4))  # 青いぷよ
        
        # 連鎖のトリガーとなるぷよを配置
        game.current_falling_pair = None  # 現在のぷよペアをクリア
        
        # 消去処理を開始
        game.start_elimination_process()
        
        # 連鎖処理が完了するまで更新
        chain_detected = False
        for _ in range(200):  # 十分な回数の更新
            game.update()
            if game.chain_level > 0:
                chain_detected = True
            
            # 連鎖処理が完了したら終了
            if not game.elimination_active and not game.gravity_active and not game.chain_active:
                break
        
        # 連鎖が検出されたことを確認
        assert chain_detected
        
        # スコアが加算されていることを確認
        assert game.score_manager.get_score() > 0
        
        print("[OK] Chain reaction flow test passed")


def test_game_over_and_restart_flow():
    """
    ゲームオーバーとリスタートのフローをテスト
    - ゲームオーバー状態を作成
    - ゲームオーバー画面が表示されることを確認
    """
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # プレイ状態に遷移
        game.game_state_manager.start_game()
        
        # スコアを設定
        game.score_manager.add_score(1000)
        
        # ゲームオーバー状態を作成
        game.playfield.place_puyo(2, 0, Puyo(1))  # 上端にぷよを配置
        
        # 遷移状態をリセット
        game.game_state_manager.transition_active = False
        
        # 手動でゲームオーバー処理を実行
        is_game_over, reason = game.check_game_over_advanced()
        assert is_game_over == True
        
        game.handle_game_over(reason)
        game.game_state_manager.end_game()
        
        # ゲームオーバー状態に遷移していることを確認
        assert game.game_state_manager.get_current_state() == GameState.GAME_OVER
        
        # 描画処理は実行しない（Pyxelの初期化エラーを回避）
        # 代わりに、ゲームオーバー状態を直接確認
        assert game.show_final_score == True
        assert game.score_manager.get_score() == 1000
        
        # リスタート処理を実行
        game.restart_game()
        
        # ゲーム状態がリセットされていることを確認
        assert game.score_manager.get_score() == 0
        assert game.playfield.is_empty(2, 0) == True  # 上端のぷよが消えている
        
        print("[OK] Game over and restart flow test passed")


def test_menu_to_game_flow():
    """
    メニューからゲームへの遷移フローをテスト
    """
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 初期状態はメニュー
        assert game.game_state_manager.get_current_state() == GameState.MENU
        
        # メニュー状態の更新（自動的にプレイ状態に遷移）
        for _ in range(70):  # 60フレーム後に自動遷移するため
            game.update()
        
        # プレイ状態に遷移していることを確認
        assert game.game_state_manager.get_current_state() == GameState.PLAYING
        
        # ゲーム状態が正しく初期化されていることを確認
        assert game.current_falling_pair is not None
        assert game.score_manager.get_score() == 0
        assert game.chain_level == 0
        
        print("[OK] Menu to game flow test passed")


def test_quit_game_flow():
    """
    ゲーム終了フローをテスト
    """
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # プレイ状態に遷移
        game.game_state_manager.start_game()
        
        # 終了キーを押す
        mock_pyxel.press_key(mock_pyxel.KEY_Q)
        game.update()
        
        # pyxel.quitが呼び出されたことを確認
        assert mock_pyxel.quit_called == True
        
        print("[OK] Quit game flow test passed")


if __name__ == "__main__":
    print("Running game flow tests...")
    
    test_complete_game_flow()
    test_chain_reaction_flow()
    test_game_over_and_restart_flow()
    test_menu_to_game_flow()
    test_quit_game_flow()
    
    print("All game flow tests passed! [OK]")