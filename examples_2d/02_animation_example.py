import os
import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.extended_kf import ExtendedKalmanFilter
from src.robot_2d_simulator import Robot2D


def main():
    np.random.seed(42)

    robot = Robot2D(
        initial_state=[0.0, 0.0, 0.0],
        process_noise_std=[0.05, 0.05, 0.02],
        observation_noise_std=[0.3, 0.3, 0.1],
        dt=1.0,
    )

    Q = np.diag([0.05**2, 0.05**2, 0.02**2])
    R = np.diag([0.3**2, 0.3**2, 0.1**2])
    x0 = np.array([0.0, 0.0, 0.0])
    P0 = np.diag([1.0, 1.0, 1.0])

    ekf = ExtendedKalmanFilter(Q=Q, R=R, x0=x0, P0=P0, dt=1.0)

    v = 1.0
    omega = 0.2

    print(f"Process Noise Q: diag([{Q[0,0]:.6f}, {Q[1,1]:.6f}, {Q[2,2]:.6f}])")
    print(f"Observation Noise R: diag([{R[0,0]:.2f}, {R[1,1]:.2f}, {R[2,2]:.2f}])")

    # データ事前生成
    true_positions = [robot.get_state()]
    observations = [robot.observation_history[0]]
    estimates = [ekf.x.copy()]

    n_steps = 30

    for step in range(n_steps):
        robot.move([v, omega])
        obs = robot.observation_history[step + 1]
        est, K = ekf.filter_step(z=obs, u=[v, omega])

        true_positions.append(robot.get_state())
        observations.append(obs)
        estimates.append(est.copy())

    # アニメーション設定
    fig, ax = plt.subplots(figsize=(10, 10))

    (line_true,) = ax.plot([], [], "g-", linewidth=2.5, label="True Path")
    (line_obs,) = ax.plot([], [], "rx", markersize=8, alpha=0.6, label="Observations")
    (line_est,) = ax.plot([], [], "b-", linewidth=2, label="EKF Estimate")
    (robot_marker,) = ax.plot([], [], "go", markersize=12, label="Robot")

    ax.set_xlim(-7, 7)
    ax.set_ylim(-2, 12)
    ax.set_xlabel("X Position (m)", fontsize=12)
    ax.set_ylabel("Y Position (m)", fontsize=12)
    ax.set_title("EKF: 2D Robot Localization", fontsize=14, fontweight="bold")
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal")

    step_text = ax.text(
        0.98,
        0.95,
        "",
        transform=ax.transAxes,
        fontsize=11,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )

    def init():
        line_true.set_data([], [])
        line_obs.set_data([], [])
        line_est.set_data([], [])
        robot_marker.set_data([], [])
        step_text.set_text("")
        return line_true, line_obs, line_est, robot_marker, step_text

    def animate(frame):
        true_arr = np.array(true_positions[: frame + 1])
        obs_arr = np.array(observations[: frame + 1])
        est_arr = np.array(estimates[: frame + 1])

        line_true.set_data(true_arr[:, 0], true_arr[:, 1])
        line_obs.set_data(obs_arr[:, 0], obs_arr[:, 1])
        line_est.set_data(est_arr[:, 0], est_arr[:, 1])

        robot_marker.set_data([true_positions[frame][0]], [true_positions[frame][1]])

        if frame > 0:
            true_pos = true_positions[frame]
            est_pos = estimates[frame]
            error = np.sqrt((true_pos[0] - est_pos[0]) ** 2 + (true_pos[1] - est_pos[1]) ** 2)
            step_text.set_text(
                f"Step: {frame}\n"
                f"True: ({true_pos[0]:.2f}, {true_pos[1]:.2f})\n"
                f"Est: ({est_pos[0]:.2f}, {est_pos[1]:.2f})\n"
                f"Error: {error:.2f}m"
            )
        else:
            step_text.set_text(f"Step: {frame}\nInitial Position")

        return line_true, line_obs, line_est, robot_marker, step_text

    anim = animation.FuncAnimation(
        fig,
        animate,
        init_func=init,
        frames=len(true_positions),
        interval=500,
        blit=True,
        repeat=True,
    )

    plt.tight_layout()

    # GIF保存
    output_path = "ekf_2d_animation.gif"
    print(f"Saving animation as {output_path}...")
    try:
        anim.save(output_path, writer="pillow", fps=2, dpi=100)
        print(f"Animation saved successfully to {output_path}")
    except Exception as e:
        print(f"Failed to save animation: {e}")
        print("Note: You may need to install Pillow: pip install Pillow")

    plt.show()


if __name__ == "__main__":
    main()
