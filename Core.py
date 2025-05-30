import requests, re, os, urllib3, json, sys
from concurrent.futures import ThreadPoolExecutor

p = ThreadPoolExecutor(20)
from tqdm import tqdm
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)
import cloudscraper
from concurrent.futures import ThreadPoolExecutor
import urllib.parse
import xml.etree.ElementTree as ET

session = requests.Session()
# 超时时间/秒
timeoutsec = 15

# 如果需要设置代理请取消注释
# proxy = "http://127.0.0.1:10809"
# session.proxies = {
#      "http": proxy,
#      "https": proxy,
# }

headers = {
    "Connection": "close",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 (From Searchgal.homes)",
}

sp = cloudscraper.create_scraper()

# 如果你想要修改正则 或者添加搜索平台 可以模仿该函数模板新建一个函数
def PinTai_Name(game: str, mode=False) -> list:
    # 设置平台的名字
    yinqin = "平台的名字"
    if mode:
        return yinqin
    try:
        # 设置好匹配的正则
        searul = re.compile(
            r"使用的正则表达式，子页面链接用(?P<URL>.*?)匹配，项目名用(?P<NAME>.*?)匹配",
            re.S,
        )

        # 设置平台的链接，搜索所使用的参数 (如果搜索页不使用GET传参s关键字，则需要另外写session规则)
        searesp = session.get(
            url="平台主链接", params={"s": game}, headers=headers, timeout=timeoutsec
        )
        if searesp.status_code != 200:
            raise Exception("自定义报错信息")

        count = 0
        gamelst = []
        for i in searul.finditer(searesp.text):
            gamelst.append({"name": i.group("NAME").strip(), "url": i.group("URL")})
            count += 1
        searesp.close()

        # 返回的内容为一个装载 包含搜索到的多个{项目名:子页面链接}字典的列表,搜索到的数量,平台的名字  (正常这里不用动)
        return [gamelst, count, yinqin]
    except Exception as e:
        # 异常处理，当搜索到的数量返回-1，会判定为搜索失败
        return [[], -1, yinqin, e]

    # 记得在底下的 search 列表追加添加新的搜索函数


def loli(game: str, mode=False) -> list:
    yinqin = "忧郁的loli"
    color = "#1FD700"
    if mode:
        return yinqin
    try:
        searul = re.compile(
            r'<p style="text-align: center;"> <a href=".*?" target="_blank">.*?<p style="text-align: center;"> <a href="(?P<URL>.*?)" title="(?P<NAME>.*?)"> <img src=',
            re.S,
        )
        searesp = session.get(
            url="https://www.ttloli.com/",
            params={"s": game},
            headers=headers,
            timeout=timeoutsec,
        )
        if searesp.status_code != 200:
            raise Exception("Search API 响应状态码为 " + str(searesp.status_code))
        count = 0
        gamelst = []
        for i in searul.finditer(searesp.text):
            if i.group("NAME") == "详细更新日志":
                continue
            gamelst.append({"name": i.group("NAME").strip(), "url": i.group("URL")})
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]


def vika(game: str, mode=False) -> list:
    yinqin = "VikaACG"
    color = "#FFD700"
    if mode:
        return yinqin
    try:
        searul = re.compile(
            r'<h2><a  target="_blank" href="(?P<URL>.*?)">(?P<NAME>.*?)<', re.S
        )
        # searul = re.compile(r'<h2><a  href="(?P<URL>.*?)">(?P<NAME>.*?)</a></h2>',re.S)
        searesp = session.post(
            url="https://www.vikacg.com/wp-json/b2/v1/getPostList",
            json={
                "paged": 1,
                "post_paged": 1,
                "post_count": 24,
                "post_type": "post-1",
                "post_cat": [6],
                "post_order": "modified",
                "post_meta": [
                    "user",
                    "date",
                    "des",
                    "cats",
                    "like",
                    "comment",
                    "views",
                    "video",
                    "download",
                    "hide",
                ],
                "metas": {},
                "search": f"{game}",
            },
            headers={
                "Connection": "close",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Content-Type": "application/json",
            },
            timeout=timeoutsec,
        )
        if searesp.status_code != 200:
            raise Exception("Search API 响应状态码为 " + str(searesp.status_code))
        restxt = (
            searesp.text.replace("\\/", "/")
            .replace("\\\\", "\\")
            .encode("utf-8")
            .decode("unicode_escape")
        )
        count = 0
        gamelst = []
        for i in searul.finditer(restxt):
            gamelst.append({"name": i.group("NAME").strip(), "url": i.group("URL")})
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]


