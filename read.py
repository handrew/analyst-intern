"""Text to speech cli."""
import os
import tempfile
import click
from openai import OpenAI
from langchain_text_splitters import TokenTextSplitter
from tqdm import tqdm



def openai_tts(text, voice="nova", model="tts-1"):
    """Uses openai to generate speech."""
    client = OpenAI()
    response = client.audio.speech.create(model=model, voice=voice, input=text)
    return response


def split_text(text, chunk_size=500, chunk_overlap=0):
    """Split text using TokenTextSplitter."""
    text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_text(text)
    return texts


def stitch_mp3s_together(fpaths, outpath):
    """Stitch mp3s together."""
    cmd = f"""ffmpeg -i 'concat:{
        '|'.join(fpaths)
    }' -c copy {outpath}"""
    os.system(cmd)


@click.command()
@click.option("--fpath", default="speech.mp3", help="Output file.")
@click.option("--text", default=None, help="txt file or string.")
@click.option("--voice", default="nova", help="Voice to use.")
@click.option("--model", default="tts-1", help="Which model.")
def cli(fpath, text, voice, model):
    """Read text."""
    assert text is not None, "Need to give text param."
    assert fpath.endswith("mp3")

    # Read text.
    if text.endswith("txt"):
        with open(text, "r", encoding="utf-8") as f:
            text = f.read()

    texts = split_text(text)

    with tempfile.TemporaryDirectory() as tmpdir:
        print("Using temporary directory: ", tmpdir)
        for i, _text in tqdm(enumerate(texts)):
            outpath = f"{i}.mp3"
            outpath = os.path.join(tmpdir, outpath)
            response = openai_tts(_text, voice=voice, model=model)
            response.stream_to_file(outpath)
            print(_text)
            print("Output to: ", outpath)

        fpaths = [os.path.join(tmpdir, f"{i}.mp3") for i in range(len(texts))]
        stitch_mp3s_together(fpaths, fpath)


if __name__ == "__main__":
    cli()

