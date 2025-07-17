# Requirements Document

## Introduction

Pyxelゲームエンジンを使用して、ぷよぷよ風のパズルゲームを開発します。このゲームでは、プレイヤーが落下するぷよ（色付きブロック）をコントロールし、同じ色のぷよを4つ以上つなげて消すことでスコアを獲得します。連鎖反応によってより高いスコアを目指すパズルゲームです。

## Requirements

### Requirement 1

**User Story:** プレイヤーとして、ゲームを開始して基本的なゲームプレイを楽しみたい

#### Acceptance Criteria

1. WHEN ゲームを起動する THEN システムは ゲーム画面を表示する SHALL
2. WHEN ゲームが開始される THEN システムは プレイフィールドとぷよを表示する SHALL
3. WHEN プレイヤーがキーを押す THEN システムは 対応するゲーム操作を実行する SHALL

### Requirement 2

**User Story:** プレイヤーとして、ぷよを操作してパズルを解きたい

#### Acceptance Criteria

1. WHEN ぷよペアが画面上部から落下する THEN システムは 重力に従ってぷよを移動させる SHALL
2. WHEN プレイヤーが左右キーを押す THEN システムは ぷよペアを左右に移動させる SHALL
3. WHEN プレイヤーが回転キーを押す THEN システムは ぷよペアを時計回りに回転させる SHALL
4. WHEN プレイヤーが下キーを押す THEN システムは ぷよの落下速度を上げる SHALL
5. WHEN ぷよが底面または他のぷよに接触する THEN システムは ぷよを固定する SHALL

### Requirement 3

**User Story:** プレイヤーとして、同じ色のぷよを消してスコアを獲得したい

#### Acceptance Criteria

1. WHEN 同じ色のぷよが4つ以上隣接して配置される THEN システムは それらのぷよを消去する SHALL
2. WHEN ぷよが消去される THEN システムは スコアを加算する SHALL
3. WHEN ぷよが消去される THEN システムは 上にあるぷよを重力で落下させる SHALL
4. WHEN 落下により新たに4つ以上の同色ぷよが隣接する THEN システムは 連鎖として追加消去とボーナススコアを与える SHALL

### Requirement 4

**User Story:** プレイヤーとして、ゲームの進行状況を把握したい

#### Acceptance Criteria

1. WHEN ゲームが進行中である THEN システムは 現在のスコアを表示する SHALL
2. WHEN ゲームが進行中である THEN システムは 次に落下するぷよペアを表示する SHALL
3. WHEN プレイフィールドが上端まで埋まる THEN システムは ゲームオーバー状態にする SHALL
4. WHEN ゲームオーバーになる THEN システムは 最終スコアとゲームオーバー画面を表示する SHALL

### Requirement 5

**User Story:** プレイヤーとして、視覚的に魅力的なゲーム体験を得たい

#### Acceptance Criteria

1. WHEN ぷよが表示される THEN システムは 異なる色で区別可能なぷよを描画する SHALL
2. WHEN ぷよが消去される THEN システムは 消去アニメーションを表示する SHALL
3. WHEN 連鎖が発生する THEN システムは 連鎖数を視覚的に表示する SHALL
4. WHEN ゲームが進行中である THEN システムは 滑らかなアニメーションでぷよの動きを表現する SHALL

### Requirement 6

**User Story:** プレイヤーとして、ゲームを再開したり終了したりできるようにしたい

#### Acceptance Criteria

1. WHEN ゲームオーバー状態である THEN システムは 新しいゲームを開始するオプションを提供する SHALL
2. WHEN プレイヤーがリスタートを選択する THEN システムは ゲーム状態をリセットして新しいゲームを開始する SHALL
3. WHEN プレイヤーが終了を選択する THEN システムは ゲームを終了する SHALL