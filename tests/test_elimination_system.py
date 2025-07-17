"""
Test file for the elimination system implementation
Requirements: 3.1, 5.2 - ぷよ消去処理とアニメーションのテスト
"""

import sys
import os
# Add the parent directory to sys.path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.puyo import Puyo
from src.playfield import PlayField


def test_erase_puyo_groups():
    """ぷよグループの消去をテスト"""
    playfield = PlayField()
    
    # 4つの赤いぷよを配置（2x2の正方形）
    puyo1 = Puyo(1)  # 赤
    puyo2 = Puyo(1)  # 赤
    puyo3 = Puyo(1)  # 赤
    puyo4 = Puyo(1)  # 赤
    
    playfield.place_puyo(1, 10, puyo1)
    playfield.place_puyo(1, 11, puyo2)
    playfield.place_puyo(2, 10, puyo3)
    playfield.place_puyo(2, 11, puyo4)
    
    # 消去前の状態確認
    assert playfield.get_puyo(1, 10) == puyo1
    assert playfield.get_puyo(1, 11) == puyo2
    assert playfield.get_puyo(2, 10) == puyo3
    assert playfield.get_puyo(2, 11) == puyo4
    
    # 消去するグループを定義
    groups_to_erase = [[(1, 10), (1, 11), (2, 10), (2, 11)]]
    
    # 消去実行
    total_erased = playfield.erase_puyo_groups(groups_to_erase)
    
    # 消去後の状態確認
    assert total_erased == 4
    assert playfield.get_puyo(1, 10) is None
    assert playfield.get_puyo(1, 11) is None
    assert playfield.get_puyo(2, 10) is None
    assert playfield.get_puyo(2, 11) is None
    
    print("[OK] Erase puyo groups test passed")


def test_erase_multiple_groups():
    """複数グループの同時消去をテスト"""
    playfield = PlayField()
    
    # 赤いぷよのグループ（4つ）
    for i in range(4):
        playfield.place_puyo(0, 8 + i, Puyo(1))  # 赤
    
    # 青いぷよのグループ（5つ）
    for i in range(5):
        playfield.place_puyo(5, 7 + i, Puyo(4))  # 青
    
    # 消去するグループを定義
    red_group = [(0, 8), (0, 9), (0, 10), (0, 11)]
    blue_group = [(5, 7), (5, 8), (5, 9), (5, 10), (5, 11)]
    groups_to_erase = [red_group, blue_group]
    
    # 消去実行
    total_erased = playfield.erase_puyo_groups(groups_to_erase)
    
    # 消去後の状態確認
    assert total_erased == 9  # 4 + 5
    
    # 赤いぷよが消去されている
    for i in range(4):
        assert playfield.get_puyo(0, 8 + i) is None
    
    # 青いぷよが消去されている
    for i in range(5):
        assert playfield.get_puyo(5, 7 + i) is None
    
    print("[OK] Erase multiple groups test passed")


def test_process_puyo_elimination():
    """ぷよ消去処理の統合テスト"""
    playfield = PlayField()
    
    # 消去可能なグループを作成（4つの緑のぷよ）
    for i in range(4):
        playfield.place_puyo(2, 8 + i, Puyo(3))  # 緑
    
    # 消去不可能なグループを作成（3つのオレンジのぷよ）
    for i in range(3):
        playfield.place_puyo(4, 9 + i, Puyo(2))  # オレンジ
    
    # 消去処理実行
    eliminated, total_erased, group_count = playfield.process_puyo_elimination()
    
    # 結果確認
    assert eliminated == True
    assert total_erased == 4
    assert group_count == 1
    
    # 緑のぷよが消去されている
    for i in range(4):
        assert playfield.get_puyo(2, 8 + i) is None
    
    # オレンジのぷよは残っている
    for i in range(3):
        assert playfield.get_puyo(4, 9 + i) is not None
    
    print("[OK] Process puyo elimination test passed")


def test_process_puyo_elimination_no_erasable():
    """消去可能なぷよがない場合のテスト"""
    playfield = PlayField()
    
    # 消去不可能なぷよのみ配置（3つずつ）
    for i in range(3):
        playfield.place_puyo(1, 9 + i, Puyo(1))  # 赤
        playfield.place_puyo(3, 9 + i, Puyo(2))  # オレンジ
    
    # 消去処理実行
    eliminated, total_erased, group_count = playfield.process_puyo_elimination()
    
    # 結果確認
    assert eliminated == False
    assert total_erased == 0
    assert group_count == 0
    
    # ぷよが残っている
    for i in range(3):
        assert playfield.get_puyo(1, 9 + i) is not None
        assert playfield.get_puyo(3, 9 + i) is not None
    
    print("[OK] Process puyo elimination no erasable test passed")


def test_get_puyo_colors_in_groups():
    """グループ内のぷよの色取得をテスト"""
    playfield = PlayField()
    
    # 異なる色のグループを作成
    # 赤いグループ
    for i in range(4):
        playfield.place_puyo(0, 8 + i, Puyo(1))  # 赤
    
    # 青いグループ
    for i in range(5):
        playfield.place_puyo(2, 7 + i, Puyo(4))  # 青
    
    # グループを定義
    red_group = [(0, 8), (0, 9), (0, 10), (0, 11)]
    blue_group = [(2, 7), (2, 8), (2, 9), (2, 10), (2, 11)]
    groups = [red_group, blue_group]
    
    # 色を取得
    colors = playfield.get_puyo_colors_in_groups(groups)
    
    # 結果確認
    assert len(colors) == 2
    assert colors[0] == 1  # 赤
    assert colors[1] == 4  # 青
    
    print("[OK] Get puyo colors in groups test passed")


