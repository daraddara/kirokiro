from src.puyo import Puyo
from src.puyo_pair import PuyoPair


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