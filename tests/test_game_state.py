"""
Test file for the game state management system implementation
Requirements: 4.3, 4.4 - ゲーム状態管理と遷移制御のテスト
"""

import sys
import os
# Add the parent directory to sys.path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game_state import GameStateManager, GameState


def test_game_state_manager_initialization():
    """GameStateManagerの初期化をテスト"""
    manager = GameStateManager()
    
    # 初期状態の確認
    assert manager.get_current_state() == GameState.MENU
    assert manager.previous_state is None
    assert manager.state_change_timer == 0
    assert manager.transition_active == False
    assert manager.menu_selection == 0
    assert manager.game_over_timer == 0
    
    print("[OK] Game state manager initialization test passed")


def test_game_state_enum():
    """GameState列挙型をテスト"""
    # 各状態の値を確認
    assert GameState.MENU.value == "menu"
    assert GameState.PLAYING.value == "playing"
    assert GameState.GAME_OVER.value == "game_over"
    
    # 状態の比較
    assert GameState.MENU != GameState.PLAYING
    assert GameState.PLAYING != GameState.GAME_OVER
    assert GameState.GAME_OVER != GameState.MENU
    
    print("[OK] Game state enum test passed")


def test_state_checking():
    """状態確認機能をテスト"""
    manager = GameStateManager()
    
    # 初期状態（MENU）の確認
    assert manager.is_state(GameState.MENU) == True
    assert manager.is_state(GameState.PLAYING) == False
    assert manager.is_state(GameState.GAME_OVER) == False
    
    # 状態変更後の確認
    manager.change_state(GameState.PLAYING)
    assert manager.is_state(GameState.MENU) == False
    assert manager.is_state(GameState.PLAYING) == True
    assert manager.is_state(GameState.GAME_OVER) == False
    
    print("[OK] State checking test passed")


def test_state_transition():
    """状態遷移をテスト"""
    manager = GameStateManager()
    
    # 初期状態はMENU
    assert manager.get_current_state() == GameState.MENU
    
    # MENU -> PLAYING への遷移
    manager.change_state(GameState.PLAYING)
    assert manager.get_current_state() == GameState.PLAYING
    assert manager.previous_state == GameState.MENU
    assert manager.transition_active == True
    assert manager.state_change_timer == 0
    
    # PLAYING -> GAME_OVER への遷移
    manager.change_state(GameState.GAME_OVER)
    assert manager.get_current_state() == GameState.GAME_OVER
    assert manager.previous_state == GameState.PLAYING
    assert manager.transition_active == True
    
    print("[OK] State transition test passed")


def test_transition_validation():
    """状態遷移の妥当性チェックをテスト"""
    manager = GameStateManager()
    
    # MENU状態からの有効な遷移
    assert manager.can_transition_to(GameState.PLAYING) == True
    assert manager.can_transition_to(GameState.GAME_OVER) == False
    assert manager.can_transition_to(GameState.MENU) == False  # 同じ状態への遷移は無効
    
    # PLAYING状態に変更
    manager.change_state(GameState.PLAYING)
    
    # 遷移中は新しい遷移を許可しない
    assert manager.can_transition_to(GameState.GAME_OVER) == False
    assert manager.can_transition_to(GameState.MENU) == False
    
    # 遷移完了後
    manager.transition_active = False
    assert manager.can_transition_to(GameState.GAME_OVER) == True
    assert manager.can_transition_to(GameState.MENU) == True
    assert manager.can_transition_to(GameState.PLAYING) == False  # 同じ状態への遷移は無効
    
    print("[OK] Transition validation test passed")


def test_game_control_methods():
    """ゲーム制御メソッドをテスト"""
    manager = GameStateManager()
    
    # ゲーム開始（MENU -> PLAYING）
    result = manager.start_game()
    assert result == True
    assert manager.get_current_state() == GameState.PLAYING
    
    # 遷移完了後にゲーム終了（PLAYING -> GAME_OVER）
    manager.transition_active = False
    result = manager.end_game()
    assert result == True
    assert manager.get_current_state() == GameState.GAME_OVER
    
    # ゲーム再開始（GAME_OVER -> PLAYING）
    manager.transition_active = False
    result = manager.restart_game()
    assert result == True
    assert manager.get_current_state() == GameState.PLAYING
    
    # メニューに戻る（PLAYING -> MENU）
    manager.transition_active = False
    result = manager.return_to_menu()
    assert result == True
    assert manager.get_current_state() == GameState.MENU
    
    print("[OK] Game control methods test passed")


