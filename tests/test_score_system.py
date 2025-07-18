"""
Test file for the score system implementation
Requirements: 3.2 - スコア計算と管理システムのテスト
"""

import sys
import os
# Add the parent directory to sys.path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.score_manager import ScoreManager


def test_score_manager_initialization():
    """ScoreManagerの初期化をテスト"""
    score_manager = ScoreManager()
    
    # 初期状態の確認
    assert score_manager.get_score() == 0
    assert score_manager.get_chain_count() == 0
    
    print("[OK] Score manager initialization test passed")


def test_basic_score_calculation():
    """基本スコア計算をテスト"""
    score_manager = ScoreManager()
    
    # 4個のぷよを消去（1連鎖）
    score = score_manager.calculate_score(4, 1)
    expected_score = 4 * 10 * 1 * 1  # 4個 × 10点 × 1倍（連鎖） × 1倍（その他ボーナス）
    assert score == expected_score
    
    # 6個のぷよを消去（1連鎖）
    score = score_manager.calculate_score(6, 1)
    expected_score = 6 * 10 * 1 * (1 + 4)  # 6個 × 10点 × 1倍 × (1 + グループボーナス4)
    assert score == expected_score
    
    print("[OK] Basic score calculation test passed")


def test_chain_bonus_calculation():
    """連鎖ボーナス計算をテスト"""
    score_manager = ScoreManager()
    
    # 1連鎖（ボーナス倍率1）
    score = score_manager.calculate_score(4, 1)
    expected_score = 4 * 10 * 1 * 1  # 基本 × 連鎖倍率 × その他ボーナス
    assert score == expected_score
    
    # 2連鎖（ボーナス倍率8）
    score = score_manager.calculate_score(4, 2)
    expected_score = 4 * 10 * 8 * 1
    assert score == expected_score
    
    # 3連鎖（ボーナス倍率16）
    score = score_manager.calculate_score(4, 3)
    expected_score = 4 * 10 * 16 * 1
    assert score == expected_score
    
    # 5連鎖（ボーナス倍率64）
    score = score_manager.calculate_score(4, 5)
    expected_score = 4 * 10 * 64 * 1
    assert score == expected_score
    
    print("[OK] Chain bonus calculation test passed")


def test_color_bonus_calculation():
    """色数ボーナス計算をテスト"""
    score_manager = ScoreManager()
    
    # 1色（ボーナス0）
    score = score_manager.calculate_score(4, 1, color_count=1)
    expected_score = 4 * 10 * 1 * 1  # 基本 × 連鎖倍率 × (1 + 色ボーナス0)
    assert score == expected_score
    
    # 2色（ボーナス3）
    score = score_manager.calculate_score(4, 1, color_count=2)
    expected_score = 4 * 10 * 1 * (1 + 3)  # 基本 × 連鎖倍率 × (1 + 色ボーナス3)
    assert score == expected_score
    
    # 3色（ボーナス6）
    score = score_manager.calculate_score(4, 1, color_count=3)
    expected_score = 4 * 10 * 1 * (1 + 6)  # 基本 × 連鎖倍率 × (1 + 色ボーナス6)
    assert score == expected_score
    
    print("[OK] Color bonus calculation test passed")


def test_group_bonus_calculation():
    """グループボーナス計算をテスト"""
    score_manager = ScoreManager()
    
    # 4個（グループボーナス0）
    score = score_manager.calculate_score(4, 1)
    expected_score = 4 * 10 * 1 * 1  # 基本 × 連鎖倍率 × (1 + グループボーナス0)
    assert score == expected_score
    
    # 5個（グループボーナス2）
    score = score_manager.calculate_score(5, 1)
    expected_score = 5 * 10 * 1 * (1 + 2)  # 基本 × 連鎖倍率 × (1 + グループボーナス2)
    assert score == expected_score
    
    # 8個（グループボーナス8）
    score = score_manager.calculate_score(8, 1)
    expected_score = 8 * 10 * 1 * (1 + 8)  # 基本 × 連鎖倍率 × (1 + グループボーナス8)
    assert score == expected_score
    
    print("[OK] Group bonus calculation test passed")


def test_combined_bonus_calculation():
    """複合ボーナス計算をテスト"""
    score_manager = ScoreManager()
    
    # 2連鎖 + 2色 + 6個のぷよ
    score = score_manager.calculate_score(6, 2, color_count=2)
    # 基本60 × 連鎖倍率8 × (1 + 色ボーナス3 + グループボーナス4) = 60 × 8 × 8
    expected_score = 6 * 10 * 8 * (1 + 3 + 4)
    assert score == expected_score
    
    # 3連鎖 + 3色 + 10個のぷよ
    score = score_manager.calculate_score(10, 3, color_count=3)
    # 基本100 × 連鎖倍率16 × (1 + 色ボーナス6 + グループボーナス12) = 100 × 16 × 19
    expected_score = 10 * 10 * 16 * (1 + 6 + 12)
    assert score == expected_score
    
    print("[OK] Combined bonus calculation test passed")


