# 用业务粒度检验 Agent 的跨会话记忆

问数助手从上次对话中记下“把订单与支付连起来，就能算收入”。当时订单都恰好一次付清，查询结果也通过了核对。下次数据中出现拆分支付，这条经验还成立吗？

## 先辨认需要纠正的对象

历史观察可以回到当时的记录查证。Anthropic 描述过一个导航案例：助手把地标方位记反，离线回看行动轨迹后修正了笔记，随后选择了不同的路线。业务指标还多一层约定。订单时间和到账时间都可能记录无误，销售问成交额、财务问实收额时，却应该得到不同的答案。保存一条可复用的查询经验时，应记录它回答的问题、指标版本、聚合粒度，以及一个会让旧写法出错的样本。[Anthropic 研究原文](https://www.anthropic.com/research/components-of-agent-memory) · [Snowflake 语义视图文档](https://docs.snowflake.com/en/user-guide/views-semantic/overview)

## 一个可以直接运行的反例

两笔不同的订单各 50 元。第一笔分两次收款，金额分别为 20 元和 30 元；第二笔尚未付款。先预测下单总额与实收总额，再在 SQLite 中运行：

```sql
WITH
  orders(order_id, amount) AS (VALUES (1, 50), (2, 50)),
  payments(payment_id, order_id, paid) AS (VALUES (11, 1, 20), (12, 1, 30))
SELECT
  (SELECT SUM(amount) FROM orders) AS ordered,
  (SELECT SUM(paid) FROM payments) AS collected,
  (SELECT SUM(amount) FROM orders LEFT JOIN payments USING (order_id)) AS joined_sum,
  (SELECT SUM(DISTINCT amount) FROM orders) AS distinct_sum;
```

| 字段 | 实测值 | 如何解释 |
|---|---:|---|
| ordered | 100 | 每个订单计一次，两笔等额订单都应保留 |
| collected | 50 | 每笔支付计一次，未付款订单尚无流水 |
| joined_sum | 150 | 左连接保留未付订单，同时把已付订单的 50 元复制到两行 |
| distinct_sum | 50 | 按金额去重，把不同订单错误地合并了 |

这组数据里，错误的 distinct_sum 甚至能碰巧给出正确的实收额。把第二笔订单增加一笔 10 元的部分付款，实收额应变为 60 元，下单总额仍是 100 元。这个变体能检查助手是否理解了计数对象，还是只针对上一个答案调整了 SQL。

## 怎样用于评测

把“总收入是多少”分别改写成“按下单日期统计订单金额”和“按到账日期统计成功收款”。要求助手同时给出金额、使用的键和日期字段。订单指标按订单 ID 汇总，实收指标按支付流水 ID 汇总；涉及跨表维度时，先确认连接在目标粒度上是否仍是一行对应一个对象。

如果业务方还没有约定“收入”的含义，把两种结果和差异写进回答更有用。随后可以把确认过的定义放入受版本管理的语义层，笔记只记录适用条件和反例。这里更新的是助手调用的外部知识与查询规则，模型权重并未参与这次验证。

**迁移练习。** 一笔成功支付后来部分退款。要计算“本月净实收”，还缺什么？合格答案应指出退款流水的键、退款应归属的期间，并说明支付和退款各自在哪一层聚合。合成样本检验了上述 SQL 的算术结果；真实数据中的退款、币种和确认政策需要业务定义。
