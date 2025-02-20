from mido import MidiFile, MidiTrack, Message, MetaMessage
import sys

# Create a MIDI file
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Set tempo (140 BPM = 428571 microseconds per beat)
track.append(Message('control_change', control=0, value=0, time=0))  # Bank select (optional)
track.append(Message('program_change', program=0, time=0))  # Piano sound
mid.ticks_per_beat = 480  # Standard resolution
track.append(MetaMessage('set_tempo', tempo=428571, time=0))  # 140 BPM

# Note to MIDI number mapping
note_map = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
time = 0

# Read the tune from text file
with open('tune.txt', 'r') as f:
    for line in f:
        # Skip empty lines or lines that are purely comments
        if line.startswith('#') or not line.strip():
            continue
        # Split on comma and take only the first three parts, strip comments
        parts = line.split(',')[:3]  # Take only note, velocity, duration
        if len(parts) < 3:
            continue  # Skip malformed lines
        note = parts[0].strip()
        velocity = int(parts[1].strip())
        # Remove any inline comment after duration
        duration_str = parts[2].split('#')[0].strip()
        duration = float(duration_str) * 480  # Convert quarter notes to ticks

        pitch = note_map[note[0]] + (int(note[1]) + 1) * 12  # Convert to MIDI pitch
        track.append(Message('note_on', note=pitch, velocity=velocity, time=time))
        track.append(Message('note_off', note=pitch, velocity=0, time=int(duration)))
        time = 0  # Reset time for next note (sequential)

# Save the MIDI file
mid.save('output.mid')
print("MIDI file 'output.mid' created!")