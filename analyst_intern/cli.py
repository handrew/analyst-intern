"""Intern CLI."""
import os
import tempfile
import click
from tqdm import tqdm
from rich import print
from playwright.sync_api import sync_playwright
from analyst_intern.utils import llm_call
from analyst_intern.utils import openai_tts, split_text, stitch_mp3s_together


@click.group()
def cli():
    """Intern CLI."""


@cli.command()
@click.argument("prompt")
@click.option("--url", multiple=True, required=True, help="List of urls to visit.")
@click.option(
    "--headless", is_flag=True, help="Whether or not to run the browser headless."
)
@click.option(
    "--model",
    default="gemini/gemini-2.5-flash",
    help="Which model to use.",
)
@click.option(
    "--output",
    default=None,
    help="Output file to save the results to.",
)
def research(prompt, url, headless, model, output):
    """
    Visit provided urls, apply the prompt, summarize the results.
    """
    extracted_texts = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        for link in url:
            page.goto(link)
            page.wait_for_load_state("load")
            text = page.inner_text("body")
            extracted_texts.append(text)

        browser.close()

    markdown_string = "# Research Results\n\n"
    llm_responses = []

    for text in tqdm(extracted_texts):
        combined_prompt = f"{text}\n\n----\n\n{prompt}"
        response = llm_call(combined_prompt, model=model)
        llm_responses.append(response)
        markdown_string += (
            f"## Results for {url[extracted_texts.index(text)]}\n\n{response}\n\n"
        )

    markdown_string += "## Overall Summary\n\n"
    summary_prompt = f"Summarize the following content with respect to the original prompt: '{prompt}'\n\n{markdown_string}"
    summary = llm_call(summary_prompt, model=model)

    # Prepend it to the markdown string.
    markdown_string = f"{summary}\n\n{markdown_string}"

    click.echo(markdown_string)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(markdown_string)


@cli.command()
@click.option("--output", required=True, default="speech.mp3", help="Output file.")
@click.option("--text", required=True, default=None, help="txt or md file or string.")
@click.option("--voice", required=True, default="nova", help="Voice to use.")
@click.option("--model", required=True, default="tts-1", help="Which model.")
def read(output, text, voice, model):
    """Given a file, read it out and save the speech to an mp3 file."""
    assert text is not None, "Need to give text param."
    assert output.endswith("mp3")

    # Read text.
    if text.endswith("txt") or text.endswith(".md"):
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

        outputs = [os.path.join(tmpdir, f"{i}.mp3") for i in range(len(texts))]
        stitch_mp3s_together(outputs, output)


if __name__ == "__main__":
    cli()
