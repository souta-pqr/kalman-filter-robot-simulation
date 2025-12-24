# Kalman Filter Robot Simulation

ノイズのある観測値からロボットの位置を推定するカルマンフィルタのシミュレーション

## 概要

本プロジェクトは、カルマンフィルタを実装し、ノイズを含むセンサ観測値から真の状態を推定するシミュレーションを行います。

**実装内容:**
- **1次元ロボットの位置推定**: 線形カルマンフィルタを用いた直線移動ロボットの位置推定
- **2次元ロボットの位置・姿勢推定**: 拡張カルマンフィルタ (EKF) を用いた平面移動ロボットの状態推定


## 背景

### カルマンフィルタとは

カルマンフィルタは、ノイズを含む観測値から対象の真の状態を推定する最適フィルタです。ベイズフィルタの一種であり、状態が線形システムに従い、ノイズがガウス分布に従う場合に、最小二乗誤差の意味で最適な推定を行います。


## 線形カルマンフィルタ (1D Robot)

1次元空間を直線移動するロボットの位置推定を行います。

**シミュレーション設定:**
- ロボットは毎ステップ 1m 移動
- プロセスノイズ: $\sigma_w = 0.1$ m
- 観測ノイズ: $\sigma_v = 0.5$ m

![Linear Kalman Filter Animation](assets/kalman_filter_animation.gif)

*図: 線形カルマンフィルタによる1次元ロボットの位置推定。緑線が真の位置、赤×が観測値、青線がカルマンフィルタの推定値、青色の帯が推定の不確実性（±2σ）を示す。*

## 拡張カルマンフィルタ (2D Robot)

2次元平面を移動するロボットの位置と姿勢を推定します。

**シミュレーション設定:**
- 制御入力: $v = 1.0$ m/s, $\omega = 0.2$ rad/s（円弧運動）
- プロセスノイズ: $\sigma_{w,x} = \sigma_{w,y} = 0.05$ m, $\sigma_{w,\theta} = 0.02$ rad
- 観測ノイズ: $\sigma_{v,x} = \sigma_{v,y} = 0.3$ m, $\sigma_{v,\theta} = 0.1$ rad

![Extended Kalman Filter Animation](assets/ekf_2d_animation.gif)

*図: 拡張カルマンフィルタによる2次元ロボットの軌跡推定。緑線が真の軌跡、赤×が観測値、青線がEKFの推定軌跡を示す。*

## 動作確認済み環境

- Ubuntu 22.04, 24.04
- Python 3.9, 3.10, 3.11, 3.12, 3.13

## 環境構築

```bash
# conda環境の作成
conda create -n kalman python=3.11

# 環境の有効化
conda activate kalman

# パッケージのインストール
pip install -r requirements.txt
```

## 実行方法

```bash
# 線形カルマンフィルタ
python examples/01_linear_example.py
python examples/02_animation_example.py

# 拡張カルマンフィルタ
python examples_2d/01_nonlinear_example.py
python examples_2d/02_animation_example.py
```

## 参考文献

- [上田先生が開講された確率ロボティクスの授業](https://github.com/ryuichiueda/slides_marp/tree/master/prob_robotics_2025)
