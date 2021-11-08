import inspect
import random
import requests
import telebot
import sqlite3
import pymysql
import pyodbc
import mysql.connector as connector
import yagmail
import socket


class Treasure:
    def __init__(self, Id: int, InnerId: str, Description: str, UID: int, WID: int):
        self.Id = Id
        self.InnerID = InnerId
        self.Description = Description
        self.UID = UID
        self.WID = WID

    def __init__(self):
        self.Id = 0
        self.InnerID = ""
        self.Description = ""
        self.UID = 0
        self.WID = 0

    def __repr__(self):
        return "Id:" + str(
            self.Id) + "; InnerID:" + self.InnerID + "; Description: " + self.Description + "; UID:" + str(
            self.UID) + "; WID:" + str(self.WID)


class WebPage:
    def __init__(self, Id: int, Url: str, MinId: int, MaxId: int, BaseTags: str, BaseAntiTags: str, TagMarkL: str,
                 TagMarkR: str, SearchPage: str):
        self.Id = Id
        self.Url = Url
        self.MinId = MinId
        self.MaxId = MaxId
        self.BaseTags = BaseTags
        self.BaseAntiTags = BaseAntiTags
        self.TagMarkL = TagMarkL
        self.TagMarkR = TagMarkR
        self.SearchPage = SearchPage

    def __init__(self):
        self.Id = 0
        self.Url = ""
        self.MinId = 0
        self.MaxId = 0
        self.BaseTags = ""
        self.BaseAntiTags = ""
        self.TagMarkL = ""
        self.TagMarkR = ""
        self.SearchPage = ""

    def UrlDual(self):
        if len(self.Url.split(' ')) > 1:
            return True
        return False

    def ConstructUrl(self, innerid: int):
        linkparts = self.Url.split(' ')
        if len(linkparts) > 1:
            return linkparts[0] + str(innerid) + linkparts[1]
        else:
            return self.Url + str(innerid)

    def __repr__(self):
        return "Id:" + str(self.Id) + "; Url: " + self.Url + "; MinId: " + str(self.MinId) + "; MaxId: " + str(
            self.MaxId) + "; BaseTags: " + self.BaseTags + "; BaseAntiTags: " + self.BaseAntiTags + "; TagMarkL: " + self.TagMarkL + "; TagMarkR: " + self.TagMarkR + "; SearchPage: " + self.SearchPage


class UWebSett:
    def __init__(self, Id, MinId: int, MaxId: int, BaseTags: str, BaseAntiTags: str, StrictTag: str, TGID: int,
                 WID: int):
        self.Id = Id
        self.MinId = MinId
        self.MaxId = MaxId
        self.BaseTags = BaseTags
        self.BaseAntiTags = BaseAntiTags
        self.StrictTag = StrictTag
        self.TGID = TGID
        self.WID = WID

    def __init__(self):
        self.Id = 0
        self.MinId = 0
        self.MaxId = 0
        self.BaseTags = ""
        self.BaseAntiTags = ""
        self.StrictTag = True
        self.TGID = 0
        self.WID = 0

    def __repr__(self):
        return "MinID: " + str(self.MinId) + "; MaxID: " + str(
            self.MaxId) + "; Base Tags: " + self.BaseTags + "; Base Anti Tags: " + self.BaseAntiTags + "; Strict tag: " + str(
            bool(self.StrictTag))


def SendMessage(text: str, reciever: str = "michelotakuwatson@gmail.com", subject: str = "Picker message"):
    yag = yagmail.SMTP("michelotakuwatson@gmail.com", "I.am.the.sauce lord")
    yag.send(reciever, subject, text)


def ProcessError(err: BaseException, funcName: str, message=None, bot=None):
    errMsg = "Read about it and retry: " + str(err)
    if message is None or bot is None:
        bot.reply_to(message, funcName + "(): " + errMsg)
    print(funcName + "(): " + errMsg)
    SendMessage(funcName + "(): " + errMsg, "michelotakuwatson@gmail.com", "ERROR")

def GetPageText(url:str):
    return requests.get(url).text.lower()


def TagsFound(tags, pageText: str, tagmarkL: str, tagmarkR: str):
    res = []
    for el in tags:
        if pageText.__contains__(tagmarkL + el + tagmarkR):
            res.append(el)
        else:
            print("!" + tagmarkL + el + tagmarkR)
    return res


def AntiTagsFound(antitags, pageText: str, tagmakrL: str, tagmarkR: str):
    res = []
    for el in antitags:
        if pageText.__contains__(tagmakrL + el + tagmarkR):
            res.append(el)
    return res


def GetPageTags(url: str, tags):
    matches = []
    text = requests.get(url).text
    for t in tags:
        if text.__contains__(t):
            matches.append(t)
    return matches


