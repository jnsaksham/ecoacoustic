import numpy as np
import librosa
import os, glob
import pandas as pd


def read_audio(fname):
    audio, sample_rate = librosa.load(fname, sr=44100)
    return audio, sample_rate

def trim_audio(audio, sample_rate, tempo, numBeats):
    samplesPerBeat = 60/tempo*sample_rate
    numSamples = int(numBeats*samplesPerBeat)

    endPt = len(audio)-numSamples

    # Select a random number between 1 and 5000
    start = int(np.random.randint(1,endPt))

    return audio[start:start+numSamples]

def loop_audio(chunk, numLoops):
    final_audio = []
    for i in range(numLoops):
        final_audio.extend(chunk)
    return final_audio

def extend_samples_audio(audio, final_block_length):
    # FInal block length is in samples
    length_audio = len(audio)
    numLoops = int(final_block_length//length_audio)
    final_audio = loop_audio(audio, numLoops)
    length_audio = len(final_audio)
    final_audio.extend(audio[:final_block_length-length_audio])
    return final_audio

def get_soundTypes_esc():
    df = pd.read_csv('ESC-50-master/meta/esc50.csv')
    return df['category'].unique()

# Write a function that returns all the filenames for a given sound type
def get_filenames_esc(sound_type):
    df = pd.read_csv('ESC-50-master/meta/esc50.csv')
    return df[df['category'] == sound_type]['filename'].values

def get_track_names(sound_types):
    filenames = []
    for sound_type in sound_types:
        filenames.extend(get_filenames_esc(sound_type))
    return filenames

def select_track(filenames):
    # Select a random index from the list
    index = np.random.randint(0,len(filenames))
    trackname = filenames[index]
    # Remove trackname from filenames
    filenames.remove(trackname)
    return trackname, filenames

def randomize_gain(audio):
    # Randomize gain between 0.5 and 1.5
    gain = np.random.uniform(0.1,0.9)
    return audio*gain

# def apply_band_pass_filter(audio, sample_rate, lowcut, highcut):
#     # Apply band pass filter
#     audio = butter_bandpass_filter(audio, lowcut, highcut, sample_rate, order=5)
#     return audio

# Write a function that adds tracks corresponding to input sound types to the background track. Add one track every 3s from the mentioned sample number
def add_tracks(bg_track, t_start, t_end, timePerTrack, sound_types, sample_rate, tempo, numBeats):
    pin = t_start*sample_rate
    pend = t_end*sample_rate
    # Get all fnames corresponding to sound_types
    
    while pin < pend:
        tracknames = get_track_names(sound_types)
        trackname, tracknames = select_track(tracknames)
        audio, sample_rate = read_audio(f'ESC-50-master/audio/{trackname}')
        audio = randomize_gain(audio)
        trimmed_audio = trim_audio(audio, sample_rate, tempo, numBeats)
        final_block_length = len(bg_track)-pin
        extended_audio = extend_samples_audio(trimmed_audio, final_block_length)
        bg_track[pin:] += extended_audio
        pin += timePerTrack*sample_rate
    return bg_track

def apply_looping_algorithm(audio, t_start, t_end, loop_duration, sample_rate, tempo):
    chunk = audio[t_start:t_end]
    numBeats = loop_duration/60*tempo
    trimmed_chunk = trim_audio(chunk, sample_rate, tempo, numBeats)
    final_block_length = len(chunk)
    extended_chunk = extend_samples_audio(trimmed_chunk, final_block_length)
    audio[t_start:t_end] = extended_chunk
    return audio

def loop_final_audio(t_loop, sample_rate, trim_durations, audio, beat_dur_index):
    loop_start_sample = int(t_loop*sample_rate)
    loop_duration = trim_durations[beat_dur_index]
    loop_end_sample = int(loop_start_sample + loop_duration*sample_rate)
    loop = audio[int(loop_start_sample):int(loop_end_sample)]
    remaining_song_length = int(len(audio)-loop_start_sample)
    # extend loop_1 to remaining_song length
    loop = extend_samples_audio(loop, remaining_song_length)
    audio[loop_start_sample:] = loop
    return audio