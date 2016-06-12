#!/usr/bin/env python
#-*- coding: utf-8 -*-
#filename:upload_sespider.py

import os
import time
import sys
from collections import deque

with open('upload_sespider_ip.cfg','rb') as setip:
    iplist = setip.readlines()
    ip = []
    for i in range(len(iplist)):
        if iplist[i] == '\r\n':
            pass
        elif iplist[i] == '\n':
            pass
        elif iplist[i] == '\r':
            pass
        else:
            iplist[i] = iplist[i].replace('\r','')
            iplist[i] = iplist[i].replace('\n','')
            iplist[i] = iplist[i].replace(' ','')
            ip.append(iplist[i])
print ip

with open('tencentpasswd.cfg','rb') as settc:
    tclist = settc.readlines()
    tc = []
    for i in range(len(tclist)):
        if tclist[i] == '\r\n':
            pass
        elif tclist[i] == '\n':
            pass
        elif tclist[i] == '\r':
            pass
        else:
            tclist[i] = tclist[i].replace('\r','')
            tclist[i] = tclist[i].replace('\n','')
            tclist[i] = tclist[i].replace(' ','')
            tc.append(tclist[i])
print tc

if len(ip) == 0:
    print u'没有获取到IP'
    sys.exit()
elif len(tc) == 0:
    print u'没有获取到帐号'
    sys.exit()
elif len(ip) != len(tc):
    print u'IP的数量和帐号数量不一致,请核对后再试'
    sys.exit()
else:
    pass

tcque = deque(tc)
#spiderbase.cfg webmon.tencent.user=
#sespider.cfg SETencentMblog=
#scp -pr ~/spiders/sespider/ appadmin@211.149.199.70:~/
#sed -i "s/^spider_group=.*/spider_group=888/g" ~/spiders/sespider_888/sespider.cfg

start = raw_input('请确认IP和帐号都是否正确,若不正确,可直接按回车键退出\n确认后请输入一个起始Gid:\n')

if start.isdigit():
    pass
else:
    sys.exit()

log = open('upload.log','a+')
ctime = time.strftime('%Y%m%d %H%M%S')
log.write('\n')
log.write(ctime)
log.write('\n')

for i in ip:
    itc = tcque.popleft()
    print i+':sespider_'+str(start)+':'+itc

    mvspider = 'mv ~/upload/spiders/sespider_* ~/upload/spiders/sespider_'+str(start)
    os.system(mvspider)

    sedgroup = 'sed -i "s/^spider_group=.*/spider_group='+str(start)+'/g" ~/upload/spiders/sespider_'+str(start)+'/sespider.cfg'
    os.system(sedgroup)

    sedtc = 'sed -i "s/^SETencentMblog.*/SETencentMblog='+itc+'/g" ~/upload/spiders/sespider_'+str(start)+'/sespider.cfg'
    os.system(sedtc)

    sedgid = 'sed -i "s/^webmon\.sespider\.gid.*/webmon.sespider.gid='+str(start)+'/g" ~/upload/spiders/sespider_'+str(start)+'/spiderbase.cfg'
    os.system(sedgid)

    sedtcuser = 'sed -i "s/^webmon\.tencent\.user.*/webmon.tencent.user='+itc+'/g" ~/upload/spiders/sespider_'+str(start)+'/spiderbase.cfg'
    os.system(sedtcuser)

    upload = 'scp -pr ~/upload/spiders/sespider_'+str(start)+' appadmin@'+i+':~/'
    os.system(upload)
    
    l = i+':sespider_'+str(start)+':'+itc
    log.write(l)
    log.write('\n')
    print 'Complete.\n'

    start = int(start)+1

log.close()
