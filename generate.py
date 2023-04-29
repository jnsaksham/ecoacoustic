import numpy as np
import audiomentations
import librosa
import os, glob
from util import *
import soundfile as sf

"""
T = 40: Start inserting animals at 40s for 30s. Build a track selector. Add one track every 3s
T = 70: Start inserting humans for 30s. Use the above track selector - Use acoustic scenes
T = 100: Start inserting machines for 30s. Use the above track selector
T = 130: Loop first 25% for 4 beat durations. 3s x 4 = 12s
T = 142: Loop 50% of the ongoing samples for 4 beat durations. 3s x 4 = 12s
T = 154: Loop 75% of the ongoing samples for 4 beat durations. 3s x 4 = 12s
T = 166: Loop 100% of the ongoing samples for 4 beat durations. 3s x 4 = 12s
T = 178: Drop 20% of the ongoing samples for 4 beat durations. 3s x 4 = 12s
T = 190: Drop 20% of the ongoing samples for 4 beat durations. 3s x 4 = 12s
T = 202: Drop 20% of the ongoing samples for 4 beat durations. 3s x 4 = 12s
T = 214: Drop 20% of the ongoing samples for 4 beat durations. 3s x 4 = 12s
T = 226: Drop 20% of the ongoing samples for 4 beat durations. 3s x 4 = 12s

"""


backgrounds = ['airport', 'bus', 'metro', 'park']
bg = backgrounds[1]

files = glob.glob(f'./{bg}/*.wav')
f_index = 2

fname = files[f_index]

fname = 'ESC-50-master/audio/1-1791-A-26.wav'


# Define song parameters
tempo = 80
beat_duration = 60/tempo
trim_durations = [beat_duration, beat_duration*2, beat_duration*4, beat_duration*8, beat_duration*16, beat_duration*0.5, beat_duration*0.25]

sounds = get_soundTypes_esc()
# print (sounds)

bg_sound_types = ['rain', 'chirping_birds', 'crackling_fire', 'pouring_water', 'insects', 'clock_tick', 'wind']
animals_sound_types = ['cat', 'breathing', 'frog', 'dog', 'crickets', 'hen', 'sheep']
human_sound_types = ['footsteps', 'laughing', 'sneezing', 'clapping', 'coughing', 'brushing_teeth', 'drinking_sipping']
machine_sound_types = ['helicopter', 'car_horn', 'engine', 'airplane', 'washing_machine', 'train', 'keyboard_typing', 'can_opening']

t_start_animals = 40
t_start_humans = 70
t_start_machines = 100
t_loop_1 = 130
t_loop_2 = int(t_loop_1 + 4*beat_duration*12)
t_loop_3 = int(t_loop_2 + 4*beat_duration*12)
t_loop_4 = int(t_loop_3 + 4*beat_duration*12)
t_loop_5 = int(t_loop_4 + 4*beat_duration*12)
t_loop_6 = int(t_loop_5 + 4*beat_duration*12)

if __name__ == '__main__':
    # Import background track
    audio, sample_rate = read_audio('bg.wav')
    song_duration = len(audio)/sample_rate # Song duration in seconds
    timePerTrack = 3 # Time in seconds between triggering each track
    
    audio = add_tracks(audio, t_start_animals, t_start_humans, timePerTrack, animals_sound_types, sample_rate, tempo, trim_durations[3])
    audio = add_tracks(audio, t_start_humans, t_start_machines, timePerTrack, human_sound_types, sample_rate, tempo, trim_durations[3])
    audio = add_tracks(audio, t_start_machines, t_loop_1, timePerTrack, machine_sound_types, sample_rate, tempo, trim_durations[3])
    
    # audio = loop_final_audio(t_loop_1, sample_rate, trim_durations, audio, 3)
    audio = loop_final_audio(t_loop_2, sample_rate, trim_durations, audio, 2)
    audio = loop_final_audio(t_loop_3, sample_rate, trim_durations, audio, 1)
    audio = loop_final_audio(t_loop_4, sample_rate, trim_durations, audio, 0)
    audio = loop_final_audio(t_loop_4, sample_rate, trim_durations, audio, -2)
    audio = loop_final_audio(t_loop_4, sample_rate, trim_durations, audio, -1)

    sf.write(f'output/looped_final.wav', audio, sample_rate)