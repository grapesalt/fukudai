import argparse
import whisper
from moviepy.editor import VideoFileClip
import tempfile

from utils import format_time

from os import path, remove

parser = argparse.ArgumentParser(prog="fukudai", description="Automatically generates a SRT file for given video.")

parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", required=True)

args = parser.parse_args()
input, output = args.input, args.output

model = whisper.load_model("medium")

if path.exists(input):
    filename, _ = path.splitext(input)
    clip = VideoFileClip(input)
    audio_file = path.join(tempfile.gettempdir(), f'extracted-audio.wav')
    clip.audio.write_audiofile(audio_file)

    segments = model.transcribe(audio_file)['segments']
    
    with open(path.join(output, f'{filename}.srt'), 'a') as f:
        for index, segment in enumerate(segments):
            f.write(f"""{index}
{format_time(segment['start'])} --> {format_time(segment['end'])}
{segment['text']}

""")

    remove(audio_file)
else:
    print(f"{input} does not exist.")