# 倒了
# def jidian(game:str,mode=False) -> list:
#     yinqin = "极点ACG"
#     if mode: return yinqin
#     try:
#         searul = re.compile(r'<a itemprop="url" rel="bookmark" href="(?P<URL>.*?)" title=".*?" target="_blank"><span class="post-sign">.*?</span>(?P<NAME>.*?)</a></h3>',re.S)
#         searesp = session.get(url='https://lspgal.us/', params={'s':game}, headers=headers)
# if searesp.status_code != 200: raise Exception
#         count = 0
#         gamelst = []
#         for i in searul.finditer(searesp.text):
#             gamelst.append({'name':i.group('NAME').strip(),'url':i.group('URL')})
#             count += 1
#         searesp.close()
#         return [gamelst,count,yinqin]
#     except:
#         return [[],-1,yinqin]


def tianyou(game: str, mode=False) -> list:
    yinqin = "天游二次元"
    color = "#FFD700"
    if mode:
        return yinqin
    try:
        searul = re.compile(
            r'</i></a><h2><a href="(?P<URL>.*?)" title="(?P<NAME>.*?)"', re.S
        )
        searesp = session.get(
            url=f"https://www.tiangal.com/search/{game}",
            headers=headers,
            timeout=timeoutsec,
        )
        if searesp.status_code != 200:
            raise Exception("Search API 响应状态码为 " + str(searesp.status_code))
        count = 0
        gamelst = []
        for i in searul.finditer(searesp.text):
            gamelst.append({"name": i.group("NAME").strip(), "url": i.group("URL")})
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]


def acgyyg(game: str, mode=False) -> list:
    yinqin = "ACG嘤嘤怪"
    if mode:
        return yinqin
    try:
        searul = re.compile(
            r'<a  target="_blank" href="(?P<URL>.*?)" title="(?P<NAME>.*?)"  class="post-overlay">'
        )
        searesp = session.get(
            url=f"https://acgyyg.ru/",
            params={"s": game},
            headers=headers,
            timeout=timeoutsec,
        )
        if searesp.status_code != 200:
            raise Exception("Search API 响应状态码为 " + str(searesp.status_code))
        count = 0
        gamelst = []
        for i in searul.finditer(searesp.text):
            gamelst.append({"name": i.group("NAME").strip(), "url": i.group("URL")})
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]


def zygal(game: str, mode=False, zypassword="") -> list:
    yinqin = "紫缘Gal"
    if mode:
        return yinqin
    try:
        data = {
            "parent": "/",
            "keywords": game,
            "scope": 0,
            "page": 1,
            "per_page": 20,
            "password": zypassword,
        }
        searesp = session.post(
            url=f"https://galzy.eu.org/api/fs/search",
            json=data,
            headers=headers,
            timeout=timeoutsec,
        )
        resjson = json.loads(searesp.text)
        if resjson["message"] != "success":
            raise Exception(str(resjson))
        count = 0
        gamelst = []
        mainurl = "https://galzy.eu.org"
        reslen = len(resjson["data"]["content"])
        if (reslen != resjson["data"]["total"]) and (reslen != 20):
            raise Exception("访问密码错误")
        for i in resjson["data"]["content"]:
            gamelst.append(
                {
                    "name": i["name"].strip(),
                    "url": mainurl + i["parent"] + "/" + i["name"],
                }
            )
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]


# 倒了
# def xinling(game:str,mode=False) -> list:
#     yinqin = "杏铃ACG"
#     if mode: return yinqin
#     try:
#         searul = re.compile(r'<a href="(?P<URL>.*?)">(?P<NAME>.*?)</a>',re.S)
#         searesp = session.get(url='https://g.杏铃.top/', params={'q':game}, headers=headers)
#         if searesp.status_code != 200: raise Exception
#         count = 0
#         gamelst = []
#         flag = False
#         for i in searul.finditer(searesp.text):
#             if flag == False:
#                 flag = True
#                 continue
#             gamelst.append({'name':i.group('NAME').strip(),'url':i.group('URL')})
#             count += 1
#         searesp.close()
#         return [gamelst,count,yinqin]
#     except:
#         return [[],-1,yinqin]


