# -*- coding: utf-8 -*-
import requests
import json

chat = """
李阳  09:55:42
李阳：
昨天：整理spl未做完的需求，开始spl获取mapping优化的问题，讨论mapping优化策略
今天：整理mapping的设计文档，开发分index获取mapping部分
张梓聪  09:55:54
黎叔说10点之前没进会议室的都要发红包，大家别迟到了
你 撤回了一条消息
胡明昊  11:36:58
胡明昊：
昨天：修改算法服务接口，review自动部署代码，开发自动部署接口
今天：继续开发自动部署接口
张梓聪  11:38:20
张梓聪：
昨天：准备分享PPT，修改review，健康度调研
今天：解决review不能提交的问题，开发健康度demo
bug：无
赵俊炜  11:41:26
赵俊炜：
昨天：
1. 修改分页问题  2. 继续修改前面写的模块代码
今天：
1. Review 资源连表操作的代码 2. 开始新版仪表盘Grid控件开发
孙小晶  11:45:55
孙小晶：
昨天：补充趋势图多值表格的自动化用例，研究元素拖拽
今天：查看元素拖拽不生效原因，寻找其他解决方案
孙晓辰  11:57:58
孙晓辰：
昨天：提bug：1个 RZY-3985
           验证bugfix；在232升级环境验证智能运维功能；收集测试群售前的问题在jira上提出改进
今天：继续在232升级环境验证智能运维功能
王月明  12:01:17
王月明：
昨天：查web打包不成功问题，定位问题后，转交前端；打包测试3.0release；
今天：修改enkins每个子模块、YDP、rpm拷贝到其他路径
王月明  12:05:07
修正：
王月明：
昨天：查web打包不成功问题，定位问题后，转交前端；打包测试3.0release；
今天：修改jenkins每个子模块、YDP、rpm拷贝到其他路径
吕伟朝  14:10:47
吕伟朝：
昨天：完成api 资源操作工具类，自测，开发api 报表75%
今天：完成api 报表模块
徐玥  14:29:51
徐玥：
昨天：
1. 详情页开发：数据集树的交互，进度80%
2. 修改数据集API，添加批量更改数据集节点接口
今天：
1. 继续详情页开发：数据集树的交互
2. 详情页剩余部分开发
秋.实  14:31:22
王秋实：
昨天：继续讨论仪表盘改版问题，资源包导入功能65%
今天：研发季度会，讨论告警和定时任务处理流程，资源包导入功能67%？
孙文举  14:31:39
孙文举：
昨天：
	上午：办理入职手续
	下午：安装环境和熟悉系统
今天：
	熟悉react框架
张珈齐  14:31:47
张珈齐：
昨天：完成开发结算管理并自测api, 适配apps层代码40%
今天：预计完成适配apps层代码并自测
阳光  14:33:10
马阳光：
昨天：
-大屏四期新任务整理；
-大屏弧形柱图控件开发-10%
今天：
-解决 v3.0 前端打包问题；
蒋娜蝶  14:35:07
蒋娜蝶
昨天：阅读日志易v3.0Manager使用手册，
安装2.4.0.5版本并上传数据，升级Manager Server版本，升级Agent版本并提出优化RZY-3984，更新日志易安装包
今天：
验证manager用例
陈爽  14:35:23
陈爽：
昨天：验证manager升级；验证：SPL及beaver-50%；
今天：继续
郭晨  14:40:40
郭晨：
昨天：完成apikey模块的api和yottaweb层代码
今天：测试apikey接口，开始实现apikey界面
黎吾平  14:44:37
黎吾平：
昨天：1、review智能运维的代码，研发季度会PPT整理
今天：1、继续研究一下streamset的processor配置与界面交互方案
贺星瑞  14:44:49
贺星瑞：
昨天：调研itsi近期任务，查看已完成代码，字段提取列表页功能适配。
今天：查看两个itsi bug 3980，3985，开始写训练验证分离。
剩余两个low级别bug。
李英  14:46:40

李英
昨天：1.熟悉国网黑龙江定制版yottaweb连接通用版环境问题及方案；
           2. 官网主题模板增加侧栏功能；开发官网首页80% -> 经讨论另改方案。
今天：云服务->SAAS页面的开发；
代彬  14:47:24
代彬：
昨天：
    继续PieChat的Bar图
	给新员工培训
今天：
	继续PieChart的Bar图，预计完成60%
董娇阳  14:52:14
董娇阳 
昨天：修改整理测试报告。
           继续开发解析bson path的逻辑。
           Fix jpath的功能支持问题以及协助spl看mapping的问题。
今天：jpath功能问题修改。
           继续开发测试bson path的逻辑。
陈熠祺  14:53:21
陈熠祺：
昨天：1、继续测esper重启逻辑方面语句；2、优化review中提到的问题。
今天：1、开会；2、写单元测试。
秦凯  14:55:20
秦凯
昨天：梳理国网cas相关问题讲解，数据集栏拖动效果根据设计优化，搜索页上部数据集和数据权限页面展示部分完成
今天：遗留问题处理
丘木子  14:56:07
丘木子
昨天：提交license代码，mysql库相关，写tokenfinder和getdomain增加返回值
今天：上午开会，继续写tokenfinder和getdomain增加返回值，增加license单元测试，整理并开始开发auth和collector之间的接口
李阳  15:18:36
@孟猛,@王阳阳,@豆蔷,@康鹏,@刘诗韵,@康华阳,@尹云飞,@程涛,@田燕芳 请注意晨报
supertim  15:20:58
程涛
昨天 & 今天 review代码，帮助协查问题
康鹏  15:21:07
康鹏：
昨天：修复两个bug，自动检测部分code review，继续单元测试
今天：修复两个bug[RZY-3421]，继续自动检测算法返回值解析，自动检测部分90%
豆蔷  15:22:25
豆蔷：
昨天：
1. 写定时任务的zk选举部分并添加单元测试
2. 下午请假
今天：
1. 上午开会
2. 看亿联的备份的gc问题
3. 看定时任务的review
4. 改worker的单元测试
田燕芳  15:22:29
田燕芳：
昨天：事假1天
今天：继续进行租户管理系统测试，并对jira中的问题进行跟踪验证
康华阳  15:42:03
康华阳：
昨天：定时任务重构数据库异常处理
今天：继续
孟猛  16:03:05
孟猛：
昨天：讨论测试遇到的问题，解决IP识别问题
今天：无待解决bug，整理代码补充replacement优先级结构
李阳  16:04:42
已截止
刘诗韵  16:05:01
刘诗韵：
昨天：1.【客服】回答一些客户问题。
　　　（1）华夏银行 -- 李昕禹 -- API问题。
　　　（2）其它：回答其他一些问题。
　　　2.【通用】修改插件为内置三种样例，讨论测试跑通，提交review。
今天：1.【通用】定时任务迁移 — 根据review修改，优化一些问题。
　　　2.【客服】回答调查解决客户问题。
刘诗韵  16:05:29
"""