def test_score_addition():
    """スコア加算をテスト"""
    score_manager = ScoreManager()
    
    # 初期スコア確認
    assert score_manager.get_score() == 0
    
    # スコア加算
    score_manager.add_score(100)
    assert score_manager.get_score() == 100
    
    # 追加でスコア加算
    score_manager.add_score(250)
    assert score_manager.get_score() == 350
    
    # 負の値は加算されない
    score_manager.add_score(-50)
    assert score_manager.get_score() == 350
    
    print("[OK] Score addition test passed")


def test_score_reset():
    """スコアリセットをテスト"""
    score_manager = ScoreManager()
    
    # スコアを設定
    score_manager.add_score(1000)
    score_manager.set_chain_count(5)
    
    # リセット前の確認
    assert score_manager.get_score() == 1000
    assert score_manager.get_chain_count() == 5
    
    # リセット実行
    score_manager.reset()
    
    # リセット後の確認
    assert score_manager.get_score() == 0
    assert score_manager.get_chain_count() == 0
    
    print("[OK] Score reset test passed")


def test_chain_score_calculation():
    """連鎖スコア計算をテスト"""
    score_manager = ScoreManager()
    
    # テスト用の消去グループ
    # グループ1: 4個のぷよ
    group1 = [(0, 8), (0, 9), (1, 8), (1, 9)]
    # グループ2: 5個のぷよ
    group2 = [(2, 7), (2, 8), (2, 9), (3, 8), (3, 9)]
    
    eliminated_groups = [group1, group2]
    
    # 2連鎖でのスコア計算
    score = score_manager.calculate_chain_score(eliminated_groups, 2)
    
    # 総消去数: 9個、色数: 2、連鎖レベル: 2
    # 基本90 × 連鎖倍率8 × (1 + 色ボーナス3 + グループボーナス10) = 90 × 8 × 14
    expected_score = 9 * 10 * 8 * (1 + 3 + 10)
    assert score == expected_score
    
    print("[OK] Chain score calculation test passed")


def test_score_formatting():
    """スコア表示フォーマットをテスト"""
    score_manager = ScoreManager()
    
    # 小さなスコア
    score_manager.add_score(123)
    formatted = score_manager.format_score()
    assert formatted == "123"
    
    # 大きなスコア
    score_manager.reset()
    score_manager.add_score(12345)
    formatted = score_manager.format_score()
    assert formatted == "12,345"
    
    # 非常に大きなスコア
    score_manager.reset()
    score_manager.add_score(1234567)
    formatted = score_manager.format_score()
    assert formatted == "1,234,567"
    
    # 指定したスコアのフォーマット
    formatted = score_manager.format_score(9876543)
    assert formatted == "9,876,543"
    
    print("[OK] Score formatting test passed")


def test_chain_bonus_multiplier():
    """連鎖ボーナス倍率取得をテスト"""
    score_manager = ScoreManager()
    
    # 各連鎖レベルのボーナス倍率確認
    assert score_manager.get_chain_bonus_multiplier(1) == 1
    assert score_manager.get_chain_bonus_multiplier(2) == 8
    assert score_manager.get_chain_bonus_multiplier(3) == 16
    assert score_manager.get_chain_bonus_multiplier(4) == 32
    assert score_manager.get_chain_bonus_multiplier(5) == 64
    
    # 範囲外の値
    assert score_manager.get_chain_bonus_multiplier(0) == 0
    assert score_manager.get_chain_bonus_multiplier(-1) == 0
    
    # 最大値を超えた場合
    max_multiplier = score_manager.get_chain_bonus_multiplier(10)
    expected_max = score_manager.chain_bonus_multiplier[-1]
    assert max_multiplier == expected_max
    
    print("[OK] Chain bonus multiplier test passed")


def test_zero_cleared_count():
    """消去数0の場合のテスト"""
    score_manager = ScoreManager()
    
    # 消去数0の場合はスコア0
    score = score_manager.calculate_score(0, 1)
    assert score == 0
    
    # 負の消去数の場合もスコア0
    score = score_manager.calculate_score(-5, 1)
    assert score == 0
    
    print("[OK] Zero cleared count test passed")


def test_high_chain_level():
    """高連鎖レベルのテスト"""
    score_manager = ScoreManager()
    
    # 非常に高い連鎖レベル（配列の範囲を超える）
    score = score_manager.calculate_score(4, 20)
    # 最大ボーナス倍率が使用される
    max_bonus = score_manager.chain_bonus_multiplier[-1]
    expected_score = 4 * 10 * max_bonus * 1  # 基本 × 連鎖倍率 × その他ボーナス
    assert score == expected_score
    
    print("[OK] High chain level test passed")


if __name__ == "__main__":
    print("Running score system tests...")
    
    test_score_manager_initialization()
    test_basic_score_calculation()
    test_chain_bonus_calculation()
    test_color_bonus_calculation()
    test_group_bonus_calculation()
    test_combined_bonus_calculation()
    test_score_addition()
    test_score_reset()
    test_chain_score_calculation()
    test_score_formatting()
    test_chain_bonus_multiplier()
    test_zero_cleared_count()
    test_high_chain_level()
    
    print("All score system tests passed! [OK]")