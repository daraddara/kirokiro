"""
Test file for the score display system implementation
Requirements: 4.1, 4.4 - スコア表示とアニメーションのテスト
"""

import sys
import os
# Add the parent directory to sys.path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game import PuyoPuyoGame
from src.score_manager import ScoreManager
import unittest.mock as mock


class MockPyxel:
    """Pyxelのモック - テスト用"""
    
    def __init__(self):
        self.keys_pressed = set()
        self.keys_just_pressed = set()
        self.quit_called = False
        self.init_called = False
        self.run_called = False
        self.drawn_texts = []  # 描画されたテキストを記録
        self.drawn_rects = []  # 描画された矩形を記録
        
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
        self.drawn_rects.append(('rect', x, y, w, h, color))
    
    def rectb(self, x, y, w, h, color):
        self.drawn_rects.append(('rectb', x, y, w, h, color))


def test_score_display_initialization():
    """スコア表示システムの初期化をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # スコア表示システムの初期状態を確認
        assert game.score_animation_active == False
        assert game.score_animation_timer == 0
        assert game.score_animation_phase == 0.0
        assert game.last_displayed_score == 0
        assert game.score_increment_amount == 0
        assert game.show_final_score == False
        
        print("[OK] Score display initialization test passed")


def test_score_animation_trigger():
    """スコア変更時のアニメーション開始をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # スコアを変更
        game.score_manager.add_score(100)
        
        # スコア表示システムを更新
        game.update_score_display_system()
        
        # アニメーションが開始されていることを確認
        assert game.score_animation_active == True
        # update_score_display_system内でタイマーが1増加するため、1になる
        assert game.score_animation_timer == 1
        assert game.score_increment_amount == 100
        assert game.last_displayed_score == 100
        
        print("[OK] Score animation trigger test passed")


def test_score_animation_update():
    """スコアアニメーションの更新をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # アニメーションを手動で開始
        game.score_animation_active = True
        game.score_animation_timer = 0
        game.score_animation_phase = 0.0
        
        # アニメーションを数フレーム更新
        for i in range(10):
            game.update_score_display_system()
        
        # アニメーション状態が更新されていることを確認
        assert game.score_animation_timer == 10
        assert game.score_animation_phase > 0.0
        assert game.score_animation_active == True
        
        print("[OK] Score animation update test passed")


def test_score_animation_completion():
    """スコアアニメーションの完了をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # アニメーションを手動で開始
        game.score_animation_active = True
        game.score_animation_timer = 0
        
        # アニメーション完了まで更新（60フレーム）
        for i in range(60):
            game.update_score_display_system()
        
        # アニメーションが完了していることを確認
        assert game.score_animation_active == False
        assert game.score_animation_timer == 0
        
        print("[OK] Score animation completion test passed")


def test_enhanced_score_display_drawing():
    """強化されたスコア表示の描画をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # スコアを設定
        game.score_manager.add_score(1234)
        
        # 強化されたスコア表示を描画
        game.draw_enhanced_score_display(100, 50)
        
        # 描画されたテキストを確認
        drawn_texts = mock_pyxel.drawn_texts
        assert len(drawn_texts) >= 2  # 最低でもラベルとスコア値
        
        # "SCORE"ラベルが描画されていることを確認
        score_label_found = any("SCORE" in text for _, _, text, _ in drawn_texts)
        assert score_label_found
        
        # スコア値が描画されていることを確認
        score_value_found = any("1,234" in text for _, _, text, _ in drawn_texts)
        assert score_value_found
        
        # 背景枠が描画されていることを確認
        assert len(mock_pyxel.drawn_rects) >= 1
        
        print("[OK] Enhanced score display drawing test passed")


def test_score_display_with_animation():
    """アニメーション中のスコア表示をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # スコアを設定してアニメーションを開始
        game.score_manager.add_score(500)
        game.score_animation_active = True
        game.score_increment_amount = 500
        game.score_animation_phase = 1.0
        
        # アニメーション中のスコア表示を描画
        game.draw_enhanced_score_display(100, 50)
        
        # 描画されたテキストを確認
        drawn_texts = mock_pyxel.drawn_texts
        
        # スコア増加量が表示されていることを確認
        increment_found = any("+500" in text for _, _, text, _ in drawn_texts)
        assert increment_found
        
        print("[OK] Score display with animation test passed")


