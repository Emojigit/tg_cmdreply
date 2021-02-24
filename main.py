# -*- coding: utf-8 -*-
import sys, re, logging, requests, json, emoji, traceback
exit = sys.exit
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackContext
from telegram.ext.filters import Filters
from telegram.error import InvalidToken
from telegram import ParseMode, Update, Bot
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s[%(name)s] %(message)s")
log = logging.getLogger("MainScript")

def jsondata():
    with open("cmds.json", encoding='utf-8') as json_file:
        return json.load(json_file)

def token():
    try:
        with open("token.txt","r") as f:
            return f.read().rstrip('\n')
    except FileNotFoundError:
        log.error("No token.txt!")
        return ""

def starttxt():
    try:
        with open("start.txt","r") as f:
            return f.read().rstrip('\n')
    except FileNotFoundError:
        log.warning("No start.txt, using the example.")
        try:
            with open("start.txt.example","r") as f:
                return f.read().rstrip('\n')
        except FileNotFoundError:
            log.warning("No start.txt.example!")
            return ""

def logc():
    try:
        with open("logc.txt","r") as f:
            return f.read().rstrip('\n')
    except FileNotFoundError:
        log.error("No logc.txt!")
        return ""

def GetCMDCallBack(cname,rcont,loc,bot):
    def CMDCB(update: Update, context: CallbackContext):
        log.info("Got {} command!".format(cname))
        update.message.reply_text(rcont,parse_mode=ParseMode.MARKDOWN_V2)
        bot.send_message(loc,disable_notification=True, text="Type: Command Log\nUser ID: {}\nFirst name: {}\nUsed Command: /{}".format(update.message.from_user.id,update.message.from_user.first_name,cname))
    return CMDCB

helptxt = "Source code: https://github\.com/Emojigit/tg\_cmdreply\nLicense: GPLv3"

def main():
    tok = token()
    if tok == "":
        log.critical("No token!")
        exit(3)
    loc = logc()
    if loc == "":
        log.critical("No log channel!")
        exit(3)
    try:
        bot = Bot(token=tok)
        updater = Updater(bot=bot, use_context=True)
        log.info("Get updater success!")
    except InvalidToken:
        log.critical("Invalid Token! Plase edit token.txt and fill in a valid token.")
        raise
    dp = updater.dispatcher
    FCL = []
    for key,txt in jsondata().items():
        log.info("Registering {} command with '{}'".format(key,txt))
        try:
            if key == "help" or key == "ping" or key == "start":
                raise ValueError("The `{}` command is for special use, please do not register it.".format(key))
            dp.add_handler(CommandHandler(key, GetCMDCallBack(key,txt,loc,bot)))
        except ValueError as error:
            log.warning("Not register {} because error".format(key), exc_info=True)
            #log.exception(error)
            continue
        FCL.insert(-1,key)
    dp.add_handler(CommandHandler("ping", GetCMDCallBack("ping","pong",loc,bot)))
    dp.add_handler(CommandHandler("start", GetCMDCallBack("start",starttxt(),loc,bot)))
    FCL.insert(-1,"help")
    FCL.insert(-1,"ping")
    FCL.insert(-1,"start")
    dp.add_handler(CommandHandler("help", GetCMDCallBack("help","I have these commands: {}\n{}".format("/" + " /".join(map(str, FCL)),helptxt),loc,bot)))
    log.info("Finally i registered these commands: {}".format(str(FCL)))
    updater.start_polling()
    log.info("Started the bot! Use Ctrl-C to stop it.")
    updater.idle()

if __name__ == '__main__':
    main()
