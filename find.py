#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from lxml import html
import re
import json
from pprint import pprint

def getDetails(pageFactory, page):
    pageRoot = pageFactory(page)
    xpathBase = "(//h2[starts-with(text(),%s)]/following::div)[1]//div"

    def parseElement(ele):
        return ele.text_content().strip().encode("utf-8")

    castElements =       pageRoot.xpath(xpathBase % "'Cast'")
    staffElements =      pageRoot.xpath(xpathBase % "'Staff'")
    guestElements =      pageRoot.xpath(xpathBase % "'Guest'")
    highlightsElements = pageRoot.xpath(xpathBase % "'Show'")
    videosElements =     pageRoot.xpath(xpathBase % "'Videos'")
    artJamElements =     pageRoot.xpath(xpathBase % "'Art'")
    lastWordsElements =  pageRoot.xpath(xpathBase % '\'"Last Words"\'')

    episode =    int(re.search("[0-9]*$", page).group(0))
    cast =       map(parseElement, castElements)
    staff =      map(parseElement, staffElements)
    guests =     map(parseElement, guestElements)
    highlights = map(parseElement, highlightsElements)
    videos =     map(parseElement, videosElements)
    artJams =    map(parseElement, artJamElements)
    lastWords =  map(parseElement, lastWordsElements)

    return {"Episode":    episode,
            "Cast":       cast,
            "Staff":      staff,
            "Guests":     guests,
            "Highlights": highlights,
            "Videos":     videos,
            "Art Jams":   artJams,
            "Last Words": lastWords}

def getAllDetails():
    def getPageFactory(baseUrl):
        def getPageWithBase(url):
            fullUrl = baseUrl + url
            page = urllib.urlopen(fullUrl).read()
            return html.fromstring(page)

        return getPageWithBase

    domain = "http://www.pawpet.tv"
    pageFactory = getPageFactory(domain)
    mainPageUrl = "/episode_guide"
    mainPage = pageFactory(mainPageUrl)
    allLinks = mainPage.xpath('//a')
    detailsLinks = filter(lambda link: link.text == '[Details]', allLinks)
    episodeHrefs = map(lambda link: link.attrib["href"], detailsLinks)

    return map(lambda href: getDetails(pageFactory, href), episodeHrefs)

def main():
    allDetails = getAllDetails()

    with open("site-data.json", "w") as outFile:
        outFile.write(json.dumps(allDetails, indent=4))

if __name__ == '__main__':
    main()

