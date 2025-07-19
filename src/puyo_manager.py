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
        
        # 特殊ぷよの色コード
        self.OBSTACLE_PUYO = 5  # お邪魔ぷよの色コード
        
        # 色の出現履歴（バランスの取れた色分布のため）
        self.color_history = []
        self.history_max_size = 8  # 履歴の最大サイズ
        
        # 難易度設定（0.0-1.0、高いほど難しい）
        self.difficulty = 0.5
        
        # 現在のぷよペアと次のぷよペア
        self.current_pair = None
        self.next_pair = None
        
        # お邪魔ぷよの発生カウンター
        self.obstacle_counter = 0
        self.obstacle_threshold = 25  # この回数ぷよを配置するとお邪魔ぷよが発生
        
        # 初期ペアを生成
        self.generate_initial_pairs()
    
    def generate_random_color(self):
        """
        バランスの取れたランダムな色を生成
        履歴に基づいて、最近出現していない色が出やすくなる
        
        Returns:
            int: ランダムな色（1-4）
        """
        # 完全にランダムな場合（20%の確率）
        if self.random.random() < 0.2:
            return self.random.choice(self.available_colors)
        
        # 履歴に基づいた重み付け
        if len(self.color_history) > 0:
            # 各色の出現回数をカウント
            color_counts = {color: 0 for color in self.available_colors}
            for color in self.color_history:
                if color in color_counts:
                    color_counts[color] += 1
            
            # 出現回数が少ない色ほど重みを大きくする
            weights = {}
            max_count = max(color_counts.values()) if color_counts else 1
            for color, count in color_counts.items():
                # 出現回数が少ないほど重みが大きくなる
                weights[color] = max_count - count + 1
            
            # 重み付き抽選
            total_weight = sum(weights.values())
            r = self.random.uniform(0, total_weight)
            cumulative_weight = 0
            for color, weight in weights.items():
                cumulative_weight += weight
                if r <= cumulative_weight:
                    selected_color = color
                    break
            else:
                # 万が一の場合は完全ランダム
                selected_color = self.random.choice(self.available_colors)
        else:
            # 履歴がない場合は完全ランダム
            selected_color = self.random.choice(self.available_colors)
        
        # 履歴を更新
        self.color_history.append(selected_color)
        if len(self.color_history) > self.history_max_size:
            self.color_history.pop(0)  # 古い履歴を削除
        
        return selected_color
    
    def create_random_puyo_pair(self, x=2, y=0):
        """
        ランダムな色のぷよペアを作成
        難易度に応じて同色ペアの出現確率を調整
        
        Args:
            x (int): ペアの初期X座標（デフォルト: 2）
            y (int): ペアの初期Y座標（デフォルト: 0）
        
        Returns:
            PuyoPair: 新しいランダムなぷよペア
        """
        main_color = self.generate_random_color()
        
        # 難易度に応じて同色ペアの確率を調整
        # 難易度が低いほど同色ペアが出やすい（初心者向け）
        same_color_chance = 0.3 - (self.difficulty * 0.2)  # 難易度0.0で30%、難易度1.0で10%
        
        if self.random.random() < same_color_chance:
            # 同色ペア
            sub_color = main_color
        else:
            # 異なる色のペア
            sub_color = self.generate_random_color()
            # メインと同じ色になった場合は再抽選（最大3回）
            attempts = 0
            while sub_color == main_color and attempts < 3:
                sub_color = self.generate_random_color()
                attempts += 1
        
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
        
        # 初期位置を設定（中央上部）
        # サブぷよが画面内に収まるように、下向きの回転状態で配置
        self.current_pair.set_position(2, 0)  # 初期位置を上端に設定
        self.current_pair.rotation = 2  # 下向きの回転状態に設定（サブぷよが下に来る）
        
        # お邪魔ぷよカウンターを更新
        self.obstacle_counter += 1
        
        # 新しい次のペアを生成
        if self.should_generate_obstacle_puyo():
            self.next_pair = self.create_obstacle_puyo_pair()
            self.obstacle_counter = 0  # カウンターリセット
        else:
            self.next_pair = self.create_random_puyo_pair()
        
        return self.current_pair
    
    def reset(self):
        """
        PuyoManagerをリセット（新しいゲーム開始時）
        """
        # 色履歴をクリア
        self.color_history = []
        # 初期ペアを生成
        self.generate_initial_pairs()
        
    def set_difficulty(self, difficulty):
        """
        難易度を設定する
        
        Args:
            difficulty (float): 難易度（0.0-1.0、高いほど難しい）
        """
        self.difficulty = max(0.0, min(1.0, difficulty))  # 0.0-1.0の範囲に制限
    
    def should_generate_obstacle_puyo(self):
        """
        お邪魔ぷよを生成すべきかどうかを判定
        
        Returns:
            bool: お邪魔ぷよを生成する場合True
        """
        # 難易度に応じてお邪魔ぷよの発生頻度を調整
        adjusted_threshold = self.obstacle_threshold - int(self.difficulty * 10)  # 難易度が高いほど早く発生
        
        # 一定回数ぷよを配置するとお邪魔ぷよが発生
        return self.obstacle_counter >= adjusted_threshold
    
    def create_obstacle_puyo_pair(self, x=2, y=0):
        """
        お邪魔ぷよペアを作成
        
        Args:
            x (int): ペアの初期X座標（デフォルト: 2）
            y (int): ペアの初期Y座標（デフォルト: 0）
        
        Returns:
            PuyoPair: お邪魔ぷよを含むペア
        """
        # 難易度に応じてお邪魔ぷよの数を決定
        if self.random.random() < self.difficulty:
            # 難易度が高い場合、両方お邪魔ぷよ
            main_puyo = Puyo(self.OBSTACLE_PUYO)
            sub_puyo = Puyo(self.OBSTACLE_PUYO)
        else:
            # 片方だけお邪魔ぷよ
            main_puyo = Puyo(self.OBSTACLE_PUYO)
            sub_color = self.generate_random_color()
            sub_puyo = Puyo(sub_color)
        
        return PuyoPair(main_puyo, sub_puyo, x, y)
    
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