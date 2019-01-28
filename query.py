#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import json
from operator import itemgetter

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getEpisodes():
    with open("site-data.json", "r") as data:
        episodes = json.loads(data.read())

    return sorted(episodes, key=itemgetter("Episode"))

def showResultsFor(lookIn, category, search):
    def isRelevant(thing):
        return re.search(search, thing)
        # return search.lower() in thing.lower()

    def query(category, search):
        return lambda episode: filter(isRelevant, episode[category]) != []

    def printDetail(episode):
        def printIt(it):
            print it.encode('ascii', 'ignore')

        detail = map(lambda item: "* %s" % item, episode[category])
        relevantDetail = filter(isRelevant, detail)

        print "%sEpisode %s:%s" % (bcolors.OKBLUE, episode["Episode"], bcolors.ENDC)
        map(printIt, relevantDetail)

    foundEpisodes = filter(query(category, search), lookIn)
    map(printDetail, foundEpisodes)

def main(category, query):
    episodes = getEpisodes()
    showResultsFor(episodes, category, query)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

