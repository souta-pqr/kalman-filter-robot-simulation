import os
import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

# パスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.linear_kf import LinearKalmanFilter
from src.robot_simulator import Robot1D


def main():

    # 乱数シード
    np.random.seed(42)

    # ロボットとカルマンフィルタの初期化
    process_noise = 0.1
    observation_noise = 0.5
    robot = Robot1D(
        initial_position=0.0,
        process_noise_std=process_noise,
        observation_noise_std=observation_noise,
    )

    Q = process_noise**2
    R = observation_noise**2
    kf = LinearKalmanFilter(Q=Q, R=R, x0=0.0, P0=1.0)

    print(f"Process Noise Q: {Q:.4f}")
    print(f"Observation Noise R: {R:.2f}")

    # データ保存
    true_positions = [robot.get_position()]
    observations = [robot.observe()]
    estimates = [kf.x]
    kalman_gains = []
    uncertainties = [kf.P]

    n_steps = 30

    # シミュレーション実行（データを事前生成）
    for step in range(1, n_steps + 1):
        true_pos = robot.move(distance=1.0)
        obs = robot.observe()
        estimate, K = kf.filter_step(z=obs, u=1.0)

        true_positions.append(true_pos)
        observations.append(obs)
        estimates.append(estimate)
        kalman_gains.append(K)
        uncertainties.append(kf.P)

    # アニメーション設定
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # 初期化
    (line_true,) = ax1.plot([], [], "g-", linewidth=2, label="True Position")
    (line_obs,) = ax1.plot([], [], "rx", markersize=8, alpha=0.6, label="Observations")
    (line_est,) = ax1.plot([], [], "b-", linewidth=2, label="Kalman Estimate")
    # fill_uncertainty = ax1.fill_between([], [], [], alpha=0.3, color="blue", label="Uncertainty")
    (robot_marker,) = ax1.plot([], [], "go", markersize=12, label="Robot")

    ax1.set_xlim(0, n_steps)
    ax1.set_ylim(-2, n_steps + 2)
    ax1.set_xlabel("Time Step", fontsize=12)
    ax1.set_ylabel("Position (m)", fontsize=12)
    ax1.set_title("Kalman Filter: Robot Position Estimation", fontsize=14, fontweight="bold")
    ax1.legend(loc="upper left", fontsize=10)
    ax1.grid(True, alpha=0.3)

    # カルマンゲイン
    (line_gain,) = ax2.plot([], [], "r-", linewidth=2, marker="o")
    ax2.set_xlim(0, n_steps)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel("Time Step", fontsize=12)
    ax2.set_ylabel("Kalman Gain", fontsize=12)
    ax2.set_title("Kalman Gain Evolution", fontsize=14, fontweight="bold")
    ax2.grid(True, alpha=0.3)

    # ステップ表示用テキスト
    step_text = ax1.text(
        0.98,
        0.95,
        "",
        transform=ax1.transAxes,
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
        line_gain.set_data([], [])
        step_text.set_text("")
        return line_true, line_obs, line_est, robot_marker, line_gain, step_text

    def animate(frame):
        # データ更新
        steps = list(range(frame + 1))

        # 真の位置
        line_true.set_data(steps, true_positions[: frame + 1])

        # 観測値
        line_obs.set_data(steps, observations[: frame + 1])

        # 推定値
        line_est.set_data(steps, estimates[: frame + 1])

        # 不確実性（信頼区間）
        if frame > 0:

            for coll in list(ax1.collections):
                coll.remove()
            std = np.sqrt(uncertainties[frame])
            ax1.fill_between(
                steps,
                np.array(estimates[: frame + 1]) - 2 * std,
                np.array(estimates[: frame + 1]) + 2 * std,
                alpha=0.3,
                color="blue",
            )

        # ロボットの現在位置
        robot_marker.set_data([frame], [true_positions[frame]])

        # カルマンゲイン
        if frame > 0:
            gain_steps = list(range(1, frame + 1))
            line_gain.set_data(gain_steps, kalman_gains[:frame])

        # ステップ情報
        if frame > 0:
            error = abs(true_positions[frame] - estimates[frame])
            step_text.set_text(
                f"Step: {frame}\n"
                f"True: {true_positions[frame]:.2f}m\n"
                f"Obs: {observations[frame]:.2f}m\n"
                f"Est: {estimates[frame]:.2f}m\n"
                f"Error: {error:.2f}m\n"
                f"K: {kalman_gains[frame-1]:.3f}"
            )
        else:
            step_text.set_text(f"Step: {frame}\nInitial Position: {true_positions[0]:.2f}m")

        return line_true, line_obs, line_est, robot_marker, line_gain, step_text

    # アニメーション作成
    anim = animation.FuncAnimation(
        fig,
        animate,
        init_func=init,
        frames=len(true_positions),
        interval=500,  # 500ms = 0.5秒
        blit=True,
        repeat=True,
    )

    plt.tight_layout()

    # GIFとして保存
    output_path = "kalman_filter_animation.gif"
    try:
        anim.save(output_path, writer="pillow", fps=2, dpi=100)
    except Exception as e:
        print(f"Failed to save animation: {e}")

    plt.show()


if __name__ == "__main__":
    main()
