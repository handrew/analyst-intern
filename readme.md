# Intern CLI

## Installation

1. `pip install analyst-intern`
2. Install ffmpeg with homebrew.
3. Set your `OPENAI_API_KEY` in your `.bashrc` or `.vimrc` or `.zshrc`. Can also support Gemini and Anthropic.

## Usage

Run `intern --help`:

```
Usage: intern [OPTIONS] COMMAND [ARGS]...

  Intern CLI.

Options:
  --help  Show this message and exit.

Commands:
  read      Given a file, read it out and save the speech to an mp3 file.
  research  Visit provided links, apply the prompt, summarize the results.
```

### `intern read`

Given a txt file, md file, or string, use OpenAI's TTS to save an mp3 file. 

```
Usage: intern read [OPTIONS]

  Given a file, read it out and save the speech to an mp3 file.

Options:
  --output TEXT  Output file.  [required]
  --text TEXT    txt or md file or string.  [required]
  --voice TEXT   Voice to use.  [required]
  --model TEXT   Which model.  [required]
  --help         Show this message and exit.
```

### `intern research`

```
Usage: intern research [OPTIONS] PROMPT

  Visit provided urls, apply the prompt, summarize the results.

Options:
  --url TEXT                      List of urls to visit.  [required]
  --headless                      Whether or not to run the browser headless.
  --model [openai|anthropic|gemini]
                                  Which model to use.
  --output TEXT                   Output file to save the results to.
  --help                          Show this message and exit.
```
