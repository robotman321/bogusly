#!/usr/bin/env python2.7

# Copyright 2017 Andrew Sinnett
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import random
import urllib2
import sys
from time import sleep

dryrun = True
# Your API token from bonusly
# Note that your token MUST be read/write and not just readonly
token = 'CHANGEMEWITHYOURAPITOKEN'

# Random reason generation
def gen_reason():
    starter = [line.rstrip('\n') for line in open('starter.txt')]
    ender = [line.rstrip('\n') for line in open('ender.txt')]

    l = [starter,ender]
    return ' '.join([random.choice(i) for i in l])

# Hashtag generation
def gen_hash():
    tags = [line.rstrip('\n') for line in open('tags.txt')]
    selection = []

    for _ in range(0, random.randint(1,5)):
        selection.append(random.choice(tags))

    selection = list(set(selection))
    return ' '.join(str(e) for e in selection)


# Getting current available balance
try:
    response = urllib2.urlopen('https://bonus.ly/api/v1/users/me?access_token=%s' % (token))
    data = json.load(response)
    bal = data["result"]["giving_balance"]
    uname = data["result"]["username"]
except HTTPError:
    print 'FATAL: current user info retrieval failed'
    sys.exit(1)
else:
    print 'Retrieved current user info'

# Getting lst of users
u_list = urllib2.urlopen('https://bonus.ly/api/v1/users?access_token=%s' % (token))

try:
    obj = json.load(u_list)
except ValueError, e:
    print 'FATAL: %s' % (e)
    sys.exit(1)
else:
    print 'Retrieved user list'


userlist = []
dothis = []

for user in obj["result"]:
    # You can't give bonuses to yourself or to the Welcome Bot
    if uname != user["username"] and "bot" not in user["username"]:
        userlist.append(user["username"])

# This may not be necessary. I just wanted the list sorted first.
userlist.sort()

if dryrun != True:
    print "WARNING: Sending bonuses in 5 seconds"
    sleep(5)
else:
    print "Outputting lines:"

while len(dothis) < bal:
    dothis.append(random.choice(userlist))
    dothis = list(set(dothis))

for x in dothis:
    sleep(random.randint(3,14))
    data = {"reason": "+1 @%s %s! %s" % (x, gen_reason(), gen_hash())}
    if dryrun != True:
        try:
            req = urllib2.Request('https://bonus.ly/api/v1/bonuses?access_token=%s' %  (token))
            req.add_header('Content-Type', 'application/json')

            response = urllib2.urlopen(req, json.dumps(data))
        except HTTPError, e:
            print 'ERROR: %s' % (e)
        else:
            print 'Sent bonus: %s' % (data)
    else:
        print data
