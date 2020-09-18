import requests
import re
import os
from time import sleep as tsleep

def wifi_detect():
    result = os.popen('netsh WLAN show interfaces')
    context=result.read()
    for line in context.splitlines():
        if '系统上没有无线接口' in line:
            return 'False'
        if 'SSID' in line:
            if 'BSSID' in line:
                pass
            else:
                result.close()
                SSID=line.split(':')[1].strip(' ')
                return SSID


print('自动登录正在工作，数据参见本工具同目录下的autologin_OTP.txt')
OTP_path=os.getcwd()+'\\autologin_OTP.txt'
if os.path.exists(OTP_path) == True:
    with open(OTP_path,'r') as OTP:
        for line in OTP.readlines():
            line=line.strip('\n')
            if 'username' in line:
                username=line.split(':')[1]
            if 'password' in line:
                password=line.split(':')[1]
            if 'ISP' in line:
                channelshow=line.split(':')[1]
else:
    with open(OTP_path,'w') as OTP:
        print('OTP文件不存在，本工具仅在第一次使用或删除autologin_OTP.txt后需要手动输入')
        username=input('输入学号：')
        password=input('输入密码：')
        channelshow_number=input('输入运营商（1为中国移动，2为中国电信）：')
        if channelshow_number=='1':
            channelshow='中国移动'
        elif channelshow_number=='2':
            channelshow='中国电信'
        OTP.writelines('//自动登录工具依赖本文件，请勿删除'+'\n'+
        '//示例：'+'\n'
        '//username:输入学号'+'\n'+
        '//password:输入密码'+'\n'+
        '//ISP:输入运营商（中国移动或中国电信）'+'\n'+
        '=====以下为你需要输入的数据====='+'\n'+
        'username:%s'%(username)+'\n'+
        'password:%s'%(password)+'\n'+
        'ISP:%s'%(channelshow)
        )

SSID=wifi_detect()
if SSID == 'False':
    pass
else:
    while SSID != 'Njtech-Home':
        SSID=wifi_detect()
        print('当前Wifi未连接到 Njtech-Home，正在等待..')

if SSID == 'Njtech-Home':
    tsleep(2)

if channelshow=='中国移动':
    channel='@cmcc'
elif channelshow=='中国电信':
    channel='@telecom'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
    }

session=requests.session()

def get_post_url():
    page=session.get('http://i.njtech.edu.cn/')
    text=page.text
    url_param=re.findall('(?<=action=").*(?=" method)',text)[0]
    execution=re.findall('(?<=execution" value=").*(?=" />)',text)[0]
    lt=re.findall('(?<=lt" value=").*(?=" />)',text)[0]
    post_url='https://u.njtech.edu.cn'+url_param
    return post_url,execution,lt

post_url,execution,lt=get_post_url()

params={
    'username':username,
    'password':password,
    'channelshow':channelshow,
    'channel':channel,
    'lt':lt,
    'execution':execution,
    '_eventId':'submit',
    'login':'登录'
}

login_response=session.post(post_url,params,headers)
os.system('PAUSE')
