from flask import render_template, redirect, url_for
from threading import enumerate
from web import app
from web.bot import bots
from web.bot_handler import bot_iter, load_bot, BotThread
from web.forms import BotStartForm, BotAddUserForm, BotRemoveUserForm, BotStopForm


@app.route('/start', methods=['GET', 'POST'])
def start():
    message = None
    start_form = BotStartForm(csrf_enabled=False)

    if start_form.validate_on_submit():
        if start_form.is_new_field.data:
            for thread in enumerate():
                if type(thread) is BotThread:
                    thread.is_active = False
                    thread.join()
                    break

            bot = bots.ControlBot(start_form.token_field.data)
            bot.save_bot()

        thread_exists = False
        for thread in enumerate():
            thread_exists = type(thread) is BotThread
            if thread_exists:
                break
        if not thread_exists:
            bot_th = BotThread()
            bot_th.start()
            message = {'text': "Bot started", 'color': 'green'}
        else:
            message = {'text': "Bot is already started", 'color': 'red'}

    return render_template('start_bot.html', start_form=start_form, message=message)


@app.route('/stop', methods=["GET", "POST"])
def stop():
    message = None
    stop_form = BotStopForm(csrf_enabled=False)

    if stop_form.validate_on_submit():
        thread_exists = False
        for thread in enumerate():
            if type(thread) is BotThread:
                thread_exists = True
                thread.is_active = False
                thread.join()
                message = {'text': 'Bot stopped', 'color': 'green'}
                break
        if not thread_exists:
            message = {'text': "Bot is not running", 'color': 'red'}

    return render_template('stop_bot.html', stop_form=stop_form, message=message)
