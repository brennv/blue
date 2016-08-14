from .logger import log
from .emoji import random_emoji
from .google import search_site
from .browser import browser
from .giphy import giphy
from .text import mood
# from .rhforce import watchlist
import bottom


def run_lambda(this, send, subs):
    """ Run 'lambdas' from the lexicon. """
    if send['lambda'] == 'say_hello':
        return ['hello ' + random_emoji(subset='faces')]
    if send['lambda'] == 'say_thanks':
        return ['thanks ' + random_emoji(subset='misc')]
    if send['lambda'] == 'get_watchlist':
        return watchlist(this)
    if send['lambda'] == 'google_site':
        return search_site(this, subs)
    if send['lambda'] == 'giphy':
        return giphy(this, subs)
    if send['lambda'] == 'mood':
        return mood(this, subs)


class Blue(object):
    """ State for the app. """
    def __init__(self, config):
        self.config = config
        self.config['browser'] = browser
        host = self.config['bot']['host']
        port = self.config['bot']['port']
        ssl = self.config['bot']['ssl']
        self.config['client'] = bottom.Client(host=host, port=port, ssl=ssl)
        chron_jobs = []
        for item in self.config['lexicon']:
            if 'hourly' in item['help']:
                chron_jobs.append(item['call'])
        self.config['chron_jobs'] = chron_jobs
        log.debug('registering chron_jobs: %s' % chron_jobs)


def send_notes(this, target, notes, limit=10):
    """ Send count-limited responses. """
    bot = this['client']
    for count, note in enumerate(notes):
        count += 1
        if count <= limit:
            bot.send('PRIVMSG', target=target, message=note)
            print(target, note)
        else:
            bot.send('PRIVMSG', target=target, message='...')
            print(target, '...')
            return


def send_help(this, target):
    """ Send lexicon keywords and help instructions. """
    commands = ' '.join(sorted([x['call'] for x in this['lexicon']]))
    help_note = 'The available commands are: ' + commands
    follow_up = 'For command help run: [command] [options] help'
    see_readme = 'Source: ' + this['bot']['realname']
    send_notes(this, target=target, notes=[help_note, follow_up, see_readme])


def respond(this, message, target, note_count=0):
    """ Compose notes based on lexicon and message context. """
    for item in this['lexicon']:
        if item['call'] in message:
            log.debug('writing notes')
            call, sends, _help = item['call'], item['send'], item['help']
            subs = message.lower().split(call)[1].strip().split(' ')
            subs = list(filter(None, subs))
            if subs:
                if subs[0] == 'help' or subs[-1] == 'help':
                    send_notes(this, target=target, notes=[call + ' ' + _help])
                    return
            for send in sends:
                if type(send) == str:
                    note_count += 1
                    send_notes(this, target=target, notes=[send])
                else:
                    if 'watchlist' in send['lambda']:  # for debugging
                        send_notes(this, target=this['bot']['dev_channel'], notes=['running watchlist'])  #
                    lambda_notes = run_lambda(this, send, subs)
                    if lambda_notes and type(lambda_notes) == list:
                        note_count += len(lambda_notes)
                        send_notes(this, target=target, notes=lambda_notes)
    if note_count == 0:
        called_help = ('#help' in message)
        said_help = ('help' in message)
        mentions_bot = (this['bot']['nick'] in message)
        if called_help or (said_help and mentions_bot):
            send_help(this, target)
