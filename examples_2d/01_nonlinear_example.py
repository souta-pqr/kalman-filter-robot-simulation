import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.robot_2d_simulator import Robot2D
from src.visualizer_2d import plot_trajectory


def main():
    np.random.seed(42)

    robot = Robot2D(
        initial_state=[0.0, 0.0, 0.0],
        process_noise_std=[0.0, 0.0, 0.0],
        observation_noise_std=[0.0, 0.0, 0.0],
        dt=1.0
    )
    
    v = 1.0  # 前進速度 1 m/s
    omega = 0.2  # 角速度 0.2 rad/s
    
    print("2D Robot Motion (No Noise)")
    print(f"Control: v={v} m/s, omega={omega} rad/s")
    print()
    
    for t in range(30):
        robot.move([v, omega])
    
    # プロット
    states = np.array(robot.state_history)
    plot_trajectory(states, title="Robot Trajectory")


if __name__ == "__main__":
    main()
