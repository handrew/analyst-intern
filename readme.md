# tts-cli

1. Install ffmpeg with homebrew.
2. `pip install requirements.txt` in your favorite virtual env.
3. Set your `OPENAI_API_KEY` in your `.bashrc` or `.vimrc` or `.zshrc`.
4. Then: 
```
python read.py --help

Usage: read.py [OPTIONS]

  Read text.

Options:
  --fpath TEXT  Output file.
  --text TEXT   txt file or string.
  --voice TEXT  Voice to use.
  --model TEXT  Which model.
  --help        Show this message and exit.
```
5. Listen to it at the specified `fpath`.