def GetTagsById(wp: WebPage, Id):
    tags = wp.BaseTags.split(';')
    resTags = TagsFound(tags, GetPageText(wp.ConstructUrl(Id)), wp.TagMarkL, wp.TagMarkR)
    return resTags


def RecreateWST():
    conn = sqlite3.connect("treasure.db")
    command = conn.cursor()
    deleteQuery = r"drop table if exists UserWebSetts"
    command.execute(deleteQuery)  # Fixed str size
    createquery = r"create table UserWebSetts(Id integer primary key,MinId integer, MaxId integer, BaseTags text,BaseAntiTags text,StrictTag int, TGID integer, WID integer)"
    command.execute(createquery)  # Fixed str size
    conn.commit()
    conn.close()


def RecreateWPT():
    conn = sqlite3.connect("treasure.db")
    command = conn.cursor()
    deleteQuery = r"drop table if exists WebPages"
    command.execute(deleteQuery)  # Fixed str size
    createquery = r"create table WebPages(Id integer primary key, Url text, MinId integer, MaxId integer, BaseTags text,BaseAntiTags text, TagMarkL text, TagMarkR text, SearchPage text)"
    command.execute(createquery)  # Fixed str size
    conn.commit()
    conn.close()


def RecreateTRT():
    conn = sqlite3.connect("treasure.db")
    command = conn.cursor()
    deleteQuery = r"drop table if exists Treasures"
    command.execute(deleteQuery)  # Fixed str size
    createquery = r"create table Treasures(Id integer primary key, InnerID text, Description text, TGID integer, WID integer)"
    command.execute(createquery)  # Fixed str size
    conn.commit()
    conn.close()


def CheckTRT():
    conn = sqlite3.connect("treasure.db")
    command = conn.cursor()
    createquery = r"create table if not exists Treasures(Id integer primary key, InnerID text, Description text, TGID integer, WID integer)"
    command.execute(createquery)  # Fixed str size
    conn.commit()
    conn.close()


def AddTreasure(url: str, innerid: str, desc: str, tgid: int):
    CheckTRT()
    ws = GetWebSettByTGID(tgid)
    wp = GetWebPageByUrl(url)
    if wp.Id > 0:
        addQuery = "Insert into Treasures (InnerID, Description, TGID, WID) values('" + str(innerid) + "', '" + str(
            desc) + "', " + str(ws.Id) + ", " + str(
            wp.Id) + ")"
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        command.execute(addQuery)
        conn.commit()
        conn.close()
        print("Treasure saved")
        return True
    else:
        print("No such website: " + url)
        SendMessage("No such website: " + url)
    return False


def RecreateDB():
    RecreateWST()
    RecreateWPT()
    RecreateTRT()


def GetUrlPage(url: str):
    return url[:url.rindex('/') + 1]


def GetUrlId(url):
    return url[url.rindex('/') + 1:]


class RTFResult:
    def __init__(self, attempts, tags, antitags, innerid, wp):
        self.attempts = attempts
        self.tags = tags
        self.antitags = antitags
        self.innerid = innerid
        self.wp = wp


class RResult:
    def __init__(self, tags, antitags, innerid, wp):
        self.tags = tags
        self.antitags = antitags
        self.innerid = innerid
        self.wp = wp


def ClearEmptyElems(arr):
    res = []
    for el in arr:
        if len(el.strip(' ')) > 0:
            res.append(el)
    return res


def RandomSingle(wp: WebPage, stct: bool = False):
    print(str(wp.MinId) + " " + str(wp.MaxId) + " " + wp.TagMarkL + " " + wp.TagMarkR)
    iid = random.randint(wp.MinId, wp.MaxId)
    url = wp.ConstructUrl(iid)
    tags = wp.BaseTags.split(';')
    antis = wp.BaseAntiTags.split(';')
    if not stct:
        wp.TagMarkR = ""
        wp.TagMarkL = ""
    pagetext=GetPageText(url)
    resTags = ClearEmptyElems(TagsFound(tags, pagetext, wp.TagMarkL, wp.TagMarkR))
    resAnti = ClearEmptyElems(AntiTagsFound(antis, pagetext, wp.TagMarkL, wp.TagMarkR))
    return RResult(resTags, resAnti, iid, wp)