def test_invalid_transitions():
    """無効な状態遷移をテスト"""
    manager = GameStateManager()
    
    # MENU状態から無効な遷移を試行
    result = manager.end_game()  # MENU -> GAME_OVER は無効
    assert result == False
    assert manager.get_current_state() == GameState.MENU
    
    # PLAYING状態に変更
    manager.change_state(GameState.PLAYING)
    manager.transition_active = False
    
    # PLAYING状態から無効な遷移を試行
    result = manager.start_game()  # PLAYING -> PLAYING は無効（同じ状態）
    assert result == False
    assert manager.get_current_state() == GameState.PLAYING
    
    print("[OK] Invalid transitions test passed")


def test_state_update_system():
    """状態更新システムをテスト"""
    manager = GameStateManager()
    
    # 初期状態でのタイマー
    initial_timer = manager.state_change_timer
    
    # 更新処理を実行
    manager.update()
    
    # タイマーが増加していることを確認
    assert manager.state_change_timer == initial_timer + 1
    
    # 遷移中の場合の処理
    manager.change_state(GameState.PLAYING)
    assert manager.transition_active == True
    
    # 数回更新して遷移完了を確認
    for i in range(5):
        manager.update()
    
    # 遷移が完了していることを確認
    assert manager.transition_active == False
    
    print("[OK] State update system test passed")


def test_state_info_retrieval():
    """状態情報取得をテスト"""
    manager = GameStateManager()
    
    # 初期状態の情報取得
    info = manager.get_state_info()
    assert info['current_state'] == 'menu'
    assert info['previous_state'] is None
    assert info['state_change_timer'] == 0
    assert info['transition_active'] == False
    
    # 状態変更後の情報取得
    manager.change_state(GameState.PLAYING)
    info = manager.get_state_info()
    assert info['current_state'] == 'playing'
    assert info['previous_state'] == 'menu'
    assert info['transition_active'] == True
    
    print("[OK] State info retrieval test passed")


def test_time_in_current_state():
    """現在の状態にいる時間の取得をテスト"""
    manager = GameStateManager()
    
    # 初期状態での時間
    assert manager.get_time_in_current_state() == 0
    
    # 数回更新
    for i in range(10):
        manager.update()
    
    # 時間が正しく計測されていることを確認
    assert manager.get_time_in_current_state() == 10
    
    # 状態変更後は時間がリセットされることを確認
    manager.change_state(GameState.PLAYING)
    assert manager.get_time_in_current_state() == 0
    
    print("[OK] Time in current state test passed")


def test_transition_active_check():
    """遷移中フラグのチェックをテスト"""
    manager = GameStateManager()
    
    # 初期状態では遷移中ではない
    assert manager.is_in_transition() == False
    
    # 状態変更すると遷移中になる
    manager.change_state(GameState.PLAYING)
    assert manager.is_in_transition() == True
    
    # 手動で遷移完了にする
    manager.transition_active = False
    assert manager.is_in_transition() == False
    
    print("[OK] Transition active check test passed")


def test_state_specific_initialization():
    """状態別の初期化処理をテスト"""
    manager = GameStateManager()
    
    # MENU状態への遷移
    manager.change_state(GameState.MENU)
    assert manager.menu_selection == 0
    
    # GAME_OVER状態への遷移
    manager.change_state(GameState.GAME_OVER)
    assert manager.game_over_timer == 0
    
    # PLAYING状態への遷移（特別な初期化はないが、エラーが発生しないことを確認）
    manager.change_state(GameState.PLAYING)
    assert manager.get_current_state() == GameState.PLAYING
    
    print("[OK] State specific initialization test passed")


def test_game_over_timer():
    """ゲームオーバータイマーをテスト"""
    manager = GameStateManager()
    
    # GAME_OVER状態に変更
    manager.change_state(GameState.GAME_OVER)
    initial_timer = manager.game_over_timer
    
    # 更新処理を実行
    manager.update()
    
    # ゲームオーバータイマーが増加していることを確認
    assert manager.game_over_timer == initial_timer + 1
    
    print("[OK] Game over timer test passed")


if __name__ == "__main__":
    print("Running game state management system tests...")
    
    test_game_state_manager_initialization()
    test_game_state_enum()
    test_state_checking()
    test_state_transition()
    test_transition_validation()
    test_game_control_methods()
    test_invalid_transitions()
    test_state_update_system()
    test_state_info_retrieval()
    test_time_in_current_state()
    test_transition_active_check()
    test_state_specific_initialization()
    test_game_over_timer()
    
    print("All game state management system tests passed! [OK]")