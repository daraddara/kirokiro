import pyxel


class Puyo:
    """
    個別のぷよを表現するクラス
    Requirements: 5.1 - システムは異なる色で区別可能なぷよを描画する
    """
    
    def __init__(self, color, x=0, y=0):
        """
        ぷよの初期化
        
        Args:
            color (int): ぷよの色（1-4）
            x (int): X座標（相対位置）
            y (int): Y座標（相対位置）
        """
        self.color = color  # ぷよの色（1-4）
        self.x = x  # 相対位置X
        self.y = y  # 相対位置Y
    
    def draw(self, screen_x, screen_y):
        """
        ぷよを画面に描画する
        
        Args:
            screen_x (int): 画面上のX座標
            screen_y (int): 画面上のY座標
        """
        # デザイン文書の色定義に基づく色マッピング
        color_map = {
            1: 8,   # 赤
            2: 9,   # オレンジ
            3: 11,  # 緑
            4: 12   # 青
        }
        
        # ぷよのサイズは24x24ピクセル（デザイン文書に基づく）
        puyo_size = 24
        
        # 有効な色の場合のみ描画
        if self.color in color_map:
            draw_color = color_map[self.color]
            
            # ぷよ本体を描画（塗りつぶし円）
            pyxel.circ(screen_x + puyo_size // 2, screen_y + puyo_size // 2, 
                      puyo_size // 2 - 2, draw_color)
            
            # ぷよの輪郭を描画（白色の円）
            pyxel.circb(screen_x + puyo_size // 2, screen_y + puyo_size // 2, 
                       puyo_size // 2 - 2, 7)
            
            # ぷよの光沢効果（小さな白い円）
            pyxel.circ(screen_x + puyo_size // 2 - 4, screen_y + puyo_size // 2 - 4, 
                      2, 7)
    
    def get_color(self):
        """
        ぷよの色を取得
        
        Returns:
            int: ぷよの色（1-4）
        """
        return self.color
    
    def set_position(self, x, y):
        """
        ぷよの位置を設定
        
        Args:
            x (int): X座標
            y (int): Y座標
        """
        self.x = x
        self.y = y
    
    def get_position(self):
        """
        ぷよの位置を取得
        
        Returns:
            tuple: (x, y) 座標のタプル
        """
        return (self.x, self.y)


class PuyoPair:
    """
    2つのぷよからなるペアクラス
    Requirements: 2.2, 2.3 - ぷよペアの回転と移動機能
    """
    
    def __init__(self, main_puyo, sub_puyo, x=2, y=0):
        """
        ぷよペアの初期化
        
        Args:
            main_puyo (Puyo): メインぷよ（軸となるぷよ）
            sub_puyo (Puyo): サブぷよ（回転するぷよ）
            x (int): ペアの基準X座標（デフォルト: 2 - プレイフィールド中央）
            y (int): ペアの基準Y座標（デフォルト: 0 - 最上段）
        """
        self.main_puyo = main_puyo
        self.sub_puyo = sub_puyo
        self.x = x  # ペアの基準位置X
        self.y = y  # ペアの基準位置Y
        self.rotation = 0  # 回転状態（0-3: 上、右、下、左）
        
        # 初期位置を設定
        self._update_puyo_positions()
    
    def _update_puyo_positions(self):
        """
        回転状態に基づいてぷよの相対位置を更新
        """
        # メインぷよは常に基準位置
        self.main_puyo.set_position(self.x, self.y)
        
        # サブぷよの位置は回転状態によって決まる
        # 0: 上, 1: 右, 2: 下, 3: 左
        offset_map = {
            0: (0, -1),  # 上
            1: (1, 0),   # 右
            2: (0, 1),   # 下
            3: (-1, 0)   # 左
        }
        
        offset_x, offset_y = offset_map[self.rotation]
        self.sub_puyo.set_position(self.x + offset_x, self.y + offset_y)
    
    def rotate_clockwise(self):
        """
        時計回りに90度回転
        Requirements: 2.3 - ぷよペアの回転機能
        """
        self.rotation = (self.rotation + 1) % 4
        self._update_puyo_positions()
    
    def rotate_counterclockwise(self):
        """
        反時計回りに90度回転
        Requirements: 2.3 - ぷよペアの回転機能
        """
        self.rotation = (self.rotation - 1) % 4
        self._update_puyo_positions()
    
    def move(self, dx, dy):
        """
        ペアを移動
        
        Args:
            dx (int): X方向の移動量
            dy (int): Y方向の移動量
        
        Requirements: 2.2 - ぷよペアの移動機能
        """
        self.x += dx
        self.y += dy
        self._update_puyo_positions()
    
    def set_position(self, x, y):
        """
        ペアの位置を設定
        
        Args:
            x (int): 新しいX座標
            y (int): 新しいY座標
        """
        self.x = x
        self.y = y
        self._update_puyo_positions()
    
    def get_position(self):
        """
        ペアの基準位置を取得
        
        Returns:
            tuple: (x, y) 座標のタプル
        """
        return (self.x, self.y)
    
    def get_puyo_positions(self):
        """
        両方のぷよの位置を取得
        
        Returns:
            tuple: ((main_x, main_y), (sub_x, sub_y))
        """
        return (self.main_puyo.get_position(), self.sub_puyo.get_position())
    
    def draw(self, screen_offset_x, screen_offset_y):
        """
        ペアを画面に描画
        
        Args:
            screen_offset_x (int): 画面オフセットX
            screen_offset_y (int): 画面オフセットY
        """
        # メインぷよの描画
        main_x, main_y = self.main_puyo.get_position()
        self.main_puyo.draw(
            screen_offset_x + main_x * 24,
            screen_offset_y + main_y * 24
        )
        
        # サブぷよの描画
        sub_x, sub_y = self.sub_puyo.get_position()
        self.sub_puyo.draw(
            screen_offset_x + sub_x * 24,
            screen_offset_y + sub_y * 24
        )
    
    def get_main_puyo(self):
        """メインぷよを取得"""
        return self.main_puyo
    
    def get_sub_puyo(self):
        """サブぷよを取得"""
        return self.sub_puyo
    
    def get_rotation(self):
        """現在の回転状態を取得"""
        return self.rotation


class PlayField:
    """
    プレイフィールドクラス - 6x12グリッドでぷよの配置を管理
    Requirements: 2.5 - プレイフィールドでのぷよ配置と管理
    """
    
    def __init__(self):
        """
        プレイフィールドの初期化
        6列x12行のグリッドを作成
        """
        self.width = 6   # プレイフィールドの幅
        self.height = 12  # プレイフィールドの高さ
        
        # 2次元配列でプレイフィールドを初期化（None = 空のセル）
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def is_valid_position(self, x, y):
        """
        指定された座標が有効かどうかをチェック
        
        Args:
            x (int): X座標（0-5）
            y (int): Y座標（0-11）
        
        Returns:
            bool: 有効な座標の場合True
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_empty(self, x, y):
        """
        指定された位置が空かどうかをチェック
        
        Args:
            x (int): X座標
            y (int): Y座標
        
        Returns:
            bool: 空の場合True、範囲外または占有されている場合False
        """
        if not self.is_valid_position(x, y):
            return False
        return self.grid[y][x] is None
    
    def place_puyo(self, x, y, puyo):
        """
        指定された位置にぷよを配置
        
        Args:
            x (int): X座標
            y (int): Y座標
            puyo (Puyo): 配置するぷよ
        
        Returns:
            bool: 配置に成功した場合True
        """
        if not self.is_valid_position(x, y):
            return False
        
        if not self.is_empty(x, y):
            return False
        
        # ぷよを配置し、位置を更新
        self.grid[y][x] = puyo
        puyo.set_position(x, y)
        return True
    
    def get_puyo(self, x, y):
        """
        指定された位置のぷよを取得
        
        Args:
            x (int): X座標
            y (int): Y座標
        
        Returns:
            Puyo or None: 指定位置のぷよ、または空の場合None
        """
        if not self.is_valid_position(x, y):
            return None
        return self.grid[y][x]
    
    def remove_puyo(self, x, y):
        """
        指定された位置のぷよを削除
        
        Args:
            x (int): X座標
            y (int): Y座標
        
        Returns:
            Puyo or None: 削除されたぷよ、または空だった場合None
        """
        if not self.is_valid_position(x, y):
            return None
        
        puyo = self.grid[y][x]
        self.grid[y][x] = None
        return puyo
    
    def clear(self):
        """
        プレイフィールドをクリア（全てのぷよを削除）
        """
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = None
    
    def draw(self, screen_offset_x, screen_offset_y):
        """
        プレイフィールドとその中のぷよを描画
        
        Args:
            screen_offset_x (int): 画面オフセットX
            screen_offset_y (int): 画面オフセットY
        """
        # プレイフィールドの枠を描画
        field_width = self.width * 24
        field_height = self.height * 24
        
        # 外枠
        pyxel.rectb(screen_offset_x - 2, screen_offset_y - 2, 
                   field_width + 4, field_height + 4, 7)
        
        # 内部背景
        pyxel.rect(screen_offset_x, screen_offset_y, 
                  field_width, field_height, 1)
        
        # グリッド内のぷよを描画
        for y in range(self.height):
            for x in range(self.width):
                puyo = self.grid[y][x]
                if puyo is not None:
                    screen_x = screen_offset_x + x * 24
                    screen_y = screen_offset_y + y * 24
                    puyo.draw(screen_x, screen_y)
    
    def get_width(self):
        """プレイフィールドの幅を取得"""
        return self.width
    
    def get_height(self):
        """プレイフィールドの高さを取得"""
        return self.height
    
    def get_all_puyos(self):
        """
        プレイフィールド内の全てのぷよを取得
        
        Returns:
            list: [(x, y, puyo), ...] の形式でぷよのリスト
        """
        puyos = []
        for y in range(self.height):
            for x in range(self.width):
                puyo = self.grid[y][x]
                if puyo is not None:
                    puyos.append((x, y, puyo))
        return puyos
    
    def can_place_puyo_pair(self, puyo_pair):
        """
        ぷよペアを現在の位置に配置できるかチェック
        
        Args:
            puyo_pair (PuyoPair): チェックするぷよペア
        
        Returns:
            bool: 配置可能な場合True
        
        Requirements: 2.2, 2.3, 2.5 - 衝突判定システム
        """
        main_pos, sub_pos = puyo_pair.get_puyo_positions()
        
        # 両方のぷよの位置が有効で空かどうかチェック
        return (self.is_empty(main_pos[0], main_pos[1]) and 
                self.is_empty(sub_pos[0], sub_pos[1]))
    
    def can_move_puyo_pair(self, puyo_pair, dx, dy):
        """
        ぷよペアを指定方向に移動できるかチェック
        
        Args:
            puyo_pair (PuyoPair): チェックするぷよペア
            dx (int): X方向の移動量
            dy (int): Y方向の移動量
        
        Returns:
            bool: 移動可能な場合True
        
        Requirements: 2.2, 2.5 - 移動時の衝突判定
        """
        # 一時的に移動した位置をチェック
        original_x, original_y = puyo_pair.get_position()
        puyo_pair.set_position(original_x + dx, original_y + dy)
        
        can_move = self.can_place_puyo_pair(puyo_pair)
        
        # 元の位置に戻す
        puyo_pair.set_position(original_x, original_y)
        
        return can_move
    
    def can_rotate_puyo_pair(self, puyo_pair, clockwise=True):
        """
        ぷよペアを回転できるかチェック（キックシステム付き）
        
        Args:
            puyo_pair (PuyoPair): チェックするぷよペア
            clockwise (bool): 時計回りの場合True、反時計回りの場合False
        
        Returns:
            bool: 回転可能な場合True
        
        Requirements: 2.3, 2.5 - 回転時の衝突判定とキックシステム
        """
        return self.try_rotate_with_kick(puyo_pair, clockwise)[0]
    
    def try_rotate_with_kick(self, puyo_pair, clockwise=True):
        """
        キックシステム付きの回転試行
        
        Args:
            puyo_pair (PuyoPair): チェックするぷよペア
            clockwise (bool): 時計回りの場合True、反時計回りの場合False
        
        Returns:
            tuple: (回転可能かどうか, キック方向のタプル(dx, dy))
        
        Requirements: 2.3 - キックシステムによる回転補助
        """
        # 元の状態を保存
        original_rotation = puyo_pair.get_rotation()
        original_x, original_y = puyo_pair.get_position()
        
        # 一時的に回転
        if clockwise:
            puyo_pair.rotate_clockwise()
        else:
            puyo_pair.rotate_counterclockwise()
        
        # キックの試行順序（右、左、上の順）
        kick_offsets = [
            (0, 0),   # キックなし（通常の回転）
            (1, 0),   # 右キック
            (-1, 0),  # 左キック
            (0, -1),  # 上キック
        ]
        
        for dx, dy in kick_offsets:
            # キック位置に移動
            puyo_pair.set_position(original_x + dx, original_y + dy)
            
            # この位置で配置可能かチェック
            if self.can_place_puyo_pair(puyo_pair):
                # 回転成功
                return True, (dx, dy)
        
        # 全てのキックが失敗した場合、元の状態に戻す
        puyo_pair.rotation = original_rotation
        puyo_pair.set_position(original_x, original_y)
        
        return False, (0, 0)
    
    def rotate_puyo_pair_with_kick(self, puyo_pair, clockwise=True):
        """
        キックシステム付きでぷよペアを実際に回転させる
        
        Args:
            puyo_pair (PuyoPair): 回転させるぷよペア
            clockwise (bool): 時計回りの場合True、反時計回りの場合False
        
        Returns:
            bool: 回転に成功した場合True
        
        Requirements: 2.3 - キックシステムによる回転実行
        """
        can_rotate, kick_offset = self.try_rotate_with_kick(puyo_pair, clockwise)
        
        if can_rotate:
            # 既に try_rotate_with_kick 内で回転と移動が完了している
            return True
        else:
            return False
    
    def apply_gravity(self):
        """
        重力を適用して浮いているぷよを落下させる
        
        Returns:
            bool: ぷよが移動した場合True、移動しなかった場合False
        
        Requirements: 3.3 - ぷよ消去後の重力処理
        """
        moved = False
        
        # 下から上に向かって各列をチェック
        for x in range(self.width):
            # 各列で下から上に向かってぷよを詰める
            write_y = self.height - 1  # 書き込み位置（下から）
            
            for read_y in range(self.height - 1, -1, -1):  # 読み取り位置（下から上へ）
                puyo = self.grid[read_y][x]
                
                if puyo is not None:
                    # ぷよが存在する場合
                    if write_y != read_y:
                        # 移動が必要
                        self.grid[write_y][x] = puyo
                        self.grid[read_y][x] = None
                        puyo.set_position(x, write_y)
                        moved = True
                    
                    write_y -= 1  # 次の書き込み位置
        
        return moved
    
    def get_floating_puyos(self):
        """
        浮いているぷよ（下に空きがあるぷよ）を検出する
        
        Returns:
            list: [(x, y, puyo), ...] 浮いているぷよのリスト
        """
        floating_puyos = []
        
        for x in range(self.width):
            for y in range(self.height - 1):  # 最下段は浮くことがない
                puyo = self.grid[y][x]
                if puyo is not None:
                    # このぷよの下に空きがあるかチェック
                    has_support = False
                    for check_y in range(y + 1, self.height):
                        if self.grid[check_y][x] is not None:
                            has_support = True
                            break
                    
                    # 最下段まで空きの場合、または下に空きがある場合は浮いている
                    if not has_support or self.grid[y + 1][x] is None:
                        floating_puyos.append((x, y, puyo))
        
        return floating_puyos
    
    def calculate_fall_distance(self, x, y):
        """
        指定位置のぷよがどれだけ落下するかを計算
        
        Args:
            x (int): X座標
            y (int): Y座標
        
        Returns:
            int: 落下距離（0の場合は落下しない）
        """
        if not self.is_valid_position(x, y) or self.grid[y][x] is None:
            return 0
        
        # 下方向に空きスペースを探す
        fall_distance = 0
        for check_y in range(y + 1, self.height):
            if self.grid[check_y][x] is None:
                fall_distance += 1
            else:
                break
        
        return fall_distance
    
    def find_connected_groups(self):
        """
        同色で連結されたぷよのグループを検出する
        
        Returns:
            list: [[(x, y), ...], ...] 連結グループのリスト
        
        Requirements: 3.1 - 同色ぷよの隣接判定と連結グループの検出
        """
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        connected_groups = []
        
        # 全てのセルをチェック
        for y in range(self.height):
            for x in range(self.width):
                puyo = self.grid[y][x]
                
                # ぷよが存在し、まだ訪問していない場合
                if puyo is not None and not visited[y][x]:
                    # 深度優先探索で連結グループを検出
                    group = self._dfs_connected_group(x, y, puyo.get_color(), visited)
                    
                    # グループが見つかった場合は追加
                    if group:
                        connected_groups.append(group)
        
        return connected_groups
    
    def _dfs_connected_group(self, start_x, start_y, target_color, visited):
        """
        深度優先探索で同色の連結グループを検出
        
        Args:
            start_x (int): 開始X座標
            start_y (int): 開始Y座標
            target_color (int): 対象の色
            visited (list): 訪問済みフラグの2次元配列
        
        Returns:
            list: [(x, y), ...] 連結グループの座標リスト
        """
        # 境界チェック
        if not self.is_valid_position(start_x, start_y):
            return []
        
        # 既に訪問済みの場合
        if visited[start_y][start_x]:
            return []
        
        # ぷよが存在しない場合
        puyo = self.grid[start_y][start_x]
        if puyo is None:
            return []
        
        # 色が異なる場合
        if puyo.get_color() != target_color:
            return []
        
        # 現在の位置を訪問済みにマーク
        visited[start_y][start_x] = True
        
        # 現在の位置を結果に追加
        group = [(start_x, start_y)]
        
        # 4方向（上下左右）を探索
        directions = [
            (0, -1),  # 上
            (0, 1),   # 下
            (-1, 0),  # 左
            (1, 0)    # 右
        ]
        
        for dx, dy in directions:
            next_x = start_x + dx
            next_y = start_y + dy
            
            # 再帰的に隣接する同色ぷよを探索
            adjacent_group = self._dfs_connected_group(next_x, next_y, target_color, visited)
            group.extend(adjacent_group)
        
        return group
    
    def find_erasable_groups(self):
        """
        消去可能な連結グループ（4つ以上）を検出する
        
        Returns:
            list: [[(x, y), ...], ...] 消去可能な連結グループのリスト
        
        Requirements: 3.1 - 4つ以上の連結グループの検出
        """
        all_groups = self.find_connected_groups()
        erasable_groups = []
        
        # 4つ以上のグループのみを抽出
        for group in all_groups:
            if len(group) >= 4:
                erasable_groups.append(group)
        
        return erasable_groups
    
    def get_adjacent_positions(self, x, y):
        """
        指定位置の隣接する位置（上下左右）を取得
        
        Args:
            x (int): X座標
            y (int): Y座標
        
        Returns:
            list: [(x, y), ...] 隣接する有効な位置のリスト
        """
        adjacent_positions = []
        directions = [
            (0, -1),  # 上
            (0, 1),   # 下
            (-1, 0),  # 左
            (1, 0)    # 右
        ]
        
        for dx, dy in directions:
            adj_x = x + dx
            adj_y = y + dy
            
            if self.is_valid_position(adj_x, adj_y):
                adjacent_positions.append((adj_x, adj_y))
        
        return adjacent_positions
    
    def count_connected_puyos(self, x, y):
        """
        指定位置から連結している同色ぷよの数を数える
        
        Args:
            x (int): X座標
            y (int): Y座標
        
        Returns:
            int: 連結している同色ぷよの数（自分を含む）
        """
        puyo = self.get_puyo(x, y)
        if puyo is None:
            return 0
        
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        group = self._dfs_connected_group(x, y, puyo.get_color(), visited)
        
        return len(group)
    
    def erase_puyo_groups(self, groups_to_erase):
        """
        指定された連結グループのぷよを消去する
        
        Args:
            groups_to_erase (list): 消去するグループのリスト [[(x, y), ...], ...]
        
        Returns:
            int: 消去されたぷよの総数
        
        Requirements: 3.1 - 連結グループの消去処理
        """
        total_erased = 0
        
        for group in groups_to_erase:
            for x, y in group:
                if self.is_valid_position(x, y) and self.grid[y][x] is not None:
                    self.grid[y][x] = None
                    total_erased += 1
        
        return total_erased
    
    def process_puyo_elimination(self):
        """
        ぷよの消去処理を実行する（消去可能なグループを検出して消去）
        
        Returns:
            tuple: (消去されたかどうか, 消去されたぷよ数, 消去されたグループ数)
        
        Requirements: 3.1, 5.2 - ぷよ消去処理と重力処理の連携
        """
        # 消去可能なグループを検出
        erasable_groups = self.find_erasable_groups()
        
        if not erasable_groups:
            return False, 0, 0
        
        # グループを消去
        total_erased = self.erase_puyo_groups(erasable_groups)
        
        return True, total_erased, len(erasable_groups)
    
    def get_puyo_colors_in_groups(self, groups):
        """
        指定されたグループ内のぷよの色情報を取得
        
        Args:
            groups (list): グループのリスト [[(x, y), ...], ...]
        
        Returns:
            list: 各グループの色のリスト [color1, color2, ...]
        """
        colors = []
        
        for group in groups:
            if group:
                x, y = group[0]
                puyo = self.get_puyo(x, y)
                if puyo:
                    colors.append(puyo.get_color())
                else:
                    colors.append(None)
            else:
                colors.append(None)
        
        return colors


class InputHandler:
    """
    入力処理クラス - キーボード入力の検出と処理
    Requirements: 1.3, 2.1, 2.2, 2.3, 2.4 - 入力処理システム
    """
    
    def __init__(self):
        """
        InputHandlerの初期化
        """
        # キーリピート用のタイマー
        self.left_repeat_timer = 0
        self.right_repeat_timer = 0
        self.down_repeat_timer = 0
        
        # キーリピートの設定
        self.repeat_delay = 15  # 初回リピートまでのフレーム数
        self.repeat_interval = 3  # リピート間隔のフレーム数
        
        # 高速落下の設定
        self.fast_drop_interval = 2  # 高速落下時のフレーム間隔
    
    def update(self):
        """
        入力状態の更新（毎フレーム呼び出し）
        """
        # 左右移動のリピートタイマー更新
        if pyxel.btn(pyxel.KEY_LEFT):
            self.left_repeat_timer += 1
        else:
            self.left_repeat_timer = 0
            
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.right_repeat_timer += 1
        else:
            self.right_repeat_timer = 0
            
        # 下キー（高速落下）のリピートタイマー更新
        if pyxel.btn(pyxel.KEY_DOWN):
            self.down_repeat_timer += 1
        else:
            self.down_repeat_timer = 0
    
    def should_move_left(self):
        """
        左移動を実行すべきかチェック
        
        Returns:
            bool: 左移動を実行する場合True
        """
        if pyxel.btnp(pyxel.KEY_LEFT):
            return True
        
        # キーリピート処理
        if self.left_repeat_timer > self.repeat_delay:
            if (self.left_repeat_timer - self.repeat_delay) % self.repeat_interval == 0:
                return True
        
        return False
    
    def should_move_right(self):
        """
        右移動を実行すべきかチェック
        
        Returns:
            bool: 右移動を実行する場合True
        """
        if pyxel.btnp(pyxel.KEY_RIGHT):
            return True
        
        # キーリピート処理
        if self.right_repeat_timer > self.repeat_delay:
            if (self.right_repeat_timer - self.repeat_delay) % self.repeat_interval == 0:
                return True
        
        return False
    
    def should_rotate_clockwise(self):
        """
        時計回り回転を実行すべきかチェック
        
        Returns:
            bool: 時計回り回転を実行する場合True
        """
        return pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_UP)
    
    def should_rotate_counterclockwise(self):
        """
        反時計回り回転を実行すべきかチェック
        
        Returns:
            bool: 反時計回り回転を実行する場合True
        """
        return pyxel.btnp(pyxel.KEY_Z)
    
    def should_fast_drop(self):
        """
        高速落下を実行すべきかチェック
        
        Returns:
            bool: 高速落下を実行する場合True
        """
        if pyxel.btnp(pyxel.KEY_DOWN):
            return True
        
        # 高速落下のリピート処理
        if self.down_repeat_timer > self.repeat_delay:
            if (self.down_repeat_timer - self.repeat_delay) % self.fast_drop_interval == 0:
                return True
        
        return False
    
    def should_quit_game(self):
        """
        ゲーム終了を実行すべきかチェック
        
        Returns:
            bool: ゲーム終了する場合True
        """
        return pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.KEY_ESCAPE)
    
    def should_test_gravity(self):
        """
        重力テストを実行すべきかチェック（デバッグ用）
        
        Returns:
            bool: 重力テストを実行する場合True
        """
        return pyxel.btnp(pyxel.KEY_G)
    
    def should_test_connection(self):
        """
        連結判定テストを実行すべきかチェック（デバッグ用）
        
        Returns:
            bool: 連結判定テストを実行する場合True
        """
        return pyxel.btnp(pyxel.KEY_C)
    
    def should_test_elimination(self):
        """
        消去処理テストを実行すべきかチェック（デバッグ用）
        
        Returns:
            bool: 消去処理テストを実行する場合True
        """
        return pyxel.btnp(pyxel.KEY_E)


class PuyoManager:
    """
    ぷよ管理クラス - 新しいぷよペアの生成と管理
    Requirements: 4.2 - 新しいぷよペアの生成システム
    """
    
    def __init__(self):
        """
        PuyoManagerの初期化
        """
        import random
        self.random = random
        
        # 利用可能な色（1-4）
        self.available_colors = [1, 2, 3, 4]
        
        # 現在のぷよペアと次のぷよペア
        self.current_pair = None
        self.next_pair = None
        
        # 初期ペアを生成
        self.generate_initial_pairs()
    
    def generate_random_color(self):
        """
        ランダムな色を生成
        
        Returns:
            int: ランダムな色（1-4）
        """
        return self.random.choice(self.available_colors)
    
    def create_random_puyo_pair(self, x=2, y=0):
        """
        ランダムな色のぷよペアを作成
        
        Args:
            x (int): ペアの初期X座標（デフォルト: 2）
            y (int): ペアの初期Y座標（デフォルト: 0）
        
        Returns:
            PuyoPair: 新しいランダムなぷよペア
        """
        main_color = self.generate_random_color()
        sub_color = self.generate_random_color()
        
        main_puyo = Puyo(main_color)
        sub_puyo = Puyo(sub_color)
        
        return PuyoPair(main_puyo, sub_puyo, x, y)
    
    def generate_initial_pairs(self):
        """
        初期のぷよペア（現在と次）を生成
        """
        self.current_pair = self.create_random_puyo_pair()
        self.next_pair = self.create_random_puyo_pair()
    
    def get_current_pair(self):
        """
        現在のぷよペアを取得
        
        Returns:
            PuyoPair: 現在のぷよペア
        """
        return self.current_pair
    
    def get_next_pair(self):
        """
        次のぷよペアを取得
        
        Returns:
            PuyoPair: 次のぷよペア
        """
        return self.next_pair
    
    def advance_to_next_pair(self):
        """
        次のぷよペアを現在のペアにし、新しい次のペアを生成
        
        Returns:
            PuyoPair: 新しい現在のぷよペア
        """
        # 次のペアを現在のペアにする
        self.current_pair = self.next_pair
        self.current_pair.set_position(2, 0)  # 初期位置にリセット
        
        # 新しい次のペアを生成
        self.next_pair = self.create_random_puyo_pair()
        
        return self.current_pair
    
    def reset(self):
        """
        PuyoManagerをリセット（新しいゲーム開始時）
        """
        self.generate_initial_pairs()
    
    def draw_next_pair_preview(self, screen_x, screen_y):
        """
        次のぷよペアのプレビューを描画
        
        Args:
            screen_x (int): 描画位置X
            screen_y (int): 描画位置Y
        """
        if self.next_pair is not None:
            # 次のペアを小さく表示（プレビュー用）
            main_puyo = self.next_pair.get_main_puyo()
            sub_puyo = self.next_pair.get_sub_puyo()
            
            # メインぷよを描画
            main_puyo.draw(screen_x, screen_y)
            
            # サブぷよを上に描画（次のペアは常に上向きで表示）
            sub_puyo.draw(screen_x, screen_y - 24)


class PuyoPuyoGame:
    """
    メインゲームクラス - Pyxelアプリケーションを管理
    Requirements: 1.1, 1.2
    """
    
    def __init__(self):
        """
        Pyxelアプリケーションの初期化
        """
        # 画面サイズの設定（320x480ピクセル - デザイン文書に基づく）
        pyxel.init(320, 480, title="Puyo Puyo Puzzle Game")
        
        # ゲーム状態の初期化
        self.initialize_game()
        
        # Pyxelアプリケーションの開始
        pyxel.run(self.update, self.draw)
    
    def initialize_game(self):
        """
        ゲームの初期化処理
        基本的なゲーム状態変数を設定
        """
        # ゲーム実行状態
        self.game_running = True
        
        # フレームカウンター（デバッグ用）
        self.frame_count = 0
        
        # 落下システムの設定
        # Requirements: 2.1 - 重力に従ってぷよを移動させる
        self.fall_timer = 0  # 自動落下タイマー
        self.fall_interval = 60  # 通常の落下間隔（60フレーム = 1秒）
        self.fast_fall_interval = 3  # 高速落下間隔（3フレーム）
        
        # 現在操作中のぷよペア
        self.current_falling_pair = None
        
        # テスト用のぷよを作成（Puyoクラスの動作確認用）
        self.test_puyos = [
            Puyo(1, 0, 0),  # 赤いぷよ
            Puyo(2, 1, 0),  # オレンジのぷよ
            Puyo(3, 2, 0),  # 緑のぷよ
            Puyo(4, 3, 0),  # 青いぷよ
        ]
        
        # テスト用のプレイフィールドを作成（PlayFieldクラスの動作確認用）
        self.playfield = PlayField()
        
        # プレイフィールドにテスト用ぷよを配置
        self.playfield.place_puyo(1, 10, Puyo(2))  # オレンジのぷよを下部に配置
        self.playfield.place_puyo(2, 11, Puyo(4))  # 青いぷよを最下段に配置
        self.playfield.place_puyo(3, 10, Puyo(1))  # 赤いぷよを下部に配置
        self.playfield.place_puyo(4, 11, Puyo(3))  # 緑のぷよを最下段に配置
        
        # 入力処理システムを作成（InputHandlerクラスの動作確認用）
        self.input_handler = InputHandler()
        
        # ぷよ管理システムを作成（PuyoManagerクラスの動作確認用）
        self.puyo_manager = PuyoManager()
        
        # 最初の落下ペアを設定
        self.current_falling_pair = self.puyo_manager.get_current_pair()
        
        # 重力処理システムの設定
        # Requirements: 3.3 - 重力処理のアニメーション
        self.gravity_active = False  # 重力処理中フラグ
        self.gravity_timer = 0  # 重力アニメーションタイマー
        self.gravity_interval = 5  # 重力処理の間隔（フレーム数）
        
        # 消去システムの設定
        # Requirements: 3.1, 5.2 - ぷよ消去処理とアニメーション
        self.elimination_active = False  # 消去処理中フラグ
        self.elimination_timer = 0  # 消去アニメーションタイマー
        self.elimination_interval = 30  # 消去アニメーションの間隔（フレーム数）
        self.elimination_groups = []  # 消去予定のグループ
        
        # デバッグ: 初期状態を確認
        print(f"Game initialized - gravity_active: {self.gravity_active}")
    
    def update_fall_system(self):
        """
        落下システムの更新処理
        Requirements: 2.1, 2.4, 2.5 - 自動落下、高速落下、ぷよ固定
        """
        if self.current_falling_pair is None:
            return
        
        # 落下タイマーの更新
        self.fall_timer += 1
        
        # 高速落下中かどうかをチェック
        is_fast_dropping = pyxel.btn(pyxel.KEY_DOWN)
        
        # 落下間隔の決定
        current_fall_interval = self.fast_fall_interval if is_fast_dropping else self.fall_interval
        
        # 落下タイミングかどうかをチェック
        should_fall = self.fall_timer >= current_fall_interval
        
        if should_fall:
            # 下に移動できるかチェック
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, 0, 1):
                # 下に移動
                self.current_falling_pair.move(0, 1)
                self.fall_timer = 0  # タイマーリセット
            else:
                # 移動できない場合はぷよペアを固定
                self.fix_puyo_pair()
    
    def fix_puyo_pair(self):
        """
        現在のぷよペアをプレイフィールドに固定する
        Requirements: 2.5 - ぷよが底面または他のぷよに接触する時の固定処理
        """
        if self.current_falling_pair is None:
            return
        
        # ぷよペアの両方のぷよをプレイフィールドに配置
        main_pos, sub_pos = self.current_falling_pair.get_puyo_positions()
        
        # メインぷよを配置
        main_puyo = self.current_falling_pair.get_main_puyo()
        self.playfield.place_puyo(main_pos[0], main_pos[1], main_puyo)
        
        # サブぷよを配置
        sub_puyo = self.current_falling_pair.get_sub_puyo()
        self.playfield.place_puyo(sub_pos[0], sub_pos[1], sub_puyo)
        
        # Start elimination process after puyo fixation
        # Requirements: 3.1, 5.2 - Elimination process after puyo fixation
        self.start_elimination_process()
        
        # 次のぷよペアに進む
        self.current_falling_pair = self.puyo_manager.advance_to_next_pair()
        
        # 落下タイマーをリセット
        self.fall_timer = 0
    
    def apply_gravity_after_fixation(self):
        """
        ぷよ固定後の重力処理を開始
        Requirements: 3.3 - ぷよ固定後の重力適用
        """
        # 重力処理を開始
        self.gravity_active = True
        self.gravity_timer = 0
    
    def update_gravity_system(self):
        """
        重力システムの更新処理
        Requirements: 3.3 - 浮いているぷよの落下処理、重力処理のアニメーション
        """
        if not self.gravity_active:
            return
        
        # 重力タイマーの更新
        self.gravity_timer += 1
        
        # 重力処理の実行タイミングかチェック
        if self.gravity_timer >= self.gravity_interval:
            # 重力を適用
            gravity_applied = self.playfield.apply_gravity()
            
            if gravity_applied:
                # ぷよが移動した場合、タイマーをリセットして継続
                self.gravity_timer = 0
            else:
                # ぷよが移動しなかった場合、重力処理を終了
                self.gravity_active = False
                self.gravity_timer = 0
    
    def handle_puyo_pair_input(self):
        """
        現在のぷよペアに対する入力処理
        Requirements: 2.2, 2.3, 2.4 - 移動、回転、高速落下の入力処理
        """
        if self.current_falling_pair is None:
            return
        
        # 左右移動の処理
        if self.input_handler.should_move_left():
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, -1, 0):
                self.current_falling_pair.move(-1, 0)
        
        if self.input_handler.should_move_right():
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, 1, 0):
                self.current_falling_pair.move(1, 0)
        
        # 回転の処理（キックシステム付き）
        if self.input_handler.should_rotate_clockwise():
            self.playfield.rotate_puyo_pair_with_kick(self.current_falling_pair, True)
        
        if self.input_handler.should_rotate_counterclockwise():
            self.playfield.rotate_puyo_pair_with_kick(self.current_falling_pair, False)
        
        # 高速落下の処理（個別の下移動）
        if self.input_handler.should_fast_drop():
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, 0, 1):
                self.current_falling_pair.move(0, 1)
                self.fall_timer = 0  # タイマーリセット
        
    def update(self):
        """
        ゲーム状態の更新処理（毎フレーム呼び出される）
        Requirements: 1.1 - システムは対応するゲーム操作を実行する
        """
        # フレームカウンターの更新
        self.frame_count += 1
        
        # 入力処理の更新
        self.input_handler.update()
        
        # 基本的なキー入力処理
        if self.input_handler.should_quit_game():
            pyxel.quit()
        
        # 重力テスト機能（Gキー）
        if self.input_handler.should_test_gravity():
            self.apply_gravity_after_fixation()
        
        # 連結判定テスト機能（Cキー）
        if self.input_handler.should_test_connection():
            self.test_connection_detection()
        
        # 重力システムの更新
        # Requirements: 3.3 - 浮いているぷよの落下処理、重力処理のアニメーション
        self.update_gravity_system()
        
        # 重力処理中でない場合のみ通常の落下システムと入力処理を実行
        if not self.gravity_active:
            # 落下システムの更新
            # Requirements: 2.1, 2.4, 2.5 - 自動落下、高速落下、ぷよ固定
            self.update_fall_system()
            
            # 現在のぷよペアに対する入力処理
            # Requirements: 2.2, 2.3, 2.4 - 移動、回転、高速落下の入力処理
            self.handle_puyo_pair_input()
    
    def test_connection_detection(self):
        """
        連結判定のテスト機能
        Requirements: 3.1 - 連結グループの検出とデバッグ表示
        """
        # 連結グループを検出
        connected_groups = self.playfield.find_connected_groups()
        erasable_groups = self.playfield.find_erasable_groups()
        
        print(f"=== 連結判定テスト結果 ===")
        print(f"全連結グループ数: {len(connected_groups)}")
        print(f"消去可能グループ数: {len(erasable_groups)}")
        
        # 各グループの詳細を表示
        for i, group in enumerate(connected_groups):
            if len(group) >= 4:
                print(f"グループ {i+1}: {len(group)}個 (消去可能)")
            else:
                print(f"グループ {i+1}: {len(group)}個")
            
            # グループ内のぷよの色を確認
            if group:
                x, y = group[0]
                puyo = self.playfield.get_puyo(x, y)
                if puyo:
                    color_names = {1: "赤", 2: "オレンジ", 3: "緑", 4: "青"}
                    color_name = color_names.get(puyo.get_color(), "不明")
                    print(f"  色: {color_name}, 座標: {group}")
        
        print("========================")
    
    def draw(self):
        """
        画面描画処理（毎フレーム呼び出される）
        Requirements: 1.1 - システムはゲーム画面を表示する
        Requirements: 1.2 - システムはプレイフィールドとぷよを表示する
        """
        # 画面をクリア（黒色 - デザイン文書の色定義に基づく）
        pyxel.cls(0)
        
        # ゲームタイトルの表示
        title_text = "Puyo Puyo Puzzle Game"
        title_x = (320 - len(title_text) * 4) // 2  # 中央揃え
        pyxel.text(title_x, 50, title_text, 7)  # 白色で表示
        
        # プレイフィールドの枠を描画（デザイン文書の座標に基づく）
        # プレイフィールド位置: x=88-232, y=60-348
        playfield_x = 88
        playfield_y = 60
        playfield_width = 144  # 6 * 24ピクセル
        playfield_height = 288  # 12 * 24ピクセル
        
        # プレイフィールドの描画（PlayFieldクラスの動作確認）
        self.playfield.draw(playfield_x, playfield_y)
        
        # テスト用ぷよの描画（Puyoクラスの動作確認）
        for i, puyo in enumerate(self.test_puyos):
            # プレイフィールド内の位置に描画
            screen_x = playfield_x + (i * 24)  # 24ピクセル間隔で配置
            screen_y = playfield_y + 24  # プレイフィールドの上から2行目
            puyo.draw(screen_x, screen_y)
        
        # 現在落下中のぷよペアの描画
        if self.current_falling_pair is not None:
            self.current_falling_pair.draw(playfield_x, playfield_y)
        
        # 次のぷよペアのプレビュー表示（PuyoManagerクラスの動作確認）
        next_preview_x = playfield_x + playfield_width + 20
        next_preview_y = playfield_y + 20
        
        # "NEXT" ラベルの表示
        pyxel.text(next_preview_x, next_preview_y - 15, "NEXT:", 7)
        
        # 次のペアのプレビューを描画
        self.puyo_manager.draw_next_pair_preview(next_preview_x, next_preview_y)
        
        # 操作説明の表示
        pyxel.text(50, 400, "Controls:", 7)
        pyxel.text(50, 410, "Arrow Keys: Move/Drop", 7)
        pyxel.text(50, 420, "X/UP: Rotate CW, Z: Rotate CCW", 7)
        pyxel.text(50, 430, "Q/ESC: Quit Game", 7)
        pyxel.text(50, 440, "G: Test Gravity", 7)
        pyxel.text(50, 450, "C: Test Connection", 7)
        pyxel.text(50, 460, "Test Pair: Red+Green (controllable)", 7)
        
        # デバッグ情報の表示
        pyxel.text(10, 10, f"Frame: {self.frame_count}", 7)
        
        # 重力処理状態の表示
        if self.gravity_active:
            pyxel.text(10, 20, "GRAVITY ACTIVE", 8)  # 赤色で表示
        else:
            pyxel.text(10, 20, "Gravity: Idle", 7)   # 白色で表示
        
        # 現在のぷよペア状態の表示
        if self.current_falling_pair is not None:
            pair_pos = self.current_falling_pair.get_position()
            pyxel.text(10, 30, f"Pair: ({pair_pos[0]}, {pair_pos[1]})", 7)
        else:
            pyxel.text(10, 30, "Pair: None", 7)


def main():
    """
    ゲームのエントリーポイント
    """
    PuyoPuyoGame()


if __name__ == "__main__":
    main()  
  
    def start_elimination_process(self):
        """
        消去処理を開始
        Requirements: 3.1, 5.2 - ぷよ固定後の消去処理開始
        """
        # 消去可能なグループを検出
        erasable_groups = self.playfield.find_erasable_groups()
        
        if erasable_groups:
            # 消去処理を開始
            self.elimination_active = True
            self.elimination_timer = 0
            self.elimination_groups = erasable_groups
            
            # デバッグ情報
            print(f"消去処理開始: {len(erasable_groups)}グループ、{sum(len(group) for group in erasable_groups)}個のぷよ")
        else:
            # 消去するものがない場合は重力処理に移行
            self.apply_gravity_after_fixation()
    
    def update_elimination_system(self):
        """
        消去システムの更新処理
        Requirements: 3.1, 5.2 - 消去アニメーションと処理の管理
        """
        if not self.elimination_active:
            return
        
        # 消去タイマーの更新
        self.elimination_timer += 1
        
        # 消去アニメーションの実行タイミングかチェック
        if self.elimination_timer >= self.elimination_interval:
            # 実際に消去を実行
            eliminated, total_erased, group_count = self.playfield.process_puyo_elimination()
            
            if eliminated:
                print(f"ぷよ消去完了: {total_erased}個のぷよ、{group_count}グループ")
                
                # 消去処理完了、重力処理に移行
                self.elimination_active = False
                self.elimination_timer = 0
                self.elimination_groups = []
                
                # 重力処理を開始
                self.apply_gravity_after_fixation()
            else:
                # 消去するものがなかった場合（エラー状態）
                self.elimination_active = False
                self.elimination_timer = 0
                self.elimination_groups = []
    
    def apply_gravity_after_fixation(self):
        """
        ぷよ固定後の重力処理を開始
        Requirements: 3.3 - ぷよ固定後の重力適用
        """
        # 重力処理を開始
        self.gravity_active = True
        self.gravity_timer = 0
    
    def update_gravity_system(self):
        """
        重力システムの更新処理
        Requirements: 3.3 - 浮いているぷよの落下処理、重力処理のアニメーション
        """
        if not self.gravity_active:
            return
        
        # 重力タイマーの更新
        self.gravity_timer += 1
        
        # 重力処理の実行タイミングかチェック
        if self.gravity_timer >= self.gravity_interval:
            # 重力を適用
            gravity_applied = self.playfield.apply_gravity()
            
            if gravity_applied:
                # ぷよが移動した場合、タイマーをリセットして継続
                self.gravity_timer = 0
            else:
                # ぷよが移動しなかった場合、重力処理を終了
                self.gravity_active = False
                self.gravity_timer = 0
                
                # 重力処理完了後、再度消去判定を行う（連鎖のため）
                self.check_for_chain_elimination()
    
    def check_for_chain_elimination(self):
        """
        連鎖のための消去判定をチェック
        Requirements: 3.4 - 連鎖判定（将来の実装のための準備）
        """
        # 重力処理後に新たな消去可能グループがあるかチェック
        erasable_groups = self.playfield.find_erasable_groups()
        
        if erasable_groups:
            # 連鎖発生！再度消去処理を開始
            print(f"連鎖発生！{len(erasable_groups)}グループが新たに消去可能")
            self.start_elimination_process()
        else:
            # 連鎖終了、通常のゲーム状態に戻る
            print("消去・重力処理完了")
    
    def handle_puyo_pair_input(self):
        """
        現在のぷよペアに対する入力処理
        Requirements: 2.2, 2.3, 2.4 - 移動、回転、高速落下の入力処理
        """
        if self.current_falling_pair is None:
            return
        
        # 左右移動の処理
        if self.input_handler.should_move_left():
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, -1, 0):
                self.current_falling_pair.move(-1, 0)
        
        if self.input_handler.should_move_right():
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, 1, 0):
                self.current_falling_pair.move(1, 0)
        
        # 回転の処理（キックシステム付き）
        if self.input_handler.should_rotate_clockwise():
            self.playfield.rotate_puyo_pair_with_kick(self.current_falling_pair, True)
        
        if self.input_handler.should_rotate_counterclockwise():
            self.playfield.rotate_puyo_pair_with_kick(self.current_falling_pair, False)
        
        # 高速落下の処理（個別の下移動）
        if self.input_handler.should_fast_drop():
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, 0, 1):
                self.current_falling_pair.move(0, 1)
                self.fall_timer = 0  # タイマーリセット
    
    def update(self):
        """
        ゲーム状態の更新処理（毎フレーム呼び出される）
        Requirements: 1.1 - システムは対応するゲーム操作を実行する
        """
        # フレームカウンターの更新
        self.frame_count += 1
        
        # 入力処理の更新
        self.input_handler.update()
        
        # 基本的なキー入力処理
        if self.input_handler.should_quit_game():
            pyxel.quit()
        
        # 重力テスト機能（Gキー）
        if self.input_handler.should_test_gravity():
            self.apply_gravity_after_fixation()
        
        # 連結判定テスト機能（Cキー）
        if self.input_handler.should_test_connection():
            self.test_connection_detection()
        
        # 消去処理テスト機能（Eキー）
        if self.input_handler.should_test_elimination():
            self.test_elimination_process()
        
        # 消去システムの更新
        # Requirements: 3.1, 5.2 - 消去処理とアニメーション
        self.update_elimination_system()
        
        # 重力システムの更新
        # Requirements: 3.3 - 浮いているぷよの落下処理、重力処理のアニメーション
        self.update_gravity_system()
        
        # 消去・重力処理中でない場合のみ通常の落下システムと入力処理を実行
        if not self.elimination_active and not self.gravity_active:
            # 落下システムの更新
            # Requirements: 2.1, 2.4, 2.5 - 自動落下、高速落下、ぷよ固定
            self.update_fall_system()
            
            # 現在のぷよペアに対する入力処理
            # Requirements: 2.2, 2.3, 2.4 - 移動、回転、高速落下の入力処理
            self.handle_puyo_pair_input()
    
    def test_connection_detection(self):
        """
        連結判定のテスト機能
        Requirements: 3.1 - 連結グループの検出とデバッグ表示
        """
        # 連結グループを検出
        connected_groups = self.playfield.find_connected_groups()
        erasable_groups = self.playfield.find_erasable_groups()
        
        print(f"=== 連結判定テスト結果 ===")
        print(f"全連結グループ数: {len(connected_groups)}")
        print(f"消去可能グループ数: {len(erasable_groups)}")
        
        # 各グループの詳細を表示
        for i, group in enumerate(connected_groups):
            if len(group) >= 4:
                print(f"グループ {i+1}: {len(group)}個 (消去可能)")
            else:
                print(f"グループ {i+1}: {len(group)}個")
            
            # グループ内のぷよの色を確認
            if group:
                x, y = group[0]
                puyo = self.playfield.get_puyo(x, y)
                if puyo:
                    color_names = {1: "赤", 2: "オレンジ", 3: "緑", 4: "青"}
                    color_name = color_names.get(puyo.get_color(), "不明")
                    print(f"  色: {color_name}, 座標: {group}")
        
        print("========================")
    
    def draw(self):
        """
        画面描画処理（毎フレーム呼び出される）
        Requirements: 1.1 - システムはゲーム画面を表示する
        Requirements: 1.2 - システムはプレイフィールドとぷよを表示する
        """
        # 画面をクリア（黒色 - デザイン文書の色定義に基づく）
        pyxel.cls(0)
        
        # ゲームタイトルの表示
        title_text = "Puyo Puyo Puzzle Game"
        title_x = (320 - len(title_text) * 4) // 2  # 中央揃え
        pyxel.text(title_x, 50, title_text, 7)  # 白色で表示
        
        # プレイフィールドの枠を描画（デザイン文書の座標に基づく）
        # プレイフィールド位置: x=88-232, y=60-348
        playfield_x = 88
        playfield_y = 60
        playfield_width = 144  # 6 * 24ピクセル
        playfield_height = 288  # 12 * 24ピクセル
        
        # プレイフィールドの描画（PlayFieldクラスの動作確認）
        self.playfield.draw(playfield_x, playfield_y)
        
        # 消去予定のぷよを点滅表示（アニメーション効果）
        if self.elimination_active and self.elimination_groups:
            # 点滅効果（フレーム数に基づく）
            if (self.elimination_timer // 5) % 2 == 0:  # 5フレームごとに点滅
                for group in self.elimination_groups:
                    for x, y in group:
                        screen_x = playfield_x + x * 24
                        screen_y = playfield_y + y * 24
                        # 白い枠で強調表示
                        pyxel.rectb(screen_x, screen_y, 24, 24, 7)
        
        # テスト用ぷよの描画（Puyoクラスの動作確認）
        for i, puyo in enumerate(self.test_puyos):
            # プレイフィールド内の位置に描画
            screen_x = playfield_x + (i * 24)  # 24ピクセル間隔で配置
            screen_y = playfield_y + 24  # プレイフィールドの上から2行目
            puyo.draw(screen_x, screen_y)
        
        # 現在落下中のぷよペアの描画
        if self.current_falling_pair is not None:
            self.current_falling_pair.draw(playfield_x, playfield_y)
        
        # 次のぷよペアのプレビュー表示（PuyoManagerクラスの動作確認）
        next_preview_x = playfield_x + playfield_width + 20
        next_preview_y = playfield_y + 20
        
        # "NEXT" ラベルの表示
        pyxel.text(next_preview_x, next_preview_y - 15, "NEXT:", 7)
        
        # 次のペアのプレビューを描画
        self.puyo_manager.draw_next_pair_preview(next_preview_x, next_preview_y)
        
        # 操作説明の表示
        pyxel.text(50, 400, "Controls:", 7)
        pyxel.text(50, 410, "Arrow Keys: Move/Drop", 7)
        pyxel.text(50, 420, "X/UP: Rotate CW, Z: Rotate CCW", 7)
        pyxel.text(50, 430, "Q/ESC: Quit Game", 7)
        pyxel.text(50, 440, "G: Test Gravity", 7)
        pyxel.text(50, 450, "C: Test Connection", 7)
        pyxel.text(50, 460, "Test Pair: Red+Green (controllable)", 7)
        
        # デバッグ情報の表示
        pyxel.text(10, 10, f"Frame: {self.frame_count}", 7)
        
        # 重力処理状態の表示
        if self.gravity_active:
            pyxel.text(10, 20, "GRAVITY ACTIVE", 8)  # 赤色で表示
        else:
            pyxel.text(10, 20, "Gravity: Idle", 7)   # 白色で表示
        
        # 消去処理状態の表示
        if self.elimination_active:
            pyxel.text(10, 30, "ELIMINATION ACTIVE", 9)  # オレンジ色で表示
        else:
            pyxel.text(10, 30, "Elimination: Idle", 7)   # 白色で表示
        
        # 現在のぷよペア状態の表示
        if self.current_falling_pair is not None:
            pair_pos = self.current_falling_pair.get_position()
            pyxel.text(10, 40, f"Pair: ({pair_pos[0]}, {pair_pos[1]})", 7)
        else:
            pyxel.text(10, 40, "Pair: None", 7)


def main():
    """
    ゲームのエントリーポイント
    """
    PuyoPuyoGame()


if __name__ == "__main__":
    main()    

    def test_elimination_process(self):
        """
        消去処理のテスト機能
        Requirements: 3.1, 5.2 - 消去処理のテストとデバッグ表示
        """
        # テスト用の消去可能なぷよを配置
        # 4つの赤いぷよを2x2で配置
        test_positions = [(0, 8), (0, 9), (1, 8), (1, 9)]
        for x, y in test_positions:
            if self.playfield.is_empty(x, y):
                self.playfield.place_puyo(x, y, Puyo(1))  # 赤いぷよ
        
        # 消去処理を開始
        self.start_elimination_process()
        
        print("=== 消去処理テスト実行 ===")
        print("4つの赤いぷよを左上に配置して消去処理を開始しました")
        print("========================")