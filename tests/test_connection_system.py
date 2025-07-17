"""
Test file for the connection detection system implementation
Requirements: 3.1 - 同色ぷよの隣接判定と連結グループの検出のテスト
"""

import sys
import os
# Add the parent directory to sys.path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.puyo import Puyo
from src.playfield import PlayField


def test_find_connected_groups_basic():
    """基本的な連結グループ検出をテスト"""
    playfield = PlayField()
    
    # 2x2の赤いぷよグループを作成
    playfield.place_puyo(1, 10, Puyo(1))  # 赤
    playfield.place_puyo(1, 11, Puyo(1))  # 赤
    playfield.place_puyo(2, 10, Puyo(1))  # 赤
    playfield.place_puyo(2, 11, Puyo(1))  # 赤
    
    # 単独の青いぷよを配置
    playfield.place_puyo(4, 11, Puyo(4))  # 青
    
    # 連結グループを検出
    groups = playfield.find_connected_groups()
    
    # 2つのグループが検出されるはず（赤4つ、青1つ）
    assert len(groups) == 2
    
    # グループのサイズを確認
    group_sizes = [len(group) for group in groups]
    group_sizes.sort()
    assert group_sizes == [1, 4]  # 1つと4つのグループ
    
    # 赤いぷよのグループを確認
    red_group = None
    blue_group = None
    for group in groups:
        if len(group) == 4:
            red_group = group
        else:
            blue_group = group
    
    # 赤いぷよのグループの座標を確認
    red_positions = set(red_group)
    expected_red = {(1, 10), (1, 11), (2, 10), (2, 11)}
    assert red_positions == expected_red
    
    # 青いぷよのグループの座標を確認
    blue_positions = set(blue_group)
    expected_blue = {(4, 11)}
    assert blue_positions == expected_blue
    
    print("[OK] Basic connected groups detection test passed")


def test_find_connected_groups_line():
    """直線状の連結グループをテスト"""
    playfield = PlayField()
    
    # 縦一列の緑のぷよを配置
    for y in range(8, 12):
        playfield.place_puyo(2, y, Puyo(3))  # 緑
    
    # 連結グループを検出
    groups = playfield.find_connected_groups()
    
    # 1つのグループが検出されるはず
    assert len(groups) == 1
    
    # グループのサイズを確認
    assert len(groups[0]) == 4
    
    # グループの座標を確認
    positions = set(groups[0])
    expected = {(2, 8), (2, 9), (2, 10), (2, 11)}
    assert positions == expected
    
    print("[OK] Line connected groups detection test passed")


def test_find_connected_groups_l_shape():
    """L字型の連結グループをテスト"""
    playfield = PlayField()
    
    # L字型のオレンジのぷよを配置
    playfield.place_puyo(1, 11, Puyo(2))  # オレンジ
    playfield.place_puyo(1, 10, Puyo(2))  # オレンジ
    playfield.place_puyo(1, 9, Puyo(2))   # オレンジ
    playfield.place_puyo(2, 11, Puyo(2))  # オレンジ
    playfield.place_puyo(3, 11, Puyo(2))  # オレンジ
    
    # 連結グループを検出
    groups = playfield.find_connected_groups()
    
    # 1つのグループが検出されるはず
    assert len(groups) == 1
    
    # グループのサイズを確認
    assert len(groups[0]) == 5
    
    # グループの座標を確認
    positions = set(groups[0])
    expected = {(1, 11), (1, 10), (1, 9), (2, 11), (3, 11)}
    assert positions == expected
    
    print("[OK] L-shape connected groups detection test passed")


def test_find_connected_groups_separate():
    """分離した同色グループをテスト"""
    playfield = PlayField()
    
    # 分離した2つの赤いぷよグループを配置
    # グループ1
    playfield.place_puyo(0, 10, Puyo(1))  # 赤
    playfield.place_puyo(0, 11, Puyo(1))  # 赤
    
    # グループ2（1マス空けて配置）
    playfield.place_puyo(2, 10, Puyo(1))  # 赤
    playfield.place_puyo(2, 11, Puyo(1))  # 赤
    
    # 連結グループを検出
    groups = playfield.find_connected_groups()
    
    # 2つのグループが検出されるはず
    assert len(groups) == 2
    
    # 両方とも2つのぷよからなるグループ
    group_sizes = [len(group) for group in groups]
    group_sizes.sort()
    assert group_sizes == [2, 2]
    
    # グループの座標を確認
    all_positions = set()
    for group in groups:
        all_positions.update(group)
    
    expected = {(0, 10), (0, 11), (2, 10), (2, 11)}
    assert all_positions == expected
    
    print("[OK] Separate connected groups detection test passed")


def test_find_erasable_groups():
    """消去可能グループ（4つ以上）の検出をテスト"""
    playfield = PlayField()
    
    # 4つの赤いぷよ（消去可能）
    playfield.place_puyo(1, 10, Puyo(1))  # 赤
    playfield.place_puyo(1, 11, Puyo(1))  # 赤
    playfield.place_puyo(2, 10, Puyo(1))  # 赤
    playfield.place_puyo(2, 11, Puyo(1))  # 赤
    
    # 3つの青いぷよ（消去不可能）
    playfield.place_puyo(4, 9, Puyo(4))   # 青
    playfield.place_puyo(4, 10, Puyo(4))  # 青
    playfield.place_puyo(4, 11, Puyo(4))  # 青
    
    # 5つの緑のぷよ（消去可能）
    playfield.place_puyo(0, 8, Puyo(3))   # 緑
    playfield.place_puyo(0, 9, Puyo(3))   # 緑
    playfield.place_puyo(0, 10, Puyo(3))  # 緑
    playfield.place_puyo(0, 11, Puyo(3))  # 緑
    playfield.place_puyo(1, 8, Puyo(3))   # 緑
    
    # 消去可能グループを検出
    erasable_groups = playfield.find_erasable_groups()
    
    # 2つの消去可能グループが検出されるはず（赤4つ、緑5つ）
    assert len(erasable_groups) == 2
    
    # グループのサイズを確認
    group_sizes = [len(group) for group in erasable_groups]
    group_sizes.sort()
    assert group_sizes == [4, 5]
    
    print("[OK] Erasable groups detection test passed")


