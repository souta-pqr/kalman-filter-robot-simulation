"""Tests for Linear Kalman Filter"""
import sys
from pathlib import Path

import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from linear_kf import LinearKalmanFilter


def test_initialization():
    """Test Kalman filter initialization"""
    kf = LinearKalmanFilter(Q=0.01, R=0.25, x0=0.0, P0=1.0)
    assert kf.x == 0.0
    assert kf.P == 1.0
    assert kf.Q == 0.01
    assert kf.R == 0.25


def test_predict():
    """Test prediction step"""
    kf = LinearKalmanFilter(Q=0.01, R=0.25, x0=0.0, P0=1.0)
    kf.predict(u=1.0)
    assert kf.x == 1.0
    assert kf.P == 1.01  # P0 + Q


def test_update():
    """Test update step"""
    kf = LinearKalmanFilter(Q=0.01, R=0.25, x0=0.0, P0=1.0)
    K = kf.update(z=1.0)
    
    # Kalman gain should be between 0 and 1
    assert 0 <= K <= 1
    # Uncertainty should be reduced after update
    assert kf.P < 1.0
    # State should move towards observation
    assert 0 < kf.x < 1.0


def test_filter_step():
    """Test complete filter step (predict + update)"""
    kf = LinearKalmanFilter(Q=0.01, R=0.25, x0=0.0, P0=1.0)
    x, P = kf.filter_step(z=1.0, u=1.0)
    
    assert isinstance(x, float)
    assert isinstance(P, float)
    assert P >= 0
    assert P >= 0


def test_multiple_steps():
    """Test multiple filter iterations"""
    kf = LinearKalmanFilter(Q=0.01, R=0.25, x0=0.0, P0=1.0)
    
    for i in range(100):
        kf.predict(u=1.0)
        K = kf.update(z=i + 1.0 + np.random.randn() * 0.5)
        
        # Kalman gain should remain valid
        assert 0 <= K <= 1
        # Uncertainty should remain positive
        assert kf.P >= 0
