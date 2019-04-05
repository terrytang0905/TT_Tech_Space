---
layout: post
category : database
tags : [bigdata,database,guide]
title: PostgreSQL Best Practice Note
---

[PostgreSQL&Greenplum如来神掌](https://github.com/digoal/blog/blob/master/201706/20170601_02.md)

**作者digoal**


转载目录

一、案例

1 多字段任意组合、任意维度实时圈人(ADHoc查询)

1、《多字段，任意组合(0建模) - 毫秒级实时圈人》

2、《万亿级营销(圈人)迈入毫秒时代 - 实时推荐系统数据库设计》

3、用阿里云RDS varbitx支持万亿user_tags级实时圈人

《阿里云RDS for PostgreSQL varbitx插件与实时画像应用场景介绍》

《基于 阿里云RDS PostgreSQL 打造实时用户画像推荐系统》

《阿里云RDS PostgreSQL varbitx实践 - 流式标签 (阅后即焚流式批量计算) - 万亿级，任意标签圈人，毫秒响应》

《惊天性能！单RDS PostgreSQL实例 支撑 2000亿 - 实时标签透视案例 (含dblink异步并行调用)》

4、《音视图(泛内容)网站透视分析 DB设计 - 阿里云(RDS、HybridDB) for PostgreSQL最佳实践》

5、任意维度TOP N

《秒级任意维度分析1TB级大表 - 通过采样估值满足高效TOP N等统计分析需求》

6、《画像圈人 + 人群行为透视》

7、《PostgreSQL 多字段任意组合搜索的性能》

8、《PostgreSQL 全局ID分配(数据字典化)服务 设计实践》

9、《PostgreSQL ADHoc(任意字段组合)查询 与 字典化 (rum索引加速) - 实践与方案1》

2 时序数据实时计算、处理

1、《时序数据合并场景加速分析和实现 - 复合索引，窗口分组查询加速，变态递归加速》

2、《PostgreSQL 证券行业数据库需求分析与应用》

3、ToB时序数据实时全文搜索实践

《行为、审计日志 (实时索引/实时搜索)建模 - 最佳实践 1》

《行为、审计日志 (实时索引/实时搜索)建模 - 最佳实践 2》

4、《PostgreSQL 海量时序数据(任意滑动窗口实时统计分析) - 传感器、人群、物体等对象跟踪》

5、《时序业务，求每个传感器、对象的最新值（从7秒到7毫秒的优化之旅） - 阿里云RDS PostgreSQL最佳实践》

6、《泛电网系统 海量实时计算+OLTP+OLAP DB设计 - 阿里云(RDS、HybridDB) for PostgreSQL最佳实践》

7、《PostgreSQL APP海量FEED LOG实时质量统计CASE(含percentile_disc)》

8、《PostgreSQL 时序数据案例 - 时间流逝, 自动压缩, 同比\环比》

9、《PostgreSQL 按需切片的实现(TimescaleDB插件自动切片功能的plpgsql schemaless实现)》

10、《PostgreSQL 时序数据库插件 timescaleDB 部署实践(含例子 纽约TAXI数据透视分析) - PostGIS + timescaleDB => PG时空数据库》

11、《PostgreSQL 异步消息实践 - Feed系统实时监测与响应(如 电商主动服务) - 分钟级到毫秒级的实现》

12、《PostgreSQL 业务数据质量 实时监控 实践》

13、《多流实时聚合 - 记录级实时快照 - JSON聚合与json全文检索的功能应用》

3 时间、空间、业务 多维数据实时透视

1、《数据透视 - 商场(如沃尔玛)选址应用》

2、《时间+空间 实时多维数据透视》

3、《PostgreSQL\GPDB 毫秒级海量 多维数据透视 典型案例分享》

4、《PostgreSQL\GPDB 毫秒级海量 时空数据透视 典型案例分享》

5、《时间、空间、对象多维属性 海量数据任意多维 高效检索 - 阿里云RDS PostgreSQL最佳实践》

6、《(新零售)商户网格化(基于位置GIS)运营 - 阿里云RDS PostgreSQL、HybridDB for PostgreSQL最佳实践》

4 独立事件相关性分析
1、《潘金莲改变了历史吗 - PostgreSQL舆情事件分析应用》

2、《为什么啤酒和纸尿裤最搭 - 用HybridDB/PostgreSQL查询商品营销最佳组合》

3、《PostgreSQL 独立事件相关性分析 二 - 人车拟合》

5 海量关系实时图式搜索
1、《金融风控、公安刑侦、社会关系、人脉分析等需求分析与数据库实现 - PostgreSQL图数据库场景应用》

2、《一场IT民工 与 人贩子 之间的战争 - 只要人人都献出一点爱》

3、《PostgreSQL 实践 - 内容社区(如论坛)图式搜索应用》

4、《PostgreSQL 图式搜索(graph search)实践 - 百亿级图谱，毫秒响应》

5、《PostgreSQL 大学选课相关性应用实践》

6、《PostgreSQL 家谱、族谱类应用实践 - 图式关系存储与搜索》

6 社交业务案例
1、《PCC性能大赛 - facebook\微博 like场景 - 数据库设计与性能压测》

2、《facebook linkbench 测试PostgreSQL社交关系图谱场景性能》

3、《PostgreSQL 类微博FEED系统 - 设计与性能指标》

4、《PostgreSQL 社交类好友关系系统实践 - 正反向关系查询加速》

7 流式数据实时处理案例
1、《流计算风云再起 - PostgreSQL携PipelineDB力挺IoT》

2、《(流式、lambda、触发器)实时处理大比拼 - 物联网(IoT)\金融,时序处理最佳实践》

3、《"物联网"流式处理应用 - 用PostgreSQL实时处理(万亿每天)》

4、《基于PostgreSQL的流式PipelineDB, 1000万/s实时统计不是梦》

5、《数据保留时间窗口的使用》

6、《实时数据交换平台 - BottledWater-pg with confluent》

7、《[转]流数据库 概率计算概念 - PipelineDB-Probabilistic Data Structures & Algorithms》

8、《PostgreSQL 流式统计 - insert on conflict 实现 流式 UV(distinct), min, max, avg, sum, count ...》

9、《超时流式处理 - 没有消息流入的数据异常监控》

10、《SQL流式案例 - 旋转门压缩(前后计算相关滑窗处理例子)》

11、《人、机客户服务质量 - 实时透视分析 - (多股数据流上下文相关实时分析,窗口保持)》

12、《PostgreSQL 流计算插件pipelinedb sharding 集群版原理介绍 - 一个全功能的分布式流计算引擎》

8 物联网
1、《IoT(物联网)极限写入、消费 最佳实践 - 块级(ctid)扫描》

2、物联网数据有损压缩 - 旋转门压缩

《PostgreSQL 三角函数的用法举例 - 已知3点求夹角（旋转门续）》

《旋转门数据压缩算法在PostgreSQL中的实现 - 流式压缩在物联网、监控、传感器等场景的应用》

3、范围类型助力物联网

《PostgreSQL 黑科技 range 类型及 gist index 20x+ speedup than Mysql index combine query》

《PostgreSQL 黑科技 range 类型及 gist index 助力物联网(IoT)》

4、《PostgreSQL 物联网黑科技 - 瘦身几百倍的索引(BRIN index)》

5、《PostgreSQL 10 - JSON 内容全文检索》

6、《车联网案例，轨迹清洗 - 阿里云RDS PostgreSQL最佳实践 - 窗口函数》

9 海量全文检索
《阿里云PostgreSQL zhparser中文分词使用》

1、《PostgreSQL 文本数据分析实践之 - 相似度分析》

2、《PostgreSQL 如何高效解决 按任意字段分词检索的问题》

3、《PostgreSQL 全文检索加速 快到没有朋友 - RUM索引接口(潘多拉魔盒)》

4、《聊一聊双十一背后的技术 - 分词和搜索》

5、《PostgreSQL 行级 全文检索》

6、《全文检索 不包含 优化 - 阿里云RDS PostgreSQL最佳实践》

7、《用PostgreSQL 做实时高效 搜索引擎 - 全文检索、模糊查询、正则查询、相似查询、ADHOC查询》

8、《PostgreSQL 全文检索之 - 位置匹配 过滤语法(例如 '速度 <1> 激情')》

9、《PostgreSQL - 全文检索内置及自定义ranking算法介绍 与案例》

10、《PostgreSQL 全文检索 - 词频统计》

11、《[未完待续] PostgreSQL 全文检索 大结果集优化 - fuzzy match》

10 海量模糊、正则查询案例
1、《PostgreSQL 模糊查询最佳实践》

2、《中文模糊查询性能优化 by PostgreSQL trgm》

3、《聊一聊双十一背后的技术 - 毫秒分词算啥, 试试正则和相似度》

4、《PostgreSQL 百亿数据 秒级响应 正则及模糊查询》

5、《PostgreSQL 全表 全字段 模糊查询的毫秒级高效实现 - 搜索引擎颤抖了》

6、《从难缠的模糊查询聊开 - PostgreSQL独门绝招之一 GIN , GiST , SP-GiST , RUM 索引原理与技术背景》

7、《PostgreSQL 模糊查询 与 正则匹配 性能差异与SQL优化建议》

8、《多国语言字符串的加密、全文检索、模糊查询的支持》

11 海量文本、数组、图像相似特征 实时检索
1、《电商内容去重\内容筛选应用(实时识别转载\盗图\侵权?) - 文本、图片集、商品集、数组相似判定的优化和索引技术》

2、《文本(关键词)分析理论基础 - TF/IDF》

3、《smlar插件详解》

4、《rum, smlar应用场景分析》

5、《从相似度算法谈起 - Effective similarity search in PostgreSQL》

6、《PostgreSQL 在视频、图片去重，图像搜索业务中的应用》

7、《弱水三千,只取一瓢,当图像搜索遇见PostgreSQL(Haar wavelet)》

8、《海量数据,海明(simhash)距离高效检索(smlar) - 阿里云RDS PosgreSQL最佳实践》

9、《PostgreSQL 相似搜索分布式架构设计与实践 - dblink异步调用与多机并行(远程 游标+记录 UDF实例)》

10、《PostgreSQL 相似搜索设计与性能 - 地址、QA、POI等文本 毫秒级相似搜索实践》

11、多值字段（数组、多重含义数组、全文检索） + 单值字段 组合查询加速案例

《PostgreSQL 店铺运营实践 - JSON[]数组 内部标签数据等值、范围检索100倍+加速示例 (含，单值+多值列合成)》

《PostgreSQL UDF实现tsvector(全文检索), array(数组)多值字段与scalar(单值字段)类型的整合索引(类分区索引) - 单值与多值类型复合查询性能提速100倍+ 案例 (含，单值+多值列合成)》

《PostgreSQL 多重含义数组检索与条件过滤 (标签1:属性, 标签n:属性) - 包括UPSERT操作如何修改数组、追加数组元素》

12 数据清洗、采样、脱敏、批处理、合并
1、数据采样和脱敏实践

《PostgreSQL 数据采样与脱敏》

《PostgreSQL 巧妙的数据采样方法》

2、数据清洗和去重实践

《PostgreSQL 数据去重方法大全》

《PostgreSQL 重复 数据清洗 优化教程》

3、《数据入库实时转换 - trigger , rule》

4、《PostgreSQL 如何实现批量更新、删除、插入》

5、《PostgreSQL upsert功能(insert on conflict do)的用法》

6、《PostgreSQL 如何实现upsert与新旧数据自动分离》

7、《PostgreSQL 数据rotate用法介绍 - 按时间覆盖历史数据》

8、《PostgreSQL rotate table 自动清理调度 - 约束，触发器》

9、《PostgreSQL 相似文本检索与去重 - (银屑病怎么治？银屑病怎么治疗？银屑病怎么治疗好？银屑病怎么能治疗好？)》

13 空间数据应用案例
1、《geohash vs PostGIS》

2、《PostgreSQL 物流轨迹系统数据库需求分析与设计 - 包裹侠实时跟踪与召回》

2.1、电子围栏应用

《菜鸟末端轨迹(解密支撑每天251亿个包裹的数据库) - 阿里云RDS PostgreSQL最佳实践》

3、《多点最优路径规划 - (商旅问题,拼车,餐饮配送,包裹配送,包裹取件,回程单)》

4、无人驾驶背后的数据库技术

《无人驾驶背后的技术 - PostGIS点云(pointcloud)应用 - 1》

《无人驾驶背后的技术 - PostGIS点云(pointcloud)应用 - 2》

5、《PostgreSQL 百亿地理位置数据 近邻查询性能》

6、GIS 近邻查询优化

《PostgreSQL 9.1 nearest-neighbor search use gist index》

《GIS 附近查找性能优化》

7、《空间复合索引加速空间搜索》

8、《聊一聊双十一背后的技术 - 物流、动态路径规划》

9、《SRID (空间引用识别号, 坐标系)》

《PostGIS 坐标转换(SRID)的边界问题引发的专业知识 - ST_Transform》

《地理坐标系（球面坐标系）和投影坐标系（平面坐标系）》

10、《医疗大健康行业案例(老人健康实时监测和预警) - 阿里云RDS PostgreSQL最佳实践》

11、《PostgreSQL 单列组合查询优化 - 多个多边形查询优化》

12、《PostGIS空间索引(GiST、BRIN、R-Tree)选择、优化 - 阿里云RDS PostgreSQL最佳实践》

13、《数据寻龙点穴（空间聚集分析） - 阿里云RDS PostgreSQL最佳实践》

14、《视觉挖掘与PostGIS空间数据库的完美邂逅 - 广告营销\圈人》

15、《万亿级电商广告 - brin黑科技带你(最低成本)玩转毫秒级圈人(视觉挖掘姊妹篇) - 阿里云RDS PostgreSQL, HybridDB for PostgreSQL最佳实践》

16、《PostgreSQL 助力企业打开时空之门 - 阿里云(RDS、HybridDB) for PostgreSQL最佳实践》

17、《PostGIS 点面叠加视觉判断输出》

18、《海量用户实时定位和圈人 - 团圆社会公益系统(位置寻人\圈人)》

19、《空间|时间|对象 圈人 + 透视 - 暨PostgreSQL 10与Greenplum的对比和选择》

20、空间包含查询原理、优化

《PostgreSQL 空间切割(st_split, ST_Subdivide)功能扩展 - 空间对象网格化 (多边形GiST优化)》

《PostgreSQL 空间st_contains，st_within空间包含搜索优化 - 降IO和降CPU(bound box) (多边形GiST优化)》

《PostgreSQL multipolygon 空间索引查询过滤精简优化 - IO，CPU放大优化》

《PostgreSQL raster(栅格数据) st_value 优化举例》

21、《PostgreSQL + PostGIS + SFCGAL 优雅的处理3D数据》

22、电子围栏

《PostgreSQL 电子围栏的应用场景和性能(大疆、共享设备、菜鸟。。。)》

24、《PostgreSQL 3D City 应用》

25、地图导入

《如何将谷歌地球(google earth) 的数据导入 PostgreSQL》

《OSM(OpenStreetMap) poi、路网 数据导入 PostgreSQL》

26、空间投影

《PostGIS 距离计算建议 - 投影 与 球 坐标系, geometry 与 geography 类型》

27、《PostgreSQL 实时位置跟踪 + 轨迹分析系统实践 - 单机顶千亿轨迹/天》

28、时空调度系统

《滴滴打车派单系统思考 数据库设计与实现 - 每月投入6140元, 1天最多可盈利117亿 -_-!》

《PostgreSQL 滴滴派单 高峰区域集中打车冲突优化1 - 宇宙大爆炸理论与PostgreSQL实践》

《为什么geometry+GIST 比 geohash+BTREE更适合空间搜索 - 多出的不仅仅是20倍性能提升》

14 金融业务、多副本架构
1、金融级可靠性

《PostgreSQL 10 - 任意wal副本数，金融级高可用与可靠性并存需求》

《PostgreSQL 金融行业高可用和容灾解决方案》

《PostgreSQL 9.6 同步多副本 与 remote_apply事务同步级别》

《PG多节点(quorum based), 0丢失 HA(failover,switchover)方案》

《数据库平滑switchover的要素 - 会话资源漂移》

《PostgreSQL 10 流式物理、逻辑主从 最佳实践》

《PostgreSQL - 鱼与熊掌可兼得 - 多副本0丢失与高性能兼得 - 事务级异步、同步开关》

2、线性回归与数据预测实践

《PostgreSQL 多元线性回归 - 1》

《在PostgreSQL中用线性回归分析 - 实现数据预测》

《PostgreSQL 一元线性回归 - 股价预测 1》

《PostgreSQL 一元线性回归 - 股价预测 2》

《PostgreSQL 多元线性回归 - 股价预测 3》

3、《PostgreSQL 金融类账务流水数据快照分析 案例分享》

4、《小微贷款、天使投资(风控助手)业务数据库设计 - 阿里云RDS PostgreSQL, HybridDB for PostgreSQL最佳实践》

15 异步消息应用案例
1、《[转载]postgres+socket.io+nodejs实时地图应用实践》

2、《从电波表到数据库小程序之 - 数据库异步广播(notify/listen)》

3、《从微信小程序 到 数据库"小程序"》

16 海量冷热数据分离 - 突破数据库存储限制，分级存储
1、《ApsaraDB的左右互搏(PgSQL+HybridDB+OSS) - 解决OLTP+OLAP混合需求》

2、《海量数据 "写入、共享、存储、计算" 最佳实践》

3、《从人类河流文明 洞察 数据流动的重要性》

17 倒排索引案例
1、《宝剑赠英雄 - 任意组合字段等效查询, 探探PostgreSQL多列展开式B树 (GIN)》

2、《PostgreSQL 聚集存储 与 BRIN索引 - 高并发行为、轨迹类大吞吐数据查询场景解说》

3、《PostgreSQL GIN 单列聚集索引 应用》

18 Greenplum
1. 最佳使用实践
《Greenplum 最佳实践 - 三张图读懂OLAP数据库在企业的正确使用姿势》

《Greenplum 行存、列存，堆表、AO表的原理和选择》

《Greenplum 行存、列存，堆表、AO表性能对比 - 阿里云HDB for PostgreSQL最佳实践》

《Greenplum 最佳实践 - 行存与列存的选择以及转换方法》

《Greenplum 清理垃圾、修改存储模式（行列变换） 平滑方法 - 交换数据、交互分区》

《Greenplum 最佳实践 - 数据分布黄金法则 - 分布列与分区的选择》

《Greenplum 类型一致性使用注意 - 索引条件、JOIN的类型一致性限制》

《Greenplum 跨库数据JOIN需求 - dblink的使用和弊端以及解决方案》

2. 估值计算实践
《Greenplum 最佳实践 - 估值插件hll的使用(以及hll分式聚合函数优化)》

《PostgreSQL、Greenplum 滑动窗口 分析SQL 实践》

3. 评估实践
《Greenplum 性能评估公式 - 阿里云HybridDB for PostgreSQL最佳实践》

《如何评估Greenplum master 空间以及segment元数据占用的空间》

《Greenplum 计算能力估算 - 暨多大表需要分区，单个分区多大适宜》

4. 索引使用实践
《Greenplum 最佳实践 - 什么时候选择bitmap索引》

《PostgreSQL 9种索引的原理和应用场景》

《Greenplum 空间(GIS)数据检索 b-tree & GiST 索引实践 - 阿里云HybridDB for PostgreSQL最佳实践》

5. 开发实践
《Greenplum 排序nulls first|last的 SQL写法实现》

《Greenplum 最佳实践 - 如何支持反转索引(reverse, orafunc)》

《Greenplum 最佳实践 - 多维分析的使用(CUBE, ROLLUP, GROUPING SETS in GreenPlum and Oracle)》

《Greenplum 的Oracle兼容性之 - orafunc (orafce)》

《Greenplum 最佳实践 - 函数内嵌套查询在query中调用的替代方案》

《PivotalR between R & PostgreSQL-like Databases(for exp : Greenplum, hadoop access by hawq)》

《为什么啤酒和纸尿裤最搭 - 用HybridDB/PostgreSQL查询商品营销最佳组合》

《Greenplum 模糊查询 实践》

6. OSS+GP实践
《打造云端流计算、在线业务、数据分析的业务数据闭环 - 阿里云RDS、HybridDB for PostgreSQL最佳实践》

7. 日常维护实践
《Greenplum通过gp_dist_random('gp_id') 在所有节点调用某个函数》

《PostgreSQL、Greenplum 日常监控 和 维护任务 - 最佳实践》

《Greenplum 列存表(AO表)的膨胀、垃圾检查与空间收缩》

《如何检测、清理Greenplum HEAP对象膨胀、垃圾 - 阿里云HybridDB for PG最佳实践》

8. 数据同步实践
《MySQL准实时同步到PostgreSQL, Greenplum的方案之一 - rds_dbsync》

《Greenplum, PostgreSQL 数据实时订阅的几种方式》

9. 数据导入实践
《Greenplum insert的性能(单步\批量\copy) - 暨推荐使用gpfdist、阿里云oss外部表并行导入》

10. 数据合并实践
《PostgreSQL、Greenplum DML合并操作 最佳实践》

《Greenplum merge insert 用法与性能 (insert on conflict) - 2》

《Greenplum merge insert 用法与性能 (insert on conflict) - 1》

11. 优化
《Greenplum explain analyze 解读 + 深度明细开关》

《大量使用临时表带来的系统表如pg_attribute膨胀问题，替代方案，以及如何擦屁股 - Greenplum, PostgreSQL最佳实践》

12. 诊断
《Greenplum 统计信息收集参数 - 暨统计信息不准引入的broadcast motion一例》

《Greenplum segment级锁问题排查方法 - 阿里云HybridDB for PostgreSQL最佳实践》

《Greenplum RT高的原因分析 和 优化方法》

《PostgreSQL 锁等待监控 珍藏级SQL - 谁堵塞了谁》

13. GP OLTP 实践
《Greenplum 连接池实践》

《让greenplum的oltp性能飞起来 - 直接读写数据节点》

《Greenplum segment节点直接读写配置与性能》

《Greenplum 点查询的优化(分布键)》

《Greenplum 点查(按PK查询)性能与提升空间》

《Use pgbouncer connect to GreenPlum's segment node》

14. 原理
《轻松打爆netfilter conntrack table的Greenplum SQL》

《Greenplum , HAWQ outer join与motion问题讲解》

《PostgreSQL distinct 与 Greenplum distinct 的实现与优化》

《Greenplum vacuum ao表和heap表的区别》

《PostgreSQL vs Greenplum Hash outer join hash表的选择》

《分布式DB(Greenplum)中数据倾斜的原因和解法 - 阿里云HybridDB for PostgreSQL最佳实践》

《Greenplum 列存储加字段现象 - AO列存储未使用相对偏移》

《解密上帝之手 - 阿里云HDB for PostgreSQL数据库metascan特性(存储级、块级、batch级过滤与数据编排)》

《Greenplum 内存与负载管理(resource queue)最佳实践》

《Greenplum 资源隔离的原理与源码分析》

《Greenplum ORCA 优化器的编译安装与使用》

《PostgreSQL和Greenplum的临时表空间介绍》

《Greenplum 表空间和filespace的用法》

节约98%的数据存储成本的方法

《PostgreSQL n阶乘计算, 排列组合计算 - 如何计算可变参数中有没有重复参数》

《PostgreSQL 计算 任意类型 字段之间的线性相关性》

《一个简单算法可以帮助物联网,金融 用户 节约98%的数据存储成本 (PostgreSQL,Greenplum帮你做到)》

《Greenplum hash分布算法》

《Greenplum "Sort、Group、distinct 聚合、JOIN" 不惧怕数据倾斜的黑科技和原理 - 多阶段聚合》

15. 问题集锦
《PostgreSQL, Greenplum ETL 之 - 非法字符(如0x00)过滤、转换(blob2text, bytea2text)》

《Greenplum , PostgreSQL pgcrypto 加密算法、mode、PAD的选择 - 与Oracle, MySQL的差异(安全性差异)》

《PostgreSQL 和 Greenplum pgcrypto 加解密bytea处理差异(convert, convert_from)》

《PostGIS 多点几何类型 空字符构造异常CASE - parse error - invalid geometry (lwgeom_pg.c:96)》

16. 案例
《空间|时间|对象 圈人 + 透视 - 暨PostgreSQL 10与Greenplum的对比和选择》

《音视图(泛内容)网站透视分析 DB设计 - 阿里云(RDS、HybridDB) for PostgreSQL最佳实践》

《泛电网系统 海量实时计算+OLTP+OLAP DB设计 - 阿里云(RDS、HybridDB) for PostgreSQL最佳实践》

《记录动态格式化输出(ToB日志转换业务) - 阿里云RDS PostgreSQL, HybridDB for PostgreSQL最佳实践》

《(新零售)商户网格化(基于位置GIS)运营 - 阿里云RDS PostgreSQL、HybridDB for PostgreSQL最佳实践》

《强制数据分布与导出prefix - 阿里云pg, hdb pg oss快速数据规整外部表导出实践案例》

《日增量万亿+级 实时分析、数据规整 - 阿里云HybridDB for PostgreSQL最佳实践》

《ApsaraDB的左右互搏(PgSQL+HybridDB+OSS) - 解决OLTP+OLAP混合需求》

《Greenplum roaring bitmap与业务场景 (类阿里云RDS PG varbitx, 应用于海量用户 实时画像和圈选、透视)》

19 综合应用案例
1、《从天津滨海新区大爆炸、危化品监管聊聊 IT人背负的社会责任感》

2、《(AR虚拟现实)红包 技术思考 - GIS与图像识别的完美结合》

3、《从真假美猴王谈起 - 让套牌车、克隆x 无处遁形的技术手段思考》

4、《为了部落 - 如何通过PostgreSQL基因配对，产生优良下一代》

5、《用PostgreSQL描绘人生的高潮、尿点、低谷 - 窗口/帧 or 斜率/导数/曲率/微积分?》

6、《想挑战AlphaGO吗？先和PostgreSQL玩一玩?? PostgreSQL与人工智能(AI)》

7、《PostgreSQL 特性故事汇》

8、《AI(OtterTune)引波澜 - AI会洗牌数据库行业吗? DBA如何转变思想》

9、《门禁广告销售系统需求剖析 与 PostgreSQL数据库实现》

10、《PostgreSQL 与 12306 抢火车票的思考》

11、《打造云端流计算、在线业务、数据分析的业务数据闭环 - 阿里云RDS、HybridDB for PostgreSQL最佳实践》

20 数据订阅、单元化、容灾、多机房
1、《PostgreSQL 逻辑订阅 - 给业务架构带来了什么希望？》

2、《PostgreSQL 10 - 逻辑订阅端worker数控制参数》

3、《PostgreSQL 10 - 备库支持逻辑订阅, 订阅支持主备漂移》

4、《PostgreSQL 10 - 逻辑订阅支持并行COPY初始化数据》

5、《PostgreSQL 10 - 逻辑订阅原理与最佳实践》

6、《使用PostgreSQL逻辑订阅实现 multi-master》

7、《PostgreSQL 逻辑订阅 - DDL 订阅 实现方法》

21 读写分离
1、《PostgreSQL 读写分离 proxy 1》

2、《PostgreSQL 读写分离 proxy 2 - 待编辑》

3、客户端高可用和读写分离

《PostgreSQL 10 - libpq支持多主机连接(failover,LB)让数据库HA和应用配合更紧密》

22 水平扩展
1、sharding 实践 1 - postgres_fdw + inherit

《PostgreSQL 10 - 支持分布式事务》

《PostgreSQL 10 - 索引扫描、子查询、VACUUM、fdw/csp钩子》

《PostgreSQL 10 - mergesort(Gather merge)》

《PostgreSQL 10 - pushdown 增强》

《PostgreSQL 10 - 支持Append节点并行》

《PostgreSQL 10 - postgres_fdw 多节点异步并行执行》

2、sharding 实践 2 - postgres_fdw + pg_pathman

《PostgreSQL 9.6 sharding based on FDW & pg_pathman》

《PostgreSQL 9.5+ 高效分区表实现 - pg_pathman》

《PostgreSQL 9.6 sharding + 单元化 (based on postgres_fdw) 最佳实践 - 通用水平分库场景设计与实践》

《PostgreSQL 9.6 单元化,sharding (based on postgres_fdw) - 内核层支持前传》

3、sharding 实践 3 - plproxy

《PostgreSQL 最佳实践 - 水平分库(基于plproxy)》

《A Smart PostgreSQL extension plproxy 2.2 practices》

《使用Plproxy设计PostgreSQL分布式数据库》

《阿里云ApsaraDB RDS for PostgreSQL 最佳实践 - 4 水平分库 之 节点扩展》

《阿里云ApsaraDB RDS for PostgreSQL 最佳实践 - 3 水平分库 vs 单机 性能》

《阿里云ApsaraDB RDS for PostgreSQL 最佳实践 - 2 教你RDS PG的水平分库》

4、sharding 实践 4 - citus - 待编辑

https://www.citusdata.com/

23 估值计算
《PostgreSQL count-min sketch top-n 概率计算插件 cms_topn (结合窗口实现同比、环比、滑窗分析等) - 流计算核心功能之一》

《秒级任意维度分析1TB级大表 - 通过采样估值满足高效TOP N等统计分析需求》

《PostgreSQL 任意列组合条件 行数估算 实践 - 采样估算》

《Greenplum 最佳实践 - 估值插件hll的使用(以及hll分式聚合函数优化)》

《PostgreSQL hll (HyperLogLog) extension for "State of The Art Cardinality Estimation Algorithm" - 1》

《PostgreSQL hll (HyperLogLog) extension for "State of The Art Cardinality Estimation Algorithm" - 2》

《PostgreSQL hll (HyperLogLog) extension for "State of The Art Cardinality Estimation Algorithm" - 3》

《妙用explain Plan Rows快速估算行》

《PostgreSQL pg_stats used to estimate top N freps values and explain rows》

24 实时经营分析系统
《经营、销售分析系统DB设计之PostgreSQL, Greenplum - 共享充电宝 案例实践》

《PostgreSQL 手机行业经营分析、决策系统设计 - 实时圈选、透视、估算》

25 schemaless 架构设计案例
《PostgreSQL 在铁老大订单系统中的schemaless设计和性能压测》

26 数据可视化
《[转载]易上手的数据挖掘、可视化与机器学习工具: Orange介绍》

《[未完待续]数据挖掘、可视化与机器学习工具: redash》

《[未完待续]数据挖掘、可视化与机器学习工具: superset》

27 生物科技
《PostgreSQL 遗传学应用 - 矩阵相似距离计算 (欧式距离,...XX距离)》

28 异步调用与并行计算
1、dblink异步调用、并行计算

《PostgreSQL 如何让 列存（外部列存） 并行起来》

《PostgreSQL VOPS 向量计算 + DBLINK异步并行 - 单实例 10亿 聚合计算跑进2秒》

《PostgreSQL dblink异步调用实现 并行hash分片JOIN - 含数据交、并、差 提速案例 - 含dblink VS pg 11 parallel hash join VS pg 11 智能分区JOIN》

2、PostgreSQL 11 并行计算

《PostgreSQL 11 preview - Parallel Append (多表并行计算) sharding架构并行计算核心功能之一》

《PostgreSQL 11 preview - 并行排序、并行索引 (性能线性暴增) 单实例100亿TOP-K仅40秒》

《PostgreSQL 11 preview - 分区表智能并行JOIN (已类似MPP架构，性能暴增)》

《PostgreSQL 11 preview - parallel hash (含hash JOIN , hash agg等) 性能极大提升》

29 海量数据大吞吐导出、规整
《强制数据分布与导出prefix - 阿里云pg, hdb pg oss快速数据规整外部表导出实践案例》

30 HA、sharding、多副本、读写分离
《[未完待续] [翻译] PostgreSQL 常见HA方案》

《[未完待续] PostgreSQL HA (高可用) 简明手册3 - 三节点多副本强同步架构》

《[未完待续] PostgreSQL HA (高可用) 简明手册2 - 双节点异步流复制架构》

《[未完待续] PostgreSQL MPP EXTENSION citus(分布式 sharding) 简明手册》

《[未完待续] PostgreSQL 对等架构 负载均衡(HAProxy/LVS) 简明手册》

《[未完待续] PostgreSQL 读写分离 简明手册》

《[未完待续] PostgreSQL HA (高可用) 简明手册1 - 共享存储架构》

《PostgreSQL 一主多从(多副本,强同步)简明手册 - 配置、压测、监控、切换、防脑裂、修复、0丢失 - 珍藏级》

31 未归类应用案例
《航空公司数据库设计》

《用PostgreSQL 处理 指纹 数据》

《会议室预定系统实践 - PostgreSQL tsrange(时间范围类型) + 排他约束》

《PostgreSQL 高并发任务分配系统 实践》

《PostgreSQL 电商小需求 - 凑单商品的筛选》

二、问题诊断、性能分析与优化
1、《索引顺序扫描引发的堆扫描IO放大背后的统计学原理与解决办法》

2、UUID的IO问题与实践

《PostgreSQL sharding有序UUID最佳实践 - serial global uuid stored in 64bit int8》

《PostgreSQL 优化CASE - 无序UUID性能问题诊断》

3、《自动选择正确索引访问接口(btree,hash,gin,gist,sp-gist,brin,bitmap...)的方法》

4、《优化器里的概率学 - 性能抖动原理分析》

5、《PostgreSQL 数据访问 offset 的质变 case》

6、《PostgreSQL 大行优化》

7、优化器成本因子调试

《优化器成本因子校对 - 1》

《优化器成本因子校对(disk,ssd,memory IO开销精算) - 2》

8、HINT

《PostgreSQL SQL HINT的使用(pg_hint_plan)》

《阿里云 PostgreSQL pg_hint_plan插件的用法》

《PostgreSQL 特性分析 Plan Hint》

《关键时刻HINT出彩 - PG优化器的参数优化、执行计划固化CASE》

9、《PostgreSQL 操作符与优化器详解》

10、《PostgreSQL 优化器逻辑推理能力 源码解析》

11、《聊一下PostgreSQL优化器 - in里面有重复值时PostgreSQL如何处理?》

12、《PostgreSQL SSL链路压缩例子》

13、《PostgreSQL 大表自动 freeze 优化思路》

14、《PostgreSQL的"天气预报" - 如何预测Freeze IO风暴》

15、《PostgreSQL 函数调试、诊断、优化 & auto_explain》

16、性能优化案例

《PostgreSQL性能优化综合案例讲解 - 1》

《PostgreSQL性能优化综合案例讲解 - 2》

17、《数据库界的华山论剑 tpc.org》

18、《PostgreSQL in 与 = any 的SQL语法异同与性能优化》

19、《PostgreSQL Huge Page 使用建议 - 大内存主机、实例注意》

20、《PostgreSQL 单库对象过多，触发Linux系统限制 (ext4_dx_add_entry: Directory index full!) (could not create file "xx/xx/xxxxxx": No space left on device)》

21、《PostgreSQL 垃圾版本引入的索引扫描性能下降诊断》

三、原理
1、《PostgreSQL 逻辑结构 和 权限体系 介绍》

2、数据库统计学

《PostgreSQL数据库监控中的统计学 - 对象SIZE的数据分布图》

《用PostgreSQL了解一些统计学术语以及计算方法和表示方法 - 1》

《population & sample covariance, standard deviation Aggregate in PostgreSQL》

《PostgreSQL 统计信息之 - 逻辑与物理存储的线性相关性》

3、聚合函数知识

《PostgreSQL aggregate function 1 : General-Purpose Aggregate Functions》

《PostgreSQL aggregate function 2 : Aggregate Functions for Statistics》

《PostgreSQL aggregate function 3 : Aggregate Functions for Ordered-Set》

《PostgreSQL aggregate function 4 : Hypothetical-Set Aggregate Functions》

4、数据库聚合函数运算原理

《PostgreSQL aggregate function customize》

5、分布式聚合函数运算原理

《Postgres-XC customized aggregate introduction》

6、《PostgreSQL 聚合代码优化 - OP复用浅析》

7、函数稳定性

《函数稳定性讲解 - 1》

《函数稳定性讲解 - 2》

《函数稳定性讲解 - 3》

8、《PostgreSQL nestloop/hash/merge join讲解》

9、《PostgreSQL bitmapAnd, bitmapOr, bitmap index scan, bitmap heap scan》

10、《PostgreSQL 10 - 间接索引(secondary index)》

11、《PostgreSQL 10 - 不完整索引支持复合排序》

12、《PostgreSQL 10 - 唯一约束+附加字段组合功能索引》

13、《深入浅出PostgreSQL B-Tree索引结构》

《[未完待续] PostgreSQL hash 索引结构介绍》

《PostgreSQL 黑科技 - 空间聚集存储, 内窥GIN, GiST, SP-GiST索引》

14、《PostgreSQL GIN索引实现原理》

15、《PostgreSQL GIN multi-key search 优化》

16、《懒人推动社会进步 - 多列聚合, gin与数据分布(选择性)》

17、《索引扫描优化之 - GIN数据重组优化(按元素聚合) 想象在玩多阶魔方》

18、《从一维编排到多维编排，从平面存储到3D存储 - 数据存储优化之路》

19、《列存优化(shard,大小块,归整,块级索引,bitmap scan) - (大量数据实时读写)任意列搜索》

20、字符集知识

《PostgreSQL Server Encoding sql_ascii attention》

《PostgreSQL SQL_ASCII encoding introduce》

21、数据库动态库介绍

《PostgreSQL 加载动态库详解》

《如何加快PostgreSQL结巴分词加载速度》

22、《PostgreSQL FSM 原理》

23、《PostgreSQL 如何精确计算表膨胀(fsm,数据块layout讲解) - PostgreSQL table exactly bloat monitor use freespace map data》

24、《PostgreSQL 逻辑备份一致性讲解》

25、《PostgreSQL 共享事务快照功能》

26、《PostgreSQL 事务快照功能》

27、《PostgreSQL 并行逻辑备份与一致性讲解》

28、《异步流复制模式如何保证不丢数据》

29、《执行计划选择算法 与 绑定变量》

30、《生成泊松、高斯、指数、随机分布数据》

31、《PostgreSQL 事件触发器 - PostgreSQL 9.3 Event Trigger》

32、《PostgreSQL 隐藏参数详解》

33、《PostgreSQL 9种索引的原理和应用场景》

《PostgreSQL 多查询条件，多个索引的选择算法与问题诊断方法》

《PostgreSQL 数据库多列复合索引的字段顺序选择原理》

《PostgreSQL 数据离散性 与 索引扫描性能(btree & bitmap index scan)》

34、《通过空间思想理解GiST索引的构造》

35、《解密上帝之手 - 阿里云HDB for PostgreSQL数据库metascan特性(存储级、块级、batch级过滤与数据编排)》

36、《PostgreSQL 增量备份集的有效恢复位点》

37、《PostgreSQL GUC 参数级别介绍》

38、《PostgreSQL flashback(闪回) 功能实现与介绍》

39、《GIS术语 - POI、AOI、LOI、路径、轨迹》

40、《PostgreSQL OUTER JOIN 优化的几个知识点 - 语义转换、内存带宽、JOIN算法、FILTER亲和力、TSP、HINT、命中率、存储顺序、扫描顺序、索引深度》

41、《学习 PostgreSQL Frontend/Backend protocol (通信协议)》

42、《PostgreSQL 10 自定义并行计算聚合函数的原理与实践 - (含array_agg合并多个数组为单个一元数组的例子)》

43、《PostgreSQL bitmap scan的IO放大的原理解释和优化》

44、《PostgreSQL pg_stat_reset清除track_counts的隐患》

45、《乱序写入导致的索引膨胀(B-tree, GIN, GiST皆如此)》

46、《PostgreSQL 与关系代数 (Equi-Join , Semi-Join , Anti-Join , Division)》

47、《PostgreSQL 元数据库讲解 - 对象(表、索引、函数、序列、视图...)在哪里、如何识别、如何求对象定义》

48、《Recheck Cond filter IO\CPU放大 原理与优化CASE - 含 超级大表 不包含(反选) SQL优化》

49、《PostgreSQL 并行vacuum patch - 暨为什么需要并行vacuum或分区表》

50、《PostgreSQL 通过分割heap数据文件分拆表的hacking方法》

51、《PostgreSQL checkpoint 相关参数优化设置与解释》

52、《PostgreSQL 11 preview - 分区表智能并行聚合、分组计算(已类似MPP架构，性能暴增)》

四、数据库发展方向、数据库选型
1、《数据库任督二脉 - 数据与计算的生态融合》

2、HTAP

《PostgreSQL 11 preview - JIT接口放开》

《PostgreSQL 11 preview - with_llvm JIT支持部署与试用》

《PostgreSQL 商用版本EPAS(阿里云ppas) HTAP功能之资源隔离管理 - CPU与刷脏资源组管理》

《最受开发者欢迎的HTAP数据库PostgreSQL 10特性》

《PostgreSQL 10 - 推出JIT开发框架(朝着HTAP迈进)》

《PostgreSQL 10 - OLAP增强 向量聚集索引(列存储扩展)》

《PostgreSQL 10 - OLAP提速框架, Faster Expression Evaluation Framework(含JIT)》

《PostgreSQL 向量化执行插件(瓦片式实现) 10x提速OLAP》

《分析加速引擎黑科技 - LLVM、列存、多核并行、算子复用 大联姻 - 一起来开启PostgreSQL的百宝箱》

《100TB+, 日增量1TB的OLTP OLAP混合场景数据库设计方向》

《HTAP数据库 PostgreSQL 场景与性能测试之 45 - (OLTP) 数据量与性能的线性关系(10亿+无衰减), 暨单表多大需要分区》

《HTAP数据库 PostgreSQL 场景与性能测试之 44 - (OLTP) 空间应用 - 空间包含查询(输入多边形 包含 表内空间对象)》

《HTAP数据库 PostgreSQL 场景与性能测试之 43 - (OLTP+OLAP) unlogged table 含索引多表批量写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 42 - (OLTP+OLAP) unlogged table 不含索引多表批量写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 41 - (OLTP+OLAP) 含索引多表批量写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 40 - (OLTP+OLAP) 不含索引多表批量写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 39 - (OLTP+OLAP) 含索引多表单点写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 38 - (OLTP+OLAP) 不含索引多表单点写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 37 - (OLTP+OLAP) 含索引单表批量写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 36 - (OLTP+OLAP) 不含索引单表批量写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 35 - (OLTP+OLAP) 含索引单表单点写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 34 - (OLTP+OLAP) 不含索引单表单点写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 33 - (OLAP) 物联网 - 线性字段区间实时统计》

《HTAP数据库 PostgreSQL 场景与性能测试之 32 - (OLTP) 高吞吐数据进出(堆存、行扫、无需索引) - 阅后即焚(JSON + 函数流式计算)》

《HTAP数据库 PostgreSQL 场景与性能测试之 31 - (OLTP) 高吞吐数据进出(堆存、行扫、无需索引) - 阅后即焚(读写大吞吐并测)》

《HTAP数据库 PostgreSQL 场景与性能测试之 30 - (OLTP) 秒杀 - 高并发单点更新》

《HTAP数据库 PostgreSQL 场景与性能测试之 29 - (OLTP) 空间应用 - 高并发空间位置更新（含空间索引）》

《HTAP数据库 PostgreSQL 场景与性能测试之 28 - (OLTP) 高并发点更新》

《HTAP数据库 PostgreSQL 场景与性能测试之 27 - (OLTP) 物联网 - FEED日志, 流式处理 与 阅后即焚 (CTE)》

《HTAP数据库 PostgreSQL 场景与性能测试之 26 - (OLTP) NOT IN、NOT EXISTS 查询》

《HTAP数据库 PostgreSQL 场景与性能测试之 25 - (OLTP) IN , EXISTS 查询》

《HTAP数据库 PostgreSQL 场景与性能测试之 24 - (OLTP) 物联网 - 时序数据并发写入(含时序索引BRIN)》

《HTAP数据库 PostgreSQL 场景与性能测试之 23 - (OLAP) 并行计算》

《HTAP数据库 PostgreSQL 场景与性能测试之 22 - (OLTP) merge insert|upsert|insert on conflict|合并写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 21 - (OLTP+OLAP) 排序、建索引》

《HTAP数据库 PostgreSQL 场景与性能测试之 20 - (OLAP) 用户画像圈人场景 - 多个字段任意组合条件筛选与透视》

《HTAP数据库 PostgreSQL 场景与性能测试之 19 - (OLAP) 用户画像圈人场景 - 数组相交查询与聚合》

《HTAP数据库 PostgreSQL 场景与性能测试之 18 - (OLAP) 用户画像圈人场景 - 数组包含查询与聚合》

《HTAP数据库 PostgreSQL 场景与性能测试之 17 - (OLTP) 数组相似查询》

《HTAP数据库 PostgreSQL 场景与性能测试之 16 - (OLTP) 文本特征向量 - 相似特征(海明...)查询》

《HTAP数据库 PostgreSQL 场景与性能测试之 15 - (OLTP) 物联网 - 查询一个时序区间的数据》

《HTAP数据库 PostgreSQL 场景与性能测试之 14 - (OLTP) 字符串搜索 - 全文检索》

《HTAP数据库 PostgreSQL 场景与性能测试之 13 - (OLTP) 字符串搜索 - 相似查询》

《HTAP数据库 PostgreSQL 场景与性能测试之 12 - (OLTP) 字符串搜索 - 前后模糊查询》

《HTAP数据库 PostgreSQL 场景与性能测试之 11 - (OLTP) 字符串搜索 - 后缀查询》

《HTAP数据库 PostgreSQL 场景与性能测试之 10 - (OLTP) 字符串搜索 - 前缀查询》

《HTAP数据库 PostgreSQL 场景与性能测试之 9 - (OLTP) 字符串模糊查询 - 含索引实时写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 8 - (OLTP) 多值类型(数组)含索引实时写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 7 - (OLTP) 全文检索 - 含索引实时写入》

《HTAP数据库 PostgreSQL 场景与性能测试之 6 - (OLTP) 空间应用 - KNN查询（搜索附近对象，由近到远排序输出）》

《HTAP数据库 PostgreSQL 场景与性能测试之 5 - (OLTP) 空间应用 - 空间包含查询(表内多边形 包含 输入空间对象)》

《HTAP数据库 PostgreSQL 场景与性能测试之 4 - (OLAP) 大表OUTER JOIN统计查询》

《HTAP数据库 PostgreSQL 场景与性能测试之 3 - (OLAP) 大表JOIN统计查询》

《HTAP数据库 PostgreSQL 场景与性能测试之 2 - (OLTP) 多表JOIN》

《HTAP数据库 PostgreSQL 场景与性能测试之 1 - (OLTP) 点查》

3、多核并行

《PostgreSQL 10 - 控制集群并行度》

《PostgreSQL 10 - tuplesort 多核并行创建索引》

《PostgreSQL 9.6 并行计算 优化器算法浅析》

《PostgreSQL 9.6 引领开源数据库攻克多核并行计算难题》

4、《数据库选型之 - 大象十八摸 - 致 架构师、开发者》

5、《数据库选型思考》

6、《PostgreSQL 前世今生》

7、《论云数据库编程能力的重要性》

8、《Oracle业务适合用PostgreSQL去O的一些评判标准》

9、《如何评估一款数据库产品 - 18项火眼金睛》

10、《HTAP数据库(OLTP+OLAP) - sharding 和 共享分布式存储 数据库架构 优缺点》

11、《传统分库分表(sharding)的缺陷与破解之法》

12、《阿里云 PostgreSQL 产品生态；案例、开发实践、管理实践、学习资料、学习视频》

13、《[未完待续] PostgreSQL 公司内部培训资料 - 应用开发者、架构师、CTO、DBA、内核开发者》

五、开发技巧
1、递归应用

《PostgreSQL : WITH Queries use case》

《PostgrSQL 递归SQL的几个应用 - 极客与正常人的思维》

《PostgreSQL 递归查询CASE - 树型路径分组输出》

《PostgreSQL Oracle 兼容性之 - WITH 递归 ( connect by )》

《用PostgreSQL找回618秒逝去的青春 - 递归收敛优化》

《distinct xx和count(distinct xx)的变态递归优化方法 - 索引收敛(skip scan)扫描》

《PostgreSQL 使用递归SQL 找出数据库对象之间的依赖关系》

《PostgreSQL 递归死循环案例及解法》

《PostgreSQL 递归查询一例 - 资金累加链》

《递归优化CASE - group by & distinct tuning case : use WITH RECURSIVE and min() function》

《递归优化CASE - performance tuning case :use cursor\trigger\recursive replace (group by and order by) REDUCE needed blockes scan》

《PostgreSQL 树状数据存储与查询(非递归) - Use ltree extension deal tree-like data type》

《PostgreSQL Oracle 兼容性之 - connect by》

《PostgreSQL 递归妙用案例 - 分组数据去重与打散》

《PostgreSQL Oracle 兼容性之 - INDEX SKIP SCAN (递归查询变态优化) 非驱动列索引扫描优化》

2、advisory lock应用

《PostgreSQL 使用advisory lock实现行级读写堵塞》

《PostgreSQL 无缝自增ID的实现 - by advisory lock》

《PostgreSQL 使用advisory lock或skip locked消除行锁冲突, 提高几十倍并发更新效率》

3、《PostgreSQL 如何创建不等于索引》

4、《PostgreSQL update returning NEW|OLD column value 在对账|购票|防纂改|原子操作中的妙用》

5、《如何防止数据库雪崩》

6、《随机记录并发查询与更新(转移、删除)的"无耻"优化方法》

7、《PostgreSQL 随机查询优化》

8、《论count与offset使用不当的罪名 和 分页的优化》

9、《聊一聊双十一背后的技术 - 不一样的秒杀技术, 裸秒》

《PostgreSQL 秒杀4种方法 - 增加 批量流式加减库存 方法》

10、《PostgreSQL 聚合表达式 FILTER , order , within group 用法》

11、《PostgreSQL schemaless 的实现 (类mongodb collection)》

12、《行列变换》

13、可变参数函数开发

《variable number of arguments function》

《PostgreSQL plpgsql variadic argments , parameters - 可变参数个数》

14、触发器开发

《PostgreSQL 触发器 用法详解 1》

《PostgreSQL 触发器 用法详解 2》

15、《PostgreSQL 事务，会话 GUC 变量 妙用 - 获取并跟踪事务结束时间》

16、《在PostgreSQL中实现update | delete limit》

《如何根据行号高效率的清除过期数据 - 非分区表，数据老化实践》

17、《在PostgreSQL中实现按拼音、汉字、拼音首字母搜索的例子》

18、《PostgreSQL 数组忽略大小写匹配》

19、《PostgreSQL 中如何找出记录中是否包含编码范围内的字符，例如是否包含中文》

20、《如何判断字符串是否为合法数值、浮点、科学计数等格式》

21、《如何按拼音排序 - 数据库本土化特性(collate, ctype, ...)》

22、《PostgreSQL 中生成随机汉字》

23、《PostgreSQL全角、半角互相转换》

24、《聊聊between and的坑 和 GEEK的解法》

25、《如何在PostgreSQL中调试plpgsql存储过程(pldebugger, pldbgapi)》

26、《如何优雅的修改被视图引用的表字段》

27、《采用 部分索引、表达式索引 提高搜索效率》

28、《PostgreSQL 表达式索引 - 语法注意事项》

29、《PostgreSQL UDF实现IF NOT EXISTS语法》

30、《PostgreSQL 9.6 黑科技 bloom 算法索引，一个索引支撑任意列组合查询》

31、《找对业务G点, 体验酸爽 - PostgreSQL内核扩展指南》

《[未完待续] [翻译] PostgreSQL 插件开发 5 (版本迭代) - Writing Postgres Extensions Code Organization and Versioning》

《[未完待续] [翻译] PostgreSQL 插件开发 4 (测试) - Writing Postgres Extensions - Testing》

《[未完待续] [翻译] PostgreSQL 插件开发 3 (调试) - Writing Postgres Extensions - Debugging》

《[未完待续] [翻译] PostgreSQL 插件开发 2 (类型与操作符) - Writing Postgres Extensions - Types and Operators》

《[未完待续] [翻译] PostgreSQL 插件开发 1 (基础) - Writing Postgres Extensions - the Basics》

32、《一张表有且只有一条记录(续) - 支持插入，并且更新、删除都只作用在最后一条记录上, 查询也只时间最大的记录。》

33、《人分九等，数有阶梯 - PostgreSQL 阶品（颗粒）分析函数width_bucket, kmean应用》

34、《advisory lock 实现高并发非堵塞式 业务锁》

35、《云端海量任务调度数据库最佳实践 - 阿里云RDS PostgreSQL案例》

36、《分区索引的应用和实践 - 阿里云RDS PostgreSQL最佳实践》

《PostgreSQL 范围过滤 + 其他字段排序OFFSET LIMIT(多字段区间过滤)的优化与加速》

37、《车联网案例，轨迹清洗 - 阿里云RDS PostgreSQL最佳实践 - 窗口函数》

38、《PostgreSQL 汉字转拼音的函数》

39、《PostgreSQL 空间、多维 序列 生成方法》

40、《PostgreSQL 自定义自动类型转换(CAST)》

《PostgreSQL 整型int与布尔boolean的自动转换设置(含自定义cast与cast规则介绍)》

41、《PostgreSQL 10 新特性 - identity column (serial, 自增)》

42、《[转] 快速计算Distinct Count》

43、《PostgreSQL 整型除法要注意》

44、《PostgreSQL 中英文混合分词特殊规则(中文单字、英文单词) - 中英分明》

45、《[转] java - 过滤ASCII码中的不可见字符, ASCII三部分, 各控制字符详解》

46、《[转] SqlServe到PG迁移错误:无效的编码序列"UTF8": 0x00》

47、《[转载]MySQL和PostgreSQL的常用语法差异》

48、《[转载]MySQL和PostgreSQL的数据类型对比》

49、《PostgreSQL 数据库NULL值的默认排序行为与查询、索引定义规范 - nulls first\last, asc\desc》

50、《PostgreSQL DISTINCT 和 DISTINCT ON 语法的使用》

51、《PostgreSQL UDF妙用 - mybatis等框架，不支持的语法都可以通过UDF来实现》

52、《PostgreSQL 用 CTE语法 + 继承 实现拆分大表》

53、《PostgreSQL json 任意位置 append 功能实现》

54、《PostgreSQL 索引虚拟列 - 表达式索引 - JOIN提速》

55、《电商订单 + 物流信息对称补齐案例 - A, B表，到达时间交叉，增量JOIN补全C数据》

56、《PostgreSQL 11 preview - SQL:2011 window frame clause全面支持 及 窗口、帧用法和业务场景介绍》

57、《PostgreSQL 对称加密、非对称加密用法介绍》

58、《PostgreSQL SELECT 的高级用法(CTE, LATERAL, ORDINALITY, WINDOW, SKIP LOCKED, DISTINCT, GROUPING SETS, ...)》

59、数据库函数编程

《[未完待续] PostgreSQL Oracle 兼容性之 - pl/sql 迁移到 plpgsql》

《[未完待续] PostgreSQL HeroDB GPU 加速 - pl/cuda , pg-strom , herodb》

《[未完待续] PostgreSQL 函数编程语言扩展 - pl/go》

《[未完待续] PostgreSQL 函数编程语言扩展 - pl/lua》

《[未完待续] PostgreSQL 函数编程语言扩展 - pl/swift》

60、《PostgreSQL 11 preview - MERGE 语法支持与CTE内支持，兼容SQL:2016 , 兼容 Oracle》

61、《insert on conflict - 合并写 （消除不必要更新）》

62、《PostgreSQL 11 preview - 虚拟列(自动根据表达式产生值)》

63、《PostgreSQL Oracle 兼容性之 - DBMS_SQL(存储过程动态SQL中使用绑定变量)》

六、备份、恢复、升级
1、逻辑备份与恢复

《PostgreSQL Logical Backup's TOC File》

《PostgreSQL 最佳实践 - 在线逻辑备份与恢复介绍》

2、基于全量数据文件和归档的增量备份与恢复

《PostgreSQL recovery target introduce》

《PostgreSQL PITR THREE recovery target MODE: name,xid,time USE CASE - 1》

《PostgreSQL PITR THREE recovery target MODE: name,xid,time USE CASE - 2》

《PostgreSQL standby recover的源码分析 (walreceiver唤醒时机？ 为什么standby crash后walreceiver不会立即被唤醒?)》

《PostgreSQL 最佳实践 - 在线增量备份与任意时间点恢复》

3、基于ZFS快照和归档的增量备份与恢复

《PostgreSQL 最佳实践 - 块级增量备份(ZFS篇)方案与实战》

《PostgreSQL 最佳实践 - 块级增量备份(ZFS篇)备份集自动校验》

《PostgreSQL 最佳实践 - 块级增量备份(ZFS篇)单个数据库采用多个zfs卷(如表空间)时如何一致性备份》

《PostgreSQL 最佳实践 - 块级增量备份(ZFS篇)双机HA与块级备份部署》

《PostgreSQL 最佳实践 - 块级增量备份(ZFS篇)验证 - recovery test script for zfs snapshot clone + postgresql stream replication + archive》

4、基于数据文件块级增量和归档的增量备份与恢复

《PostgreSQL 最佳实践 - 块级别增量备份(pg_rman baseon LSN)源码浅析与使用》

《PostgreSQL 最佳实践 - pg_rman 以standby为源的备份浅析》

《PostgreSQL 最佳实践 - pg_rman 数据库恢复示例 与 软件限制解说》

5、误操作闪回

《PostgreSQL 回收站功能 - 基于HOOK的recycle bin pgtrashcan》

《PostgreSQL 闪回 - flash back query emulate by trigger》

6、误操作恢复

《PostgreSQL 使用pg_xlogdump找到误操作事务号》

7、灾难恢复

《异版本pg_resetxlog后导致的控制文件差异问题处理》

《使用pg_resetxlog修复PostgreSQL控制文件的方法》

《PostgreSQL 数据文件灾难恢复 - 解析与数据dump》

《PostgreSQL 恢复大法 - 恢复部分数据库、跳过坏块、修复无法启动的数据库》

8、《Gitlab从删库到恢复 - 数据库备份恢复容灾HA的靠谱姿势》

9、《PostgreSQL on ECS多云盘的部署、快照备份和恢复》

10、跨版本升级

《fast & safe upgrade to PostgreSQL 9.4 use pg_upgrade & zfs》

《Londiste 3 replicate case - 1 上节》

《Londiste 3 replicate case - 1 下节》

七、安全、审计
1、《PostgreSQL 密码安全指南》

2、《PostgreSQL 数据库安全指南》

3、《PostgreSQL数据库在上市公司重要应用中的SOX审计》

4、《DBA专供 冈本003系列 - 数据库安全第一,过个好年》

5、《DBA一族九阳神功秘籍，标准和制度(含重大节日)》

6、《PostgreSQL 10 - SASL认证方法 之 scram-sha-256 安全认证机制》

7、《PostgreSQL 10 - 可配置是否允许执行不带where条件的updatedelete》

8、《PostgreSQL views privilege attack and security with security_barrier(视图攻击)》

10、《固若金汤 - PostgreSQL pgcrypto加密插件》

11、审计

《PostgreSQL 事件触发器 - DDL审计 , DDL逻辑复制 , 打造DDL统一管理入口》

《PostgreSQL 触发器应用 - (触发器WHEN)前置条件过滤跟踪目标记录》

《PostgreSQL 触发器应用 - use trigger audit record which column modified, insert, delete.》

《PostgreSQL 跟踪谁动了你的记录 - 1》

《PostgreSQL 跟踪谁动了你的记录 - 2》

《USE hstore store table's trace record》

12、《PostgreSQL 转义、UNICODE、与SQL注入》

13、SQL 防火墙

《PostgreSQL SQL防火墙》

《PostgreSQL 商用版本EPAS(阿里云ppas) SQL防火墙使用（白名单管理、防SQL注入、防DDL等）》

《PostgreSQL SQL filter (SQL 成本|语义过滤器) - SQL成本防火墙》

14、《[转] 关于入侵PostgreSQL的那些事儿（文件读取写入、命令执行的办法）》

15、《PostgreSQL CVE-2018-1058(search_path) - 暨数据库的那些陷阱与攻防指南》

八、DBA技巧
1、《DBA不可不知的操作系统内核参数》

2、《从PostgreSQL支持100万个连接聊起》

3、《PostgreSQL on Linux 最佳部署手册》

4、《Linux 性能诊断 perf使用指南》

5、《PostgreSQL 源码性能诊断(perf profiling)指南》

6、《PostgreSQL 锁等待监控 珍藏级SQL - 谁堵塞了谁》

7、《PostgreSQL 如何查找TOP SQL (例如IO消耗最高的SQL)》

8、《PostgreSQL 清理redo(xlog,wal,归档)的机制 及 如何手工清理》

9、《PostgreSQL物理"备库"的哪些操作或配置，可能影响"主库"的性能、垃圾回收、IO波动》

10、《从redo日志分析数据库的profile》

11、《MySQL 增量同步到 PostgreSQL》

12、《PostgreSQL 收缩膨胀表或索引 - pg_squeeze or pg_repack》

13、《PostgreSQL relcache在长连接应用中的内存霸占"坑"》

14、《PostgreSQL 老湿机图解垃圾回收的"坑"》

15、《论数据库redo/data存储规划与SSD写倾斜》

16、垃圾回收相关

16.1、数据库DATA BLOCK剩余空间跟踪原理

《PostgreSQL Free Space Map Principle》

16.2、如何计算对象膨胀

《PostgreSQL 如何精确计算表膨胀(fsm,数据块layout讲解) - PostgreSQL table exactly bloat monitor use freespace map data》

16.3、为什么长事务可能会导致膨胀

《PostgreSQL 垃圾回收代码分析 - why postgresql cann't reclaim tuple is HEAPTUPLE_RECENTLY_DEAD》

16.4、如何防止膨胀

《PostgreSQL 垃圾回收原理以及如何预防膨胀 - How to prevent object bloat in PostgreSQL》

《PostgreSQL snapshot too old补丁, 防止数据库膨胀》

《PostgreSQL 老湿机图解平安科技遇到的垃圾回收"坑"》

16.5、为什么需要FREEZE，如何防止FREEZE风暴

《PostgreSQL Freeze 风暴预测续 - 珍藏级SQL》

《PostgreSQL 的"天气预报" - 如何预测Freeze IO风暴》

《PostgreSQL 大表自动 freeze 优化思路》

《PostgreSQL 9.6 vacuum freeze大幅性能提升 代码浅析》

16.6、如何优雅的处理膨胀对象

《PostgreSQL 收缩膨胀表或索引 - pg_squeeze or pg_repack》

16.7、如何监控垃圾回收进程的开销

《PostgreSQL 10.0 preview 功能增强 - SQL执行剩余时间 - 垃圾回收过程可视pg_stat_progress_vacuum》

《PostgreSQL 10.0 preview 功能增强 - 新增数十个IO等待事件监控》

16.8、如何优化GIN索引的VACUUM锁

《PostgreSQL 10.0 preview 性能增强 - GIN索引vacuum锁降低》

16.9、备库为什么可能影响主库的垃圾回收

《PostgreSQL 物理"备库"的哪些操作或配置，可能影响"主库"的性能、垃圾回收、IO波动》

16.10、影响或控制垃圾回收的参数或因素

《影响或控制PostgreSQL垃圾回收的参数或因素》

17、《PostgreSQL 连接串URI配置(libpq兼容配置)》

18、最全健康报告、监控指南

《PostgreSQL、Greenplum 日常监控 和 维护任务 - 最佳实践》

19、《PostgreSQL 规格评估 - 微观、宏观、精准 多视角估算数据库性能(选型、做预算不求人)》

20、《PostgreSQL 事件触发器应用 - DDL审计记录》

21、数据同步、迁移

《debezium - 数据实时捕获和传输管道(CDC)》

《MySQL准实时同步到PostgreSQL, Greenplum的方案之一 - rds_dbsync》

《MySQL,Oracle,SQL Server等准实时同步到PostgreSQL的方案之一 - FDW外部访问接口》

《[未完待续] pgloader - mysql , sqlserver 迁移到 PostgreSQL - (含DDL自动迁移)》

22、《在PostgreSQL中使用 plpythonu 调用系统命令》

23、《PostgreSQL 虚拟|虚假 索引(hypothetical index) - HypoPG》

24、部署数据库

《PostgreSQL 10 + PostGIS + Sharding(pg_pathman) + MySQL(fdw外部表) on ECS 部署指南(适合新用户)》

《PostgreSQL 商用版本EPAS(阿里云ppas) - 测试环境部署(EPAS 安装、配置、管理、Oracle DBLINK、外表)》

《PostgreSQL 10 on ECS 实施 流复制备库镜像+自动快照备份+自动备份验证+自动清理备份与归档》

25、《PostgreSQL freeze 风暴导致的IOPS飙升 - 事后追溯》

26、分区表

《PostgreSQL 11 preview - 分区表用法及增强 - 增加HASH分区支持 (hash, range, list)》

《PostgreSQL 11 preview - 新功能, 分区表全局索引管理》

《PostgreSQL 10 内置分区 vs pg_pathman perf profiling》

《分区表锁粒度差异 - pg_pathman VS native partition table》

《PostgreSQL 商用版本EPAS(阿里云ppas) - 分区表性能优化 (堪比pg_pathman)》

《PostgreSQL 传统 hash 分区方法和性能》

《PostgreSQL 查询涉及分区表过多导致的性能问题 - 性能诊断与优化(大量BIND, spin lock, SLEEP进程)》

27、数据库压测、造数据

《PostgreSQL 压测功能 pgbench : 冒号处理》

《PostgreSQL 如何快速构建 海量 逼真 测试数据》

《PostgreSQL 11 preview - pgbench 变量、函数扩展 - 暨pgbench 自定义 benchmark讲解》

《PostgreSQL 生成随机身份证ID》

28、《PostgreSQL 设置单条SQL的执行超时 - 防雪崩》

29、自动索引

《PostgreSQL 商用版本EPAS(阿里云ppas) 索引推荐功能使用》

《PostgreSQL SQL自动优化案例 - 极简，自动推荐索引》

30、《PostgreSQL 如何判断idle in transaction的事务中有没有东西要提交》

31、《PostgreSQL 商用版本EPAS(阿里云ppas) 自动(postgresql.conf)参数计算与适配功能》


