# import ###############################################################

import os
import re
import csv
import time
import json
import glob
import pickle
import shutil
import inspect
import datetime
import subprocess
import collections
import pandas as pd
import pyautogui as pg
import tkinter, tkinter.filedialog
from requests_html import HTMLSession

# load ################################################################

def loadTextAsStr(path, enc="shift-jis"):
    newPath = normalizePath(path)
    with open(newPath, "r", encoding=enc) as f:
        string = f.read()
    return string

def loadTextAsL(path, enc="shift-jis"):
    newPath = normalizePath(path)
    with open(newPath, "r", encoding=enc) as f:
        stringL = f.readlines()
    return stringL

def loadCsvAsLL(path, enc="shift-jis"):
    newPath = normalizePath(path)
    with open(newPath, newline="", encoding=enc) as f:
        LL = [r for r in csv.reader(f)]
    return LL

def loadCsvAsDataFrame(path, enc="shift-jis", header=None):
    newPath = normalizePath(path)
    return pd.read_csv(newPath, encoding=enc, header=header)

def loadJsonAsDict(path, enc="shift-jis"):
    newPath = normalizePath(path)
    with open(newPath, "r", encoding=enc) as f:
        dic = json.load(f)
    return dic
    
def loadPickleAsObject(path):
    newPath = normalizePath(path)
    with open(newPath, "rb") as f:
        obj = pickle.load(f)
    return obj
    
# save ################################################################

def saveStrAsText(string, path, enc="shift-jis"):
    newPath = normalizePath(path)
    with open(newPath, "w", encoding=enc) as f:
        f.write(string)
    return newPath

def saveLAsText(L, path, separator="", enc="shift-jis"):
    return saveStrAsText(separator.join(L), path, enc)

def saveLLAsCsv(LL, path, enc="shift-jis"):
    newPath = normalizePath(path)
    with open(newPath, "w", encoding=enc, newline="") as f:
        csv.writer(f).writerows(LL)
    return newPath

def saveDataFrameAsCsv(df, path, enc="shift-jis", header=False, index=False):
    newPath = normalizePath(path)
    df.to_csv(newPath, encoding=enc, header=header, index=index)
    return newPath

def saveDictAsJson(dic, path, indent=4, enc="shift-jis"):
    newPath = normalizePath(path)
    with open(newPath, "w", encoding=enc) as f:
        json.dump(dic, f, indent=indent, ensure_ascii=False)
    return newPath

def saveObjectAsPickle(obj, path):
    newPath = normalizePath(path)
    with open(newPath, "wb") as f:
        pickle.dump(obj, f)
    return newPath

# path ################################################################

def selectFile(path=os.getenv("HOMEDRIVE")+os.getenv("HOMEPATH")+"/Desktop"):
    newPath = normalizePath(path)
    root = tkinter.Tk()
    root.withdraw()
    filePath = tkinter.filedialog.askopenfilename(initialdir=newPath)
    return filePath

def selectFiles(path=os.getenv("HOMEDRIVE")+os.getenv("HOMEPATH")+"/Desktop"):
    newPath = normalizePath(path)
    root = tkinter.Tk()
    root.withdraw()
    filePathL = list(tkinter.filedialog.askopenfilenames(initialdir=newPath))
    return filePathL

def selectDirectory(path=os.getenv("HOMEDRIVE")+os.getenv("HOMEPATH")+"/Desktop"):
    newPath = normalizePath(path)
    root = tkinter.Tk()
    root.withdraw()
    directoryPath = tkinter.filedialog.askdirectory(initialdir=newPath)
    return directoryPath

# def selectDirectories(path=os.getenv("HOMEDRIVE")+os.getenv("HOMEPATH")+"/Desktop"):
#     ??????????????
#     return directoryPathL

def getAllItemPathL(path, recursive=True):
    newPath = normalizePath(path)    
    newPath = f"{newPath}/**"
    return [normalizePath(x) for x in glob.glob(newPath, recursive=recursive)]

def getItemPathLWithRegEx(path, regex="**", recursive=True):
    newPath = normalizePath(path)    
    newPath = f"{newPath}/{regex}"
    return [normalizePath(x) for x in glob.glob(newPath, recursive=recursive)]

def getThisFileDirectory():
    return getParentPath(inspect.stack()[1].filename)

def getAbsolutePath(path):
    newPath = normalizePath(path)
    return os.path.abspath(newPath)

def qExists(path):
    newPath = normalizePath(path)
    return os.path.exists(newPath)

def qFilePath(path):
    newPath = normalizePath(path)
    return os.path.isfile(newPath)

def qDirectoryPath(path):
    newPath = normalizePath(path)
    return os.path.isdir(newPath)

def makeDirectory(path, exist_ok=True):
    newPath = normalizePath(path)
    os.makedirs(newPath, exist_ok=exist_ok)
    return newPath

def deleteItem(path):
    newPath = normalizePath(path)    
    #Item exists
    if qExists(newPath):        
        if qDirectoryPath(newPath):
            shutil.rmtree(newPath)
            print(f"{newPath}を削除しました。")
        elif qFilePath(newPath):
            os.remove(newPath)
            print(f"{newPath}を削除しました。")
        else:
            raise Exception(f'{newPath}は存在しますが、ディレクトリまたはファイルではありません。')
    #Item does not exist
    else:
        print(f"{newPath}は存在しません。")
    return newPath