# zg
def touch(game: str, mode=False) -> list:
    yinqin = "TouchGal"
    color = "#1FD700"
    if mode:
        return yinqin
    try:
        # searul = re.compile(r'.jpg" alt="(?P<NAME>.*?)" class="lazyload fit-cover radius8"></a></div><div class="item-body"><h2 class="item-heading"><a target="_blank" href="(?P<URL>.*?)">',re.S)
        # searesp = session.get(url='https://www.touchgal.com/', params={'s':game,'type':'post'}, headers=headers)
        searesp = session.post(
            url="https://www.touchgal.io/api/search",
            headers=headers,
            json={
                "queryString": '[{"type":"keyword","name":"' + game + '"}]',
                "limit": 20,
                "searchOption": {
                    "searchInIntroduction": False,
                    "searchInAlias": True,
                    "searchInTag": False,
                },
                "page": 1,
                "selectedType": "all",
                "selectedLanguage": "all",
                "selectedPlatform": "all",
                "sortField": "resource_update_time",
                "sortOrder": "desc",
                "selectedYears": ["all"],
                "selectedMonths": ["all"],
            },
            timeout=timeoutsec,
        )
        if searesp.status_code != 200:
            raise Exception("Search API 响应状态码为 " + str(searesp.status_code))
        resjson = json.loads(searesp.text)
        count = 0
        gamelst = []
        mainurl = "https://www.touchgal.io/"
        for i in resjson["galgames"]:
            gamelst.append({"name": i["name"].strip(), "url": mainurl + i["uniqueId"]})
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]

# cloudflare
# def sakustar(game: str, mode=False) -> list:
#     yinqin = "晴空咖啡馆"
#     color = "#1FD700"
#     if mode:
#         return yinqin
#     try:
#         searesp = sp.get(
#             url="https://api.aozoracafe.com/api/home/list?page=1&pageSize=100&search="
#             + game,
#             headers=headers,
#             timeout=timeoutsec,
#         )
#         resjson = json.loads(searesp.text)
#         if resjson["success"] != True:
#             raise Exception(str(resjson))
#         count = 0
#         gamelst = []
#         mainurl = "https://aozoracafe.com/detail/"
#         for i in resjson["data"]["list"]:
#             gamelst.append(
#                 {"name": i["title_cn"].strip(), "url": mainurl + str(i["id"])}
#             )
#             count += 1
#         searesp.close()
#         return [gamelst, count, yinqin]
#     except Exception as e:
#         try:
#             searesp.close()
#         except Exception:
#             pass
#         return [[], -1, yinqin, e]


def shinnku(game: str, mode=False) -> list:
    yinqin = "真红小站"
    color = "#1FD700"
    if mode:
        return yinqin
    try:
        searul = re.compile(
            r'<div class="p-4">.+?<div class="p-3 z-10 w-full justify-start items-center shrink-0 overflow-inherit color-inherit subpixel-antialiased rounded-t-large flex gap-3">.+?<span class="text-lg">(?P<NAME>.*?)</span>.+?<div class="relative flex w-full p-3 flex-auto flex-col place-content-inherit align-items-inherit h-auto break-words text-left overflow-y-auto subpixel-antialiased">\s*<p>路径：\s*<!-- -->\s*(?P<URL>.*?)</p>'
        )
        searesp = session.get(
            url="https://www.shinnku.com/search?q=" + game,
            headers=headers,
            timeout=timeoutsec,
        )
        if searesp.status_code != 200:
            raise Exception("Search API 响应状态码为 " + str(searesp.status_code))
        count = 0
        gamelst = []
        mainurl = "https://download.shinnku.com/file/shinnku/"
        for i in list(searul.finditer(searesp.text))[:20]:
            gamelst.append(
                {"name": i.group("NAME").strip(), "url": mainurl + urllib.parse.quote(i.group("URL"))}
            )
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]
    
