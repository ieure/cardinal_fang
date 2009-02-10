#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Cardinal Fang twitterbot
#
# © 2008 Buster Marx, Inc. All rights reserved.
# Author: Ian Eure <ian.eure@gmail.com>

import sys
sys.path += "./lib"
import twitter, urllib2, sqlite3
import simplejson as json

db = sqlite3.connect('./victims.sqlite')

def create_schema():
    db.execute('CREATE TABLE IF NOT EXISTS `last_search` (`id` INT PRIMARY KEY);')

def last_victim():
    last = db.execute("SELECT MAX(`id`) FROM `last_search`;").fetchall()
    last = len(last) and last[0][0] or 0
    print "Last victim: %d" % (last,)
    return last

def load_feed():
    search_url = 'http://search.twitter.com/search.json?q=spanish+inquisition&since_id=%d' % (last_victim(), )

    return json.loads(urllib2.urlopen(search_url).read())

def locate_victims():
    """Locate victims of Cardinal Fang."""
    feed = load_feed()
    update_victims(feed['max_id'])
    return [tweet['from_user'] for tweet in feed['results'] if tweet['from_user'] != 'Cardinal_Fang']

def update_victims(last):
    db.execute("DELETE FROM `last_search` WHERE id <= ?;", (last,))
    db.execute("INSERT INTO `last_search` (`id`) VALUES (?);", (last,))
    db.commit()

def burn_at_the_stake(twitter, heretics):
    for heretic in heretics:
        print "@%s NOOOOBODY expects the Spanish Inquisition!" % (heretic,)
        twitter.PostUpdate("@%s NOOOOBODY expects the Spanish Inquisition!"
                           % (heretic,))

def get_twitter():
    return twitter.Api(username="Cardinal_Fang", password="scil2oth9phij")

def __main__():
    print "Running."
    create_schema()
    victims = locate_victims()
    if victims:
        print "Victimizing: "
        burn_at_the_stake(get_twitter(), victims)
    else:
        print "Nobody to victimize"

if __name__ == '__main__':
    __main__()

