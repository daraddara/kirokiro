"""
Test file for the kick system implementation
Requirements: 2.3 - キックシステムによる回転補助のテスト
"""

import sys
import os
# Add the parent directory to sys.path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.puyo import Puyo
from src.puyo_pair import PuyoPair
from src.playfield import PlayField


def test_normal_rotation_without_kick():
    """通常の回転（キック不要）をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成（中央に配置）
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 5)  # 中央、十分な空きがある位置
    
    # 初期状態（サブぷよが上）
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (2, 5)
    assert sub_pos == (2, 4)
    
    # 通常の回転（キック不要）
    can_rotate, kick_offset = playfield.try_rotate_with_kick(pair, True)
    
    assert can_rotate == True
    assert kick_offset == (0, 0)  # キック不要
    
    # 回転後の位置確認
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (2, 5)  # メインぷよは移動しない
    assert sub_pos == (3, 5)   # サブぷよが右に移動
    
    print("[OK] Normal rotation without kick test passed")


def test_right_kick():
    """右キックによる回転をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成（左端に配置）
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 0, 5)  # 左端
    
    # 初期状態（サブぷよが上）
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (0, 5)
    assert sub_pos == (0, 4)
    
    # 反時計回りに回転（サブぷよが左に移動しようとする）
    # 左端なので通常は回転不可能だが、右キックで成功するはず
    can_rotate, kick_offset = playfield.try_rotate_with_kick(pair, False)
    
    assert can_rotate == True
    assert kick_offset == (1, 0)  # 右に1マスキック
    
    # 回転後の位置確認（右に1マス移動して回転）
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (1, 5)  # メインぷよが右に1マス移動
    assert sub_pos == (0, 5)   # サブぷよが左に配置（元の位置）
    
    print("[OK] Right kick test passed")


def test_left_kick():
    """左キックによる回転をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成（右端に配置）
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 5, 5)  # 右端
    
    # 初期状態（サブぷよが上）
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (5, 5)
    assert sub_pos == (5, 4)
    
    # 時計回りに回転（サブぷよが右に移動しようとする）
    # 右端なので通常は回転不可能だが、左キックで成功するはず
    can_rotate, kick_offset = playfield.try_rotate_with_kick(pair, True)
    
    assert can_rotate == True
    assert kick_offset == (-1, 0)  # 左に1マスキック
    
    # 回転後の位置確認（左に1マス移動して回転）
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (4, 5)  # メインぷよが左に1マス移動
    assert sub_pos == (5, 5)   # サブぷよが右に配置（元の位置）
    
    print("[OK] Left kick test passed")


def test_up_kick():
    """上キックによる回転をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成（底面に配置）
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 11)  # 最下段
    
    # 時計回りに2回回転して下向きにする
    pair.rotate_clockwise()
    pair.rotate_clockwise()
    
    # 現在の状態（サブぷよが下、プレイフィールド外）
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (2, 11)
    assert sub_pos == (2, 12)  # プレイフィールド外
    
    # 左右に障害物を配置して、上キックを強制する
    playfield.place_puyo(1, 11, Puyo(3))  # 左に障害物
    playfield.place_puyo(3, 11, Puyo(3))  # 右に障害物
    
    # さらに時計回りに回転（サブぷよが左に移動しようとする）
    # 左右が塞がっているので上キックが必要
    can_rotate, kick_offset = playfield.try_rotate_with_kick(pair, True)
    
    assert can_rotate == True
    assert kick_offset == (0, -1)  # 上に1マスキック
    
    # 回転後の位置確認（上に1マス移動して回転）
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (2, 10)  # メインぷよが上に1マス移動
    assert sub_pos == (1, 10)   # サブぷよが左に配置
    
    print("[OK] Up kick test passed")


def test_kick_failure():
    """全てのキックが失敗する場合をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 5)
    
    # 回転先の全ての位置に障害物を配置
    playfield.place_puyo(3, 5, Puyo(3))  # 右
    playfield.place_puyo(1, 5, Puyo(3))  # 左
    playfield.place_puyo(2, 4, Puyo(3))  # 上
    
    # 元の状態を記録
    original_rotation = pair.get_rotation()
    original_position = pair.get_position()
    
    # 回転を試行（全てのキックが失敗するはず）
    can_rotate, kick_offset = playfield.try_rotate_with_kick(pair, True)
    
    assert can_rotate == False
    assert kick_offset == (0, 0)
    
    # 元の状態に戻っていることを確認
    assert pair.get_rotation() == original_rotation
    assert pair.get_position() == original_position
    
    print("[OK] Kick failure test passed")


def test_corner_rotation():
    """角での回転をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成（左上角）
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 0, 1)  # 左端、上から2番目
    
    # 初期状態（サブぷよが上）
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (0, 1)
    assert sub_pos == (0, 0)
    
    # 反時計回りに回転（サブぷよが左に移動しようとする）
    # 左端なので右キックが必要
    can_rotate, kick_offset = playfield.try_rotate_with_kick(pair, False)
    
    assert can_rotate == True
    assert kick_offset == (1, 0)  # 右キック
    
    # 回転後の位置確認
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (1, 1)  # メインぷよが右に移動
    assert sub_pos == (0, 1)   # サブぷよが左に配置
    
    print("[OK] Corner rotation test passed")


def test_kick_priority():
    """キックの優先順位をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 5)
    
    # 右側に障害物を配置（右キックを阻止）
    playfield.place_puyo(3, 5, Puyo(3))
    
    # 時計回りに回転（サブぷよが右に移動しようとする）
    # 通常の回転は失敗、右キックも失敗、左キックで成功するはず
    can_rotate, kick_offset = playfield.try_rotate_with_kick(pair, True)
    
    assert can_rotate == True
    assert kick_offset == (-1, 0)  # 左キック（右キックより優先度が低い）
    
    # 回転後の位置確認
    main_pos, sub_pos = pair.get_puyo_positions()
    assert main_pos == (1, 5)  # メインぷよが左に移動
    assert sub_pos == (2, 5)   # サブぷよが右に配置（元の位置）
    
    print("[OK] Kick priority test passed")


def test_rotate_puyo_pair_with_kick():
    """rotate_puyo_pair_with_kick メソッドをテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成（右端）
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 5, 5)
    
    # 元の状態を記録
    original_position = pair.get_position()
    original_rotation = pair.get_rotation()
    
    # キック付き回転を実行
    success = playfield.rotate_puyo_pair_with_kick(pair, True)
    
    assert success == True
    
    # 回転が実行されていることを確認
    assert pair.get_rotation() != original_rotation
    
    # 位置が変更されていることを確認（左キックが発生）
    new_position = pair.get_position()
    assert new_position != original_position
    assert new_position == (4, 5)  # 左に1マス移動
    
    print("[OK] rotate_puyo_pair_with_kick test passed")


def test_multiple_kicks():
    """複数回のキックをテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成（右端）
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 5, 5)
    
    # 複数回回転してキックが継続して動作することを確認
    for i in range(4):
        success = playfield.rotate_puyo_pair_with_kick(pair, True)
        assert success == True
    
    # 4回転後は元の向きに戻る
    assert pair.get_rotation() == 0
    
    print("[OK] Multiple kicks test passed")


if __name__ == "__main__":
    print("Running kick system tests...")
    
    test_normal_rotation_without_kick()
    test_right_kick()
    test_left_kick()
    test_up_kick()
    test_kick_failure()
    test_corner_rotation()
    test_kick_priority()
    test_rotate_puyo_pair_with_kick()
    test_multiple_kicks()
    
    print("All kick system tests passed! [OK]")