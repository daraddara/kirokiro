"""
Test file for Puyo, PuyoPair, PlayField, InputHandler, and PuyoManager classes
Requirements: 2.1, 2.2, 3.1, 4.1, 5.1 - 各クラスの基本機能をテストする
"""

from main import Puyo, PuyoPair, PlayField, InputHandler, PuyoManager


def test_puyo_creation():
    """Puyoオブジェクトの作成をテスト"""
    puyo = Puyo(1, 2, 3)
    assert puyo.color == 1
    assert puyo.x == 2
    assert puyo.y == 3
    print("[OK] Puyo creation test passed")


def test_puyo_color():
    """Puyoの色取得をテスト"""
    puyo = Puyo(3)
    assert puyo.get_color() == 3
    print("[OK] Puyo color test passed")


def test_puyo_position():
    """Puyoの位置設定・取得をテスト"""
    puyo = Puyo(1)
    puyo.set_position(5, 7)
    position = puyo.get_position()
    assert position == (5, 7)
    print("[OK] Puyo position test passed")


def test_puyo_default_position():
    """Puyoのデフォルト位置をテスト"""
    puyo = Puyo(2)
    position = puyo.get_position()
    assert position == (0, 0)
    print("[OK] Puyo default position test passed")


def test_puyo_pair_creation():
    """PuyoPairオブジェクトの作成をテスト"""
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 3, 4)
    
    assert pair.get_position() == (3, 4)
    assert pair.get_rotation() == 0
    assert pair.get_main_puyo() == main_puyo
    assert pair.get_sub_puyo() == sub_puyo
    print("[OK] PuyoPair creation test passed")


def test_puyo_pair_rotation():
    """PuyoPairの回転機能をテスト"""
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 2)
    
    # 初期状態: サブぷよは上
    positions = pair.get_puyo_positions()
    assert positions[0] == (2, 2)  # メインぷよ
    assert positions[1] == (2, 1)  # サブぷよ（上）
    
    # 時計回りに回転: サブぷよは右
    pair.rotate_clockwise()
    assert pair.get_rotation() == 1
    positions = pair.get_puyo_positions()
    assert positions[1] == (3, 2)  # サブぷよ（右）
    
    # さらに時計回りに回転: サブぷよは下
    pair.rotate_clockwise()
    assert pair.get_rotation() == 2
    positions = pair.get_puyo_positions()
    assert positions[1] == (2, 3)  # サブぷよ（下）
    
    # 反時計回りに回転: サブぷよは右に戻る
    pair.rotate_counterclockwise()
    assert pair.get_rotation() == 1
    positions = pair.get_puyo_positions()
    assert positions[1] == (3, 2)  # サブぷよ（右）
    
    print("[OK] PuyoPair rotation test passed")


def test_puyo_pair_movement():
    """PuyoPairの移動機能をテスト"""
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 2)
    
    # 右に移動
    pair.move(1, 0)
    assert pair.get_position() == (3, 2)
    positions = pair.get_puyo_positions()
    assert positions[0] == (3, 2)  # メインぷよ
    assert positions[1] == (3, 1)  # サブぷよ（上）
    
    # 下に移動
    pair.move(0, 2)
    assert pair.get_position() == (3, 4)
    positions = pair.get_puyo_positions()
    assert positions[0] == (3, 4)  # メインぷよ
    assert positions[1] == (3, 3)  # サブぷよ（上）
    
    print("[OK] PuyoPair movement test passed")


def test_puyo_pair_position_setting():
    """PuyoPairの位置設定をテスト"""
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo)
    
    # 位置を直接設定
    pair.set_position(5, 6)
    assert pair.get_position() == (5, 6)
    positions = pair.get_puyo_positions()
    assert positions[0] == (5, 6)  # メインぷよ
    assert positions[1] == (5, 5)  # サブぷよ（上）
    
    print("[OK] PuyoPair position setting test passed")


def test_playfield_creation():
    """PlayFieldオブジェクトの作成をテスト"""
    playfield = PlayField()
    assert playfield.get_width() == 6
    assert playfield.get_height() == 12
    print("[OK] PlayField creation test passed")


def test_playfield_position_validation():
    """PlayFieldの座標検証をテスト"""
    playfield = PlayField()
    
    # 有効な座標
    assert playfield.is_valid_position(0, 0) == True
    assert playfield.is_valid_position(5, 11) == True
    assert playfield.is_valid_position(2, 5) == True
    
    # 無効な座標
    assert playfield.is_valid_position(-1, 0) == False
    assert playfield.is_valid_position(6, 0) == False
    assert playfield.is_valid_position(0, -1) == False
    assert playfield.is_valid_position(0, 12) == False
    
    print("[OK] PlayField position validation test passed")


def test_playfield_empty_check():
    """PlayFieldの空きチェックをテスト"""
    playfield = PlayField()
    
    # 初期状態では全て空
    assert playfield.is_empty(0, 0) == True
    assert playfield.is_empty(5, 11) == True
    
    # 範囲外は空ではない
    assert playfield.is_empty(-1, 0) == False
    assert playfield.is_empty(6, 0) == False
    
    print("[OK] PlayField empty check test passed")


