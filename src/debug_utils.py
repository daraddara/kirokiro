"""
デバッグユーティリティ - ゲーム状態の解析と出力
"""

def print_playfield_state(playfield, current_pair=None):
    """
    プレイフィールドの状態をコンソールに出力
    
    Args:
        playfield: PlayFieldオブジェクト
        current_pair: 現在のぷよペア（オプション）
    """
    width = playfield.get_width()
    height = playfield.get_height()
    
    # 現在のぷよペアの位置を取得
    pair_positions = []
    if current_pair is not None:
        main_pos, sub_pos = current_pair.get_puyo_positions()
        pair_positions = [main_pos, sub_pos]
    
    print("\n=== プレイフィールドの状態 ===")
    print("  " + " ".join([str(x) for x in range(width)]))
    
    for y in range(height):
        row = [str(y) + "|"]
        for x in range(width):
            cell = " "
            # プレイフィールド上のぷよ
            puyo = playfield.get_puyo(x, y)
            if puyo is not None:
                color = puyo.get_color()
                cell = str(color)
            
            # 現在のぷよペアの位置
            if (x, y) in pair_positions:
                if (x, y) == pair_positions[0]:
                    cell = "M"  # メインぷよ
                else:
                    cell = "S"  # サブぷよ
            
            row.append(cell)
        print(" ".join(row))
    
    print("===========================")

def analyze_game_over_state(game):
    """
    ゲームオーバー状態を詳細に解析
    
    Args:
        game: PuyoPuyoGameオブジェクト
    """
    print("\n=== ゲームオーバー状態の解析 ===")
    
    # 基本的なゲームオーバー判定
    is_game_over = game.check_game_over()
    print(f"基本的なゲームオーバー判定: {is_game_over}")
    
    # 上端（y=0）の状態を確認
    print("上端（y=0）の状態:")
    for x in range(game.playfield.get_width()):
        is_empty = game.playfield.is_empty(x, 0)
        print(f"  列 {x}: {'空' if is_empty else 'ぷよあり'}")
    
    # 現在のぷよペアの状態
    if game.current_falling_pair is not None:
        main_pos, sub_pos = game.current_falling_pair.get_puyo_positions()
        print(f"現在のぷよペア:")
        print(f"  メインぷよ位置: {main_pos}")
        print(f"  サブぷよ位置: {sub_pos}")
        print(f"  回転状態: {game.current_falling_pair.get_rotation()}")
        
        # メインぷよとサブぷよの位置にぷよがあるかチェック
        main_empty = game.playfield.is_empty(main_pos[0], main_pos[1])
        sub_empty = game.playfield.is_empty(sub_pos[0], sub_pos[1])
        print(f"  メインぷよ位置は空か: {main_empty}")
        print(f"  サブぷよ位置は空か: {sub_empty}")
    else:
        print("現在のぷよペア: なし")
    
    # 危険レベル
    danger_level = game.get_danger_level()
    print(f"危険レベル: {danger_level}")
    
    print("===============================")