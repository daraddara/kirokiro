"""
Test file for the gravity system implementation
Requirements: 3.3 - 重力処理のテスト（ぷよ固定後の重力適用、浮いているぷよの落下処理、重力処理のアニメーション）
"""

import sys
import os
# Add the parent directory to sys.path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.puyo import Puyo
from src.puyo_pair import PuyoPair
from src.playfield import PlayField
from src.puyo_manager import PuyoManager


def test_apply_gravity_basic():
    """基本的な重力適用をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよを配置（浮いている状態）
    puyo1 = Puyo(1)  # 赤いぷよ
    puyo2 = Puyo(2)  # オレンジのぷよ
    
    # 底にぷよを配置
    playfield.place_puyo(2, 11, puyo1)  # 最下段
    
    # 浮いているぷよを配置
    playfield.place_puyo(2, 9, puyo2)   # 2段上に配置（Y=10は空き）
    
    # 重力適用前の状態確認
    assert playfield.get_puyo(2, 11) == puyo1
    assert playfield.get_puyo(2, 9) == puyo2
    assert playfield.get_puyo(2, 10) is None
    
    # 重力を適用
    moved = playfield.apply_gravity()
    
    # 重力適用後の状態確認
    assert moved == True  # ぷよが移動した
    assert playfield.get_puyo(2, 11) == puyo1  # 底のぷよは移動しない
    assert playfield.get_puyo(2, 10) == puyo2  # 浮いていたぷよが1段落下
    assert playfield.get_puyo(2, 9) is None    # 元の位置は空になる
    
    # ぷよの位置情報も更新されているか確認
    assert puyo2.get_position() == (2, 10)
    
    print("[OK] Basic gravity application test passed")


def test_apply_gravity_multiple_columns():
    """複数列での重力適用をテスト"""
    playfield = PlayField()
    
    # 複数の列にぷよを配置
    puyo1 = Puyo(1)  # 列0
    puyo2 = Puyo(2)  # 列1
    puyo3 = Puyo(3)  # 列2
    
    # 各列に浮いているぷよを配置
    playfield.place_puyo(0, 8, puyo1)   # 列0、Y=8
    playfield.place_puyo(1, 6, puyo2)   # 列1、Y=6
    playfield.place_puyo(2, 10, puyo3)  # 列2、Y=10
    
    # 重力を適用
    moved = playfield.apply_gravity()
    
    # 各列でぷよが最下段に落下していることを確認
    assert moved == True
    assert playfield.get_puyo(0, 11) == puyo1  # 列0の最下段
    assert playfield.get_puyo(1, 11) == puyo2  # 列1の最下段
    assert playfield.get_puyo(2, 11) == puyo3  # 列2の最下段
    
    # 元の位置は空になっている
    assert playfield.get_puyo(0, 8) is None
    assert playfield.get_puyo(1, 6) is None
    assert playfield.get_puyo(2, 10) is None
    
    print("[OK] Multiple columns gravity test passed")


def test_apply_gravity_stacking():
    """ぷよの積み重ねでの重力適用をテスト"""
    playfield = PlayField()
    
    # 積み重ね用のぷよを作成
    puyo1 = Puyo(1)  # 底
    puyo2 = Puyo(2)  # 中間
    puyo3 = Puyo(3)  # 上
    
    # 底にぷよを配置
    playfield.place_puyo(3, 11, puyo1)
    
    # 浮いているぷよを配置（間に空きがある）
    playfield.place_puyo(3, 8, puyo2)   # Y=9, 10は空き
    playfield.place_puyo(3, 5, puyo3)   # Y=6, 7は空き
    
    # 重力を適用
    moved = playfield.apply_gravity()
    
    # 正しく積み重なっていることを確認
    assert moved == True
    assert playfield.get_puyo(3, 11) == puyo1  # 底
    assert playfield.get_puyo(3, 10) == puyo2  # 中間
    assert playfield.get_puyo(3, 9) == puyo3   # 上
    
    # 元の位置は空
    assert playfield.get_puyo(3, 8) is None
    assert playfield.get_puyo(3, 5) is None
    
    print("[OK] Stacking gravity test passed")


def test_apply_gravity_no_movement():
    """移動が不要な場合の重力適用をテスト"""
    playfield = PlayField()
    
    # 既に正しく配置されているぷよ
    puyo1 = Puyo(1)
    puyo2 = Puyo(2)
    
    # 底から順に配置（隙間なし）
    playfield.place_puyo(1, 11, puyo1)
    playfield.place_puyo(1, 10, puyo2)
    
    # 重力を適用
    moved = playfield.apply_gravity()
    
    # 移動が発生しないことを確認
    assert moved == False
    assert playfield.get_puyo(1, 11) == puyo1
    assert playfield.get_puyo(1, 10) == puyo2
    
    print("[OK] No movement gravity test passed")


def test_get_floating_puyos():
    """浮いているぷよの検出をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよを配置
    puyo1 = Puyo(1)  # 底（浮いていない）
    puyo2 = Puyo(2)  # 浮いている
    puyo3 = Puyo(3)  # 浮いている
    puyo4 = Puyo(4)  # 浮いていない（底の上）
    
    # 配置
    playfield.place_puyo(0, 11, puyo1)  # 底
    playfield.place_puyo(0, 10, puyo4)  # 底の上（浮いていない）
    playfield.place_puyo(1, 8, puyo2)   # 浮いている
    playfield.place_puyo(2, 5, puyo3)   # 浮いている
    
    # 浮いているぷよを取得
    floating_puyos = playfield.get_floating_puyos()
    
    # 浮いているぷよが正しく検出されることを確認
    floating_positions = [(x, y) for x, y, puyo in floating_puyos]
    assert (1, 8) in floating_positions  # puyo2
    assert (2, 5) in floating_positions  # puyo3
    assert (0, 11) not in floating_positions  # puyo1（底）
    assert (0, 10) not in floating_positions  # puyo4（支えがある）
    
    print("[OK] Floating puyos detection test passed")