def RandomTillFind(wp: WebPage, stct: bool = False):
    attempts = 1
    iid = random.randint(wp.MinId, wp.MaxId)
    url = wp.ConstructUrl(iid)
    tags = ClearEmptyElems(wp.BaseTags.split(';'))
    antis = ClearEmptyElems(wp.BaseAntiTags.split(';'))
    pagetext = GetPageText(url)
    resTags = ClearEmptyElems(TagsFound(tags, pagetext, wp.TagMarkL, wp.TagMarkR))
    resAnti = ClearEmptyElems(AntiTagsFound(antis, pagetext, wp.TagMarkL, wp.TagMarkR))
    if len(resTags) == 0 or len(resAnti) != 0:
        if stct:
            while (len(resTags) == 0 and len(tags) != 0) or (len(resAnti) != 0 and len(antis) != 0):
                attempts += 1
                iid = random.randint(wp.MinId, wp.MaxId)
                url = wp.ConstructUrl(iid)
                pagetext = GetPageText(url)
                if len(tags) == 0:
                    resTags = ClearEmptyElems(TagsFound(tags, pagetext, "", ""))
                else:
                    resTags = ClearEmptyElems(TagsFound(tags, pagetext, wp.TagMarkL, wp.TagMarkR))
                if len(antis) == 0:
                    resAnti = ClearEmptyElems(AntiTagsFound(antis, pagetext, "", ""))
                else:
                    resAnti = ClearEmptyElems(AntiTagsFound(antis, pagetext, wp.TagMarkL, wp.TagMarkR))
        else:
            while (len(resTags) == 0 and len(tags) != 0) or (len(resAnti) != 0 and len(antis) != 0):
                attempts += 1
                iid = random.randint(wp.MinId, wp.MaxId)
                url = wp.ConstructUrl(iid)
                pagetext = GetPageText(url)
                resTags = ClearEmptyElems(TagsFound(tags, pagetext, "", ""))
                resAnti = ClearEmptyElems(AntiTagsFound(antis, pagetext, "", ""))
    return RTFResult(attempts, resTags, resAnti, iid, wp)


def UserSettFromWeb(tup):
    uw = UWebSett()
    uw.Id = tup[0]
    uw.MinId = tup[1]
    uw.MaxId = tup[2]
    uw.BaseTags = tup[3]
    uw.BaseAntiTags = tup[4]
    uw.StrictTag = tup[5]
    uw.TGID = tup[6]
    uw.WID = tup[7]
    return uw


def WebPageFromTup(tup):
    wp = WebPage()
    wp.Id = tup[0]
    wp.Url = tup[1]
    wp.MinId = tup[2]
    wp.MaxId = tup[3]
    wp.BaseTags = tup[4]
    wp.BaseAntiTags = tup[5]
    wp.TagMarkL = tup[6]
    wp.TagMarkR = tup[7]
    wp.SearchPage = tup[8]
    return wp


def TreasureFromTup(tup):
    tr = Treasure()
    tr.Id = int(tup[0])
    tr.InnerID = tup[1]
    tr.Description = tup[2]
    tr.UID = int(tup[3])
    tr.WID = int(tup[4])
    return tr


def getWebSetts():
    conn = sqlite3.connect("treasure.db")
    command = conn.cursor()
    command.execute('Select * from UserWebSetts')
    preresult = command.fetchall()
    result = list()
    for el in preresult:
        result.append(UserSettFromWeb(el))
    conn.close()
    return result


def getWebPages():
    conn = sqlite3.connect("treasure.db")
    command = conn.cursor()
    command.execute('Select * from WebPages')
    preresult = command.fetchall()
    result = list()
    for el in preresult:
        result.append(WebPageFromTup(el))
    conn.close()
    return result;


def getTreasures():
    conn = sqlite3.connect("treasure.db")
    command = conn.cursor()
    command.execute('Select * from Treasures')
    preresult = command.fetchall()
    result = list()
    for el in preresult:
        result.append(TreasureFromTup(el))
    conn.close()
    return result;


def GetTreasureById(id):
    trs = getTreasures()
    for el in trs:
        if el.Id == id:
            return el
    return Treasure()


def GetWebPageById(id):
    wps = getWebPages()
    for el in wps:
        if el.Id == id:
            return el
    return WebPage()


def GetWebPageByUrl(url: str):
    wps = getWebPages()
    for el in wps:
        if el.Url == url:
            return el
    return WebPage()


def GetWebSettByTGID(tgid):
    wss = getWebSetts()
    for el in wss:
        if el.TGID == tgid:
            return el
    return UWebSett()


def UserSettsExist(tgid):
    uss = getWebSetts()
    for el in uss:
        if el.TGID == tgid:
            return True
    return False


def WebPageExist(id):
    wps = getWebPages()
    wid = int(id)
    for el in wps:
        if el.Id == wid:
            print(str(el.Id) + " == " + str(wid))
            return True
    return False


def TreasureExists(id):
    trs = getTreasures()
    tid = int(id)
    for el in trs:
        if el.Id == tid:
            print(str(el.Id) + " == " + str(tid))
            return True
    return False


def CreateTreasure(innerid: str, desc: str, uid: int, sid: int):
    newTrsQuery = "Insert into Treasures(InnerID, Description, UID, SID) values('" + str(innerid) + "', '" + str(
        desc) + "'," + str(uid) + "," + str(sid) + ")"
    conn = sqlite3.connect("treasure.db")
    command = conn.cursor()
    command.execute(newTrsQuery)
    conn.commit()
    conn.close()


