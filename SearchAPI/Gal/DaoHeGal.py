from ..common import *


def DaoHeGal(game: str, mode=False) -> list:
    yinqin = "稻荷GAL"
    if mode:
        return yinqin
    try:
        searesp = session.get(
            # Limit硬编码：改变无效
            url="https://inarigal.com/api/home/list?page=1&pageSize=18&search=" + game,
            headers=headers,
            timeout=timeoutsec,
        )
        resjson = json.loads(searesp.text)
        if resjson["success"] != True:
            raise Exception(str(resjson))
        count = 0
        gamelst = []
        mainurl = "https://inarigal.com/detail/"
        for i in resjson["data"]["list"][:MAX_RESULTS]:
            gamelst.append(
                {"name": i["title_cn"].strip(), "url": mainurl + str(i["id"])}
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


DaoHeGal.color = "lime"
DaoHeGal.magic = False