def nekogal(game: str, mode=False) -> list:
    yinqin = "NekoGal"
    if mode:
        return yinqin
    try:
        searul = re.compile(
            r'<div class="item-thumbnail">\s*<a target="_blank" href="(?P<URL>.*?)">.+?" alt="(?P<NAME>.*?)" class="lazyload'
        )
        searesp = session.get(
            url="https://www.nekogal.com/?type=post&s=" + game,
            headers=headers,
            timeout=timeoutsec,
        )
        if searesp.status_code != 200:
            raise Exception("Search API 响应状态码为 " + str(searesp.status_code))
        count = 0
        gamelst = []
        for i in list(searul.finditer(searesp.text)):
            gamelst.append(
                {"name": i.group("NAME").strip().strip("-NekoGAL - Galgame传递者"), "url": i.group("URL")}
            )
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]
    
def miaoyuanlingyu(game: str, mode=False) -> list:
    yinqin = "喵源领域"
    if mode:
        return yinqin
    try:
        searul = re.compile(
            r'<div class="item-thumbnail">\s*<a target="_blank" href="(?P<URL>.*?)">.+?" alt="(?P<NAME>.*?)" class="lazyload'
        )
        searesp = session.get(
            url="https://www.nyantaku.com/?type=post&s=" + game,
            headers=headers,
            timeout=timeoutsec,
        )
        if searesp.status_code != 200:
            raise Exception("Search API 响应状态码为 " + str(searesp.status_code))
        count = 0
        gamelst = []
        for i in list(searul.finditer(searesp.text)):
            gamelst.append(
                {"name": i.group("NAME").strip().strip("-喵源领域"), "url": i.group("URL")}
            )
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]
    
def ziling(game: str, mode=False) -> list:
    yinqin = "梓澪の妙妙屋"
    color = "#1FD700"
    if mode:
        return yinqin
    try:
        data = {
            "parent": "/",
            "keywords": game,
            "scope": 0,
            "page": 1,
            "per_page": 20,
            "password": "",
        }
        searesp = session.post(
            url=f"https://zi0.cc/api/fs/search",
            json=data,
            headers=headers,
            timeout=timeoutsec,
        )
        resjson = json.loads(searesp.text)
        if resjson["message"] != "success":
            raise Exception(str(resjson))
        count = 0
        gamelst = []
        mainurl = "https://zi0.cc"
        reslen = len(resjson["data"]["content"])
        if (reslen != resjson["data"]["total"]) and (reslen != 20):
            raise Exception("访问密码错误")
        for i in resjson["data"]["content"]:
            gamelst.append(
                {
                    "name": i["name"].strip(),
                    "url": mainurl + i["parent"] + "/" + i["name"],
                }
            )
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]

def KunGal(game: str, mode=False) -> list:
    yinqin = "鲲Galgame"
    color = "#1FD700"
    if mode:
        return yinqin
    try:
        searesp = session.get(
            url=f"https://www.kungal.com/api/search?keywords={game}&type=galgame&page=1&limit=12",
            headers=headers,
            timeout=timeoutsec,
            verify=False,
        )
        resjson = json.loads(searesp.text)
        count = 0
        gamelst = []
        mainurl = "https://www.kungal.com/zh-cn/galgame/"
        for i in resjson[:20]:
            zhname = i["name"]["zh-cn"].strip()
            jpname = i["name"]["ja-jp"].strip()
            gamelst.append(
                {"name": zhname if zhname else jpname, "url": mainurl + str(i["gid"])}
            )
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]


def gallibrary(game: str, mode=False) -> list:
    yinqin = "GAL图书馆"
    color = "#1FD700"
    if mode:
        return yinqin
    try:
        searesp = session.get(
            url="https://gallibrary.pw/galgame/game/manyGame?page=1&type=1&keyWord="
            + game,
            headers=headers,
            timeout=timeoutsec,
        )
        resjson = json.loads(searesp.text)
        if resjson["code"] != 200:
            raise Exception(str(resjson))
        count = 0
        gamelst = []
        mainurl = "https://gallibrary.pw/game.html?id="
        for i in resjson["data"]:
            gamelst.append(
                {
                    "name": i["listGameText"][1]["data"].strip(),
                    "url": mainurl + str(i["id"]),
                }
            )
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]


