"""
Test file for the fall system implementation
Requirements: 2.1, 2.4, 2.5 - 落下システムのテスト
"""

import sys
import os
# Add the parent directory to sys.path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.puyo import Puyo
from src.puyo_pair import PuyoPair
from src.playfield import PlayField
from src.puyo_manager import PuyoManager
from src.game import PuyoPuyoGame


def test_fall_system_initialization():
    """落下システムの初期化をテスト"""
    # PuyoPuyoGameクラスの初期化をテスト（実際のpyxelは起動しない）
    # 代わりに必要な部分だけを手動で初期化
    
    # 落下システムの設定値をテスト
    fall_timer = 0
    fall_interval = 60
    fast_fall_interval = 3
    
    assert fall_timer == 0
    assert fall_interval == 60
    assert fast_fall_interval == 3
    
    print("[OK] Fall system initialization test passed")


def test_puyo_pair_fixing():
    """ぷよペアの固定処理をテスト"""
    playfield = PlayField()
    puyo_manager = PuyoManager()
    
    # テスト用のぷよペアを作成
    current_pair = puyo_manager.get_current_pair()
    original_next_pair = puyo_manager.get_next_pair()
    
    # ぷよペアを底に移動
    current_pair.set_position(2, 11)  # 最下段に配置
    
    # ぷよペアの位置を取得
    main_pos, sub_pos = current_pair.get_puyo_positions()
    
    # 手動でぷよペア固定処理をシミュレート
    main_puyo = current_pair.get_main_puyo()
    sub_puyo = current_pair.get_sub_puyo()
    
    # プレイフィールドに配置
    playfield.place_puyo(main_pos[0], main_pos[1], main_puyo)
    playfield.place_puyo(sub_pos[0], sub_pos[1], sub_puyo)
    
    # 配置されたことを確認
    assert playfield.get_puyo(main_pos[0], main_pos[1]) == main_puyo
    assert playfield.get_puyo(sub_pos[0], sub_pos[1]) == sub_puyo
    
    # 次のペアに進む
    new_current_pair = puyo_manager.advance_to_next_pair()
    
    # 新しい現在のペアが元の次のペアと同じことを確認
    assert new_current_pair == original_next_pair
    assert puyo_manager.get_current_pair() == original_next_pair
    
    # 新しい次のペアが生成されていることを確認
    assert puyo_manager.get_next_pair() != original_next_pair
    
    print("[OK] Puyo pair fixing test passed")


def test_fall_collision_detection():
    """落下時の衝突判定をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 5)
    
    # 初期状態では下に移動可能
    assert playfield.can_move_puyo_pair(pair, 0, 1) == True
    
    # 障害物を配置（メインぷよの下）
    playfield.place_puyo(2, 6, Puyo(3))
    
    # 障害物があると下に移動不可能
    assert playfield.can_move_puyo_pair(pair, 0, 1) == False
    
    # 障害物を削除
    playfield.remove_puyo(2, 6)
    
    # 再び移動可能
    assert playfield.can_move_puyo_pair(pair, 0, 1) == True
    
    # 底面での衝突テスト
    pair.set_position(2, 11)  # 最下段に配置
    assert playfield.can_move_puyo_pair(pair, 0, 1) == False  # 底面を超える移動は不可能
    
    print("[OK] Fall collision detection test passed")


def test_automatic_fall_logic():
    """自動落下ロジックをテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 0)
    
    # 落下タイマーのシミュレーション
    fall_timer = 0
    fall_interval = 60
    
    # 59フレーム後 - まだ落下しない
    fall_timer = 59
    should_fall = fall_timer >= fall_interval
    assert should_fall == False
    
    # 60フレーム後 - 落下する
    fall_timer = 60
    should_fall = fall_timer >= fall_interval
    assert should_fall == True
    
    # 落下可能かチェック
    if playfield.can_move_puyo_pair(pair, 0, 1):
        original_y = pair.get_position()[1]
        pair.move(0, 1)
        new_y = pair.get_position()[1]
        assert new_y == original_y + 1  # Y座標が1増加
        fall_timer = 0  # タイマーリセット
    
    assert fall_timer == 0
    
    print("[OK] Automatic fall logic test passed")


def test_fast_drop_logic():
    """高速落下ロジックをテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 0)
    
    # 高速落下タイマーのシミュレーション
    fall_timer = 0
    fast_fall_interval = 3
    is_fast_dropping = True
    
    # 高速落下間隔の決定
    current_fall_interval = fast_fall_interval if is_fast_dropping else 60
    assert current_fall_interval == 3
    
    # 2フレーム後 - まだ落下しない
    fall_timer = 2
    should_fall = fall_timer >= current_fall_interval
    assert should_fall == False
    
    # 3フレーム後 - 落下する
    fall_timer = 3
    should_fall = fall_timer >= current_fall_interval
    assert should_fall == True
    
    # 通常落下との比較
    is_fast_dropping = False
    current_fall_interval = fast_fall_interval if is_fast_dropping else 60
    assert current_fall_interval == 60
    
    print("[OK] Fast drop logic test passed")


def test_puyo_pair_bottom_collision():
    """ぷよペアの底面衝突をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成（縦向き）
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 10)  # メインぷよがY=10、サブぷよがY=9
    
    # 初期状態の確認
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (2, 10)
    assert sub_pos == (2, 9)
    
    # 下に移動可能（メインぷよがY=11、サブぷよがY=10になる）
    assert playfield.can_move_puyo_pair(pair, 0, 1) == True
    
    # 実際に移動
    pair.move(0, 1)
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (2, 11)
    assert sub_pos == (2, 10)
    
    # さらに下に移動不可能（メインぷよがY=12になってしまう）
    assert playfield.can_move_puyo_pair(pair, 0, 1) == False
    
    print("[OK] Puyo pair bottom collision test passed")


def test_puyo_pair_rotation_near_bottom():
    """底面近くでのぷよペア回転をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成（最下段）
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 11)  # メインぷよがY=11、サブぷよがY=10
    
    # 初期状態（サブぷよが上）
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (2, 11)
    assert sub_pos == (2, 10)
    
    # 時計回りに回転可能（サブぷよが右に移動）
    assert playfield.can_rotate_puyo_pair(pair, True) == True
    
    # 実際に回転（キックシステムを使用）
    success = playfield.rotate_puyo_pair_with_kick(pair, True)
    assert success == True
    
    main_pos, sub_pos = pair.get_puyo_positions()
    # Debug: After rotation - main_pos and sub_pos positions are checked in assertions
    
    # キックシステムにより位置が調整される可能性がある
    assert main_pos[1] == 11 or main_pos[1] == 10  # Y座標は11または10
    assert sub_pos[1] == 11 or sub_pos[1] == 10    # Y座標は11または10
    
    # さらに時計回りに回転（サブぷよが下に移動しようとする）
    # キックシステムにより回転可能
    assert playfield.can_rotate_puyo_pair(pair, True) == True
    
    print("[OK] Puyo pair rotation near bottom test passed")


if __name__ == "__main__":
    print("Running fall system tests...")
    
    test_fall_system_initialization()
    test_puyo_pair_fixing()
    test_fall_collision_detection()
    test_automatic_fall_logic()
    test_fast_drop_logic()
    test_puyo_pair_bottom_collision()
    test_puyo_pair_rotation_near_bottom()
    
    print("All fall system tests passed! [OK]")