host = "localhost"
# host = "192.168.1.160"
port = 8012


def test_generate():
    url = "http://%s:%s/generate" % (host, port)
    d = {
        "chat_content": chat,
        "absent_persons": []
    }
    payload = json.dumps(d, ensure_ascii=False)
    headers = {'content-type': "application/json"}
    response = requests.request("POST", url, data=payload, headers=headers)
    print response.text


def test_person_stat():
    url = "http://%s:%s/person_stat" % (host, port)
    d = {
        "name": "胡明昊",
        "start_date": "20190722",
        "end_date": "20190724",
    }
    payload = json.dumps(d, ensure_ascii=False)
    headers = {'content-type': "application/json"}
    response = requests.request("POST", url, data=payload, headers=headers)
    print response.text


def test_person_history():
    url = "http://%s:%s/person_history" % (host, port)
    d = {
        "name": "胡明昊",
        "start_date": "20190722",
        "end_date": "20190724",
    }
    payload = json.dumps(d, ensure_ascii=False)
    headers = {'content-type': "application/json"}
    response = requests.request("POST", url, data=payload, headers=headers)
    print response.text


def test_total_stat():
    url = "http://%s:%s/total_stat" % (host, port)
    d = {
        "start_date": "20190722",
        "end_date": "20190724",
    }
    payload = json.dumps(d, ensure_ascii=False)
    headers = {'content-type': "application/json"}
    response = requests.request("POST", url, data=payload, headers=headers)
    print response.text


test_person_stat()