def copyItem(srcPath, dstPath):
    new_srcPath = normalizePath(srcPath)    
    new_dstPath = normalizePath(dstPath)    
    #Item exists
    if qExists(new_srcPath):        
        if qDirectoryPath(new_srcPath):
            shutil.copytree(new_srcPath, new_dstPath)
        elif qFilePath(new_srcPath):
            if qFilePath(new_dstPath):
                shutil.copyfile(new_srcPath, new_dstPath)
            if qDirectoryPath(new_dstPath):
                shutil.copy(new_srcPath, new_dstPath)
            else:
                raise Exception(f'{new_dstPath}は存在しますが、ディレクトリまたはファイルではありません。')                
        else:
            raise Exception(f'{new_srcPath}は存在しますが、ディレクトリまたはファイルではありません。')
    #Item does not exist
    else:
        print(f"{new_srcPath}は存在しません。")
    return [new_srcPath, new_dstPath]

def moveItem(srcPath, dstPath):
    new_srcPath = normalizePath(srcPath)    
    new_dstPath = normalizePath(dstPath)
    #Item exists
    if qExists(new_srcPath):
        makeDirectory(getParentPath(new_dstPath))
        shutil.move(new_srcPath, new_dstPath)
    else:
        print(f"{new_srcPath} は存在しません。")
    return [new_srcPath, new_dstPath]

def renameItem(srcPath, newName):
    new_srcPath = normalizePath(srcPath)
    new_dstPath = None
    #Item exists
    if qExists(new_srcPath):
        new_dstPath = f"{getParentPath(new_srcPath)}/{newName}"
        new_dstPath = normalizePath(new_dstPath)
        moveItem(new_srcPath, new_dstPath)
    else:
        print(f"{new_srcPath} は存在しません。")
    return [new_srcPath, new_dstPath]

# str #################################################################

def normalizePath(path, oldSeparator="\\", newSeparator="/"):
    newPath = path
    newPath = newPath.replace(oldSeparator, newSeparator)
    newPath = newPath[:-1] if newPath[-1]==newSeparator else newPath
    return newPath

def getParentPath(path):
    newPath = normalizePath(path)
    newPath = "/".join(newPath.split("/")[:-1])
    return newPath

def getItemName(path, ext=True):
    newPath = normalizePath(path)
    newPath = newPath.split("/")[-1]
    newPath = newPath if ext else ".".join(newPath.split(".")[:-1])
    return newPath

def getFileExtension(path):
    newPath = normalizePath(path)
    ext = getItemName(newPath).split(".")[-1] if qFilePath(newPath) else None        
    return ext

def getURLLFromStr(string):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return re.findall(pattern, string)

def getDateAsStr(separator="-"):
    return datetime.datetime.now().strftime(f"%Y{separator}%m{separator}%d")

def getTimeAsStr(separator1=":", separator2="."):
    return datetime.datetime.now().strftime(f"%H{separator1}%M{separator1}%S{separator2}%f")

def getDateTimeAsStr(separator1="-", separator2=" ", separator3=":", separator4="."):
    return getDateAsStr(separator1) + separator2 + getTimeAsStr(separator3, separator4)

# list ################################################################

def sortL(L, reverse=False):
    return sorted(L, reverse=reverse)

def sortLLByIndex(LL, index=0, reverse=False):
    return sorted(LL, reverse=reverse, key=lambda x: x[index])

def uniquelizeL(L):
    return list(dict.fromkeys(L))

def qDuplicatesInL(L):
    return len(L)!=len(set(L))

def flattenLx(Lx):
    return list(_flatten(Lx))

#_flatten <inner function>
def _flatten(Lx):
    for el in Lx:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from _flatten(el)
        else:
            yield el

def convertDictIntoLL(Dic):
    return [[k,v] for k,v in Dic.items()]

def convertLLIntoDict(LL):
    return {k:v for k,v in LL}

def countElementsAsD(L):
    return dict(collections.Counter(L))

def countElementsAsLL(L, reverse=True):
    return sortLLByIndex(convertDictIntoLL(countElementsAsD(L)), index=1, reverse=reverse)

def deleteLLColumn(LL, idxI):
    return [ x[:idxI]+x[idxI+1:] if idxI!=-1 else x[:-1] for x in LL ]
 
# Excel ###############################################################


# web #################################################################
def getHTML(url, isrendered=False):
    r = HTMLSession().get(url)
    if isrendered:
        r.html.render()
    return r.html.full_text

# others ##############################################################

def swapObjects(obj1, obj2):
    return obj2, obj1

def runCommands(cmdL, kickonly=True):
    if kickonly:
        subprocess.Popen(cmdL, shell=True)
    else:
        subprocess.run(cmdL, shell=True)
    print(cmdL)
    return cmdL

# pyautogui #############################################################

def getPositionXY(maxretry=100, wait=1, grid=True):
    for _ in range(maxretry):
        x,y = pg.position()
        if grid:
            x,y = int(round(x,-1)), int(round(y,-1))
        print(f"({x},{y}) grid={grid}")
        time.sleep(wait)
    return



