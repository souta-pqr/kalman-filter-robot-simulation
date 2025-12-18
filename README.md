# Kalman Filter Robot Simulation

カルマンフィルタを使ったロボットシミュレーション

## 線形カルマンフィルタ (1D Robot)

1次元ロボットの位置推定

![Linear Kalman Filter Animation](assets/kalman_filter_animation.gif)

## 拡張カルマンフィルタ (2D Robot)

2次元ロボットの位置・姿勢推定

![Extended Kalman Filter Animation](assets/ekf_2d_animation.gif)

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

- [確率ロボティクス2025](https://github.com/ryuichiueda/slides_marp/tree/master/prob_robotics_2025)
