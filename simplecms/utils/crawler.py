#coding: utf8

import sys
import requests

from lxml import etree
from simplecms.utils.s3 import s3

REPLACE_PIC_URL = "http://7xlvk7.com1.z0.glb.clouddn.com/%s"
PIC_CRAWL_FAILED = REPLACE_PIC_URL % "not_found.jpg"
REPLACE_IMG = False


def wechat_extract(root):
    candidate = root.xpath("/html/body/div/div/div/div/div")
    for node in candidate:
        if node.get("class") == "rich_media_content":
            return node
    raise Exception("xpath not found, candidate:%d\n" % len(candidate))


def content_extract(root, site):
    if site == "wechat":
        return wechat_extract(root)

    return root


def s3_name(url):
    return str(url.__hash__())
    #return requests.utils.quote(url, safe="")


def img_replace(node):
    img_url = node.get("data-src", node.get("src"))
    if img_url:
        if REPLACE_IMG:
            try:
                resp = requests.get(img_url)
                assert(resp.status_code == requests.codes.ok)
            except:
                node.set("src", PIC_CRAWL_FAILED)
                node.set("data-type", "jpg")
                return

            file_name = s3_name(img_url)
            s3.set(file_name, resp.content)
            node.set("src", REPLACE_PIC_URL % file_name)

        else:
            node.set("src", img_url)


def depth_first_traversal(node):
    if node.tag == "img":
        img_replace(node)
    else:
        for child in node.getchildren():
            depth_first_traversal(child)


def crawl_and_localize(url, site):
    resp = requests.get(url)
    assert(resp.status_code == requests.codes.ok)

    parser = etree.HTMLParser(recover=True)
    root = etree.fromstring(resp.content, parser)

    content = content_extract(root, site)

    depth_first_traversal(content)

    return etree.tostring(content, method="html")


def test():
    url = "http://mp.weixin.qq.com/s?__biz=MjM5MDcxMTQwOA==&mid=212568491&idx=1&sn=e605b31a7ac8e0bfa7e6060d23f9abca&3rd=MzA3MDU4NTYzMw==&scene=6#rd"
    return crawl_and_localize(url, "wechat")


if __name__ == "__main__":
    #print test()
    print crawl_and_localize(sys.argv[1], "wechat")