def CreateWebSett(minid: int, maxid: int, bt: str, bat: str, stct: bool, tgid: int):
    newWssQuery = "Insert into userwebsetts (MinId,MaxId,BaseTags,BaseAntiTags,StrictTag,TGID,WID) values(" + minid + ", " + maxid + ", '" + bt + "', '" + bat + "'," + str(
        int(stct)) + "'," + tgid + ");"
    conn = sqlite3.connect("treasure.db")
    command = conn.cursor()
    command.execute(newWssQuery)
    conn.commit()
    conn.close()


def CreateWebPage(minid: int, maxid: int, bt: str, bat: str, tgmkl: str, tgmkr: str, srchpg: str):
    newWpsQuery = "Insert into webpages (MinId, MaxId, BaseTags, BaseAntiTags, TagMarkL, TagMarkR, SearchPage) values (" + str(
        minid) + ", " + str(
        maxid) + ", '" + bt + "', '" + bat + "', '" + tgmkl + "', '" + tgmkr + "', '" + srchpg + "');"
    conn = sqlite3.connect("treasure.db")
    command = conn.cursor()
    command.execute(newWpsQuery)
    conn.commit()
    conn.close()


def CreateEmptyWebSett(tgid):
    newWssQuery = "Insert into userwebsetts (MinId,MaxId,BaseTags,BaseAntiTags,StrictTag,TGID,WID) values(0, 0, '', '', 1, " + str(
        tgid) + ", 0);"
    conn = sqlite3.connect("treasure.db")
    command = conn.cursor()
    command.execute(newWssQuery)
    conn.commit()
    conn.close()


def CreateWebPage(url: str, minid: int, maxid: int, bt: str, bat: str, tgmkl: str, tgmkr: str, srchpg: str):
    newWpsQuery = "Insert into webpages (MinId, MaxId, BaseTags, BaseAntiTags, TagMarkL, TagMarkR, SearchPage) values ('" + url + "'," + minid + ", " + maxid + ", '" + bt + "', '" + bat + "', '" + tgmkl + "', '" + tgmkr + "', '" + srchpg + "');"
    conn = sqlite3.connect("treasure.db")
    command = conn.cursor()
    command.execute(newWpsQuery)
    conn.commit()
    conn.close()


def CreateEmptyWebPage():
    newWpsQuery = "Insert into webpages (Url ,MinId, MaxId, BaseTags, BaseAntiTags, TagMarkL, TagMarkR, SearchPage) values ('', 0, 0, '', '', '', '', '');"
    conn = sqlite3.connect("treasure.db")
    command = conn.cursor()
    command.execute(newWpsQuery)
    conn.commit()
    conn.close()


def UpdatePageBaseTags(url: str, id: int):
    print("WID: " + str(id))
    if WebPageExist(id):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update WebPages set url='" + url + "' where id=" + str(id)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Test update web tags success")
    else:
        print("Web page not found")


def UpdateTreasureDesc(desc: str, itemid: int):
    print("ITEMID: " + str(itemid))
    if UserSettsExist(itemid):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update Treasures set Description='" + desc + "' where Id=" + str(itemid)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Test update tags success")
    else:
        print("Create item on id ")


def UpdateTreasureInnerId(innerid: str, itemid: int):
    print("ITEMID: " + str(innerid))
    if UserSettsExist(itemid):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update Treasures set InnerID='" + innerid + "' where Id=" + str(itemid)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Test update tags success")
    else:
        print("Created settings item, repeat")


def UpdateBaseTags(bt: str, tgid: int):
    print("TGID: " + str(tgid))
    if UserSettsExist(tgid):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update UserWebSetts set baseTags='" + bt + "' where tgid=" + str(tgid)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Test update tags success")
    else:
        CreateEmptyWebSett(tgid)
        print("Created settings item, repeat")


def UpdatePageBaseTags(bt: str, id: int):
    print("WID: " + str(id))
    if WebPageExist(id):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update WebPages set baseTags='" + bt + "' where id=" + str(id)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Test update web tags success")
    else:
        print("Web page not found")


def UpdateBaseAntis(bat: str, tgid: int):
    print("TGID: " + str(tgid))
    if UserSettsExist(tgid):
        updquery = r"update UserWebSetts set baseAntiTags='" + bat + "' where tgid=" + str(tgid)
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Update tags success")
    else:
        CreateEmptyWebSett(tgid)
        print("Created settings item")


def UpdatePageBaseAntis(bat: str, id: int):
    print("WID: " + str(id))
    if WebPageExist(id):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update WebPages set baseAntiTags='" + bat + "' where id=" + str(id)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Test update tags success")
    else:
        print("Create web page on id first: " + str(id))


