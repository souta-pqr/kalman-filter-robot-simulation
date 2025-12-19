import os
import sys

import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.extended_kf import ExtendedKalmanFilter
from src.robot_2d_simulator import Robot2D
from src.visualizer_2d import plot_with_estimates


def main():
    np.random.seed(42)

    robot = Robot2D(
        initial_state=[0.0, 0.0, 0.0],
        process_noise_std=[0.05, 0.05, 0.02],
        observation_noise_std=[0.3, 0.3, 0.1],
        dt=1.0,
    )

    # EKF初期化
    Q = np.diag([0.05**2, 0.05**2, 0.02**2])
    R = np.diag([0.3**2, 0.3**2, 0.1**2])
    x0 = np.array([0.0, 0.0, 0.0])
    P0 = np.diag([1.0, 1.0, 1.0])

    ekf = ExtendedKalmanFilter(Q=Q, R=R, x0=x0, P0=P0, dt=1.0)

    v = 1.0  # 前進速度 1 m/s
    omega = 0.2  # 角速度 0.2 rad/s

    print(f"Control: v={v} m/s, omega={omega} rad/s")

    estimates = [ekf.x.copy()]

    for t in range(30):
        robot.move([v, omega])
        obs = robot.observation_history[t + 1]
        est, K = ekf.filter_step(z=obs, u=[v, omega])
        estimates.append(est.copy())

    # プロット
    states = np.array(robot.state_history)
    observations = np.array(robot.observation_history)
    estimates = np.array(estimates)

    plot_with_estimates(states, observations, estimates, title="EKF Estimation")


if __name__ == "__main__":
    main()
