# -*- coding:utf-8 -*-
import websocket
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
import os
import _thread as thread
from datetime import datetime
from time import mktime
# 【关键修复】下面这行之前漏掉了，导致报错
from wsgiref.handlers import format_date_time

# 尝试导入 pygame
try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False
    print(" 警告: 未安装 pygame，无法播放声音。请运行 pip install pygame")

# ========== 科大讯飞配置 ==========
APPID = '257873c7'
APIKEY = '9734aaeac69824db067c630fc5a097da'
APISECRET = 'YWQ5MDMwOGUxODg0NjhiMTIxM2ExYTUw'
REQURL = "wss://tts-api.xfyun.cn/v2/tts"
# ================================

# 全局变量
g_tts_file = ""
g_tts_complete = False
g_error_msg = ""

class Ws_Param(object):
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # 公共参数
        self.CommonArgs = {"app_id": self.APPID}
        
        # 业务参数
        self.BusinessArgs = {
            "aue": "lame",
            "sfl": 1,
            "auf": "audio/L16;rate=16000",
            "vcn": "xx5_lingfeiyi_flow", # 基础发音人
            "tte": "utf8",
            "speed": 50,
            "volume": 50,
            "pitch": 50
        }
        
        # 数据参数
        self.Data = {
            "status": 2,
            "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")
        }

    def create_url(self):
        url = REQURL
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        return url + '?' + urlencode(v)

def on_message(ws, message):
    global g_tts_file, g_tts_complete, g_error_msg
    try:
        message = json.loads(message)
        code = message["code"]
        
        if code != 0:
            g_error_msg = message["message"]
            print(f"\n 讯飞API报错: Code {code}, Message: {g_error_msg}")
            g_tts_complete = True
            return

        data = message["data"]
        audio = data["audio"]
        audio = base64.b64decode(audio)
        status = data["status"]

        if status == 2:
            ws.close()
            g_tts_complete = True
        
        # 写入文件
        with open(g_tts_file, 'ab') as f:
            f.write(audio)
            
    except Exception as e:
        print(f"接收消息异常: {e}")
        g_tts_complete = True

def on_error(ws, error):
    print(f"WebSocket连接错误: {error}")

def on_close(ws, a, b):
    global g_tts_complete
    g_tts_complete = True

def on_open(ws):
    global ws_param
    def run(*args):
        d = {
            "common": ws_param.CommonArgs,
            "business": ws_param.BusinessArgs,
            "data": ws_param.Data,
        }
        d = json.dumps(d)
        ws.send(d)
    thread.start_new_thread(run, ())

def play_mp3(file_path):
    """使用 Pygame 播放 MP3"""
    if not HAS_PYGAME:
        return
    
    try:
        # 重新初始化 mixer 以避免频率冲突
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        pygame.mixer.init()
            
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        pygame.mixer.music.unload()
            
    except Exception as e:
        print(f"播放音频出错: {e}")

def text_to_speech(text):
    """主入口函数"""
    global g_tts_file, g_tts_complete, ws_param
    
    if not text:
        return

    # 1. 准备文件
    if not os.path.exists("tts_audio"):
        os.makedirs("tts_audio")
    
    filename = f"tts_{int(time.time())}.mp3"
    g_tts_file = os.path.join("tts_audio", filename)
    
    g_tts_complete = False
    open(g_tts_file, 'w').close()
    
    # 2. 启动 WebSocket
    ws_param = Ws_Param(APPID, APIKEY, APISECRET, text)
    wsUrl = ws_param.create_url()
    
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    
    # 3. 播放
    if os.path.exists(g_tts_file) and os.path.getsize(g_tts_file) > 0:
        play_mp3(g_tts_file)
        # 播放完删除
        try:
            os.remove(g_tts_file)
        except:
            pass
    else:
        print("未生成音频文件，请检查上方报错。")

if __name__ == "__main__":
    print("开始测试语音合成...")
    text_to_speech("恭喜你，语音模块现在完全修好了！")
    print("测试结束")