def shenshi(game: str, mode=False) -> list:
    yinqin = "绅仕天堂"
    if mode:
        return yinqin
    try:
        searul = re.compile(
            r'-->\s*<h2 class="post-list-title">\s*<a  href="(?P<URL>.*?)">(?P<NAME>.*?)</a>\s*</h2>\s*<span class="category-meta">',
            re.S,
        )
        searesp = session.get(
            url="https://www.gogalgame.com/",
            params={"s": game},
            verify=False,
            headers=headers,
            timeout=timeoutsec,
        )
        if searesp.status_code != 200:
            raise Exception("Search API 响应状态码为 " + str(searesp.status_code))
        count = 0
        gamelst = []
        for i in searul.finditer(searesp.text):
            gamelst.append({"name": i.group("NAME").strip(), "url": i.group("URL")})
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]


# 倒了
# def acgngames(game:str,mode=False) -> list:
#     yinqin = Fore.MAGENTA + "AcgnGames" + Style.RESET_ALL
#     if mode: return yinqin
#     try:
#         searul = re.compile(r'<h2 class="kratos-entry-title-new"><a href="(?P<URL>.*?)">(?P<NAME>.*?)</a></h2>',re.S)
#         searesp = session.get(url='https://acgngames.net/', params={'s':game}, headers=headers)
#         if searesp.status_code != 200: raise Exception
#         count = 0
#         gamelst = []
#         for i in searul.finditer(searesp.text):
#             gamelst.append({'name':i.group('NAME').strip(),'url':i.group('URL')})
#             count += 1
#         searesp.close()
#         return [gamelst,count,yinqin]
#     except:
#         return [[],-1,yinqin]

# 倒了
# def ercygame(game:str,mode=False) -> list:
#     yinqin = "ErcyGame"
#     if mode: return yinqin
#     try:
#         searul = re.compile(r'<section class="hidden-xs">\s*<div class="title-article">\s*<h1><a href="(?P<URL>.*?)" target="_blank">\s*<span class="animated_h1">(?P<NAME>.*?)</span>',re.S)
#         searesp = session.get(url='https://ercygame.com/', params={'s':game}, headers=headers)
#         if searesp.status_code != 200: raise Exception
#         count = 0
#         gamelst = []
#         for i in searul.finditer(searesp.text):
#             gamelst.append({'name':i.group('NAME').strip(),'url':i.group('URL')})
#             count += 1
#         searesp.close()
#         return [gamelst,count,yinqin]
#     except:
#         return [[],-1,yinqin]


def lzacg(game: str, mode=False) -> list:
    yinqin = "量子acg"
    if mode:
        return yinqin
    try:
        searul = re.compile(
            r'><h2 class="item-heading"><a target="_blank" href="(?P<URL>.*?)">(?P<NAME>.*?)</a></h2><div',
            re.S,
        )
        searesp = session.get(
            url="https://lzacg.org/",
            params={"s": game},
            headers=headers,
            timeout=timeoutsec,
        )
        if searesp.status_code != 200:
            raise Exception("Search API 响应状态码为 " + str(searesp.status_code))
        count = 0
        gamelst = []
        for i in searul.finditer(searesp.text):
            gamelst.append({"name": i.group("NAME").strip(), "url": i.group("URL")})
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]


def fufugal(game: str, mode=False) -> list:
    yinqin = "FuFuACG"
    if mode:
        return yinqin
    ynheaders = {
        "Connection": "close",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
    }
    try:
        searesp = session.get(
            url="https://www.fufugal.com/so",
            params={"query": game},
            headers=ynheaders,
            timeout=timeoutsec,
        )
        if searesp.status_code != 200:
            raise Exception
        dt = json.loads(searesp.text)
        count = len(dt["obj"])
        gamelst = []
        for i in dt["obj"]:
            gamelst.append(
                {
                    "url": "https://www.fufugal.com/detail?id=" + str(i["game_id"]),
                    "name": i["game_name"],
                }
            )
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]


