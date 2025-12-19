import os
import sys

import numpy as np

# パスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.linear_kf import LinearKalmanFilter
from src.robot_simulator import Robot1D
from src.visualizer import plot_parameter_comparison


def run_simulation(Q, R, robot, label):
    """カルマンフィルタのシミュレーションを実行"""
    kf = LinearKalmanFilter(Q=Q, R=R, x0=0.0, P0=1.0)

    estimates = [kf.x]

    for step in range(1, 11):
        obs = robot.observation_history[step]
        estimate, K = kf.filter_step(z=obs, u=1.0)
        estimates.append(estimate)

    return estimates


def main():

    # 乱数シード
    np.random.seed(42)

    # ロボットを作成（データを事前生成）
    process_noise = 0.1
    observation_noise = 0.5
    robot = Robot1D(
        initial_position=0.0,
        process_noise_std=process_noise,
        observation_noise_std=observation_noise,
    )

    # 真の位置と観測を事前生成
    robot.position_history = [0.0]
    robot.observation_history = [robot.observe()]

    for step in range(1, 11):
        true_pos = robot.move(distance=1.0)
        robot.position_history.append(true_pos)
        robot.observation_history.append(robot.observe())

    print("\nロボットの実際のノイズ:")
    print(f"  プロセスノイズ: {process_noise}")
    print(f"  観測ノイズ: {observation_noise}")

    # 3つの設定でシミュレーション
    print("\n--- 3つの設定で比較 ---\n")

    # 設定1: 正しい値
    Q1 = process_noise**2
    R1 = observation_noise**2
    estimates1 = run_simulation(Q1, R1, robot, "正しいQ,R")
    print(f"設定1: Q={Q1:.4f}, R={R1:.2f}")
    errors1 = [abs(t - e) for t, e in zip(robot.position_history[1:], estimates1[1:])]
    print(f"  平均誤差: {np.mean(errors1):.3f}m\n")

    # 設定2: Qを大きく（動きが不確実と仮定）
    Q2 = 0.1
    R2 = observation_noise**2
    estimates2 = run_simulation(Q2, R2, robot, "大きいQ")
    print(f"設定2: Q={Q2:.4f}, R={R2:.2f}")
    errors2 = [abs(t - e) for t, e in zip(robot.position_history[1:], estimates2[1:])]
    print(f"  平均誤差: {np.mean(errors2):.3f}m\n")

    # 設定3: Qを小さく（動きが確実と仮定）
    Q3 = 0.001
    R3 = observation_noise**2
    estimates3 = run_simulation(Q3, R3, robot, "小さいQ")
    print(f"設定3: Q={Q3:.4f}, R={R3:.2f}")
    errors3 = [abs(t - e) for t, e in zip(robot.position_history[1:], estimates3[1:])]
    print(f"  平均誤差: {np.mean(errors3):.3f}m\n")

    print("\n--- 結果 ---")
    print(f"設定1の誤差: {np.mean(errors1):.3f}m")
    print(f"設定2の誤差: {np.mean(errors2):.3f}m")
    print(f"設定3の誤差: {np.mean(errors3):.3f}m")

    # グラフ表示
    print("\nグラフを表示中...")
    estimates_dict = {
        "Correct Q,R": (estimates1, np.mean(errors1)),
        "Large Q": (estimates2, np.mean(errors2)),
        "Small Q": (estimates3, np.mean(errors3)),
    }
    plot_parameter_comparison(robot.position_history, robot.observation_history, estimates_dict)


if __name__ == "__main__":
    main()
