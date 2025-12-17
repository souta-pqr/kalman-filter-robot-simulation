import matplotlib.pyplot as plt


def plot_position(positions, save_path=None):
    """
    ロボットの位置をプロット
    
    Parameters
    ----------
    positions : list
        位置のリスト
    save_path : str, optional
        保存先のパス
    """
    steps = range(len(positions))
    
    plt.figure(figsize=(10, 6))
    plt.plot(steps, positions, 'bo-', label='Robot Position', linewidth=2, markersize=6)
    
    plt.xlabel('Time Step')
    plt.ylabel('Position (m)')
    plt.title('1D Robot Movement')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()
    