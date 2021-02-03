# webio整合flask需要
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
# 脚本需要
from pywebio.input import *
from pywebio.output import *
from pywebio.session import set_env
# 自己程序需要
import json
import requests
from bs4 import BeautifulSoup


# 自己程序
def task_func():
    # 不用登录就能查看知乎热榜的链接
    zhihu_hot_url = 'https://www.zhihu.com/billboard'
    # 获取网页内容
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}
    resp = requests.get(zhihu_hot_url,headers=headers)
    # bs4解析网页内容
    soup = BeautifulSoup(resp.text,features="html.parser")
    hot_topic = soup.find(attrs={"id": "js-initialData"})
    # 利用页面中嵌入的json解析知乎热榜
    json_raw = str(hot_topic).replace('<script id="js-initialData" type="text/json">','').replace('</script>','')
    hot_json = json.loads(json_raw)
    contents = hot_json['initialState']['topstory']['hotList']
    html = ''
    # 用print输出知乎热榜
    for content in contents:
        html = html + '####'+content['target']['titleArea']['text'] + '\n'
        html = html + '回答：'+str(content['feedSpecific']['answerCount'])+'个'+ '\n\n'
        if content['target']['excerptArea']['text'] != '':
            html = html + '简介：'+content['target']['excerptArea']['text']+ '\n\n'
        html = html + '链接：'+content['target']['link']['url']+ '\n'
        html = html + '*'*10+ '\n'
        put_markdown(html)
        html = ''

# Flask+WebIO框架
app = Flask(__name__)

# task_func 为使用PyWebIO编写的任务函数
app.add_url_rule('/io', 'webio_view', webio_view(task_func),
            methods=['GET', 'POST', 'OPTIONS'])  # 接口需要能接收GET、POST和OPTIONS请求

@app.route('/')
@app.route('/<path:static_file>')
def serve_static_file(static_file='index.html'):
    """前端静态文件托管"""
    return send_from_directory(STATIC_PATH, static_file)

# if __name__ == '__main__':
#     app.run(debug=True)