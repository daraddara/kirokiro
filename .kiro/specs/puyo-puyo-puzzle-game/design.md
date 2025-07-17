# Design Document

## Overview

Pyxelエンジンを使用したぷよぷよ風パズルゲームの設計書です。ゲームは320x480ピクセルの画面で動作し、オブジェクト指向設計を採用してゲーム状態、ぷよの管理、物理演算、UI表示を分離します。

## Architecture

### システム構成

```
Game (Pyxel App)
├── GameState (ゲーム状態管理)
├── PlayField (プレイフィールド管理)
├── PuyoManager (ぷよ生成・管理)
├── InputHandler (入力処理)
├── Renderer (描画処理)
└── ScoreManager (スコア管理)
```

### ゲーム状態

- `MENU`: タイトル画面
- `PLAYING`: ゲームプレイ中
- `GAME_OVER`: ゲームオーバー画面

## Components and Interfaces

### 1. Game Class (メインアプリケーション)

Pyxelアプリケーションのメインクラス。フレーム更新とイベント処理を管理。

**主要メソッド:**
- `update()`: ゲーム状態の更新
- `draw()`: 画面描画
- `init()`: ゲーム初期化

### 2. GameState Class

ゲームの現在状態を管理するステートマシン。

**属性:**
- `current_state`: 現在のゲーム状態
- `score`: 現在のスコア
- `game_over`: ゲームオーバーフラグ

### 3. PlayField Class

6x12のプレイフィールドを管理。ぷよの配置、消去判定、重力処理を担当。

**属性:**
- `grid`: 6x12の2次元配列（0=空、1-4=色）
- `width`: 6 (固定)
- `height`: 12 (固定)

**主要メソッド:**
- `place_puyo(x, y, color)`: ぷよを配置
- `check_connections()`: 連結判定
- `clear_puyos(positions)`: ぷよ消去
- `apply_gravity()`: 重力適用
- `is_game_over()`: ゲームオーバー判定

### 4. PuyoManager Class

落下中のぷよペアと次のぷよペアを管理。

**属性:**
- `current_pair`: 現在落下中のぷよペア
- `next_pair`: 次のぷよペア
- `fall_timer`: 落下タイマー
- `fall_speed`: 落下速度

**主要メソッド:**
- `generate_pair()`: 新しいぷよペア生成
- `move_pair(dx, dy)`: ぷよペア移動
- `rotate_pair()`: ぷよペア回転
- `update_fall()`: 落下処理更新

### 5. PuyoPair Class

2つのぷよからなるペアを表現。

**属性:**
- `puyo1`: メインぷよ（回転軸）
- `puyo2`: サブぷよ
- `x, y`: 位置座標
- `rotation`: 回転状態（0-3）

### 6. Puyo Class

個別のぷよを表現。

**属性:**
- `color`: ぷよの色（1-4）
- `x, y`: 相対位置

### 7. InputHandler Class

キーボード入力を処理。

**主要メソッド:**
- `handle_input()`: 入力処理
- `is_key_pressed(key)`: キー押下判定
- `is_key_just_pressed(key)`: キー押下瞬間判定

### 8. Renderer Class

画面描画を担当。

**主要メソッド:**
- `draw_playfield()`: プレイフィールド描画
- `draw_puyo(x, y, color)`: ぷよ描画
- `draw_ui()`: UI要素描画
- `draw_score()`: スコア表示

### 9. ScoreManager Class

スコア計算と管理。

**属性:**
- `score`: 現在のスコア
- `chain_count`: 連鎖数

**主要メソッド:**
- `calculate_score(cleared_count, chain_level)`: スコア計算
- `add_score(points)`: スコア加算
- `reset()`: スコアリセット

### 10. AudioManager Class

音響効果の管理。

**属性:**
- `bgm_playing`: BGM再生状態
- `sound_enabled`: 効果音有効フラグ

**主要メソッド:**
- `play_bgm()`: BGM再生
- `stop_bgm()`: BGM停止
- `play_sound(sound_type)`: 効果音再生
- `set_volume(volume)`: 音量設定

## Data Models

### 座標系

- プレイフィールド: 6x12グリッド（左上が(0,0)）
- 画面座標: 320x480ピクセル
- ぷよサイズ: 24x24ピクセル
- プレイフィールド位置: 画面中央（x=88-232, y=60-348）

### 色定義

Pyxelの16色パレットを使用:
- 0: 黒（背景）
- 7: 白（UI）
- 8: 赤（ぷよ色1）
- 9: オレンジ（ぷよ色2）
- 11: 緑（ぷよ色3）
- 12: 青（ぷよ色4）

### ゲームタイミング

- 基本落下速度: 30フレーム（0.5秒）
- 高速落下: 3フレーム
- 消去アニメーション: 15フレーム
- 連鎖間隔: 20フレーム

## Error Handling

### 入力エラー

- 無効な移動・回転: 操作を無視
- 範囲外アクセス: 境界チェックで防止

### ゲーム状態エラー

- 不正な状態遷移: ログ出力して前の状態を維持
- メモリ不足: Pyxelの制限内で動作するよう設計

### 描画エラー

- 範囲外描画: Pyxelの座標チェックに依存
- 色指定エラー: デフォルト色で代替

## Testing Strategy

### 単体テスト

1. **PlayField Class**
   - ぷよ配置テスト
   - 連結判定テスト
   - 重力処理テスト
   - ゲームオーバー判定テスト

2. **PuyoManager Class**
   - ぷよペア生成テスト
   - 移動・回転テスト
   - 衝突判定テスト

3. **ScoreManager Class**
   - スコア計算テスト
   - 連鎖ボーナステスト

### 統合テスト

1. **ゲームフロー**
   - 開始→プレイ→終了の流れ
   - 状態遷移テスト

2. **ゲームプレイ**
   - ぷよ操作から消去までの一連の流れ
   - 連鎖動作テスト

### 手動テスト

1. **ユーザビリティ**
   - 操作感の確認
   - 視覚的フィードバックの確認

2. **パフォーマンス**
   - フレームレート確認
   - メモリ使用量確認

## Implementation Notes

### Pyxel固有の考慮事項

- 320x480ピクセルの画面サイズでの最適なUI設計
- 16色制限を活かした色使い
- 60FPSでの滑らかな動作
- シンプルなキー入力処理

### パフォーマンス最適化

- 不要な描画処理の削減
- 効率的な連結判定アルゴリズム
- メモリ使用量の最小化