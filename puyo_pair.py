from puyo import Puyo


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