"""BIG ASSIGNMENT: implement MIDI <-> piano-roll conversion.
Representation: float32 array [9, 64] with -1 for silence and +1 for a hit.
The first axis is nine grouped GM percussion instruments; the second is a
16th-note grid across four bars of 4/4 at a constant BPM.
"""

from __future__ import annotations
import numpy as np
import pretty_midi
from muselab.config import (
    N_TRACKS,
    STEPS,
    PITCH_GROUPS,
    REPRESENTATIVE_PITCHES,
    check_roll_shape,
)


def midi_to_roll(
    midi: pretty_midi.PrettyMIDI, bpm: float, start_step: int = 0
) -> np.ndarray:
    """Return a bipolar [9,64] roll for the given global step offset.
    Quantize note-on times using 16th-note step seconds = 60/bpm/4.
    Map drum pitches to classes in config.PITCH_GROUPS; ignore unsupported
    pitches and non-drum instruments. Handle out-of-range events safely.
    Args:
    midi: parsed MIDI file.
    bpm: positive constant tempo in quarter-note beats per minute.
    start_step: zero-based first step of the 4-bar clip.
    """
    pattern = np.full((N_TRACKS, STEPS), -1, dtype=np.float32)
    for note in midi.instruments[0].notes:
        step = int((note.start - start_step * 60 / bpm / 4) * bpm * 4 / 60)
        if step < 0 or step >= STEPS:
            continue
        group = PITCH_GROUPS.get(note.pitch)
        if group is not None:
            pattern[group, step] = 1
    return pattern


def roll_to_midi(
    roll: np.ndarray, bpm: float, velocity: int = 100
) -> pretty_midi.PrettyMIDI:
    """Return a drum-only PrettyMIDI object for a [9,64] bipolar roll.
    A cell > 0 means hit. Use config.REPRESENTATIVE_PITCHES for output pitch;
    16th-note grid, constant BPM and short nonzero note durations.
    """
    check_roll_shape(roll.shape)
    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    drum = pretty_midi.Instrument(program=0, is_drum=True)
    midi.instruments.append(drum)
    for group in range(N_TRACKS):
        for step in range(STEPS):
            if roll[group, step] > 0:
                start = step * 60 / bpm / 4
                end = start + 0.05
                pitch = REPRESENTATIVE_PITCHES[group]
                note = pretty_midi.Note(
                    velocity=velocity, pitch=pitch, start=start, end=end
                )
                drum.notes.append(note)

    return midi