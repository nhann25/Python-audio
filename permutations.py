from pydub import AudioSegment
import itertools


# Input audio file to be sliced
audio = AudioSegment.from_file("intothesun_noise.wav", format="wav")


#size of slices
slices = audio[::900]

iter_slice = []
for i in slices:
    iter_slice.append(i.dBFS)

permu_slice = []

permu_slice = list(itertools.permutations(iter_slice))


''' 
Step #1 - Slicing the audio file into smaller chunks. 
'''
# Length of the audiofile in milliseconds
n = len(audio)
n = 200000

# Variable to count the number of sliced chunks
counter = 1

# Text file to write the recognized audio

# Interval length at which to slice the audio file.
# If length is 22 seconds, and interval is 5 seconds,
# The chunks created will be:
# chunk1 : 0 - 5 seconds
# chunk2 : 5 - 10 seconds
# chunk3 : 10 - 15 seconds
# chunk4 : 15 - 20 seconds
# chunk5 : 20 - 22 seconds
interval = 900

# Length of audio to overlap.
# If length is 22 seconds, and interval is 5 seconds,
# With overlap as 1.5 seconds,
# The chunks created will be:
# chunk1 : 0 - 5 seconds
# chunk2 : 3.5 - 8.5 seconds
# chunk3 : 7 - 12 seconds
# chunk4 : 10.5 - 15.5 seconds
# chunk5 : 14 - 19.5 seconds
# chunk6 : 18 - 22 seconds
overlap = 100

# Initialize start and end seconds to 0
start = 0
end = 0

# Flag to keep track of end of file.
# When audio reaches its end, flag is set to 1 and we break
flag = 0

# Iterate from 0 to end of the file,
# with increment = interval
chunk_list = []
for i in range(0, 2 * n, interval):

    # During first iteration,
    # start is 0, end is the interval
    if i == 0:
        start = 0
        end = interval

    # All other iterations,
    # start is the previous end - overlap
    # end becomes end + interval
    else:
        start = end - overlap
        end = start + interval

    # When end becomes greater than the file length,
    # end is set to the file length
    # flag is set to 1 to indicate break.
    if end >= n:
        end = n
        flag = 1

    # Storing audio file from the defined start to end
    chunk_list.append(audio[start:end])

    # Increment counter for the next chunk
    counter = counter + 1


zipped_chunks = zip(chunk_list, permu_slice)

sorted_chunks = sorted(zipped_chunks, key=lambda x: x[1])

sorted_audio, sorted_numbers = zip(*sorted_chunks)

export_audio = AudioSegment.silent(duration=100)

for i in range(1, len(sorted_audio)):
    export_audio += sorted_audio[i]

#change audio output name
file_handle = export_audio.export("output33.wav", format="wav")