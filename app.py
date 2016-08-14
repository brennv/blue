from blue.bot import Blue, respond
from blue.loader import jsonify
from blue.logger import logger
from blue.schedule import scheduler, async_wrapper
import os


config_file = 'config.yml'
path = os.path.dirname(__file__)
app = Blue(config=jsonify(os.path.join(path, config_file)))
bot = app.config['client']
log = logger(config=app.config['app']['mode'])


@bot.on('CLIENT_CONNECT')
def connect(**kwargs):
    """ Connect to irc channel. """
    bot.send('NICK', nick=app.config['bot']['nick'])
    bot.send('USER', user=app.config['bot']['nick'], realname=app.config['bot']['realname'])
    bot.send('JOIN', channel=app.config['bot']['channel'])


@bot.on('PING')
def keepalive(message, **kwargs):
    """ Send pongs to irc server. """
    print('pong')
    bot.send('PONG', message=message)


@bot.on('PRIVMSG')
def message(nick, target, message, config=app.config, **kwargs):
    """ Listen to channel and direct messages so we can respond accordingly. """
    print(nick, target, message)
    if nick == config['bot']['nick']:
        return
    if target == config['bot']['nick']:
        new_target = nick
    else:
        new_target = target
    respond(this=app.config, message=message, target=new_target)


def chron_jobs(this=app.config, messages=app.config['chron_jobs'], target=app.config['bot']['channel']):
    for message in messages:
        respond(this=this, message=message, target=target)


async_wrapper(scheduler(chron_jobs))
bot.loop.create_task(bot.connect())
bot.loop.run_forever()
