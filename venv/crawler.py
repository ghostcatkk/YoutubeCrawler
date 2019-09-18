import requests
import re
import json
import os
import urllib.parse
import imageio
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

headers = {
'cookie': 'SID=mQfa10bu9jyzXTsWUk2GAXJI-GFCuWLJ9ExQ2d4W8yQVjaXjM5D5Ui7FXxSnT1bAe8uJNw.; HSID=A-4rkG30jU_BY9Z0V; '
          'SSID=AuzF2RtmZQaGz_VaW; APISID=71EBeTH5FFnbtpOq/A2qYIVtATH26PG6EJ; SAPISID=EygY63saYSTilSC3/AoBbqbS45m_u6qVL7;'
          ' VISITOR_INFO1_LIVE=tpa1hNTO4T8; YSC=mycIWWHYTHg; '
          'LOGIN_INFO=AFmmF2swRgIhAPBW961i0YXDlkcDEwKk5b15NulI2x3O5BaWOhUbcF5eAiEAoFFlZKYRqz7K1dFFufVne6nhKKN'
          '_nRe4mMKYuLu5Z8M:QUQ3MjNmeUhGVG1oZVo2SkZtTzFaVDZxdXBQYTRSOC1CNDBiNXJfdTljSHQycldWS05GTWdJcFJya1p5RUhjdnh'
          'EajN6VS05VmNYZDV4WlhtSTlaTXpHcFltT2F1Q0syTEIzTzJfdmdOVzVfV2J0XzlPeV9zRzBSd0FCTHBfbFNVUWtnWkRORVk4aGJFTjVQVkpNd'
          'E5GZEt4ajVQMTFBbnpaOW9yZVh6c0wyNGJWQjFrd1pkdVNB; s_gl=ca02b225c88e6fda0cbe664706f57e38cwIAAABUVw==; PREF=f1='
          '50000000&f4=4000000&f5=30&al=zh-CN+en-SG; SIDCC=AN0-TYvrADoJ9K6Kzq1p-FO8i8vqkR0KV4ND6S0x-YQSUO3JikyOC_R3CTevp7LM9VN3NEQnZw',0
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 S'
}

addon = "&ratebyte = yes"
title = "COOLEST GUMI"
if not os.path.exists("Midea"):
    os.mkdir("Midea")


def crawl(url):
    """
    主方法
    :param url: 视频链接
    :return
     """
    headless(url)
    json = analyse(url)
    video = json["url"][0]+addon
    video = requests.get(video, headers=headers, stream=True)
    downloader(video, "video", ".mp4")
    for i in range(0,len(json["type"])):
        regular = re.search('(audio/mp4)', json["type"][i])
        if regular is not None:
            audio = json["url"][i]
            audio = requests.get(audio, headers=headers, stream=True)
            downloader(audio, "audio", ".mp3")
            break
    video_add_mp3("Midea" + os.sep + "video.mp4","Midea" + os.sep + "audio.mp3")
    os.remove("Midea" + os.sep + "video.mp4")
    os.remove("Midea" + os.sep + "audio.mp3")
    os.rename("Midea/video-txt.mp4", "Midea" + os.sep + title+".mp4")


def analyse(url):
    """
    分析视频链接,提取json
    :param url: 视频链接
    :return: json
     """
    res = requests.get(url, headers=headers)
    regular = re.search('"args":({".*?"}),"', res.text)
    if regular is None:
        regular = re.search('"args":({.*?})};', res.text)
    js = json.loads(regular.group(1))
    videoJson = urllib.parse.parse_qs(js["adaptive_fmts"])
    return videoJson


def downloader(video, name, type):
    chunk_size = 1024
    size = 0
    if video.status_code == 200:
        fileName = "Midea" + os.sep + name + type
        with open(fileName, 'wb') as file:
            for data in video.iter_content(chunk_size=chunk_size):
                file.write(data)
                size += len(data)


def video_add_mp3(file_name, mp3_file):
    """
     视频添加音频
    :param file_name: 传入视频文件的路径
    :param mp3_file: 传入音频文件的路径
    :return:
    """
    outfile_name = file_name.split('.')[0] + '-txt.mp4'
    subprocess.call('ffmpeg -i ' + file_name
                    + ' -i ' + mp3_file + ' -strict -2 -f mp4 '
                    + outfile_name, shell=True)


def headless(url):
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path="/home/wyvern/PycharmProjects/YoutubeCrawler/venv/headless/chromedriver",
                              options=chrome_options)
    driver.get(url)
    global title
    title = driver.title


if __name__ == '__main__':
    crawl("https://www.youtube.com/watch?v=67MwE9pWTKQ&list=RD67MwE9pWTKQ&start_radio=1")
    print("done!")
