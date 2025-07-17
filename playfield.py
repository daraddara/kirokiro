import pyxel
from puyo import Puyo


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