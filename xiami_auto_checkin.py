#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# +-----------------------------------------------------------------------------
# | File: xiami_auto_checkin.py
# | Author: clampist
# | E-mail: clampist[at]gmail[dot]com
# | Created: 2012-06-23
# | Last modified: 2012-09-08
# | Description:
# |     auto checkin for xiami.com
# | Forked from: huxuan/xiami_auto_checkin
# | Copyrgiht (c) 2012 by clampist. All rights reserved.
# | License: GPLv3
# +-----------------------------------------------------------------------------

import re
import os
import sys
import urllib
import urllib2
import datetime
import cookielib
import subprocess

def check(response):
    """Check whether checkin is successful

    Args:
        response: the urlopen result of checkin

    Returns:
        If succeed, return a string like '已经连续签到**天'
            ** is the amount of continous checkin days
        If not, return False
    """
    pattern = re.compile(r'<div class="idh">(已连续签到\d+天)</div>')
    result = pattern.search(response)
    if result: return result.group(1)
    return False

def main():
    """Main process of auto checkin
    """
    # Get log file
    LOG_DIR = os.path.join(os.path.expanduser("~"), '.log')
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    LOG_PATH = os.path.join(LOG_DIR, 'xiami_auto_checkin.log')
    f = LOG_FILE = file(LOG_PATH, 'a')
    print >>f # add a blank space to seperate log

    # Get email and password
    if len(sys.argv) != 3:
        subprocess.call('notify-send -i error "[Error] Please input email & password as sys.argv!"', shell=True)
        print >>f, '[Error] Please input email & password as sys.argv!'
        print >>f, datetime.datetime.now()
        print '[Error] Please input email & password as sys.argv!'
        return
    email = sys.argv[1]
    password = sys.argv[2]

    # Init
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)

    # Login
    login_url = 'http://www.xiami.com/web/login'
    login_data = urllib.urlencode({'email':email, 'password':password, 'LoginButton':'登陆',})
    login_headers = {'Referer':'http://www.xiami.com/web/login', 'User-Agent':'Opera/9.60',}
    login_request = urllib2.Request(login_url, login_data, login_headers)
    login_response = urllib2.urlopen(login_request).read()

    # Checkin
    checkin_pattern = re.compile(r'<a class="check_in" href="(.*?)">')
    checkin_result = checkin_pattern.search(login_response)
    if not checkin_result:
        # Checkin Already | Login Failed
        result = check(login_response)
        if result:
            subprocess.call('notify-send -i info "[Already] Checkin Already! ' + email +' '+ result + '"', shell=True)
            print >>f, '[Already] Checkin Already!', email, result
            print '[Already] Checkin Already!', email, result
        else:
            subprocess.call('notify-send -i error "[Error] Login Failed! ' + email + '"', shell=True)
            print >>f, '[Error] Login Failed!', email
            print '[Error] Login Failed!', email
        print >>f, datetime.datetime.now()
        return
    checkin_url = 'http://www.xiami.com' + checkin_result.group(1)
    checkin_headers = {'Referer':'http://www.xiami.com/web', 'User-Agent':'Opera/9.60',}
    checkin_request = urllib2.Request(checkin_url, None, checkin_headers)
    checkin_response = urllib2.urlopen(checkin_request).read()

    # Result
    result = check(checkin_response)
    if result:
        subprocess.call('notify-send -i notification-message-email "[Success] Checkin Succeed! ' + email +' '+ result + '"', shell=True)
        print >>f, '[Success] Checkin Succeed!', email, result
        print '[Success] Checkin Succeed!', email, result
    else:
        subprocess.call('notify-send -i error "[Error] Checkin Failed!"', shell=True)
        print >>f, '[Error] Checkin Failed!'
        print '[Error] Checkin Failed!'
    print >>f, datetime.datetime.now()

if __name__=='__main__':
    main()