def test_playfield_puyo_placement():
    """PlayFieldのぷよ配置をテスト"""
    playfield = PlayField()
    puyo = Puyo(1)
    
    # ぷよの配置
    result = playfield.place_puyo(2, 5, puyo)
    assert result == True
    assert playfield.is_empty(2, 5) == False
    assert playfield.get_puyo(2, 5) == puyo
    
    # 同じ位置への重複配置は失敗
    puyo2 = Puyo(2)
    result = playfield.place_puyo(2, 5, puyo2)
    assert result == False
    assert playfield.get_puyo(2, 5) == puyo  # 元のぷよが残る
    
    # 範囲外への配置は失敗
    result = playfield.place_puyo(-1, 0, puyo2)
    assert result == False
    
    print("[OK] PlayField puyo placement test passed")


def test_playfield_puyo_removal():
    """PlayFieldのぷよ削除をテスト"""
    playfield = PlayField()
    puyo = Puyo(3)
    
    # ぷよを配置してから削除
    playfield.place_puyo(1, 3, puyo)
    removed_puyo = playfield.remove_puyo(1, 3)
    
    assert removed_puyo == puyo
    assert playfield.is_empty(1, 3) == True
    assert playfield.get_puyo(1, 3) == None
    
    # 空の位置からの削除
    removed_puyo = playfield.remove_puyo(1, 3)
    assert removed_puyo == None
    
    print("[OK] PlayField puyo removal test passed")


def test_playfield_clear():
    """PlayFieldのクリア機能をテスト"""
    playfield = PlayField()
    
    # いくつかのぷよを配置
    playfield.place_puyo(0, 0, Puyo(1))
    playfield.place_puyo(2, 5, Puyo(2))
    playfield.place_puyo(5, 11, Puyo(3))
    
    # クリア前の確認
    assert playfield.is_empty(0, 0) == False
    assert playfield.is_empty(2, 5) == False
    assert playfield.is_empty(5, 11) == False
    
    # クリア実行
    playfield.clear()
    
    # クリア後の確認
    assert playfield.is_empty(0, 0) == True
    assert playfield.is_empty(2, 5) == True
    assert playfield.is_empty(5, 11) == True
    
    print("[OK] PlayField clear test passed")


def test_playfield_get_all_puyos():
    """PlayFieldの全ぷよ取得をテスト"""
    playfield = PlayField()
    
    # 初期状態では空
    puyos = playfield.get_all_puyos()
    assert len(puyos) == 0
    
    # ぷよを配置
    puyo1 = Puyo(1)
    puyo2 = Puyo(2)
    puyo3 = Puyo(3)
    
    playfield.place_puyo(1, 2, puyo1)
    playfield.place_puyo(3, 4, puyo2)
    playfield.place_puyo(5, 6, puyo3)
    
    # 全ぷよを取得
    puyos = playfield.get_all_puyos()
    assert len(puyos) == 3
    
    # 位置とぷよの確認
    positions = [(x, y) for x, y, puyo in puyos]
    assert (1, 2) in positions
    assert (3, 4) in positions
    assert (5, 6) in positions
    
    print("[OK] PlayField get all puyos test passed")


def test_playfield_collision_detection():
    """PlayFieldの衝突判定をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 2)
    
    # 空のプレイフィールドでは配置可能
    assert playfield.can_place_puyo_pair(pair) == True
    
    # 障害物を配置
    playfield.place_puyo(2, 2, Puyo(3))  # メインぷよの位置に障害物
    
    # 障害物があると配置不可能
    assert playfield.can_place_puyo_pair(pair) == False
    
    # 障害物を削除
    playfield.remove_puyo(2, 2)
    
    # 再び配置可能
    assert playfield.can_place_puyo_pair(pair) == True
    
    print("[OK] PlayField collision detection test passed")


def test_playfield_movement_collision():
    """PlayFieldの移動時衝突判定をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 2)
    
    # 右に移動可能かチェック
    assert playfield.can_move_puyo_pair(pair, 1, 0) == True
    
    # 右端近くに障害物を配置
    playfield.place_puyo(3, 2, Puyo(3))
    
    # 右に移動不可能
    assert playfield.can_move_puyo_pair(pair, 1, 0) == False
    
    # 下に移動は可能
    assert playfield.can_move_puyo_pair(pair, 0, 1) == True
    
    # 境界外への移動は不可能
    pair.set_position(5, 2)  # 右端に移動
    assert playfield.can_move_puyo_pair(pair, 1, 0) == False  # 右端を超える移動
    
    print("[OK] PlayField movement collision test passed")