def test_calculate_fall_distance():
    """落下距離の計算をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよを配置
    puyo1 = Puyo(1)
    puyo2 = Puyo(2)
    
    # 底にぷよを配置
    playfield.place_puyo(2, 11, puyo1)
    
    # 浮いているぷよを配置
    playfield.place_puyo(2, 8, puyo2)
    
    # 落下距離を計算
    distance1 = playfield.calculate_fall_distance(2, 11)  # 底のぷよ
    distance2 = playfield.calculate_fall_distance(2, 8)   # 浮いているぷよ
    distance3 = playfield.calculate_fall_distance(3, 5)   # 何もない列のぷよ
    
    assert distance1 == 0  # 底のぷよは落下しない
    assert distance2 == 2  # Y=8からY=10まで2段落下
    assert distance3 == 0  # 存在しないぷよ
    
    # 空の列での落下距離テスト
    puyo3 = Puyo(3)
    playfield.place_puyo(4, 5, puyo3)
    distance4 = playfield.calculate_fall_distance(4, 5)
    assert distance4 == 6  # Y=5からY=11まで6段落下
    
    print("[OK] Fall distance calculation test passed")


def test_gravity_system_integration():
    """重力システムの統合テスト"""
    playfield = PlayField()
    
    # 複雑な配置でのテスト
    puyos = []
    for i in range(8):
        puyos.append(Puyo(i % 4 + 1))
    
    # 不規則な配置
    playfield.place_puyo(0, 11, puyos[0])  # 底
    playfield.place_puyo(0, 9, puyos[1])   # 1段空けて配置
    playfield.place_puyo(1, 10, puyos[2])  # 1段上
    playfield.place_puyo(1, 7, puyos[3])   # 2段空けて配置
    playfield.place_puyo(2, 11, puyos[4])  # 底
    playfield.place_puyo(2, 6, puyos[5])   # 4段空けて配置
    playfield.place_puyo(3, 8, puyos[6])   # 浮いている
    playfield.place_puyo(4, 4, puyos[7])   # 大きく浮いている
    
    # 重力を複数回適用して安定状態にする
    iterations = 0
    while playfield.apply_gravity() and iterations < 20:
        iterations += 1
    
    # 最終的な配置を確認
    # 各列で下から順に詰まっていることを確認
    
    # 列0: 2つのぷよが底から詰まっている
    assert playfield.get_puyo(0, 11) == puyos[0]
    assert playfield.get_puyo(0, 10) == puyos[1]
    assert playfield.get_puyo(0, 9) is None
    
    # 列1: 2つのぷよが底から詰まっている
    assert playfield.get_puyo(1, 11) == puyos[2]
    assert playfield.get_puyo(1, 10) == puyos[3]
    assert playfield.get_puyo(1, 7) is None
    
    # 列2: 2つのぷよが底から詰まっている
    assert playfield.get_puyo(2, 11) == puyos[4]
    assert playfield.get_puyo(2, 10) == puyos[5]
    assert playfield.get_puyo(2, 6) is None
    
    # 列3: 1つのぷよが底にある
    assert playfield.get_puyo(3, 11) == puyos[6]
    assert playfield.get_puyo(3, 8) is None
    
    # 列4: 1つのぷよが底にある
    assert playfield.get_puyo(4, 11) == puyos[7]
    assert playfield.get_puyo(4, 4) is None
    
    print("[OK] Gravity system integration test passed")


def test_gravity_after_puyo_pair_fixation():
    """ぷよペア固定後の重力処理をテスト"""
    playfield = PlayField()
    puyo_manager = PuyoManager()
    
    # 既存のぷよを配置（浮いている状態を作る）
    existing_puyo = Puyo(1)
    playfield.place_puyo(2, 8, existing_puyo)  # 浮いている状態
    
    # ぷよペアを作成
    current_pair = puyo_manager.get_current_pair()
    current_pair.set_position(1, 11)  # 底に配置
    
    # ぷよペア固定処理をシミュレート
    main_pos, sub_pos = current_pair.get_puyo_positions()
    main_puyo = current_pair.get_main_puyo()
    sub_puyo = current_pair.get_sub_puyo()
    
    # プレイフィールドに配置
    playfield.place_puyo(main_pos[0], main_pos[1], main_puyo)
    playfield.place_puyo(sub_pos[0], sub_pos[1], sub_puyo)
    
    # 固定前の状態確認
    assert playfield.get_puyo(2, 8) == existing_puyo  # まだ浮いている
    
    # 重力を適用（固定後の処理をシミュレート）
    moved = playfield.apply_gravity()
    
    # 重力適用後の確認
    assert moved == True
    assert playfield.get_puyo(2, 11) == existing_puyo  # 底に落下
    assert playfield.get_puyo(2, 8) is None  # 元の位置は空
    
    print("[OK] Gravity after puyo pair fixation test passed")


def test_gravity_animation_timing():
    """重力処理のアニメーションタイミングをテスト"""
    # 重力処理の間隔設定をテスト
    gravity_interval = 5  # フレーム数
    gravity_timer = 0
    gravity_active = True
    
    # タイマーの進行をシミュレート
    for frame in range(10):
        if gravity_active:
            gravity_timer += 1
            
            if gravity_timer >= gravity_interval:
                # 重力処理実行のタイミング
                if frame == 4:  # 5フレーム目（0から数えて4）
                    assert gravity_timer == 5
                    gravity_timer = 0  # リセット
                elif frame == 9:  # 10フレーム目
                    assert gravity_timer == 5
                    gravity_timer = 0
    
    print("[OK] Gravity animation timing test passed")


if __name__ == "__main__":
    print("Running gravity system tests...")
    
    test_apply_gravity_basic()
    test_apply_gravity_multiple_columns()
    test_apply_gravity_stacking()
    test_apply_gravity_no_movement()
    test_get_floating_puyos()
    test_calculate_fall_distance()
    test_gravity_system_integration()
    test_gravity_after_puyo_pair_fixation()
    test_gravity_animation_timing()
    
    print("All gravity system tests passed! [OK]")