def jimengacg(game: str, mode=False) -> list:
    yinqin = "绮梦ACG"
    color = "#1FD700"
    if mode:
        return yinqin
    try:
        # searul = re.compile(r'<div class="flex-1">\s*?<a href="(?P<URL>.*?)" class="text-lg xl:text-xl font-semibold line-2">(?P<NAME>.*?)</a>',re.S)
        searul = re.compile(
            r'<div class="p-2 sm:p-3">.+?<a href="(?P<URL>.*?)" class="dark:hover:text-\[var\(--primary\)\] hover:text-\[var\(--primary\)\] duration-300 text-sm sm:text-base font-bold line-clamp-9">(?P<NAME>.*?)</a>',
            re.S,
        )
        searesp = session.get(
            url=f"https://game.acgs.one/search/{game}",
            headers=headers,
            timeout=timeoutsec,
        )
        if searesp.status_code != 200:
            raise Exception("Search API 响应状态码为 " + str(searesp.status_code))
        count = 0
        gamelst = []
        for i in searul.finditer(searesp.text):
            gamelst.append({"name": i.group("NAME").strip(), "url": i.group("URL")})
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]


def qingjiacg(game: str, mode=False) -> list:
    yinqin = "青桔ACG"
    color = "#1FD700"
    if mode:
        return yinqin
    try:
        searul = re.compile(
            r'" class="lazyload fit-cover radius8"></a></div><div class="item-body"><h2 class="item-heading"><a href="(?P<URL>.*?)">(?P<NAME>.*?)</a></h2>',
            re.S,
        )
        searesp = sp.get(
            url="https://www.qingju.org/",
            params={"s": game, "type": "post"},
            headers=headers,
            timeout=timeoutsec,
        )
        # print(searesp.text)
        if searesp.status_code != 200:
            raise Exception("Search API 响应状态码为 " + str(searesp.status_code))
        count = 0
        gamelst = []
        for i in searul.finditer(searesp.text):
            if "</p>" in i.group("URL"):
                continue
            gamelst.append({"name": i.group("NAME").strip(), "url": i.group("URL")})
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]
    
def lstacg(game: str, mode=False) -> list:
    yinqin = "莉斯坦ACG"
    color = "#1FD700"
    if mode:
        return yinqin
    try:
        searesp = session.get(
            url=f"https://www.limulu.moe/search.xml",
            headers=headers,
            timeout=timeoutsec,
        )
        if searesp.status_code != 200:
            raise Exception("Search API 响应状态码为 " + str(searesp.status_code))
        root = ET.fromstring(searesp.text)
        count = 0
        gamelst = []
        main_URL = "https://www.limulu.moe"
        for entry in root.findall('entry'):
            if game not in entry.findtext("title"): continue
            gamelst.append({"name": entry.findtext("title").strip(), "url": main_URL + entry.findtext("url")})
            count += 1
        searesp.close()
        return [gamelst, count, yinqin]
    except Exception as e:
        try:
            searesp.close()
        except Exception:
            pass
        return [[], -1, yinqin, e]


# Cli命令行搜索平台
search = [
    vika,
    touch,
    # sakustar,
    tianyou,
    shinnku,
    KunGal,
    shenshi,
    acgyyg,
    loli,
    gallibrary,
    lzacg,
    fufugal,
    jimengacg,
    qingjiacg,
    nekogal,
    miaoyuanlingyu,
    ziling,
    lstacg
]

# GUI图形化搜索平台
# FFD700 金色  1FD700 绿色  FFFFFF 白色
searchGUI = [
    (vika, "#FFD700", True),
    (touch, "#1FD700", False),
    (zygal, "#FFFFFF", False),
    # (sakustar, "#1FD700", False),
    (shinnku, "#1FD700", False),
    (KunGal, "#1FD700", False),
    (tianyou, "#FFFFFF", False),
    (shenshi, "#FFD700", True),
    (acgyyg, "#FFFFFF", False),
    (loli, "#1FD700", False),
    (gallibrary, "#1FD700", False),
    (lzacg, "#FFFFFF", False),
    (fufugal, "#FFFFFF", False),
    (jimengacg, "#1FD700", False),
    (qingjiacg, "#1FD700", False),
    (nekogal, "#FFFFFF", False),
    (miaoyuanlingyu, "#FFFFFF", False),
    (ziling, "#1FD700", False),
    (lstacg, "#1FD700", False),
]
tmp = None
color_map = {"#FFD700": "gold", "#1FD700": "lime", "#FFFFFF": "white"}

PLATFORMS = [
    {
        "func": func,
        "color": color_map.get(color, "unknown"),
        "magic": magic,
        "name": func("", True),
    }
    for func, color, magic in searchGUI
]
