from dataclasses import dataclass

@dataclass
class ScoreConfig:
    # filtering
    min_conf: float = 0.50
    max_gap_frames_to_interp: int = 5  

    # smoothing
    sg_window: int = 15   
    sg_poly: int = 3

    # reversal detection
    vx_deadband_px_s = 40.0
    min_reversal_separation_s = 0.05
    
    # weighted averages
    w_speed: float = 45
    w_reversals: float = 20
    w_smoothness: float = 15
    w_tightness: float = 5
    w_rhythm: float = 15