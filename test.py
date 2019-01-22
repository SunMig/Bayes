#微信自动给某人发信息

from __future__ import unicode_literals
from threading import  Timer
from wxpy import *
import requests

bot=Bot()
def get_new1():
    url="http://open.iciba.com/dsapi/"
    r=requests.get(url)
    contents=r.json()['content']
    translation=r.json()['translation']
    return contents,translation

def send_news():
    try:
        my_friend=bot.friends().search(u'sukn')[0]
        my_friend.send(get_new1()[0])
        my_friend.send(get_new1()[1][5:])
        my_friend.send(u"from 孙猛 的心灵鸡汤！")
        t=Timer(5,send_news)
        t.start()
    except:
        my_friend=bot.friends().search('paul_sunshine')[0]
        my_friend.send(u"send failed !")

if __name__=='__main__':
    send_news()