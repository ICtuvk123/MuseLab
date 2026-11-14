import numpy as np
import pretty_midi
from muselab.config import PITCH_GROUPS
from muselab.data.symbolic import midi_to_roll, roll_to_midi

def test_midi_quantization():
    pm = pretty_midi.PrettyMIDI(initial_tempo=120)
    drum = pretty_midi.Instrument(program=0, is_drum=True)
    drum.notes.append(pretty_midi.Note(velocity=100, pitch=36, start=0.0, end=0.1))  # Kick at step 0
    drum.notes.append(pretty_midi.Note(velocity=100, pitch=38, start=0.125, end=0.225))  # Snare at step 1
    pm.instruments.append(drum)
    roll = midi_to_roll(pm, bpm=120)
    assert roll.shape == (9, 64)
    assert roll[0, 0] == 1  # Kick
    assert roll[1, 1] == 1  # Snare     
    assert np.isin(roll[2:, :], -1).all()  # Other tracks should be -1

def test_midi_roundtrip_event_positions():
    x = np.full((9, 64), -1, dtype=np.float32)
    x[0,[0, 8, 16, 24]] = 1  # Kick on every bar
    x[1,[4, 12, 20, 28]] = 1  # Snare on every bar
    midi = roll_to_midi(x, bpm=120)
    roll = midi_to_roll(midi, bpm=120)
    assert np.array_equal(x, roll)  # Roundtrip should preserve the pattern 
    assert midi.instruments[0].is_drum
    assert all(note.pitch in PITCH_GROUPS for note in midi.instruments[0].notes)  # All pitches should be valid
    assert all(note.start >= 0 for note in midi.instruments[0].notes)  # All notes should have non-negative start times
    recovered_roll = midi_to_roll(midi, bpm=120)
    assert np.array_equal(x, recovered_roll)  # Roundtrip should preserve the pattern

def test_clip_offset_and_unmapped_pitches():
    pm = pretty_midi.PrettyMIDI(initial_tempo=120)
    drum = pretty_midi.Instrument(program=0, is_drum=True)
    drum.notes.append(pretty_midi.Note(velocity=100, pitch=36, start=0.0, end=0.1))  # Kick at step 0
    drum.notes.append(pretty_midi.Note(velocity=100, pitch=38, start=0.125, end=0.225))  # Snare at step 1
    drum.notes.append(pretty_midi.Note(velocity=100, pitch=60, start=0.25, end=0.35))  # Unmapped pitch
    pm.instruments.append(drum)
    roll = midi_to_roll(pm, bpm=120, start_step=1)  # Start from step 1
    assert roll.shape == (9, 64)
    assert roll[0, 0] == -1  # Kick should be out of range
    assert roll[1, 0] == 1 # Snare should be out of range
    assert np.isin(roll[2:, :], -1).all()  # Other tracks should be -1