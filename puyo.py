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