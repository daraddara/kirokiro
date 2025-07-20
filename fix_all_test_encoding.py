#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全てのテストファイルのエンコーディング問題を修正するスクリプト
"""

import os
import re

def fix_test_file_encoding():
    """テストファイルのエンコーディング問題を修正"""
    test_dir = "tests"
    
    # 修正対象のファイル一覧
    test_files = [
        "test_audio_manager.py",
        "test_chain_system.py", 
        "test_connection_system.py",
        "test_elimination_system.py",
        "test_fall_system.py",
        "test_game_flow.py",
        "test_game_integration.py",
        "test_game_over.py",
        "test_game_state.py",
        "test_gravity_system.py",
        "test_kick_system.py",
        "test_puyo.py",
        "test_restart.py",
        "test_score_display.py",
        "test_score_system.py"
    ]
    
    for filename in test_files:
        filepath = os.path.join(test_dir, filename)
        if os.path.exists(filepath):
            print(f"Fixing {filename}...")
            try:
                # ファイルを読み込み（エラーを無視）
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 破損した文字を修正
                content = re.sub(r'チE.*?チE', 'テスト', content)
                content = re.sub(r'チE.*?ト', 'テスト', content)
                content = re.sub(r'モチE.*?', 'モック', content)
                content = re.sub(r'琁E.*?', '処理', content)
                content = re.sub(r'誁E.*?', '認', content)
                content = re.sub(r'管琁E.*?', '管理', content)
                content = re.sub(r'裁E.*?', '装', content)
                content = re.sub(r'シスチE.*?', 'システム', content)
                content = re.sub(r'オーバ.*?E', 'オーバー', content)
                content = re.sub(r'キチE.*?', 'キック', content)
                content = re.sub(r'アニメーション.*?E.*?', 'アニメーション', content)
                content = re.sub(r'グループ.*?E', 'グループ', content)
                content = re.sub(r'スチE.*?', 'スコア', content)
                content = re.sub(r'表示.*?E', '表示', content)
                content = re.sub(r'計算.*?E', '計算', content)
                content = re.sub(r'機.*?E', '機能', content)
                content = re.sub(r'基本.*?E', '基本', content)
                content = re.sub(r'各.*?E', '各', content)
                content = re.sub(r'吁E.*?', '各', content)
                content = re.sub(r'ラス.*?E', 'ラス', content)
                content = re.sub(r'をテストすめE', 'をテストする', content)
                content = re.sub(r'ぁE.*?', 'す', content)
                content = re.sub(r'離ぁE', '離す', content)
                content = re.sub(r'押ぁE', '押す', content)
                content = re.sub(r'終亁E.*?', '終了時', content)
                content = re.sub(r'フレーム終亁E.*?の処琁E', 'フレーム終了時の処理', content)
                content = re.sub(r'統合テスチE', '統合テスト', content)
                content = re.sub(r'ゲーム.*?E基本機.*?Eが正常に動作することを確.*?E', 'ゲームの基本機能が正常に動作することを確認', content)
                content = re.sub(r'同色ぷよ.*?E隣接判定と連結グループ.*?E検.*?E', '同色ぷよの隣接判定と連結グループの検出', content)
                content = re.sub(r'連鎖判定.*?E実.*?E', '連鎖判定の実装', content)
                content = re.sub(r'落下システム.*?E', '落下システム', content)
                content = re.sub(r'ゲームフロー全体.*?E', 'ゲームフロー全体', content)
                content = re.sub(r'ぷよ消去処.*?E.*?アニメーション.*?E', 'ぷよ消去処理とアニメーション', content)
                content = re.sub(r'ゲームオーバ.*?E判定と状態.*?E移.*?E', 'ゲームオーバー判定と状態遷移', content)
                content = re.sub(r'ゲーム状態管.*?E.*?遷移制御.*?E', 'ゲーム状態管理と遷移制御', content)
                content = re.sub(r'重力処.*?E.*?（.*?Eよ固定後.*?E重力適用、浮.*?E.*?E.*?ぷよ.*?E落下.*?E.*?E.*?力.*?E.*?E.*?アニメーション.*?E.*?', '重力処理（ぷよ固定後の重力適用、浮いているぷよの落下処理、重力処理のアニメーション）', content)
                content = re.sub(r'キ.*?E.*?システム.*?E.*?による回転補助.*?E', 'キックシステムによる回転補助', content)
                content = re.sub(r'スコア表示とアニメーション.*?E', 'スコア表示とアニメーション', content)
                content = re.sub(r'スコア計算と管.*?E.*?スチE.*?E', 'スコア計算と管理システム', content)
                
                # 特殊文字を削除
                content = re.sub(r'\\ufffd', '', content)
                content = re.sub(r'\\u[0-9a-fA-F]{4}', '', content)
                
                # ファイルに書き戻し
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                print(f"Fixed {filename}")
                
            except Exception as e:
                print(f"Error fixing {filename}: {e}")
        else:
            print(f"File {filename} not found, skipping...")

if __name__ == "__main__":
    fix_test_file_encoding()
    print("All test files encoding fix complete!")