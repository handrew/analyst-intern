"""Text to speech cli."""
import os
import tempfile
import click
from openai import OpenAI
from langchain_text_splitters import TokenTextSplitter
from tqdm import tqdm


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

    # Split text.
    text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=0)
    texts = text_splitter.split_text(text)

    # Text to speech.
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, _text in tqdm(enumerate(texts)):
            client = OpenAI()
            response = client.audio.speech.create(model=model, voice=voice, input=_text)
            outpath = fpath.replace(".mp3", f"_{i}.mp3")
            outpath = os.path.join(tmpdir, outpath)
            response.stream_to_file(outpath)
            print(_text)

        # ffmpeg it together.
        cmd = f"""ffmpeg -i 'concat:{
            '|'.join([os.path.join(tmpdir, fpath.replace('.mp3', f'_{i}.mp3')) for i in range(len(texts))])
        }' -c copy {fpath}"""
        os.system(cmd)


if __name__ == "__main__":
    cli()