def test_playfield_rotation_collision():
    """PlayFieldの回転時衝突判定をテスト"""
    playfield = PlayField()
    
    # テスト用のぷよペアを作成
    main_puyo = Puyo(1)
    sub_puyo = Puyo(2)
    pair = PuyoPair(main_puyo, sub_puyo, 2, 2)
    
    # 初期状態では回転可能
    assert playfield.can_rotate_puyo_pair(pair, True) == True
    assert playfield.can_rotate_puyo_pair(pair, False) == True
    
    # 回転先に障害物を配置
    playfield.place_puyo(3, 2, Puyo(3))  # 右の位置に障害物
    
    # 時計回りの回転は可能（キックシステムにより左キックで成功）
    assert playfield.can_rotate_puyo_pair(pair, True) == True
    
    # 反時計回りの回転は可能（サブぷよが左に移動するため）
    assert playfield.can_rotate_puyo_pair(pair, False) == True
    
    # 境界での回転テスト - キックシステムにより多くの場合で回転可能
    # より厳しい条件でテスト：全方向を塞ぐ
    pair.set_position(2, 2)  # 中央に戻す
    playfield.place_puyo(1, 2, Puyo(4))  # 左に障害物
    playfield.place_puyo(2, 1, Puyo(4))  # 上に障害物
    playfield.place_puyo(2, 3, Puyo(4))  # 下に障害物
    # 全方向が塞がれた場合のみ回転不可能
    assert playfield.can_rotate_puyo_pair(pair, True) == False
    
    print("[OK] PlayField rotation collision test passed")


def test_puyo_manager_creation():
    """PuyoManagerオブジェクトの作成をテスト"""
    manager = PuyoManager()
    
    # 初期状態で現在と次のペアが存在する
    assert manager.get_current_pair() is not None
    assert manager.get_next_pair() is not None
    
    # 現在と次のペアは異なるオブジェクト
    assert manager.get_current_pair() != manager.get_next_pair()
    
    print("[OK] PuyoManager creation test passed")


def test_puyo_manager_color_generation():
    """PuyoManagerの色生成をテスト"""
    manager = PuyoManager()
    
    # 複数回色を生成して有効な範囲内かチェック
    for _ in range(20):
        color = manager.generate_random_color()
        assert 1 <= color <= 4
    
    print("[OK] PuyoManager color generation test passed")


def test_puyo_manager_pair_creation():
    """PuyoManagerのペア作成をテスト"""
    manager = PuyoManager()
    
    # ランダムペアの作成
    pair = manager.create_random_puyo_pair(3, 5)
    
    # ペアの位置確認
    assert pair.get_position() == (3, 5)
    
    # ペア内のぷよの色が有効範囲内
    main_color = pair.get_main_puyo().get_color()
    sub_color = pair.get_sub_puyo().get_color()
    assert 1 <= main_color <= 4
    assert 1 <= sub_color <= 4
    
    print("[OK] PuyoManager pair creation test passed")


def test_puyo_manager_advance_pair():
    """PuyoManagerのペア進行をテスト"""
    manager = PuyoManager()
    
    # 初期状態を記録
    original_current = manager.get_current_pair()
    original_next = manager.get_next_pair()
    
    # ペアを進行
    new_current = manager.advance_to_next_pair()
    
    # 次のペアが現在のペアになる
    assert new_current == original_next
    assert manager.get_current_pair() == original_next
    
    # 新しい次のペアが生成される
    assert manager.get_next_pair() != original_next
    assert manager.get_next_pair() is not None
    
    # 現在のペアの位置がリセットされる
    assert manager.get_current_pair().get_position() == (2, 0)
    
    print("[OK] PuyoManager advance pair test passed")


def test_puyo_manager_reset():
    """PuyoManagerのリセット機能をテスト"""
    manager = PuyoManager()
    
    # ペアを進行させて状態を変更
    manager.advance_to_next_pair()
    manager.advance_to_next_pair()
    
    # 初期状態のペアを記録
    before_reset_current = manager.get_current_pair()
    before_reset_next = manager.get_next_pair()
    
    # リセット実行
    manager.reset()
    
    # 新しいペアが生成される
    assert manager.get_current_pair() != before_reset_current
    assert manager.get_next_pair() != before_reset_next
    assert manager.get_current_pair() is not None
    assert manager.get_next_pair() is not None
    
    print("[OK] PuyoManager reset test passed")


if __name__ == "__main__":
    print("Running Puyo, PuyoPair, PlayField, and PuyoManager class tests...")
    
    # Puyo tests
    test_puyo_creation()
    test_puyo_color()
    test_puyo_position()
    test_puyo_default_position()
    
    # PuyoPair tests
    test_puyo_pair_creation()
    test_puyo_pair_rotation()
    test_puyo_pair_movement()
    test_puyo_pair_position_setting()
    
    # PlayField tests
    test_playfield_creation()
    test_playfield_position_validation()
    test_playfield_empty_check()
    test_playfield_puyo_placement()
    test_playfield_puyo_removal()
    test_playfield_clear()
    test_playfield_get_all_puyos()
    test_playfield_collision_detection()
    test_playfield_movement_collision()
    test_playfield_rotation_collision()
    
    # PuyoManager tests
    test_puyo_manager_creation()
    test_puyo_manager_color_generation()
    test_puyo_manager_pair_creation()
    test_puyo_manager_advance_pair()
    test_puyo_manager_reset()
    
    print("All tests passed! [OK]")