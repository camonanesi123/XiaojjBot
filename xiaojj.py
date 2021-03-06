#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import html
import logging
import os
import re
import time
from base64 import b64encode
from functools import wraps
from random import random, choice
import random
import pymysql
import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent,InlineKeyboardButton, InlineKeyboardMarkup
import requests
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler,CallbackQueryHandler
import json
message_list = os.listdir("message")

TOKEN1 = "1080551756:AAFyFgZ3jBg6F4bIFk5IK9Wko8X59eTPSpU"
DB_UNAME = 'root'
DB_PASSWD = '123qwe'

proDir = os.path.dirname(os.path.realpath(__file__))
welcome_dir = os.path.join(proDir, "message/")
message_list = os.listdir(welcome_dir)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func
    
    return decorator
send_typing_action = send_action(telegram.ChatAction.TYPING)
send_upload_video_action = send_action(telegram.ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = send_action(telegram.ChatAction.UPLOAD_PHOTO)


@send_typing_action
def reply_handler(update, context):
    """Reply message."""
    text = update.message.text
    update.message.reply_text(text)

@send_typing_action
def start(update, context):
    '''这是一个全国小姐姐性息查询机器人，每天更新全国各地小姐姐性息。
    请输入 /xingxi <地名> 开始你的表演！每次随机选取一个地区的小姐姐联系方式发出来'''
    print('/start command executed!')
    update.message.reply_text("这是一个全国小姐姐性息查询机器人，每天更新全国各地小姐姐性息。\n\
    输入:/xjj <兼职> <城市名> 查询当前城市兼职妹子性息\n\
    输入:/xjj <洗浴> <城市名> 查询当前城市洗浴中心性息\n\
    输入:/xjj <外围> <城市名> 查询当前城市外围女性息\n\
    输入:/xjj <酒店> <城市名> 查询当前城市酒店妹子性息\n\
    输入:/xjj <丝足> <城市名> 查询当前城市丝足会所性息\n\
    每次随机选取一个地区的小姐姐联系方式发出来")

#欢迎新加入群组的人
def welcome(update, context):
    for new_user_obj in update.message.new_chat_members:
        chat_id = update.message.chat.id
        new_user = ""
        message_rnd = random.choice(message_list)
        WELCOME_MESSAGE = open(welcome_dir + message_rnd , 'r', encoding='UTF-8').read().replace("\n", "")

        try:
            new_user = "@" + new_user_obj['username']
        except Exception as e:
            new_user = new_user_obj['first_name'];
        WELCOME_MESSAGE=WELCOME_MESSAGE.replace("username",str(new_user))
        print(WELCOME_MESSAGE)
        context.bot.send_message(chat_id=chat_id, text=WELCOME_MESSAGE, parse_mode=telegram.ParseMode.HTML)
        
@send_typing_action        
def get_random_pornhub(update,context):
    db = pymysql.connect(host='localhost', port=3306,user=DB_UNAME, passwd=DB_PASSWD, db='gatherinfo', charset='utf8')
    cursor = db.cursor()
    sqlSel = "select * from pornhub ORDER BY RAND() limit 1"
    try:
        cursor.execute(sqlSel)
        rs = cursor.fetchone()
        maopian = {}
        if rs==None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="目前还没有你需要的动作片",
                                     parse_mode=telegram.ParseMode.HTML)
        else:
            #print("Database version : %s " % rs[1])
            link = 'https://telegram.me/sexinfochina'
            share_link = 'https://telegram.me/share/url?url={0}&text=Click%20the%20link%20to%20join%20the%20chinese%20sex%20club%20'.format(link)
            keyboard = [
            [InlineKeyboardButton("广告位500/月", url='https://t.me/komonado')],
            [InlineKeyboardButton('点此分享至5个群截图，找群主索取单女资料', url=share_link)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            maopian['视频标题'] = rs[0]
            maopian['时长']=rs[1]
            maopian['当前观看总量']=rs[2]
            maopian['点赞率']=rs[3]
            maopian['发布时间']=rs[4]
            maopian['视频链接']=rs[5]
            maopian['抓取时间']=rs[6]
            out_put1 = "视频标题:{0}\n时长:{1}\n当前观看总量:{2}\n点赞率:{3}\n发布时间:{4}\n抓取时间:{5}\n视频链接:{6}\n"\
                .format(rs[0], rs[1],rs[2],rs[3],rs[4],\
                        rs[6],rs[5])
            context.bot.send_message(chat_id=update.effective_chat.id, text=out_put1,
                 parse_mode=telegram.ParseMode.HTML,reply_markup=reply_markup)

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()



@send_typing_action        
def get_random_pornhub_cn(update,context):
    db = pymysql.connect(host='localhost', port=3306,user=DB_UNAME, passwd=DB_PASSWD, db='gatherinfo', charset='utf8')
    cursor = db.cursor()
    sqlSel = "select * from pornhub_cn ORDER BY RAND() limit 1"
    try:
        cursor.execute(sqlSel)
        rs = cursor.fetchone()
        maopian = {}
        if rs==None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="目前还没有你需要的中国动作片",
                                     parse_mode=telegram.ParseMode.HTML)
        else:
            #print("Database version : %s " % rs[1])
            link = 'https://telegram.me/sexinfochina'
            share_link = 'https://telegram.me/share/url?url={0}&text=Click%20the%20link%20to%20join%20the%20chinese%20sex%20club%20'.format(link)
            keyboard = [
            [InlineKeyboardButton("广告位500/月", url='https://t.me/komonado')],
            [InlineKeyboardButton('点此分享至5个群截图，找群主索取单女资料', url=share_link)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            maopian['视频标题'] = rs[0]
            maopian['时长']=rs[1]
            maopian['当前观看总量']=rs[2]
            maopian['点赞率']=rs[3]
            maopian['发布时间']=rs[4]
            maopian['视频链接']=rs[5]
            maopian['抓取时间']=rs[6]
            out_put1 = "视频标题:{0}\n时长:{1}\n当前观看总量:{2}\n点赞率:{3}\n发布时间:{4}\n抓取时间:{5}\n视频链接:{6}\n"\
                .format(rs[0], rs[1],rs[2],rs[3],rs[4],\
                        rs[6],rs[5])
            context.bot.send_message(chat_id=update.effective_chat.id, text=out_put1,
                 parse_mode=telegram.ParseMode.HTML,reply_markup=reply_markup)

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()
        
#@run_async
@send_typing_action
def getXjjInfo(update,context):
    """Send a message when the command /xingxi is issued."""
    if len(context.args)!=2:
        context.bot.send_message(chat_id=update.effective_chat.id, text='请输入正确的查询命令 例如:/xjj 兼职 北京')
        return
    style= ''.join(context.args[0])
    district=''.join(context.args[1])
    if style not in ("兼职","洗浴","外围","酒店","丝足"):
        context.bot.send_message(chat_id=update.effective_chat.id, text='请输入正确的类别 例如:/xjj 兼职 北京')
        return
    print(district,style)
    link = 'https://telegram.me/sexinfochina'
    share_link = 'https://telegram.me/share/url?url={0}&text=点击链接加入小姐姐性息免费分享群'.format(link)
    keyboard = [[InlineKeyboardButton("助勃延时", callback_data='yinduweige2020'),InlineKeyboardButton("迷奸水专卖", url='https://t.me/ghbchina')],
	[InlineKeyboardButton("广告位500/月", url='https://t.me/komonado')],
	[InlineKeyboardButton('点此分享5个群，白嫖数据等您拿', url=share_link)]
	]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # 打开数据库连接
    db = pymysql.connect(host='localhost', port=3306,user=DB_UNAME, passwd=DB_PASSWD, db='gatherinfo', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sqlSel = "select * from detail_info where   LOCATE('{0}', style)>0  and locate('{1}',district)>0  ORDER BY RAND()  limit 1".format(style,district)
    fast_sql = "select * from detail_info q1 inner join (select (min(q2.id) + round(rand()*(max(q2.id) - min(q2.id)))) as id from detail_info q2 where  LOCATE('{0}', q2.style)>0  and locate('{1}',q2.district)>0) as t on q1.id >= t.id limit 1".format(style,district)
    print(sqlSel)
    # 使用 execute()  方法执行 SQL 查询
    try:
        cursor.execute(sqlSel)
        rs = cursor.fetchone()
        xiaojj = {}
        data = {}
        if rs==None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="你查询的地方没有小姐姐性息，或者查询失败",
                                     parse_mode=telegram.ParseMode.HTML)
        else:
            #print("Database version : %s " % rs[1])
            xiaojj['id'] = rs[0]
            xiaojj['title']=rs[3]
            xiaojj['district']=rs[5]
            xiaojj['detailAddr']=rs[6]
            xiaojj['age']=rs[9]
            xiaojj['appear']=rs[11]
            xiaojj['price']=rs[13]
            xiaojj['serive']=rs[12]
            #xiaojj['photo'] = b64encode(rs[18].decode("utf-8"))
            xiaojj['contact']="http://www.younglass.com/image/{0}".format(xiaojj['id'])
            contact = "<a href ='{0}'>点击查看，耐心等待</a>".format(xiaojj['contact'])
            xiaojj['detail']=rs[19]
            xiaojj['detail'] = re.sub("<[^>]*?>", "", xiaojj['detail'])
            xiaojj['detail'] = html.unescape(xiaojj['detail'])

            out_put1 = "主题:{0}\n区域:{1}\n地址:{2}\n价位:{3}\n编号:{4}\n服务:{5}\n详情:{6}\n联系:{7}\n"\
                .format(xiaojj['title'], xiaojj['district'],xiaojj['detailAddr'], xiaojj['price'],xiaojj['id'],\
                        xiaojj['serive'],xiaojj['detail'],contact)
            context.bot.send_message(chat_id=update.effective_chat.id, text=out_put1,
                 parse_mode=telegram.ParseMode.HTML,reply_markup=reply_markup)

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
#从配置文件读取TELEGRAM BOT的TOKEN值


#定时作业回调函数 每一分钟给用户发一条消息
def callback_minute(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id='@sexinfochina', 
                             text='每一分钟提醒一次，表示机器人没有挂')


#查询疫情接口
@send_typing_action
def covid19_details(update,context):
    r = requests.get('https://lab.isaaclin.cn/nCoV/api/overall?latest=1')
    print('请求到数据')
    print(r.text)
    #用自带的json工具把字符串转成字典
    dictinfo = json.loads(r.text)
    #输出字典
    print(dictinfo)
    a=dictinfo['results'][0]['currentConfirmedCount']
    b=dictinfo['results'][0]['confirmedCount']
    c=dictinfo['results'][0]['suspectedCount']
    d=dictinfo['results'][0]['curedCount']
    e=dictinfo['results'][0]['deadCount']
    f=dictinfo['results'][0]['remark1']
    g=dictinfo['results'][0]['note2']
    h=dictinfo['results'][0]['note1']
    i=dictinfo['results'][0]['note3']
    out_put1 = "现存确诊:{0}\n累计确诊:{1}\n疑似病例:{2}\n治愈:{3}\n死亡人数:{4}\n易感染群:{5}\n病毒名:{6}\n传染源:{7}\n传染方式:{8}\n"\
    .format(a,b,c,d,e,f,g,h,i)
    context.bot.send_message(chat_id=update.effective_chat.id, text=out_put1,
    parse_mode=telegram.ParseMode.HTML)
    #用字典的方法获取值
    #print(dictinfo['status'])
    
#91porn随机小电影播放
@send_typing_action
def sex_porn(update,context):
	#从1,100中随机抽取一个页码作为page参数
    page = random.randint(1,10)
    r = requests.get('https://91povideo.com/api/list_info?category=&page={0}'.format(page))
    print('请求到数据')
    print(r.text)
    #用自带的json工具把字符串转成字典
    dictinfo = json.loads(r.text)
    #输出字典
    print(dictinfo)
    viewkey=dictinfo['data']['list'][random.randint(0,9)]['viewkey']
    #再把密钥拿到去请求视频网址 每天更新
    userKey = 'd42c5'
    r = requests.get('https://91povideo.com/api/video_info?viewkey={0}&userKey={1}'.format(viewkey,userKey))
    print('请求到数据')
    print(r.text)
    dictinfo = json.loads(r.text)
    videoSrc = dictinfo['data']['videoSrc']
    title = dictinfo['data']['title']

    out_put1 = "视频题目:{0}\n视频连接:{1}\n"\
    .format(title,videoSrc)
    context.bot.send_message(chat_id=update.effective_chat.id, text=out_put1,
    parse_mode=telegram.ParseMode.HTML)
    #用字典的方法获取值
    #print(dictinfo['status'])

def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    #query.answer()
    context.bot.answer_callback_query(query.id, text="微信妹子客服: {}".format(query.data), show_alert=True)
    #query.edit_message_text(text="微信号: {}".format(query.data))
    
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN1, use_context=True)
    # Get the dispatcher to register handlers
    # 注册一个任务分派器
    dispatcher = updater.dispatcher
    # 将回调函数绑定到分派器上
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dispatcher.add_handler(CommandHandler("xjj", getXjjInfo))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("covid19", covid19_details))
    dispatcher.add_handler(CommandHandler("kanpian", get_random_pornhub))   
    dispatcher.add_handler(CommandHandler("maopian", get_random_pornhub_cn)) 
    dispatcher.add_handler(CommandHandler("91porn", sex_porn)) 
    dispatcher.add_handler(CallbackQueryHandler(button))
    # log all errors
    dispatcher.add_error_handler(error)
    # Start the Bot
    j = updater.job_queue
	#调用每一分钟的发送消息
    #job_minute = j.run_repeating(callback_minute, interval=60, first=0)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()