def UpdateMinId(minid: int, tgid: int):
    print("TGID: " + str(tgid))
    if UserSettsExist(tgid):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update UserWebSetts set minid=" + str(minid) + " where tgid=" + str(tgid)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Test update tags success")
    else:
        CreateEmptyWebSett(tgid)
        print("Created settings item, repeat")


def UpdatePageMinId(minid: int, id: int):
    print("WID: " + str(id))
    if WebPageExist(id):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update WebPages set minid=" + str(minid) + " where id=" + str(id)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Test update tags success")
    else:
        print("Set custom settings first")


def UpdateMaxId(maxid: int, tgid: int):
    print("TGID: " + str(tgid))
    if UserSettsExist(tgid):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update UserWebSetts set maxid=" + str(maxid) + " where tgid=" + str(tgid)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Test update tags success")
    else:
        CreateEmptyWebSett(tgid)
        print("Created settings item, repeat")


def UpdatePageMaxId(maxid: int, id: int):
    print("WID: " + str(id))
    if UserSettsExist(id):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update WebPages set maxid=" + str(maxid) + " where id=" + str(id)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Test update tags success")
    else:
        print("Set custom settings first")


def UpdateStrict(stct: bool, tgid: int):
    strstct = str(int(stct))
    print("TGID: " + str(tgid))
    if UserSettsExist(tgid):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update UserWebSetts set StrictTag=" + strstct + " where tgid=" + str(tgid)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Test update tags success")
    else:
        CreateEmptyWebSett(tgid)
        print("Created settings item, repeat")


def SyncWepSetts(wp: WebPage):
    wi = wp.Id
    print("SyncWepSetts():")
    UpdateBaseTags(wp.BaseTags, wi)
    print("BaseTags synced")
    UpdateBaseAntis(wp.BaseAntiTags, wi)
    print("BaseAntiTags synced")
    UpdateMinId(wp.MinId, wi)
    print("MinId synced")
    UpdateMaxId(wp.MaxId, wi)
    print("MaxId synced")


def UpdateWebId(wid: int, tgid: int):
    print("WID: " + str(wid))
    if WebPageExist(wid):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update UserWebSetts set WID='" + str(wid) + "' where tgid=" + str(tgid)
        print(updquery)
        command.execute(updquery)
        conn.commit()
        conn.close()
        wp = GetWebPageById(wid)
        SyncWepSetts(wp)
        print("Update web id success")
    else:
        print("No such web")


def UpdatePageSearch(srchpg: str, id: int):
    print("WID: " + str(id))
    if WebPageExist(id):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update WebPages set SearchPage='" + srchpg + "' where id=" + str(id)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Search now goes on: " + srchpg)
    else:
        print("No object with id " + str(id))


def UpdatePageTagL(tgmrkl: str, id: int):
    print("WID: " + str(id) + " => " + tgmrkl)
    if WebPageExist(id):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update WebPages set TagMarkL='" + tgmrkl + "' where id=" + str(id)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Test update tags success")
    else:
        print("Set custom settings first")
        print("WebPage.Id: " + str(GetWebPageById(id)))


def UpdatePageTagR(tgmrkr: str, id: int):
    print("WID: " + str(id) + " => " + tgmrkr)
    if WebPageExist(id):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update WebPages set TagMarkR='" + tgmrkr + "' where id=" + str(id)
        command.execute(updquery)
        conn.commit()
        conn.close()
        print("Test update tags success")
    else:
        print("Set custom settings first")
        print("WebPage.Id: " + str(GetWebPageById(id)))


def UpdatePageUrl(id: int, url: str):
    print("WID: " + str(id))
    if WebPageExist(id):
        conn = sqlite3.connect("treasure.db")
        command = conn.cursor()
        updquery = r"update WebPages set Url='" + url + "' where id=" + str(id)
        command.execute(updquery)
        print("Test update url success")
        conn.commit()
        conn.close()
        return True
    else:
        print("Create webpage with id " + id + " first")
        return False


def ListWebs():
    wps = getWebPages()
    res = ""
    for el in wps:
        res += str(el.Id) + " - " + el.Url + "\n"
    res.strip('\n')
    return res


def FullListWebs():
    wps = getWebPages()
    res = ""
    for el in wps:
        res += str(el) + "\n"
    res.strip('\n')
    return res


def GetHostIP():
    local_ip = "<local_ip>"
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3])
    return local_ip


bot = telebot.TeleBot('2071174422:AAG8WE350ZAP88Lbr68BvSRK66oL361xEB0');


@bot.message_handler(commands=['reset'])
def ResetDb(message):
    try:
        RecreateDB()
        bot.reply_to(message, "Db reset")
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['get_one'])
def getOne(message):
    webSett = GetWebSettByTGID(message.chat.id)
    webPage = GetWebPageById(webSett.WID)
    webPage = SyncWebSettWithPage(webPage, webSett)
    rsr = RandomSingle(webPage, bool(webSett.StrictTag))
    bot.reply_to(message, webPage.ConstructUrl(rsr.innerid) + "\n" + ", ".join(rsr.tags))


