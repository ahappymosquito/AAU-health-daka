#!/bin/sh

log=$(cat /gaozimin/log.txt)
echo $log | mail -s "健康打卡情况" 484673216@qq.com

