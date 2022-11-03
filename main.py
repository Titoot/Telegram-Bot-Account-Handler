import os
import re
import time
from telegram import Update
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext import (Updater, CallbackContext, CommandHandler)

from keep_alive import keep_alive
from dbHandler import db_conn, insertCommand

my_secret = os.environ['TOKEN']
updater = Updater(my_secret, use_context=True)

def UserCheck(user):
  command = f"SELECT user_id,role from users WHERE user_id = {user['id']}"
  userchecker = insertCommand(command)
  return userchecker


def AdminCheck(user):
  command = f"SELECT user_id,role from users WHERE user_id = {user['id']} AND role = 'Admin'"
  isAdmin = insertCommand(command)
  return isAdmin

def createAcc(update: Update, context: CallbackContext):
  user = update.message.from_user
  check = f"SELECT user_id,role from users WHERE user_id = {user['id']}"
  userchecker = insertCommand(check)

  if not userchecker:
    accMatch = re.match(r'/createAcc\s([a-zA-Z0-9_.-]*)\s([a-zA-Z0-9_.-]*)', update.message.text)
    if not accMatch:
      update.message.reply_text('/createAcc username password')
    else:
      username, password = accMatch.group(1), accMatch.group(2)
      dt = time.ctime()
      print(dt)
      uniqueUser = f"SELECT acc_user from users WHERE acc_user = '{username}'"
      uniqueUserCheck = insertCommand(uniqueUser)
      if uniqueUserCheck:
        update.message.reply_text('Username Already Exists')
        return
        ###Change to Admin if you want
      create = f"INSERT INTO users(user_id, acc_user, acc_pass, role, LAST_EDIT) VALUES ({user['id']}, '{username}', '{password}','User', '{dt}');"
      insertCommand(create)
      update.message.reply_text('Created Account Successfully!')
  else:
    update.message.reply_text('You Already Have An Account!')


def start(update: Update, context: CallbackContext):
  user = update.message.from_user
  print(f"You talk with user {user['username']} and his user ID: {user['id']}")
  

  if UserCheck(user) and not AdminCheck(user):
    update.message.reply_text('User Account')

  elif UserCheck(user) and AdminCheck(user):
    update.message.reply_text('Admin Account')

  else:
    update.message.reply_text('not signed up?\nfor creating an account /createAcc')
    return

  update.message.reply_text(f"User: {user['username']}\nID: {user['id']}")
  update.message.reply_text("Please write /help to see the commands available.")


def help(update: Update, context: CallbackContext):
  update.message.reply_text("""nothing here yet...""")


def sqlcomm(update: Update, context: CallbackContext):
  user = update.message.from_user
  matcher = re.match(r'/db\s(.*)', update.message.text).group(1)
  if matcher and AdminCheck(user):

    comm = insertCommand(matcher)
    for i in comm:
      update.message.reply_text(i)
  else:
    update.message.reply_text(f"Sorry {update.message.text} is not a valid command")


def unknown(update: Update, context: CallbackContext):
  update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))

updater.dispatcher.add_handler(CommandHandler('help', help))

updater.dispatcher.add_handler(CommandHandler('db', sqlcomm))
updater.dispatcher.add_handler(CommandHandler('createAcc', createAcc))

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

keep_alive()
updater.start_polling()
db_conn()