def SyncWebSettWithPage(wp, ws):
    if ws.MinId > 0:
        wp.MinId = ws.MinId
    if ws.MaxId > 0:
        wp.MaxId = ws.MaxId
    if len(ws.BaseTags) > 0:
        wp.BaseTags = ws.BaseTags
    if len(ws.BaseAntiTags) > 0:
        wp.BaseAntiTags = ws.BaseAntiTags
    return wp


@bot.message_handler(commands=['get'])
def get(message):
    try:
        wp = WebPage()
        wp.MinId = 130000
        wp.MaxId = 350000
        wp.Url = 'https://nhentai.net/g/'
        wp.TagMarkR = ''
        wp.TagMarkL = ''
        wp.BaseTags = ""
        wp.BaseAntiTags = ""
        webSetts = getWebSetts()
        if len(webSetts) > 0:
            tempmsg = bot.reply_to(message, "Reaching database...")
            webSett = GetWebSettByTGID(message.chat.id)
            webPage = GetWebPageById(webSett.WID)
            queueMsg = "Searching match in between IDs " + str(webSett.MinId) + " to " + str(
                webSett.MaxId) + "\nWebsite: " + webPage.Url + "\nTags in use:" + webSett.BaseTags
            bot.edit_message_text(text=queueMsg, chat_id=tempmsg.chat.id,
                                  message_id=tempmsg.message_id)
            if len(webPage.Url) > 0:
                wp.Url = "https://yande.re/post/show/"
                print("url on Id " + str(webSett.WID) + ": " + wp.Url)
            else:
                print("url on Id " + str(webSett.WID) + " is empty\n")
            print(webPage.TagMarkL + " is >")
            wp = SyncWebSettWithPage(webPage, webSett)
            rtfRes = RandomTillFind(wp, bool(webSett.StrictTag))
            SendMessage(
                wp.ConstructUrl(
                    rtfRes.innerid) + "\nTags found: " + ", ".join(rtfRes.tags) + "\nWithin attempts" + str(
                    rtfRes.attempts) + "\nFrom TGID: " + str(
                    message.chat.id) + "\nOn ip: " + str(
                    GetHostIP()),
                "michelotakuwatson@gmail.com")
            resUrl = wp.Url + str(rtfRes.innerid)
            resText = "Found within " + str(rtfRes.attempts) + " attempts\n" + resUrl + "\n" + ", ".join(rtfRes.tags)
            bot.edit_message_text(text=resText, chat_id=tempmsg.chat.id,
                                  message_id=tempmsg.message_id)
            print("Random till find within " + str(rtfRes.attempts) + " attempts (" + rtfRes.wp.ConstructUrl(
                rtfRes.innerid) + "): " + ", ".join(rtfRes.tags))
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_tags'])
def setTags(message):
    try:
        tags = str(message.text[message.text.index(' ') + 1:].strip(' ').lower())
        tgid = int(message.chat.id)
        if UserSettsExist(tgid):
            UpdateBaseTags(tags, tgid)
            bot.reply_to(message, "New tags: " + tags)
            print("New tags: " + tags)
        else:
            CreateEmptyWebSett(tgid)
            bot.reply_to(message, "User settings created")
            print("User settings created")
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_antis'])
def setAntis(message):
    try:
        tags = str(message.text[message.text.index(' ') + 1:].strip(' ').lower())
        sid = int(message.chat.id)
        if UserSettsExist(sid):
            UpdateBaseAntis(tags, sid)
            bot.reply_to(message, "New antis: " + tags)
            print("New antis: " + tags)
        else:
            CreateEmptyWebSett(message.chat.id)
            bot.reply_to(message, "User settings created")
            print("User settings created")
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_min'])
def setMinId(message):
    try:
        minid = int(message.text[message.text.index(' ') + 1:].strip(' '))
        sid = int(message.chat.id)
        if UserSettsExist(sid):
            UpdateMinId(minid, sid)
            bot.reply_to(message, "New min: " + str(minid))
            print("New min: " + str(minid))
        else:
            CreateEmptyWebSett(message.chat.id)
            bot.reply_to(message, "User settings created")
            print("User settings created")
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_max'])
def setMaxId(message):
    try:
        maxid = int(message.text[message.text.index(' ') + 1:].strip(' '))
        sid = int(message.chat.id)
        if UserSettsExist(sid):
            UpdateMaxId(maxid, sid)
            print("New maxid: " + str(maxid))
            bot.reply_to(message, "New maxid: " + str(maxid))
        else:
            CreateEmptyWebSett(message.chat.id)
            bot.reply_to(message, "User settings created")
            print("User settings created")
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_strict'])
def setStrict(message):
    try:
        stct = bool(int(message.text[message.text.index(' ') + 1:].strip(' ')))
        sid = int(message.chat.id)
        if UserSettsExist(sid):
            UpdateStrict(stct, sid)
            bot.reply_to(message, "New strict: " + str(stct))
            print("New strict: " + str(stct))
        else:
            CreateEmptyWebSett(message.chat.id)
            bot.reply_to(message, "User settings created")
            print("User settings created")
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_web_id'])
def setWebID(message):
    try:
        webid = int(message.text.split(' ')[1].strip(' '))
        uid = int(message.chat.id)
        if UserSettsExist(uid):
            if WebPageExist(webid):
                try:
                    UpdateWebId(webid, message.chat.id)
                    print("New webid: " + str(webid))
                    bot.reply_to(message, "New webid: " + str(webid))
                except BaseException as err:
                    print("setWebID: " + str(err))
            else:
                bot.reply_to(message, "Created web on tgid: " + str(uid))
                print("Created web on tgid: " + str(uid))
                CreateEmptyWebSett(message.chat.id)
        else:
            bot.reply_to(message, "User settings created")
            print("User settings created")
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['settings'])
def listSetts(message):
    try:
        text = str(GetWebSettByTGID(message.chat.id)).replace('; ', '\n').strip('\n')
        print(text)
        bot.reply_to(message, text)
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['web_info'])
def webInfo(message):
    try:
        print("TGID: " + str(message.chat.id))
        text = str(GetWebPageById(GetWebSettByTGID(message.chat.id).WID)).replace('; ', '\n')
        bot.reply_to(message, text)
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['add_page'])
def addPage(message):
    try:
        CreateEmptyWebPage()
        wps = getWebPages()
        lwp = wps[len(wps) - 1]
        print("WID: " + str(lwp.Id))
        bot.reply_to(message, "WID: " + str(lwp.Id) + " created")
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_web_url'])
def addPage(message):
    try:
        elId = int(message.text.split(' ')[1])
        elUrl = str(message.text.split(' ')[2])
        if UpdatePageUrl(elId, elUrl):
            bot.reply_to(message, "Update on id " + str(elId) + " to " + elUrl + " success")
            print("Update on id " + str(elId) + " to " + elUrl + " success")
        else:
            bot.reply_to(message, "Update on id " + str(elId) + " to " + elUrl + " failed for non-existing page")
            print("Update on id " + str(elId) + " to " + elUrl + " failed for non-existing page")
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_web_min'])
def addPage(message):
    try:
        elId = int(message.text.split(' ')[1])
        minid = int(message.text.split(' ')[2])
        UpdatePageMinId(elId, minid)
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_web_max'])
def addPage(message):
    try:
        elId = int(message.text.split(' ')[1])
        maxid = int(message.text.split(' ')[2])
        UpdatePageMaxId(elId, maxid)
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_web_tags'])
def addPage(message):
    try:
        elId = str(message.text.split(' ')[1])
        tags = str(message.text.split(' ')[2])
        UpdatePageBaseTags(elId, tags)
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_web_antis'])
def addPage(message):
    try:
        elId = str(message.text.split(' ')[1])
        antis = str(message.text.split(' ')[2])
        UpdatePageBaseAntis(elId, antis)
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_page_tag_l'])
def setPageTagL(message):
    try:
        elId = str(message.text.split(' ')[1])
        tgmrkl = str(message.text.split(' ')[2])
        UpdatePageTagL(tgmrkl, elId);
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_page_tag_r'])
def setPageTagR(message):
    try:
        elId = str(message.text.split(' ')[1])
        tgmrkl = str(message.text.split(' ')[2])
        UpdatePageTagR(tgmrkl, elId);
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_search'])
def set_search(message):
    try:
        request = message.text[message.text.index(' ') + 1:].strip(' ').replace(' ', '+')
        UpdatePageSearch(request, GetWebSettByTGID(message.chat.id).WID)
        bot.reply_to(message, "Attempting to change search page.")
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['search'])
def search(message):
    try:
        request = GetWebPageById(GetWebSettByTGID(message.chat.id).WID).SearchPage + message.text[
                                                                                     message.text.index(
                                                                                         ' ') + 1:].strip(
            ' ').replace(' ', '+')
        bot.reply_to(message, request)
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['list_webs'])
def listWs(message):
    try:
        bot.reply_to(message, ListWebs())
        print(ListWebs())
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['full_list_webs'])
def listWs(message):
    try:
        rep = FullListWebs().replace('; ', '\n')
        bot.reply_to(message, rep)
        print(rep)
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


