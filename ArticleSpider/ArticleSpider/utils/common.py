# !\C:\Users\admin\PycharmProjects
# _*_ coding:utf-8 _*_

import hashlib

def get_md5(url):
    if isinstance(url,str):   #如果url是unicode,str 指的就是unicode的意思
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == "__main__":
    print(get_md5("http://www.jobbole.com".encode("utf-8")))