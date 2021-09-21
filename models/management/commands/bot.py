from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.utils.request import Request

from models.models import Message
from models.models import Profile
from models.models import Group

import re


def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'ERROR: {e}'
            print(error_message)
            raise e

    return inner


def parse_command(format_list, command_text):
    """
    format_list - list of strings
    command_text - text of command
    groups - message groups
    """

    first_line = re.split('\n', command_text)[0]
    tokens = re.split(r"\s+", first_line)
    non_empty_tokens = list(filter(lambda string: string != '', tokens))

    value_list = []
    for i, f in enumerate(format_list):
        if i >= len(non_empty_tokens):
            value_list.append(None)
            continue
        token = non_empty_tokens[i]

        if f == "command":
            value_list.append(token)

        elif f == "digital":
            if token.isdigit():
                value_list.append(token)
            else:
                value_list.append(None)

        elif f == "group":
            value_list.append(token)

        elif f == "date":
            value_list.append(None)

    return value_list


@log_errors
def do_message_proc(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    profile, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )

    first_text_word = re.split(r"\s+", text)[0]
    user_group_names = Group.objects.filter(profile__external_id=chat_id)

    if user_group_names.filter(group_name=first_text_word).exists():
        Message(
            profile=profile,
            text=text,
            group_name=first_text_word,
        ).save()
        update.message.reply_text(
            text=f"Message saved in group {first_text_word}"
        )
    else:
        update.message.reply_text(
            text=f"Group {first_text_word} does not exist. Message ignored"
        )


@log_errors
def do_create_group(update: Update, context: CallbackContext):

    chat_id = update.message.chat_id

    profile, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )

    command_text = update.message.text

    _, group_name = parse_command(['command', 'group'], command_text)

    if group_name is not None:
        user_group_names = Group.objects.filter(
            profile__external_id=update.message.chat_id)

        if user_group_names.filter(group_name=group_name).exists():
            update.message.reply_text(
                text=f"Group {group_name} already exists"
            )
        else:
            Group(
                group_name=group_name,
                profile=profile
            ).save()
            update.message.reply_text(
                text=f"Created {group_name} group"
            )

    else:
        update.message.reply_text(
            text="To create a new group input valid group name"
        )


@log_errors
def do_show_groups(update: Update, context: CallbackContext):
    user_group_names = Group.objects.filter(
        profile__external_id=update.message.chat_id)
    user_group_names = user_group_names.values_list('group_name', flat=True)

    update.message.reply_text(
        text='\n'.join(user_group_names)
    )


@log_errors
def do_show_tail(update: Update, context: CallbackContext):

    user_group_names = Group.objects.filter(
        profile__external_id=update.message.chat_id)
    user_group_names = user_group_names.values_list('group_name', flat=True)

    user_messages = Message.objects.filter(
        profile__external_id=update.message.chat_id)

    _, group, tail_len = parse_command(
        ['command', 'group', 'digital'], update.message.text)

    if group in user_group_names and tail_len is not None:
        group_messages = user_messages.filter(
            group_name=group).order_by('-created_at')

        tail_len = min(int(tail_len), len(group_messages))

        rng = list(range(tail_len))[::-1]

        for i in rng:
            msg = group_messages[i]
            update.message.reply_text(
                text=msg.text
            )
    else:
        update.message.reply_text(
            text='Input group name and number of messages'
        )


@log_errors
def do_start(update: Update, context: CallbackContext):
    msg = [
        'Makenotes Bot', 'You can gather messages in groups',
        'To add a new group use /new **groupname**',
        'To put message in a group write **groupname**',
        'in the first line of the message', 'To see all groups use /show',
        'To see last messages in a group use',
        '/tail **groupname** **number of messages**'
    ]

    update.message.reply_text(
        text='\n'.join(msg)
    )


class Command(BaseCommand):
    help = 'Telegram bot'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )
        print(bot.get_me())

        updater = Updater(
            bot=bot,
            use_context=True,
        )

        add_group_handler = CommandHandler('new', do_create_group)
        updater.dispatcher.add_handler(add_group_handler)

        show_all_groups_handler = CommandHandler('show', do_show_groups)
        updater.dispatcher.add_handler(show_all_groups_handler)

        show_tail_handler = CommandHandler('tail', do_show_tail)
        updater.dispatcher.add_handler(show_tail_handler)

        start_command_handler = CommandHandler(['start', 'help'], do_start)
        updater.dispatcher.add_handler(start_command_handler)

        message_handler = MessageHandler(Filters.text, do_message_proc)
        updater.dispatcher.add_handler(message_handler)

        updater.start_polling()
        updater.idle()