def test_final_score_display():
    """最終スコア表示をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 最終スコアを設定
        game.score_manager.add_score(9876)
        game.show_final_score = True
        
        # 最終スコア表示を描画
        game.draw_final_score_display()
        
        # 描画されたテキストを確認
        drawn_texts = mock_pyxel.drawn_texts
        
        # "FINAL SCORE"ラベルが描画されていることを確認
        final_label_found = any("FINAL SCORE" in text for _, _, text, _ in drawn_texts)
        assert final_label_found
        
        # 最終スコア値が描画されていることを確認
        final_score_found = any("9,876" in text for _, _, text, _ in drawn_texts)
        assert final_score_found
        
        # リスタート指示が描画されていることを確認
        restart_found = any("Press R to Restart" in text for _, _, text, _ in drawn_texts)
        assert restart_found
        
        # 背景が描画されていることを確認
        background_rects = [r for r in mock_pyxel.drawn_rects if r[0] == 'rect']
        border_rects = [r for r in mock_pyxel.drawn_rects if r[0] == 'rectb']
        assert len(background_rects) >= 1
        assert len(border_rects) >= 1
        
        print("[OK] Final score display test passed")


def test_show_final_score_screen():
    """最終スコア画面表示機能をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 初期状態では最終スコア画面は表示されていない
        assert game.show_final_score == False
        
        # 最終スコア画面を表示
        game.show_final_score_screen()
        
        # 最終スコア画面が表示状態になっていることを確認
        assert game.show_final_score == True
        
        print("[OK] Show final score screen test passed")


def test_score_display_integration():
    """スコア表示システムの統合テスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 初期状態でのスコア表示
        game.draw_enhanced_score_display(100, 50)
        initial_texts = len(mock_pyxel.drawn_texts)
        
        # スコアを変更
        game.score_manager.add_score(250)
        game.update_score_display_system()
        
        # アニメーション状態を確認
        assert game.score_animation_active == True
        assert game.score_increment_amount == 250
        
        # アニメーション中の描画
        mock_pyxel.drawn_texts.clear()
        game.draw_enhanced_score_display(100, 50)
        animated_texts = len(mock_pyxel.drawn_texts)
        
        # アニメーション中は追加のテキスト（増加量）が表示される
        assert animated_texts > initial_texts
        
        print("[OK] Score display integration test passed")


def test_score_formatting_in_display():
    """スコア表示でのフォーマット機能をテスト"""
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), mock.patch('src.input_handler.pyxel', mock_pyxel):
        # ゲーム初期化
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # 大きなスコアを設定
        game.score_manager.add_score(123456)
        
        # スコア表示を描画
        game.draw_enhanced_score_display(100, 50)
        
        # 描画されたテキストを確認
        drawn_texts = mock_pyxel.drawn_texts
        
        # 3桁区切りでフォーマットされたスコアが表示されていることを確認
        formatted_score_found = any("123,456" in text for _, _, text, _ in drawn_texts)
        assert formatted_score_found
        
        print("[OK] Score formatting in display test passed")


if __name__ == "__main__":
    print("Running score display system tests...")
    
    test_score_display_initialization()
    test_score_animation_trigger()
    test_score_animation_update()
    test_score_animation_completion()
    test_enhanced_score_display_drawing()
    test_score_display_with_animation()
    test_final_score_display()
    test_show_final_score_screen()
    test_score_display_integration()
    test_score_formatting_in_display()
    
    print("All score display system tests passed! [OK]")