def NoTagging(tgid):
    UpdateBaseTags("", tgid)
    UpdateBaseAntis("", tgid)
    UpdateStrict(False, tgid)


@bot.message_handler(commands=['no_tagging'])
def listWs(message):
    try:
        tgid = message.chat.id
        NoTagging(tgid)
        bot.reply_to(message, "Tags cleared and context security disabled")
        print("Tags cleared and context security disabled")
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['save_url'])
def saveUrl(message):
    msgText = message.text
    commKey = msgText.split(' ')[0]
    url = msgText.split(' ')[1]
    innerid = url[url.rindex('/') + 1:]
    urlHome = url[:url.rindex('/') + 1]
    desc = msgText.replace(commKey, '').replace(url, '').strip(' ')
    if AddTreasure(urlHome, innerid, desc, message.chat.id):
        bot.reply_to(message, "Adding " + url + " with comment: " + desc)
    else:
        bot.reply_to(message, "No website in db for this url")


@bot.message_handler(commands=['list_saves'])
def listSaves(message):
    liStr = ""
    treas = getTreasures()
    for el in treas:
        liStr += str(el).replace('; ', ' - ') + "\n"
    bot.reply_to(message, liStr)


@bot.message_handler(commands=['backup'])
def backup(message):
    wps = getWebPages()
    resWPS = "create table WebPages(Id integer primary key, Url text, MinId integer, MaxId integer, BaseTags text,BaseAntiTags text, TagMarkL text, TagMarkR text, SearchPage text);\n"
    for w in wps:
        resWPS += "Insert int WebPages (MinId, MaxId, BaseTags, BaseAntiTags, TagMarkL, TagMarkR, SearchPage) values (" + str(
            w.MinId) + ", " + str(
            w.MaxId) + ", '" + w.BaseTags + "', '" + w.BaseAntiTags + "', '" + w.TagMarkL + "', '" + w.TagMarkR + "', '" + w.SearchPage + "');\n"
    trs = getTreasures()
    resTRS = "create table Treasures(Id integer primary key, InnerID text, Description text, TGID integer, WID integer);\n"
    for t in trs:
        resTRS += "insert into Treasures (InnerID, Description, TGID, WID) values ('" + t.InnerID + "', '" + t.Description + "', " + str(
            t.UID) + ", " + str(t.WID) + ");\n"
    uws = getWebSetts()
    resUWS = "create table UserWebSetts(Id integer primary key,MinId integer, MaxId integer, BaseTags text,BaseAntiTags text,StrictTag int, TGID integer, WID integer);\n"
    for u in uws:
        resUWS += "insert into UserWebSetts (MinId,MaxId,BaseTags,BaseAntiTags,StrictTag,TGID,WID) values(" + str(
            u.MinId) + ", " + str(u.MaxId) + ", '" + u.BaseTags + "', '" + u.BaseAntiTags + "'," + str(
            int(u.StrictTag)) + ", " + str(u.TGID) + ", " + str(u.WID) + ");\n"
    SendMessage(resWPS, "michelotakuwatson@gmail.com", "WebPageBackup")
    SendMessage(resTRS, "michelotakuwatson@gmail.com", "TreasuresBackup")
    SendMessage(resUWS, "michelotakuwatson@gmail.com", "UserWebSettsBackup")


