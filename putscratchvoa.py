###put  VOA精听听写 音频、文本抓取
import urllib.request
from bs4 import BeautifulSoup
import time, datetime
import re


###生成cookie，利用cookie，发送请求
def withcookie(url):
    user_agent="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    cookie="Hm_lvt_4e7c74660fca105e4398ab0e17867537=1542861523; cdb_cookietime=2592000; smile=1D1; discuz_collapse=_sidebar_; cdb_auth=f9a0lXPbFFY1LTeIF8iniSWwYlCQia%2B6lr3Z6hGZnXT5eVJs%2FhY3koWRjfNdUkaWBNFD7MptDJGesZYZeuC9gACEZ1cBRQ; cdb_visitedfid=169; Hm_lvt_c077b0c8f9ed9c09781846279500eae4=1543367533,1543368729,1543384920,1543454248; cdb_oldtopics=D535945D; cdb_fid169=1543435995; put_cookie_expire=7200; cdb_sid=6ddVB2; Hm_lpvt_c077b0c8f9ed9c09781846279500eae4=1543469236"
    headers={"User-Agent":user_agent,"Cookie":cookie}
    rt=urllib.request.Request(url,headers=headers)
    response=urllib.request.urlopen(rt)
    contents = response.read()
    return contents
###判断日期的准确性
def is_date(str):
    try:
        time.strptime(str,"%y.%m.%d")
        return True
    except:
        return False
###MP3下载地址获取
def search_mp3(inputdate):
    MAINURL = "http://forum.putclub.com/forumdisplay.php?fid=170&page=" #下载用html
    page=1
    flag=0
    mp3=""
    audiourl="http://forum.putclub.com/"

    while flag==0 and page<=10:
        html=MAINURL+str(page)
        bsobj=BeautifulSoup(withcookie(html),"lxml")
        itemlists = bsobj.findAll("a", {"href": re.compile("3D1$")})  # 匹配出章节网址链接
        for item in itemlists:
            if item.get_text() == inputdate:
                flag=1
                mp3=item["href"]
                break
        page+=1
    if flag==1:
        return (audiourl+mp3)
    else:
        return None


###MP3加文本抓取(必须已经回复过，否则出错)
def scratchmp3(url,inputdate):


    html=withcookie(url)
    bsobj=BeautifulSoup(html,"lxml")
    mp3path=bsobj.find("a", {"href": re.compile("\.mp3$")})["href"]
    txt=bsobj.find("font",{"face":"Verdana"}).get_text()
    formertxt=re.sub(r'[\u4e00-\u9fa5]+.*$',"",txt)

    txt=bsobj.find_all("span",{"style":"FONT-SIZE: 14pt; FONT-FAMILY: 'Times New Roman'"})[0].get_text()
    hiddentxt=re.sub(r'[\u4e00-\u9fa5]+.*$',"",txt)
    #print(formertxt)
    finaltxt=re.sub(r'_+',hiddentxt,re.sub(r'_+$','',re.sub(r'\W$','',formertxt)))
    #finaltxt=re.sub(r'_+',hiddentxt,formertxt)
    ###文本抓取，中文过滤
    f=open("E:\A个人工作\put听力训练\VOA精听\\"+inputdate+".mp3","wb")
    f.write((urllib.request.urlopen(mp3path)).read())
    f.close()
    f=open("E:\A个人工作\put听力训练\VOA精听\\"+inputdate+".txt","w")
    endtxt=re.sub(r'[\\。]','',re.sub(r'\. \.','. ',re.sub(r'\s+',' ',finaltxt)))
    f.write(endtxt)
    f.close()
    ###mp3及文本写入对应文件

def main():

    dt=""
    inputdate=""

    while True:
        dt=input("请输入你要整理的日期：")
        dt2=input("整理到？：")
        if dt:
            if is_date(dt) and is_date(dt2):
                date1=time.strptime(dt,"%y.%m.%d")
                date2=time.strptime(dt2,"%y.%m.%d")
                break
            else:
                print("请输入正确的日期！")
        else:
            dt=datetime.datetime.now()
            date1=time.strptime(str(dt),"%Y-%m-%d %H:%M:%S.%f")
            date2=time.strptime(str(dt),"%Y-%m-%d %H:%M:%S.%f")
            break


    day=date1[2]
    str_day=""
    str_month=""
    while day<=date2[2]:
        if day<10:
            str_day="0"+str(day)
        else:
            str_day=str(day)
        if month<10:
            str_month="0"+str(month)
        else:
            str_month=str(month)
        inputdate=str(date1[0])+"-"+str_month+"-"+str_day
        inputdate="VOA标准精精听"+inputdate
        scratchmp3(search_mp3(inputdate),inputdate)
        day+=1
    input("键入enter退出...")
main()

