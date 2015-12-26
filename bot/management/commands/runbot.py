import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from teams.models import Team, Player, PLAYING_STATES

from bot.models import TelegramGroup

import telebot

TOKEN_PATH = os.path.join('bot', 'token')
with open(TOKEN_PATH) as f:
    TOKEN = f.read().strip()

bot = telebot.TeleBot(TOKEN)


def better_message_handler(command):
    def dec(func):

        @bot.message_handler(commands=[command])
        def handler(message):
            args = message.text.replace('/' + command, '').strip()
            response = func(message, args)
            return bot.reply_to(message, response)

    return dec


def mandatory_args_message_handler(command, mandatory_missing_msg):
    def dec(func):

        @better_message_handler(command)
        def handler(message, args):
            if args:
                return func(message, args)
            else:
                return mandatory_missing_msg

    return dec


def group_message_handler(command):
    def dec(func):

        @better_message_handler(command)
        def handler(message, args):
            chat_id = message.chat.id
            try:
                telegram_group = TelegramGroup.objects.get(chat_id=chat_id)
            except TelegramGroup.DoesNotExist:
                return 'No group set - run /setgroup'
            else:
                return func(message, args, telegram_group.group)

    return dec


@mandatory_args_message_handler('setgroup', 'Name of group is missing')
def handler(message, args):
    try:
        group = Team.objects.get(name=args)
    except Team.DoesNotExist:
        return "Group {} doesn't exist".format(args)

    chat_id = message.chat.id
    try:
        old_group = TelegramGroup.objects.get(chat_id=chat_id)
    except TelegramGroup.DoesNotExist:
        TelegramGroup.objects.create(group=group, chat_id=chat_id)
    else:
        old_group.group = group
        old_group.save()
    return 'Great, lets create teams!'


@group_message_handler('list')
def handler(message, args, group):
    court = group.player_set.filter(state=PLAYING_STATES['on_the_court'])
    bench = group.player_set.filter(state=PLAYING_STATES['on_the_bench'])
    if not court and not bench:
        return 'No one to play with :-('
    final = []
    if court:
        final.append('<-- On the court -->')
        final += [p.name for p in court]
    if bench:
        final.append('<-- On the bench -->')
        final += [p.name for p in bench]
    return '\n'.join(final)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        bot.polling()
