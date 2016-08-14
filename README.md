# blue

An asyncio python 3.5+ irc client built on [bottom](https://github.com/numberoverzero/bottom).

## Getting started

Install the python requirements as well as [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/getting-started).

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python app.py
```

## Help

For help with the lexicon, send a channel or private message with `blue help` or just `#help`.

## Extending the lexicon

Extend the client lexicon by modifying `config.yml`. Here's an example lexicon entry that responds with `hello` then calls a function for the weather.

```
lexicon:
  - call: '#hello'
    help: Say hello.
    send:
      - hello
      - lambda: get_weather
```

## Development

If you're adding a 'lambda' to the lexicon, you'll want to include it in `blue/bot.py: run_lambda()`. All functions should return a list, each item in the list will be sent as a message line.

Run tests with:

```
python -m pytest tests/
```
