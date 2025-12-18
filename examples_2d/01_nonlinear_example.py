import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.robot_2d_simulator import Robot2D
from src.visualizer_2d import plot_with_observations


def main():
    np.random.seed(42)

    robot = Robot2D(
        initial_state=[0.0, 0.0, 0.0],
        process_noise_std=[0.0, 0.0, 0.0],
        observation_noise_std=[0.3, 0.3, 0.1],
        dt=1.0
    )
    
    v = 1.0  # 前進速度 1 m/s
    omega = 0.2  # 角速度 0.2 rad/s
    
    print("2D Robot Motion with Observation Noise")
    print(f"Control: v={v} m/s, omega={omega} rad/s")
    print(f"Observation noise: [0.3, 0.3, 0.1]")
    print()
    
    for t in range(30):
        robot.move([v, omega])
    
    # プロット
    states = np.array(robot.state_history)
    observations = np.array(robot.observation_history)
    plot_with_observations(states, observations, title="Robot Trajectory with Observation Noise")


if __name__ == "__main__":
    main()
