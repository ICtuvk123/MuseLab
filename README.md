# MuseLab
From-zero symbolic drum generation with DDPM and Flow Matching.
## Reproduce
1. Create Python venv.
2. `python -m pip install -e '.[dev]'`
3. Run `python -m pytest -q` after implementing the TODOs.
## Contract
- Shape: [9,64], dtype float32, bipolar values {-1,+1}
- Four 4/4 bars, 16 steps per bar, constant BPM
- Real MIDI is required for evaluating musical quality