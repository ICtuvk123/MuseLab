from pathlib import path
import numpy as np
import pretty_midi
from muselab.data.symbolic import roll_to_midi, midi_to_roll

x = np.full((9, 64), -1, dtype=np.float32)
for bar in range(4):
    offset = 16 * bar
    x[0, [offset, offset + 8]] = +1
    x[1, [offset + 4, offset + 12]] = +1
    x[3, offset : offset + 16 : 2] = +1
out = Path("runs/manual.mid")
out.parent.mkdir(parents=True, exist_ok=True)
roll_to_midi(x, bpm=120).write(str(out))
recovered = midi_to_roll(pretty_midi.PrettyMIDI(str(out)), 120)
print(out, np.array_equal(recovered, x))
