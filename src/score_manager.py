"""
ScoreManagerクラス - スコア計算と管理
Requirements: 3.2 - スコア加算と管理システム
"""


class ScoreManager:
    """
    スコア管理クラス - 基本スコア計算と連鎖ボーナスの管理
    Requirements: 3.2 - スコア加算と管理
    """
    
    def __init__(self):
        """
        ScoreManagerの初期化
        """
        self.score = 0  # 現在のスコア
        self.chain_count = 0  # 連鎖数
        
        # スコア計算の基本設定
        self.base_score_per_puyo = 10  # ぷよ1個あたりの基本スコア
        self.chain_bonus_multiplier = [1, 8, 16, 32, 64, 96, 128, 160, 192, 224]  # 連鎖ボーナス倍率
        self.color_bonus = {1: 0, 2: 3, 3: 6, 4: 12, 5: 24}  # 色数ボーナス
        self.group_bonus = 0  # グループボーナス（4個以上で追加）
    
    def calculate_score(self, cleared_count, chain_level, color_count=1, group_count=1):
        """
        スコアを計算する
        
        Args:
            cleared_count (int): 消去されたぷよの数
            chain_level (int): 連鎖レベル（1から開始）
            color_count (int): 消去された色の種類数（デフォルト1）
            group_count (int): 消去されたグループ数（デフォルト1）
        
        Returns:
            int: 計算されたスコア
        
        Requirements: 3.2 - 基本スコア計算と連鎖ボーナス
        """
        if cleared_count <= 0:
            return 0
        
        # 基本スコア = 消去ぷよ数 × 基本スコア
        base_score = cleared_count * self.base_score_per_puyo
        
        # 連鎖ボーナス倍率
        chain_multiplier = 1
        if chain_level > 0 and chain_level <= len(self.chain_bonus_multiplier):
            chain_multiplier = self.chain_bonus_multiplier[chain_level - 1]
        elif chain_level > len(self.chain_bonus_multiplier):
            # 最大連鎖を超えた場合は最大値を使用
            chain_multiplier = self.chain_bonus_multiplier[-1]
        
        # 色数ボーナス
        color_bonus = self.color_bonus.get(color_count, 0)
        
        # グループボーナス（4個以上のグループに対して）
        group_bonus = max(0, (cleared_count - 4) * 2) if cleared_count >= 4 else 0
        
        # 総合ボーナス
        total_bonus = color_bonus + group_bonus
        
        # 最終スコア = 基本スコア × 連鎖倍率 × (1 + その他ボーナス)
        final_score = base_score * chain_multiplier * max(1, 1 + total_bonus)
        
        return final_score
    
    def add_score(self, points):
        """
        スコアを加算する
        
        Args:
            points (int): 加算するスコア
        
        Requirements: 3.2 - スコア加算
        """
        if points > 0:
            self.score += points
    
    def get_score(self):
        """
        現在のスコアを取得する
        
        Returns:
            int: 現在のスコア
        """
        return self.score
    
    def set_chain_count(self, chain_count):
        """
        連鎖数を設定する
        
        Args:
            chain_count (int): 連鎖数
        """
        self.chain_count = chain_count
    
    def get_chain_count(self):
        """
        現在の連鎖数を取得する
        
        Returns:
            int: 現在の連鎖数
        """
        return self.chain_count
    
    def reset(self):
        """
        スコアと連鎖数をリセットする
        
        Requirements: 3.2 - スコアリセット
        """
        self.score = 0
        self.chain_count = 0
    
    def get_chain_bonus_multiplier(self, chain_level):
        """
        指定された連鎖レベルのボーナス倍率を取得する
        
        Args:
            chain_level (int): 連鎖レベル
        
        Returns:
            int: ボーナス倍率
        """
        if chain_level <= 0:
            return 0
        elif chain_level <= len(self.chain_bonus_multiplier):
            return self.chain_bonus_multiplier[chain_level - 1]
        else:
            return self.chain_bonus_multiplier[-1]
    
    def calculate_chain_score(self, eliminated_groups, chain_level):
        """
        連鎖による総スコアを計算する
        
        Args:
            eliminated_groups (list): 消去されたグループのリスト [[(x, y), ...], ...]
            chain_level (int): 連鎖レベル
        
        Returns:
            int: 計算されたスコア
        
        Requirements: 3.2 - 連鎖ボーナス計算
        """
        if not eliminated_groups:
            return 0
        
        # 総消去ぷよ数を計算
        total_cleared = sum(len(group) for group in eliminated_groups)
        
        # 色の種類数を計算（将来的に実装）
        color_count = len(eliminated_groups)  # 簡易実装：グループ数を色数とする
        
        # グループ数
        group_count = len(eliminated_groups)
        
        # スコアを計算
        score = self.calculate_score(total_cleared, chain_level, color_count, group_count)
        
        return score
    
    def format_score(self, score=None):
        """
        スコアを表示用にフォーマットする
        
        Args:
            score (int, optional): フォーマットするスコア。Noneの場合は現在のスコア
        
        Returns:
            str: フォーマットされたスコア文字列
        """
        if score is None:
            score = self.score
        
        # 3桁区切りでフォーマット
        return f"{score:,}"