def test_get_adjacent_positions():
    """隣接位置の取得をテスト"""
    playfield = PlayField()
    
    # 中央の位置
    adjacent = playfield.get_adjacent_positions(2, 5)
    expected = [(2, 4), (2, 6), (1, 5), (3, 5)]  # 上、下、左、右
    assert set(adjacent) == set(expected)
    
    # 左上角
    adjacent = playfield.get_adjacent_positions(0, 0)
    expected = [(0, 1), (1, 0)]  # 下、右のみ
    assert set(adjacent) == set(expected)
    
    # 右下角
    adjacent = playfield.get_adjacent_positions(5, 11)
    expected = [(5, 10), (4, 11)]  # 上、左のみ
    assert set(adjacent) == set(expected)
    
    # 左端
    adjacent = playfield.get_adjacent_positions(0, 5)
    expected = [(0, 4), (0, 6), (1, 5)]  # 上、下、右
    assert set(adjacent) == set(expected)
    
    print("[OK] Adjacent positions test passed")


def test_count_connected_puyos():
    """連結ぷよ数のカウントをテスト"""
    playfield = PlayField()
    
    # T字型の赤いぷよを配置
    playfield.place_puyo(2, 10, Puyo(1))  # 赤（中心）
    playfield.place_puyo(1, 10, Puyo(1))  # 赤（左）
    playfield.place_puyo(3, 10, Puyo(1))  # 赤（右）
    playfield.place_puyo(2, 9, Puyo(1))   # 赤（上）
    
    # 各位置から連結ぷよ数をカウント
    count_center = playfield.count_connected_puyos(2, 10)
    count_left = playfield.count_connected_puyos(1, 10)
    count_right = playfield.count_connected_puyos(3, 10)
    count_top = playfield.count_connected_puyos(2, 9)
    
    # 全て同じ連結グループなので4つ
    assert count_center == 4
    assert count_left == 4
    assert count_right == 4
    assert count_top == 4
    
    # 空の位置
    count_empty = playfield.count_connected_puyos(0, 0)
    assert count_empty == 0
    
    print("[OK] Count connected puyos test passed")


def test_complex_connected_groups():
    """複雑な連結グループのテスト"""
    playfield = PlayField()
    
    # 複雑な形状の連結グループを作成
    # 赤いぷよで複雑な形を作る
    red_positions = [
        (1, 11), (2, 11), (3, 11),  # 底辺
        (2, 10),                     # 中央上
        (2, 9), (3, 9),             # 上部
        (4, 9), (4, 10)             # 右側
    ]
    
    for x, y in red_positions:
        playfield.place_puyo(x, y, Puyo(1))  # 赤
    
    # 青いぷよで別のグループを作る
    blue_positions = [
        (0, 10), (0, 11),           # 左側
        (5, 10), (5, 11)            # 右側（分離）
    ]
    
    for x, y in blue_positions:
        playfield.place_puyo(x, y, Puyo(4))  # 青
    
    # 連結グループを検出
    groups = playfield.find_connected_groups()
    
    # 3つのグループが検出されるはず（赤8つ、青2つ、青2つ）
    assert len(groups) == 3
    
    # グループのサイズを確認
    group_sizes = [len(group) for group in groups]
    group_sizes.sort()
    assert group_sizes == [2, 2, 8]
    
    # 赤いぷよのグループを確認
    red_group = None
    for group in groups:
        if len(group) == 8:
            red_group = group
            break
    
    assert red_group is not None
    red_positions_set = set(red_group)
    expected_red = set(red_positions)
    assert red_positions_set == expected_red
    
    print("[OK] Complex connected groups test passed")


def test_no_connected_groups():
    """連結グループが存在しない場合をテスト"""
    playfield = PlayField()
    
    # 単独のぷよを配置（連結しない）
    playfield.place_puyo(0, 11, Puyo(1))  # 赤
    playfield.place_puyo(2, 11, Puyo(2))  # オレンジ
    playfield.place_puyo(4, 11, Puyo(3))  # 緑
    
    # 連結グループを検出
    groups = playfield.find_connected_groups()
    
    # 3つの単独グループが検出されるはず
    assert len(groups) == 3
    
    # 全て1つのぷよからなるグループ
    group_sizes = [len(group) for group in groups]
    group_sizes.sort()
    assert group_sizes == [1, 1, 1]
    
    # 消去可能グループは存在しない
    erasable_groups = playfield.find_erasable_groups()
    assert len(erasable_groups) == 0
    
    print("[OK] No connected groups test passed")


if __name__ == "__main__":
    print("Running connection detection system tests...")
    
    test_find_connected_groups_basic()
    test_find_connected_groups_line()
    test_find_connected_groups_l_shape()
    test_find_connected_groups_separate()
    test_find_erasable_groups()
    test_get_adjacent_positions()
    test_count_connected_puyos()
    test_complex_connected_groups()
    test_no_connected_groups()
    
    print("All connection detection system tests passed! [OK]")