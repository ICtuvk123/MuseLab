"""Fixed v0 scope: 4 bars of 4/4 drums, 16 steps/bar, nine drum classes."""
from __future__ import annotations
from turtle import shape
N_TRACKS = 9
STEPS_PER_BEAT = 4
BEATS_PER_BAR = 4
BARS = 4
STEPS = STEPS_PER_BEAT * BEATS_PER_BAR * BARS
# Group -> GM drum pitch for export. Each incoming GM pitch maps to one group.
DRUM_GROUPS = (
"kick", "snare", "clap", "closed_hat", "open_hat",
"low_tom", "mid_tom", "high_tom", "cymbal",
)
REPRESENTATIVE_PITCHES = (36, 38, 39, 42, 46, 45, 47, 50, 49)
PITCH_GROUPS = {
35: 0, 36: 0,
37: 1, 38: 1, 40: 1,
39: 2,
22: 3, 42: 3, 44: 3,
26: 4, 46: 4,
41: 5, 43: 5, 58: 5,
45: 6, 47: 6,
48: 7, 50: 7,
49: 8, 51: 8, 52: 8, 53: 8, 55: 8, 57: 8, 59: 8,
}
def check_roll_shape(shape: tuple[int, ...]) -> None:
    if shape != (N_TRACKS, STEPS):
        raise ValueError(f"Expected {(N_TRACKS, STEPS)}, got {shape}")