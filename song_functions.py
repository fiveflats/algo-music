import pandas as pd
import numpy as np

class song:
    def __init__(self, time, melody, changes):
        self.time = time
        self.melody = melody
        self.changes = changes

        total_beats = sum(melody[i][1] for i in range(len(melody))) + 1

        map_measure = []
        measure_beat = []

        for i in range(len(melody) - 1, -1, -1):
            total_beats = total_beats - melody[i][1]
            msr = int((total_beats - 1) / time) + 1
            map_measure.append(msr)
            measure_beat.append(total_beats - (msr - 1) * time)

        map_measure.reverse()
        measure_beat.reverse()

        self.map_measure = map_measure
        self.measure_beat = measure_beat


class chromatic_data:
    triads = {'maj': (0, 4, 7), 'min': (0, 3, 7)}
    maj_scale = {1: 1, 2: 3, 3: 5, 4: 6, 5: 8, 6: 10, 7: 12}

    def __init__(self):
        self.triads = triads
        self.maj_scale = maj_scale


class beats_data:
    def __init__(self, time):
        self.beats = [i + 1 for i in range(time)]


def chords_by_measure(changes):
    chrom = chromatic_data
    chord_array = []
    chrom_note_index = []
    for j in range(len(changes)):
        chrom_note_index.append(changes[j][0])
        chrom_note_row = []
        chord = []
        chrom_note_col = []

        for i in range(len(chrom.triads[changes[0][2]])):
            note = chrom.maj_scale[changes[j][1]] + chrom.triads[changes[j][2]][i]
            if note > 12:
                note = note - 12
            chord.append(note)

        for m in range(12):
            chrom_note_row.append(((m + 1) in set(chord)) * 1)
            col_label = "chord_note" + str(m + 1)
            chrom_note_col.append(col_label)

        chord_array.append(tuple(chrom_note_row))

    result = pd.DataFrame(chord_array, index=chrom_note_index, columns=chrom_note_col)
    result.index.name = "measure"

    return result


def melody_notes(melody):
    chrom = chromatic_data
    melody_array = []
    for j in range(len(melody)):
        chrom_note_row = []
        chrom_note_col = []

        note = chrom.maj_scale[melody[j][0]]

        for m in range(12):
            chrom_note_row.append(((m + 1) == note) * 1)
            col_label = "melody_note" + str(m + 1)
            chrom_note_col.append(col_label)

        melody_array.append(tuple(chrom_note_row))

    result = pd.DataFrame(melody_array, columns=chrom_note_col)
    result.index.name = "note_index"

    return result


def melody_lengths(melody):
    length_array = []

    for j in range(len(melody)):
        length_array.append(melody[j][1])

    result = pd.DataFrame(length_array, columns=["note_length"])
    result.index.name = "note_index"

    return result


def on_beats(time, measure_beat):
    beats = beats_data(time)
    on_beat_array = []
    for j in range(len(measure_beat)):
        beat_row = []
        beat_col = []

        for m in range(len(beats.beats)):
            beat_row.append((beats.beats[m] == measure_beat[j]) * 1)
            col_label = "on_beat" + str(m + 1)
            beat_col.append(col_label)

        on_beat_array.append(tuple(beat_row))

    result = pd.DataFrame(on_beat_array, columns=beat_col)
    result.index.name = "note_index"

    return result


def measure_to_melody(map_measure):
    result = pd.DataFrame(map_measure, columns=["measure"])
    result.index.name = "note_index"
    return result


def analysis_data(class_instance):
    notes = melody_notes(class_instance.melody)
    #    on_beat = on_beats(class_instance.time,class_instance.measure_beat)
    length = melody_lengths(class_instance.melody)
    measure_map = measure_to_melody(class_instance.map_measure)
    changes = chords_by_measure(class_instance.changes)

    result = pd.concat([notes, measure_map], axis=1, join='inner', join_axes=[notes.index])
    result = pd.merge(result, changes, right_index=True, left_on='measure')
    result.set_index(['measure'], append=True, inplace=True)

    result = result.multiply(length["note_length"].pow(0.5), axis=0, level="note_index")

    ones = [[1] * len(result.index.levels[0])]
    df_ones = pd.DataFrame(ones[0], index=result.index, columns=["constant"])
    result = pd.concat([result, df_ones], axis=1)

    return result