@bot.message_handler(commands=['set_item_desc'])
def setItemDesc(message):
    try:
        cmdParts = message.text.split()
        itemid = int(cmdParts[1])
        desc = str(message.text[message.text.index(' ') + 1:].replace(cmdParts[1], '').strip(' '))
        if TreasureExists(itemid):
            UpdateTreasureDesc(desc, itemid)
            bot.reply_to(message, "New desc: " + desc)
            print("New desc: " + desc)
        else:
            bot.reply_to(message, "Treasure doesn't exist yet")
            print("Treasure doesn't exist yet")
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


@bot.message_handler(commands=['set_item_innerid'])
def setItemInner(message):
    try:
        cmdParts = message.text.split()
        itemid = int(cmdParts[1])
        innerid = int(message.text[message.text.index(' ') + 1:].replace(cmdParts[1], '').strip(' '))
        if TreasureExists(itemid):
            UpdateTreasureInnerId(innerid, itemid)
            bot.reply_to(message, "New innerid: " + innerid)
            print("New innerid: " + innerid)
        else:
            bot.reply_to(message, "Treasure doesn't exist yet")
            print("Treasure doesn't exist yet")
    except BaseException as err:
        ProcessError(err, inspect.stack()[0][3], message, bot)


def ListTreasures():
    trs = getTreasures()
    res = ""
    for el in trs:
        res += str(el) + "\n"
    res.strip('\n')
    return res


@bot.message_handler(commands=['list_treasures'])
def listTreasures(message):
    try:
        bot.reply_to(message, ListTreasures().replace(';', ' -'))
        print(ListTreasures())
    except BaseException as err:
        print(str(err))


@bot.message_handler(commands=['hello'])
def test(message):
    bot.reply_to(message, "Hello!")


bot.polling()
