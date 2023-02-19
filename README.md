# 安徽农业大学健康打卡
- 2023.2.19健康打卡重新移出内网，同时cookie中增加了cookiesession1，目前最新版本已发布
- 2023.2.13开学打卡一周，需连接学校内网
- 2022.12.15更新为安全打卡，新增是否在校，是否感染选项
- 已经结束咧2023.1.1
## 食用方法
1. 安装几个依赖库
2. 安装chrome版driver放在/opt/google/chrome/chromedriver
3. 填上ll列表 学号密码姓名邮箱
4. 使用crontab定时任务 
> ~~蹲个大佬pull个rsa加密解决方法~~
## 目前功能   
1. 每日健康打卡
2. 每日请销假 //~~疫情期间不允许请假了~~放开喽
## TODO
1. 完成rsa加密算法的初始登陆，代替之前的selenium
2. 网站管理打卡数据，避免手动录入数据
3. 将定时，发送邮件写入程序中，摆脱系统依赖
4. maybe can use github Actions to promiss privacy
5. split yaml for usr/pw
6. catch except and restart

<img src="/xsLogin.png"
     alt="null"
     style="zoom:20%"/>
<!-- <center><p>http://fresh.ahau.edu.cn/yxxt-v5/web/xsLogin/login.zf?rdt=web%2Fjkxxtb%2FtbJkxx</p></center> -->

<img src="/tbJkxx.png"
     alt="null"
     style="zoom:1%"/>
<!-- <center><p>http://fresh.ahau.edu.cn/yxxt-v5/web/jkxxtb/tbJkxx.zf</p></center> -->

## 免责声明
### 下载, 使用脚本时均视为已经仔细阅读并完全同意以下条款:
+ 脚本仅供个人学习与交流使用，严禁用于商业以及不良用途
+ 使用本脚本所存在的风险将完全由其本人承担，脚本作者不承担任何责任
+ 本声明未涉及的问题请参见国家有关法律法规，当本声明与国家有关法律法规冲突时，以国家法律法规为准