def test_elimination_with_gravity_integration():
    """消去と重力の統合テスト"""
    playfield = PlayField()
    
    # 底に支えのぷよを配置
    playfield.place_puyo(2, 11, Puyo(1))  # 赤（支え）
    
    # 消去可能なグループを上に配置
    for i in range(4):
        playfield.place_puyo(2, 7 + i, Puyo(3))  # 緑（消去対象）
    
    # 浮いているぷよを配置
    playfield.place_puyo(2, 5, Puyo(2))  # オレンジ（浮いている）
    
    # 消去処理実行
    eliminated, total_erased, group_count = playfield.process_puyo_elimination()
    
    # 消去確認
    assert eliminated == True
    assert total_erased == 4
    
    # 緑のぷよが消去されている
    for i in range(4):
        assert playfield.get_puyo(2, 7 + i) is None
    
    # 重力適用
    gravity_applied = playfield.apply_gravity()
    
    # 重力確認
    assert gravity_applied == True
    
    # オレンジのぷよが落下している
    assert playfield.get_puyo(2, 5) is None  # 元の位置は空
    assert playfield.get_puyo(2, 10) is not None  # 落下先にある
    
    # 支えの赤いぷよは残っている
    assert playfield.get_puyo(2, 11) is not None
    
    print("[OK] Elimination with gravity integration test passed")


def test_chain_detection_setup():
    """連鎖検出のセットアップをテスト"""
    playfield = PlayField()
    
    # より単純な連鎖のセットアップを作成
    # 底に青いぷよ（4つ、消去対象）
    playfield.place_puyo(1, 11, Puyo(4))  # 青
    playfield.place_puyo(2, 11, Puyo(4))  # 青
    playfield.place_puyo(3, 11, Puyo(4))  # 青
    playfield.place_puyo(4, 11, Puyo(4))  # 青
    
    # 青いぷよの上に赤いぷよ（3つ、落下後に連鎖を起こす予定）
    playfield.place_puyo(1, 9, Puyo(1))   # 赤
    playfield.place_puyo(2, 9, Puyo(1))   # 赤
    playfield.place_puyo(3, 9, Puyo(1))   # 赤
    
    # 間に別の色のぷよ（1つ、障害物）
    playfield.place_puyo(1, 10, Puyo(2))  # オレンジ
    
    # 最初の消去処理
    eliminated, total_erased, group_count = playfield.process_puyo_elimination()
    
    # 青いぷよが消去される
    assert eliminated == True
    assert total_erased == 4  # 青いぷよ4つのみ
    
    # 重力適用
    gravity_applied = playfield.apply_gravity()
    assert gravity_applied == True  # 重力が適用される
    
    # 重力後の状態確認
    # 赤いぷよが下に落ちている（3つなので連鎖は起こらない）
    assert playfield.get_puyo(1, 11) is not None  # 赤いぷよが底に
    assert playfield.get_puyo(2, 11) is not None  # 赤いぷよが底に
    assert playfield.get_puyo(3, 11) is not None  # 赤いぷよが底に
    
    # オレンジのぷよも落下している
    assert playfield.get_puyo(1, 10) is not None  # オレンジのぷよ
    
    # 再度消去判定（赤いぷよは3つなので消去されない）
    eliminated2, total_erased2, group_count2 = playfield.process_puyo_elimination()
    
    # 赤いぷよは3つなので消去されない
    assert eliminated2 == False
    assert total_erased2 == 0
    
    print("[OK] Chain detection setup test passed")


def test_complex_elimination_scenario():
    """複雑な消去シナリオをテスト"""
    playfield = PlayField()
    
    # 複雑な配置を作成
    # L字型の赤いぷよ（5つ、消去対象）
    red_positions = [(1, 11), (2, 11), (3, 11), (1, 10), (1, 9)]
    for x, y in red_positions:
        playfield.place_puyo(x, y, Puyo(1))  # 赤
    
    # T字型の青いぷよ（4つ、消去対象）
    blue_positions = [(5, 11), (4, 10), (5, 10), (5, 9)]  # 有効な範囲内
    for x, y in blue_positions:
        if playfield.is_valid_position(x, y):
            playfield.place_puyo(x, y, Puyo(4))  # 青
    
    # 単独のぷよ（消去対象外）
    playfield.place_puyo(0, 11, Puyo(2))  # オレンジ
    
    # 消去処理実行
    eliminated, total_erased, group_count = playfield.process_puyo_elimination()
    
    # 結果確認
    assert eliminated == True
    assert total_erased >= 8  # 少なくとも赤5つ + 青4つ（範囲内のもの）
    assert group_count >= 1   # 少なくとも1グループ
    
    # 単独のオレンジのぷよは残っている
    assert playfield.get_puyo(0, 11) is not None
    
    print("[OK] Complex elimination scenario test passed")


if __name__ == "__main__":
    print("Running elimination system tests...")
    
    test_erase_puyo_groups()
    test_erase_multiple_groups()
    test_process_puyo_elimination()
    test_process_puyo_elimination_no_erasable()
    test_get_puyo_colors_in_groups()
    test_elimination_with_gravity_integration()
    test_chain_detection_setup()
    test_complex_elimination_scenario()
    
    print("All elimination system tests passed! [OK]")