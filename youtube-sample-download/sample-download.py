from pytube import YouTube
from moviepy.editor import *
from pathvalidate import sanitize_filepath


# This script is supposed to make downloading samples from youtube easier
# ('sample' as in a short music loop that is used in beat-making)
# It does so by allowing the user to specify which part of the video they want
# to sample (download) by inputting values in seconds for start time and
# end time in the specified video

# It outputs a .mp3 file with a name inputted by a user and previously specified length

def user_input():
    # Get URL
    print('Enter youtube URL:')
    url = input()
    # Get filename
    print('How would like your sample to be named (saved as)?')
    file_name = input()
    file_name = sanitize_filepath(file_name).replace('/', '').replace('.', '').replace(',', '')
    print(file_name)
    # Get audio start time and validate the input
    print('When would you like the audio sample to start (in seconds)?')
    try:
        start_time = float(input())
        if start_time < 0:
            print('Invalid start time - it has to be a bigger number than 0 and smaller than duration of the clip. Exiting...')
            exit(1)
    except ValueError:
        print('Invalid input. It has to be a number. Exiting...')
        exit(1)
    # Get audio end time and validate the input
    print('When would you like the audio sample to end (in seconds)?')
    try:
        end_time = float(input())
        if end_time < start_time:
            print('Invalid end time - it has to be a bigger number than start time. Exiting...')
            exit(1)
    except ValueError:
        print('Invalid input. It has to be a number. Exiting...')
        exit(1)

    return url, file_name, start_time, end_time


# Downloading, trimming[start_time:end_time] and saving the audio sample
def download_and_process(url, file_name, start_time, end_time):
    # Validate the link
    try:
        sample = YouTube(url)
    except:
        print('Invalid link. Sorry, exiting...')
        exit(1)
    # Download the video
    sample.streams.first().download(filename=file_name)

    # Get the name of the downloaded file
    temp_file = file_name

    # Convert the downloaded video into a trimmed audio clip
    sample_video = VideoFileClip(f'{temp_file}.mp4')
    audioclip = sample_video.audio
    # Invalid (too big) end time handling
    if audioclip.duration < end_time:
        end_time = audioclip.duration
    sample_video.close
    audioclip.subclip(start_time, end_time).write_audiofile(f'{file_name}.mp3')

    # Deleting unused objects so the temporary .mp4 file can be deleted
    del sample_video.reader, sample_video, audioclip.reader, audioclip

    return temp_file, sample.title


def remove_temp(temp_file):
    # Deleting the original video (temporary file) after conversion
    os.remove(f'{temp_file}.mp4')


def main():
    url, file_name, start_time, end_time = user_input()
    temp_file, title = download_and_process(url, file_name, start_time, end_time)

    remove_temp(temp_file)

    print('Audio (.mp3) file has been created')
    print(f'Have fun sampling {title}')


if __name__ == '__main__':
    main()
