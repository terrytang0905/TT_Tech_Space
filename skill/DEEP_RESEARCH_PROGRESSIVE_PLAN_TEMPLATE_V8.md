# Deep Research Progressive Plan Template

> template_version: `v8`
> 用途：把“给定一个 seed 目录，围绕其中若干初步 topic / opinion 做逐轮 Deep Research，并让本地知识库持续生长”的方法，实例化为某一轮可执行 plan。
>
> 强约束：本模板默认必须配套生成两个执行态文件：
> - `STATUS_PATH = <PLAN_BASENAME>.status.md`
> - `QUEUE_PATH = <PLAN_BASENAME>.queue.md`

## 这份文件的真实定位

这份文件不是普通“研究提纲模板”，也不是只用来生成一篇 plan 文档的填空框架。

它同时承担 4 个角色：

- `template`：定义一轮 Deep Research plan 必须具备的结构、参数、波次、产物与验收方式
- `instantiation contract`：定义如何从 `SEED_DIR` 冷启动生成本轮 `plan + status + queue`
- `execution protocol`：定义默认推进方式、允许中断用户的条件、证据落库规则、推进与 closeout 规则
- `handoff contract`：定义 plan、status、queue、README、reference、artifact、resume checkpoint 之间如何协同，保证新 agent 不依赖对话上下文也能接着做

这套东西的设计目标，不是让 agent 更会“汇报进度”，而是让基于它生成出来的 plan 在长程任务中默认静默自主推进：

- 能持续往前跑，而不是做一小步就停下来汇报
- 能在局部卡住时通过 `suspend / archive / redirect` 维持主线不断流
- 能把进度、判断、缺口、恢复入口写进本地文件，而不是留在聊天上下文里
- 只有真正满足中断条件时，才主动打断用户

## Single-File Block Map

| block | purpose | when to read | may be copied into instantiated output |
| --- | --- | --- | --- |
| `A. Routing + Core Contract` | 路由闸门、SSOT、术语、固定枚举、复制边界与运行期权威绑定 | 进入任何 mode 之前先读 | 默认 `no`；只允许继承白名单规则 |
| `B. Instantiation Output Boundary` | 实例化最小输入、最短路径、唯一检查清单、初始化预设、skeleton | 生成或修复 `plan + status + queue` 时读 | `plan/status/queue skeleton` only |
| `C. Execution Protocol` | execution entry、推进方式、`QUEUE_PATH`、分支处置、证据采集、停止与 closeout | 明确进入 `Execution Mode` 后读 | `no`；execution-only |
| `D. Appendix / Maintenance` | 模板维护校准与不变原则 | 迭代模板本身时读 | `no` |

## A. Routing + Core Contract

这一块是 single-file `V8` 的前置控制层；如果后文 prose 与本块中的 canonical table 冲突，以本块 table 为准。

## Instantiation-Execution Routing Gate（MUST READ FIRST）

这不是“快速说明”或“使用提示”，而是本模板的首要路由闸门。

它只回答一个问题：当前任务现在是否被允许进入 `Execution Mode`。

如果只检索一段内容就准备开始行动，优先检索 `Instantiation-Execution Routing Gate`。

| detected task shape | choose mode | allowed output | must not do |
| --- | --- | --- | --- |
| 生成、修复、审查、补全本轮 `plan + status + queue` | `Instantiation Mode` | 只产出实例化后的 `plan skeleton + status skeleton + queue skeleton` | 不初始化目录、不创建 `README` / `_INDEX.md`、不落 `reference/artifact`、不进入 `Wave 0` |
| 明确要求继续本轮、初始化执行表面、落证据、更新 live status | `Execution Mode` | 初始化目录与导航入口，然后推进 `Wave 0 -> Wave 1 -> Wave 2 -> Readiness Check` | 不再把“实例化模板”误当成“已经开始研究” |

1. 如果任务存在歧义，默认选择 `Instantiation Mode`。
2. 在 `Instantiation Mode` 中，只复制 `BEGIN PLAN SKELETON / END PLAN SKELETON`、`BEGIN STATUS SKELETON / END STATUS SKELETON`、以及 `BEGIN QUEUE SKELETON / END QUEUE SKELETON` 之间内容。
   - 先填写 `Instance Config`
   - section 级复制许可，以后文 `Instantiation Copy Boundary` 为准
   - 不能确定但不阻塞执行的值，显式写成“暂按假设执行”
3. `Instantiation Mode` 的硬停点：
   - status 至少写到：
     `current_mode = instantiation_only`
     `current_wave = Instantiation`
     `current_gate = instantiation_complete`
   - queue 至少写到：
     `current_task`
     `next_task`
     `next_after_next`
     `queue_health = ready`
   - 到这里就停止
   - **MUST NOT** 初始化目录、创建 README、创建 `_INDEX.md`、落 `reference/artifact`、进入 `Wave 0`
4. `Execution Mode` 只能在下面条件同时满足时开始：
   - `plan + status + queue` 已存在
   - 实例化检查已经通过
   - 当前任务明确要求进入执行
5. 默认状态沟通机制是 `STATUS_PATH`；默认执行动作入口是 `QUEUE_PATH`，都不是聊天上下文。
6. 如果 seed 信息不足以稳定生成 `topic registry`，先写显式假设、gap 或 pending candidate；不要发明 topic、对象、趋势结论或证据。

## Core Contract（核心契约）

### Canonical Terms（最小术语表）

本模板从这里开始统一术语；后文默认不再混用近义词。

- `Source of Record`：某类信息的唯一权威记录点
- `design-time`：目标、结构、参数、验收层级、拓扑基线这类静态设计信息
- `run-time`：当前状态、当前阻塞、当前 gate、执行摘要、挂起分支、恢复入口这类执行态信息
- `controlled mutation`：允许在 `PLAN_PATH` 中进行的受控更新，只限实例参数修订、拓扑正式化、主任务变化或 Hard Gate 决策；不写实时进度
- `Authoritative Copy`：进入 `<REFERENCE_DIR>` 的本地来源副本；它是该来源在本轮研究中的可复用证据本体
- `topic registry`：研究线注册表；它是本轮 topic 编号、slug、seed_files、must_answer 的唯一设计态注册点
- `gate model`：plan 中定义的允许关卡集合、默认推进路径与最小 gate 绑定
- `gate state`：status 中记录的当前 gate、下一 gate 与下一得分动作
- `QUEUE_PATH`：本轮独立的显性执行队列文件；它是连续执行动作的唯一 `Source of Record`
- `Execution Queue`：`QUEUE_PATH` 中维护的连续派工队列；默认至少保持 `current_task / next_task / next_after_next` 三层非空
- `navigation pointer`：跨文件回指字段；只用于定位权威文件，不形成新的 `Source of Record`

约定：

- 本模板统一以 `Source of Record` 作为主术语。
- 历史文档中出现的 `Source of Truth`，在本模板语境下等价理解为对应对象的 `run-time` 或 `design-time Source of Record`。
- `_INDEX.md` 即使物理上放在 `<REFERENCE_DIR>` 中，语义上仍属于 `navigation layer`，不是 evidence 本体，也不是 artifact。

### Canonical Retrieval Names（固定检索名）

后续实例化、执行、handoff 或局部提醒中，优先使用下面这些英文 canonical names 做检索、定位和引用：

- `Instantiation-Execution Routing Gate`
- `Instantiation Mode`
- `Execution Mode`
- `Autonomous Execution Protocol`
- `Topology Formalization Gate`
- `Exploration-Exploitation Decision Framework`
- `Foundation Sufficiency Check`
- `Early Saturation Protocol`
- `Structural Spine`
- `Minimal Runtime Bindings`
- `Canonical Field Role Notes`
- `Canonical Runtime Authority`
- `Suspended Branch Protocol`
- `QUEUE_PATH`
- `Execution Queue`
- `30-Second Local Evidence Retrieval`
- `human-on-the-loop`

避免用“Quick Start”“60 秒使用说明”这类弱锚点做检索；默认统一使用上述 canonical names。

### Structural Spine（结构主线）

每份实例化 plan 都必须能快速回答：哪个对象记录什么，谁能改什么，什么不能写到哪里。

| object | role | mutation boundary |
| --- | --- | --- |
| `PLAN_PATH` | `design-time Source of Record`；定义目标、参数、拓扑基线、Wave 设计、验收层级、中断规则 | 允许 `controlled mutation`；不写实时进度、worklog、当前阻塞 |
| `STATUS_PATH` | `run-time Source of Record`；记录当前状态、当前 gate、当前缺口、阻塞、执行摘要、挂起分支、失败探索和恢复入口 | 持续更新；不重写 plan 中的静态蓝图 |
| `QUEUE_PATH` | `authoritative execution queue`；记录当前动作、后续动作、queue refill 与 promotion 规则 | 持续更新；不重写完整状态面，也不替代设计态蓝图 |
| `SEED_DIR` | `living output surface`；承接本轮输入，也是回填后的长期主题文档 | 只写 topic 内容与回填；不写执行态控制信息 |
| `REFERENCE_DIR` | `evidence Source of Record`；承接可定位、可追溯的 ground truth | 每个重要来源单独成文；不写过程性状态或临时想法 |
| `ARTIFACT_DIR` | `derived synthesis layer`；承接 evidence summary、question list、cross-topic synthesis | 不替代证据本体，也不替代执行状态 |
| `README / _INDEX` | `navigation layer`；承接 `Read Path` 与 30 秒导航 | 不承接长篇论证、执行状态或证据本体 |

补充规则：

- `PLAN_PATH` 不是“完全静态、绝不改动”的文档，而是允许 `controlled mutation` 的设计态权威文档。
- 如果中途 formalize 出新 topic，允许更新 `PLAN_PATH`；但这类更新必须体现为结构同步，而不是实时进度记录。
- 如果新增规则无法明确落到上面某个对象，或者说不清谁是它的 `Source of Record`，先不要加入模板。

### Canonical State and Record Matrix

下面 3 张表用于把 single-file `V8` 的单点规则压实。

- 如果 prose 解释与这些表冲突，以这些表为准。
- 如果某个字段、状态或 section 无法落到这些表中，先不要扩写实例产物。

#### Source of Record Matrix

| information class | authoritative location | allowed duplication | mutation rule |
| --- | --- | --- | --- |
| `instance parameters` | `PLAN_PATH -> Instance Config` | 其他位置只可引用，不重复定义 | 只允许在 `PLAN_PATH` 做 `controlled mutation` |
| `topic registry` | `PLAN_PATH -> 研究线注册表（topic registry）` | 其他 section 只引用编号、slug 或计数 | topic 变化先更新 registry，再更新其他对象 |
| `derived_topic_count` | `PLAN_PATH -> Instance Config`，且由 `topic registry` 派生 | 不允许在其他 section 维护第二份计数器 | registry 变化后同步修订该派生值 |
| `topology baseline` | `PLAN_PATH -> 当前拓扑基线（Current Topology Baseline）` | `STATUS_PATH` 只记录 delta，不重写 baseline | 正式拓扑变化先改 `PLAN_PATH` |
| `topology delta` | `STATUS_PATH -> Topology Delta / Formalization State` | `PLAN_PATH` 不记录实时变化日志 | 运行中只写增量、候选与最近一次正式化说明；plan/status 同步摘要另写 `Plan / Status Sync` |
| `gate model` | `PLAN_PATH -> Control Map -> Minimal Runtime Bindings` | `STATUS_PATH` 只写 `gate state` | `PLAN_PATH` 只定义 allowed values、默认路径与最小 gate 绑定 |
| `gate state / next action` | `STATUS_PATH -> Gate State` | `PLAN_PATH` 只保留 allowed values，不写当前态 | 执行推进只更新 `STATUS_PATH` |
| `execution queue` | `QUEUE_PATH` | `STATUS_PATH` 只保留 `queue_path` 指针与必要恢复摘要；不镜像 `queue_health` 或 active queue | 每次完成当前任务前先补齐后续队列 |
| `runtime wave progress` | `STATUS_PATH -> Wave 0 / Wave 1 / Wave 2 / Readiness Check` | `PLAN_PATH` 只定义验收标准，不写进度 | 所有实时进度只写 `STATUS_PATH` |
| `branch disposition` | `STATUS_PATH -> Suspended Branches` | 协议区可定义动作名，但不维护并行运行态副本 | 状态记录统一使用 canonical status enum |
| `evidence body` | `<REFERENCE_DIR>/*.md` | `SEED_DIR` / `ARTIFACT_DIR` / `README` 只引用或综合 | 重要来源必须先落为 reference 本体 |
| `derived synthesis` | `<ARTIFACT_DIR>` | 可在 seed 中引用结果，不替代 evidence 本体 | 只承接 summary / question list / synthesis |
| `navigation / read path` | `README / _INDEX` | 可短引，不承载长篇协议、长篇证据或 live status | 只维护导航，不争夺证据和状态权威 |

#### Canonical Enum Registry

| enum class | allowed values | note |
| --- | --- | --- |
| `Current Execution Snapshot.state` | `not_started / in_progress / blocked / completed` | 只用于本轮整体执行快照 |
| `current_mode` | `instantiation_only / execution` | 不引入第三种 mode |
| `current_wave` | `Instantiation / Wave 0 / Wave 1 / Wave 2 / Readiness Check` | `Setup` 不是独立 wave |
| `current_gate` | `instantiation_complete / setup_ready / wave0_complete / wave1_complete / wave2_complete / readiness_passed` | 当前态只记录于 `STATUS_PATH` |
| `queue_health` | `ready / thin / blocked` | 只出现在 `QUEUE_PATH -> Active Queue` |
| `interrupt_condition_matched` | `not_applicable / mainline_blockage / direction_reset / high_risk_action / user_requested_realtime_collab` | 仅当 `queue_health = blocked` 时使用非 `not_applicable` 值 |
| `next_scoring_action` | `+reference / +backfill / +artifact / +index / +decision` | 不扩展临时动作值 |
| `Wave 0.completion_status` | `not_started / in_progress / passed / failed` | 只用于 Wave 0 |
| `Wave 1 topic status / Wave 2 status` | `not_started / in_progress / passed / blocked` | 不默认使用 `failed` |
| `topic_stop_decision` | `not_assessed / continue / early_saturation / suspend / archive / redirect` | 只用于 Wave 1 研究线级处置；未完成一轮搜集前默认 `not_assessed` |
| `topology_sync_state` | `synced / status_pending / plan_pending` | 只用于 plan/status 结构同步摘要 |
| `Readiness Check item` | `pass / partial / fail` | `overall_status` 只用 `pass / fail` |
| `primary_source_coverage` | `insufficient / sufficient / saturated` | 只用于 primary source 覆盖 / 饱和度维度 |
| `branch disposition state` | `discarded / compressed / suspended / archived / redirected` | 协议动作名可用原型；status 记录统一用过去分词态 |

#### Canonical Field Role Notes

| field or concept | role | authoritative location | note |
| --- | --- | --- | --- |
| `current_task / next_task / next_after_next` | `authoritative` | `QUEUE_PATH -> Active Queue` | 不在 `STATUS_PATH` 维护第二份 active queue |
| `queue_path` | `navigation-pointer` | `PLAN_PATH / STATUS_PATH / QUEUE_PATH` header backlink | 只用于跨文件定位；不是 queue state，也不是第二份 authority |
| `required_next_step` | `summary-only` | `STATUS_PATH -> Current Execution Snapshot` | 只写当前单步摘要，不替代 `QUEUE_PATH` |
| `topic_stop_decision` | `decision-state` | `STATUS_PATH -> Wave 1` | 未完成一轮搜集前保持 `not_assessed`；完成 stop assessment 后再写其他值 |
| `primary_source_coverage` | `dimension-status` | `STATUS_PATH -> Wave 1` | 只描述 primary source 覆盖 / 饱和度；不替代研究线级 `topic_stop_decision` |
| `topology_sync_state` | `sync-summary` | `STATUS_PATH -> Plan / Status Sync` | 只写 plan/status 哪一侧尚待同步 |
| `queue_resume_entry` | `pointer-only` | `STATUS_PATH -> Resume Checkpoint` | 固定回指 `QUEUE_PATH`，不复制下一步动作 |
| `Suspended Branches.state` | `branch-record-state` | `STATUS_PATH -> Suspended Branches` | 统一使用过去分词态；不与协议动作名混写 |
| `derived_topic_count` | `derived` | `PLAN_PATH -> Instance Config` | 唯一来源是 `topic registry` 条目数 |

#### Canonical Runtime Authority

| runtime concern | canonical design-time definition | run-time record location | note |
| --- | --- | --- | --- |
| `output contract` | `PLAN_PATH -> 输出契约` | `<STATUS_PATH>.目录与集成状态` + `Worklog` | 不在 runtime 层重写第二份输出契约 |
| `wave design and readiness` | `PLAN_PATH -> Wave 设计与验收` | `<STATUS_PATH>.Wave 0 / Wave 1 / Wave 2 / Readiness Check` | `PLAN_PATH` 定义目标与 floor，`STATUS_PATH` 记录当前态 |
| `topic stop decision` | `PLAN_PATH -> 搜够了没有：停止条件` | `<STATUS_PATH>.Wave 1` + `Suspended Branches` | `continue` 可只留在主线；`early_saturation / suspend / archive / redirect` 需要补齐对应分支记录或显式理由 |
| `post-pass success state` | `PLAN_PATH -> 成功标准` | closeout judgment + `<STATUS_PATH>.Readiness Check` | `成功标准` 不是额外 gate |
| `hard-gate overlay` | `PLAN_PATH -> Hard Gates` | `<STATUS_PATH>.Readiness Check` 或 `blocking_issue` | 只在 `hard_gates_enabled = yes` 时叠加 |

执行约束：

- 如果执行中发现设计态定义需要变化，先在 `PLAN_PATH` 做 `controlled mutation`，再继续推进
- 如果实例 plan 缺少上表中的关键 section，先修 `PLAN_PATH`，不要靠对话临时补规则
- runtime 层可以引用这张表，但不再维护第二份并行版本

#### Instantiation Copy Boundary

| section family | instantiate into `PLAN_PATH` | instantiate into `STATUS_PATH` | instantiate into `QUEUE_PATH` | note |
| --- | --- | --- | --- | --- |
| `A. Routing + Core Contract` | `no` | `no` | `no` | 只允许 white-listed minimum rules 约束实例 payload |
| `B. Instantiated Output Self-Containment Rules` | `no` | `no` | `no` | 约束实例内容必须自包含，但不单独复制整节 |
| `B. Plan Skeleton` | `yes` | `no` | `no` | 只复制 marker 内正文 |
| `B. Status File Skeleton` | `no` | `yes` | `no` | 只复制 marker 内正文 |
| `B. Queue File Skeleton` | `no` | `no` | `yes` | 只复制 marker 内正文 |
| `C. Execution Protocol` | `no` | `no` | `no` | execution-only；实例 plan 只继承白名单最小规则 |
| `D. Appendix / Maintenance` | `no` | `no` | `no` | 只服务模板维护 |

如果某 section 不在上表中标记为 `yes`，默认不要复制进实例产物。

## 适用场景

这个模板不是普通研究提纲模板，也不打算覆盖所有研究类型。

默认服务于科学研究、工程技术、技术选型、technical best practice，以及技术机制 / 趋势 / 约束 / 失败模式研究。

如果主题明显偏向文学研究、泛人文评论、纯创作分析或高主观性文本解读，建议另做实例化或变体，而不是继续泛化主模板。

它适用于下面这种工作流：

- 输入是一个指定目录
- 目录里有 1 到 N 份初步 topic seed、已有摘要、候选判断、问题清单或路线假设
- 本轮任务不是重写这些 seed，而是围绕它们继续深挖
- 深挖的目标不是“多搜链接”，而是把一套可靠的本地 ground truth、机制理解、趋势判断、难点与反例逐步沉淀下来
- 本轮结束后，输入目录本身会长出新内容，同时新增一批本地 reference 文档与 artifacts，供下一轮继续往下走

这个模板要保留的核心，不是某个具体主题，而是下面这套方法论：

- 先证据，后综合
- 先共享地基，再分题深挖，再横向收束
- 以“本地可复用落库”作为完成单位，而不是以“看过网页”作为完成单位
- 以“停止条件”和“Readiness Check”替代“感觉搜够了”
- 以 `Suspended Branch Protocol` 处理高难但暂不可得的问题，默认 `human-on-the-loop`，不让同步人工反馈阻塞主线
- 让输入目录持续生长，而不是每轮都另起一堆无法承接的报告

## B. Instantiation Output Boundary

这一块只负责“如何稳定地产出本轮 `plan + status + queue`”；只允许 skeleton marker 内正文进入实例产物。

## Instantiation Contract（实例化契约）

### 先明确这些实例参数

每一份实例化 plan 都必须有一个 `Instance Config` 区；它是本轮实例参数的唯一设计态注册点。

复制模板前，先明确下面这些参数：

- `PLAN_NAME`：这轮计划的名称
- `TEMPLATE_VERSION`：本轮实例化所继承的模板版本，默认直接抄写模板顶部的 `template_version`
- `ROUND_LABEL`：例如 `一轮`、`二轮`、`第三轮`
- `PLAN_PATH`：具体计划文件路径
- `STATUS_PATH`：状态文件路径
- `QUEUE_PATH`：执行队列文件路径，默认建议设为 `<PLAN_BASENAME>.queue.md`
- `SEED_DIR`：本轮输入目录
- `REFERENCE_DIR`：本轮落 ground truth 的目录，默认建议直接设为 `<SEED_DIR>/_reference`
- `ARTIFACT_DIR`：本轮 artifacts 目录，默认建议直接设为 `<SEED_DIR>/_artifacts`
- `FINAL_DELIVERABLE`：这轮调研最终服务于什么产出
- `AUDIENCE`：谁会读最终产出
- `ROUND_FOCUS`：本轮主任务；例如 `扩事实 / 补机制 / 补趋势 / 补限制 / 组合`
- `DERIVED_TOPIC_COUNT`：固定派生表达；实例中写成 `= count(topic registry entries)`，不要把它当作人工填写的自由值
- `TOPIC_REGISTRY`：对 `PLAN_PATH -> 研究线注册表（topic registry）` 的简写引用；不是独立文件或独立 Source of Record
- `WAVE0_SHARED_DOC_FLOOR`：Wave 0 共享资料最低配额
- `WAVE1_DOC_FLOOR_PER_TOPIC`：每条研究线的最低文档配额
- `PRIMARY_SOURCE_FLOOR`：每条研究线一手来源最低配额
- `SECONDARY_SOURCE_FLOOR`：每条研究线高质量二手来源最低配额
- `RECENT_SOURCE_FLOOR`：每条研究线近期趋势来源最低配额
- `LIMITATION_SOURCE_FLOOR`：每条研究线限制 / 争议 / 失败模式来源最低配额
- `HARD_GATES_ENABLED`：本轮是否启用 Hard Gates；`yes / no`

默认建议值：

- `WAVE0_SHARED_DOC_FLOOR = max(8, DERIVED_TOPIC_COUNT * 2)`
- `WAVE1_DOC_FLOOR_PER_TOPIC = 8`
- `PRIMARY_SOURCE_FLOOR = 4`
- `SECONDARY_SOURCE_FLOOR = 2`
- `RECENT_SOURCE_FLOOR = 1`
- `LIMITATION_SOURCE_FLOOR = 1`
- `HARD_GATES_ENABLED = no`

如果研究范围明显更窄或更宽，可以改，但必须在具体 plan 中显式写清楚为什么改。

### 冷启动使用协议（Cold Start Usage）

本模板必须能在没有任何历史对话上下文的环境中单独使用。新的 agent 只加载这一个文件时，应按下面顺序工作。

#### Instantiation Mode

1. 确认最小输入：至少需要一个 `SEED_DIR`。如果连 `SEED_DIR` 都没有，无法实例化，应中断并请求用户提供。
2. 从 `SEED_DIR` 读取 seed 文件、README、已有 artifacts / reference，推断 `PLAN_PATH -> 研究线注册表（topic registry）`、`DERIVED_TOPIC_COUNT`、`FINAL_DELIVERABLE` 与 `AUDIENCE`。
3. 无法确定但不阻塞实例化的字段，先在 `Instance Config` 中写成显式假设，不要把它留在对话上下文里。
4. 复制 `## 可直接复制的 Plan Skeleton`，完成 `PLAN_PATH`，并填实本轮具体参数、gap、topic registry 与 research-line goals。
5. 复制 `## 配套 Status File Skeleton`，完成 `STATUS_PATH`；保留其默认 `instantiation_complete` 起点，只按本轮 topic 数量展开 `Wave 1` block，并修正路径、假设与恢复入口。
6. 复制 `## 配套 Queue File Skeleton`，完成 `QUEUE_PATH`；默认保留 handoff queue，除非你已经知道更具体的第一个 execution 动作。
7. 删除所有模板说明残留、示例 scaffold 和未替换 placeholder，使 `plan + status + queue` 本身自包含。
8. 按后文 `Instantiation Checklist` 与 `Instantiation Reject Gate` 检查通过后停止，不自动进入目录初始化与 Wave 执行。

Instantiation-only stop condition：

- `Instantiation Mode` 的完成态是：`plan + status + queue` 已可交付给下一步执行者，而不是“已经开始 Setup”
- 到达这个停止点后立即停止；不要继续目录初始化、证据落盘或 Wave 执行
- 具体检查项统一以 `Instantiation Checklist` 为准，不在其他 prose 中维护第二份并行列表

冷启动时不要假设：

- 用户记得上一轮对话里的口头约定
- 当前 agent 能访问创建模板时的讨论上下文
- 未写入 plan / status / queue / README 的判断会被下一位接手者知道
- status 和 queue 都不能稍后再补；它们都是执行协议的一部分，不是收尾文档

### Instantiated Output Self-Containment Rules（实例产物必须自包含）

这一节只起约束作用，不单独复制进实例产物。

- 实例化后的 `plan + status + queue` 必须在不重读本模板其余章节的情况下可理解、可 handoff、可继续执行
- 允许保留的跨文件回指，只有具体路径与具体文件字段；这些回指只是 `navigation pointer`，不是新的 `Source of Record`
- 实例产物中不要留下对模板专用章节名的裸引用，例如 `Structural Spine`、`Canonical Enum Registry`、`Canonical Field Role Notes`、`Canonical Runtime Authority`、`Early Saturation Protocol`
- 如果某条规则对实例执行仍然必要，把最小必要规则改写进 skeleton 本身，而不是写成“回读模板”
- 实例 payload 的质量，以实例文件自身是否闭环为准，不以隐藏模板上下文补足

### Instantiation Checklist（实例化检查清单）

完成 `plan + status + queue` 后，统一按这一节检查；不要在其他 prose 中维护第二份实例化质量规则。

- 所有 `<PLACEHOLDER>`、模板说明文本与示例 scaffold 都已替换或删除；必要假设已改写为显式 prose
- `PLAN_PATH`、`STATUS_PATH`、`QUEUE_PATH`、`SEED_DIR`、`REFERENCE_DIR`、`ARTIFACT_DIR` 都可定位
- `Instance Config` 已存在且已填实
- 研究线注册表（topic registry）已写入 plan，而不是只存在于临时分析中
- `PLAN_PATH` 的内容是“本轮具体 plan”，不是模板复述或规则讲解
- `STATUS_PATH` 的内容停留在稳定起点，不提前汇报 Wave 进度
- `STATUS_PATH` 已存在，并包含当前恢复入口
- `STATUS_PATH` 仍停留在 `instantiation_only / Instantiation / instantiation_complete`
- `QUEUE_PATH.Active Queue.current_task.action` 指向实例化完成后的第一个未完成 execution 动作
- `QUEUE_PATH` 已存在，并包含连续可执行队列
- `PLAN_PATH.Instance Config.queue_path`、`STATUS_PATH.queue_path` 与实际 `QUEUE_PATH` 三者一致
- `derived_topic_count` 保持固定派生写法 `= count(topic registry entries)`，且 topic 数量不在其他 section 维护第二份计数器
- 枚举和值域统一以 `Canonical Enum Registry` 与 skeleton 字段注释为准
- `reference_dir` 与 `artifact_dir` 默认从 `seed_dir` 派生；若 override，已显式写明原因
- 尚未声明目录初始化完成、未进入 `Wave 0`、未落 `reference/artifact`
- `QUEUE_PATH` 尚未写入 execution-only live branch routing
- `STATUS_PATH` 不镜像 `queue_health` 或 active queue；只保留 `queue_path` 与恢复指针

### Instantiation Reject Gate（未通过不得交付）

出现下面任一情况，都视为实例化未完成，必须回到 skeleton 继续修：

- 仍出现 `<...>`、`[这里...]`、`BEGIN ...`、`END ...`、`marker 内正文` 这类模板残留
- 仍出现 `回读`、`按模板`、`满足模板中的`、`推荐结构`、`见上文 canonical table` 这类模板元文本
- 仍出现示例残留，例如 `topic-slug-1`、`topic-title-1`、`current topic gap`、`YYYY-MM-DD`、`Add one block per`
- `PLAN_PATH` 写入了 live progress、blocked state、worklog 或 active queue
- `STATUS_PATH` 复制了完整 active queue，或 `QUEUE_PATH` 复制了完整状态面
- 在 `Instantiation Mode` 中提前宣称 README / `_INDEX.md` / `reference` / `artifact` 已初始化完成
- 实例产物里仍保留模板示例 code block，而不是本轮具体内容
- `none_recorded_yet: yes` 与真实 branch / exploration 记录同时存在

---

## 可直接复制的 Plan Skeleton

复制时只取 `BEGIN PLAN SKELETON` 与 `END PLAN SKELETON` 之间内容，不包含 marker 本身。

<!-- BEGIN PLAN SKELETON -->
# <PLAN_NAME>

> 对应状态文件：`<STATUS_PATH>`
> 对应执行队列：`<QUEUE_PATH>`
> 本文件只记录设计态蓝图；实时状态与连续动作分别写入 `<STATUS_PATH>` 与 `<QUEUE_PATH>`。

## Instance Config

> 这是本轮实例参数的唯一设计态注册点。除 `topic registry` 本体外，后文不再重复定义这些参数。

| field | value |
| --- | --- |
| `plan_name` | `<PLAN_NAME>` |
| `template_version` | `<TEMPLATE_VERSION>` |
| `round_label` | `<ROUND_LABEL>` |
| `plan_path` | `<PLAN_PATH>` |
| `status_path` | `<STATUS_PATH>` |
| `queue_path` | `<QUEUE_PATH>` |
| `seed_dir` | `<SEED_DIR>` |
| `reference_dir` | `<REFERENCE_DIR>` |
| `artifact_dir` | `<ARTIFACT_DIR>` |
| `final_deliverable` | `<FINAL_DELIVERABLE>` |
| `audience` | `<AUDIENCE>` |
| `round_focus` | `<ROUND_FOCUS>` |
| `derived_topic_count` | `= count(topic registry entries)` |
| `wave0_shared_doc_floor` | `<WAVE0_SHARED_DOC_FLOOR>` |
| `wave1_doc_floor_per_topic` | `<WAVE1_DOC_FLOOR_PER_TOPIC>` |
| `primary_source_floor` | `<PRIMARY_SOURCE_FLOOR>` |
| `secondary_source_floor` | `<SECONDARY_SOURCE_FLOOR>` |
| `recent_source_floor` | `<RECENT_SOURCE_FLOOR>` |
| `limitation_source_floor` | `<LIMITATION_SOURCE_FLOOR>` |
| `hard_gates_enabled` | `<HARD_GATES_ENABLED>` |

## 调研目的与服务对象

这轮 Deep Research 不是为了产出调研笔记本身。

真正的目的是：为 `<FINAL_DELIVERABLE>` 提供可靠的原材料地基。

最终产出的读者是：`<AUDIENCE>`

本轮主任务是：`<ROUND_FOCUS>`

这份最终产出至少要满足下面要求：

- 系统性：覆盖关键维度，不遗漏，不失衡
- 逻辑性：每个判断都有证据支撑，推理链条可追溯
- 一致性：跨主题术语统一、口径统一、评估框架统一
- 专业可读：默认读者是专业人士，不需要手把手解释，但需要准确、严谨、无歧义

权威信源优先规则（最高优先级，不可违反）：

> 当权威一手来源已经足以支撑某个判断时，不为满足配额额外引入低质量二手来源。配额是防止搜太浅的下限，不是必须凑满的目标。宁缺毋滥。

## 本轮核心缺口

- Gap 1:
- Gap 2:
- Gap 3:

## Control Map

本轮实例 plan 只保留最小控制绑定，避免在实例正文里重写模板级 authority tables。

### Minimal Runtime Bindings

- `PLAN_PATH` 只记录设计态蓝图、实例参数、拓扑基线、Wave 设计与验收；不写实时进度、阻塞、worklog 或 active queue
- `STATUS_PATH` 只记录当前状态、gate、阻塞、拓扑 delta、分支处置与恢复上下文；不重写完整设计态蓝图
- `QUEUE_PATH` 是唯一连续派工入口；只记录 active queue、blocked state、refill pool 与 promotion rules
- `setup_ready` 是 gate，不是独立 wave；它表示 execution surface 已初始化完成、尚未关闭第一步 `Wave 0` 证据落库
- 默认 gate 路径为 `instantiation_complete -> setup_ready -> wave0_complete -> wave1_complete -> wave2_complete -> readiness_passed`
- `topic_stop_decision` 是研究线级决策；`primary_source_coverage` 只描述 primary source 覆盖 / 饱和度维度
- `Readiness Check` 是 round closeout gate；`成功标准` 只描述 pass 后的完成态；`Hard Gates` 只作为可选加严层

## 输入建模

本轮研究直接以 `<SEED_DIR>` 为起点。

输入对象包括：

- 目录中的 topic seed 文件
- 目录中的已有摘要 / 初步判断 / 问题清单
- 上一轮留下的 `_artifacts` 与相关本地 `_reference`（如果存在）

在正式执行前，必须先把输入目录建模成“研究线注册表（topic registry）”。

每条研究线至少要写清楚：

- 编号
- slug
- 主题标题
- 对应 seed 文件
- 当前假设或当前缺口
- 为什么它值得继续深挖
- 本轮必须回答的问题

### 研究线注册表（topic registry）

topic 数量、编号顺序与 slug 统一以这一节为准；其他 section 只引用，不再维护第二份列表。

| id | slug | title | seed_files | current_hypothesis | why_it_matters | must_answer |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

### 当前拓扑基线（Current Topology Baseline）

这里写的是本轮实例化时正式采用的 `topology baseline`；它属于 `PLAN_PATH` 的设计态结构，不是执行中的实时工作日志。

- carry_forward_topics:
- new_topics:
- recent_change:
- pending_topic_candidates:

当前有效 topic 数量始终由 `topic registry` 派生，不在其他 section 单独维护第二个计数器。

执行中的 topic 增减、推进中的结构变化与最近一次正式化说明写入 `<STATUS_PATH>.Topology Delta / Formalization State`；plan/status 哪一侧尚待同步则写入 `<STATUS_PATH>.Plan / Status Sync.topology_sync_state`。

## 输出契约

### 1. Ground Truth 参考材料

- 所有进入最终推理链条的重要来源，都应以独立 `md` 的 `Authoritative Copy` 形式落在 `<REFERENCE_DIR>`
- `REFERENCE_DIR` 的完成单位不是“看过这个链接”，而是“这个链接已经被整理成可复用、可定位、可引用、可自给自足的独立 `md` 文档”
- `<REFERENCE_DIR>/_INDEX.md` 负责 `30-Second Local Evidence Retrieval`，语义上属于 `navigation layer`

### 2. 输入目录的持续生长

`<SEED_DIR>` 不是只读输入，而是这轮研究的 `living output surface`。

每条研究线对应的 seed 文件都应被更新，并新增下面固定章节：

- `历史摘要（保留，不修改）`
- `本轮新增证据`：每条新增事实都带本地 reference 引用
- `本轮新增机制理解`：从描述上升到为什么这样设计
- `本轮新增趋势与难点`：有时间证据支撑的趋势、实践难点与失败模式
- `当前判断（本轮综合后）`：综合历史内容与本轮新增后的判断，每条判断带本地 reference 引用

规则：

- 历史摘要不删改，只保留
- 所有本轮新增内容进入固定章节
- 每条新增关键判断都必须带本地引用
- 如果某个判断被本轮推翻或修正，在“当前判断”中注明，不删除旧内容

### 3. 过程性 Artifacts

`<ARTIFACT_DIR>` 是 `derived synthesis layer`；它承接 evidence summary、question list 与 cross-topic synthesis，但不替代 `REFERENCE_DIR` 存放证据本体，也不替代 `STATUS_PATH` 存放当前执行状态。

至少包括：

- 每条研究线一份 `evidence-summary`
- 每条研究线一份 `question-list`
- 一份横向综合 `W2-cross-topic-synthesis`
- 一份 `ARTIFACT_DIR/README.md`

## Wave 设计与验收

### Wave 0：建立共同 Ground Truth 地基

- purpose: 固定共享地基、共同术语和高可信入口，避免各研究线各自从零开始
- minimum:
  - 至少 `<WAVE0_SHARED_DOC_FLOOR>` 份共享型 ground truth
  - 其中大多数来自官方文档、官方仓库、官方规范或高可信研究
  - 至少 1 份来自安全 / 限制 / 约束相关材料
  - 至少 1 份来自高质量对比、实践复盘或失败分析
  - `<REFERENCE_DIR>`、`<ARTIFACT_DIR>` 与 `STATUS_PATH` 已经先被初始化

### Foundation Sufficiency Check（Wave 0 → Wave 1）

进入 Wave 1 前至少确认：

- 核心术语已有工作定义，对象分类已有共享地基
- 每条研究线已有明确深挖起点
- `<REFERENCE_DIR>/_INDEX.md` 已经可用

### Wave 1：按研究线分别深挖

- purpose: 把每条研究线从“名称和观点”推进到“机制和证据”
- 每条研究线都要从 5 个视角扩展：
  - 证据
  - 根本机制
  - 趋势
  - 难度
  - 争议 / 失败模式
- minimum per topic:
  - 至少 `<WAVE1_DOC_FLOOR_PER_TOPIC>` 份该研究线专属 ground truth
  - 至少 `<PRIMARY_SOURCE_FLOOR>` 份一手来源
  - 至少 `<SECONDARY_SOURCE_FLOOR>` 份高质量二手分析
  - 至少 `<RECENT_SOURCE_FLOOR>` 份近期趋势来源
  - 至少 `<LIMITATION_SOURCE_FLOOR>` 份限制 / 失败 / 争议来源
- 每条研究线都必须形成一份 `evidence-summary` 和一份 `question-list`

只有当该研究线已完成一轮 stop assessment、`must_answer` 已有本地证据支撑、且限制 / 失败模式补搜已明确记录时，才允许使用 `early_saturation`，并且必须写入 `<STATUS_PATH>.Wave 1`。

### Wave 2：横向比对与综合判断

- purpose: 把分题结果重新收束成整体结构和跨主题判断
- minimum:
  - 每个横向判断都能追溯到具体 `<REFERENCE_DIR>/*.md`
  - 每条研究线至少有 2 个与其他研究线发生交叉验证的结论
  - 明确区分“硬事实”“分析判断”“趋势推测”

### Readiness Check：最终验收闸门

至少覆盖下面 5 项：

- `30-Second Local Evidence Retrieval`
- 每线“机制 + 趋势 + 难点”检查
- 横向综合检查
- 拓扑稳定性检查
- 接手可继续性检查

### 搜够了没有：停止条件（topic-level stop condition）

每条研究线在 stop assessment 完成前，`topic_stop_decision` 保持 `not_assessed`。

完成一轮搜集并进入 stop assessment 后，必须把当前状态明确归类为 `continue / early_saturation / suspend / archive / redirect` 之一。

其中，只有同时满足下面条件，才允许把该研究线视为“已搜够一轮”并进入 `early_saturation / archive / redirect` 这类停止型决策：

- 核心对象清单已经稳定，不再持续新增关键名字
- 新搜到的材料大多在重复已知事实，而不是贡献新信息
- 该研究线的固定问题都已经有证据支撑
- 至少有 1 轮对“反例、限制、争议”的专门补搜
- 已完成一次“官方说法 vs 第三方验证 / 实践证据 / 事故复盘”交叉核验
- 所有重要但未解的问题，都已经被明确归类为 `continue / early_saturation / suspend / archive / redirect`

补充判定：

- `continue`：当前线仍有高价值缺口，且继续深挖预期能改变判断质量
- `early_saturation`：该维度已明显饱和，继续搜索主要只会引入低质量重复材料
- `suspend`：重要，但当前受限于材料、访问或时机，暂不继续
- `archive`：继续下钻的边际收益低，短期内不太可能改变核心判断
- `redirect`：问题重心应转移到其他研究线或新 formalized topic

## 研究线的具体目标

<!-- duplicate one block per actual topic; do not redefine must_answer here -->
### 研究线 <topic_id>：<topic_slug>

- registry_ref: `PLAN_PATH -> 研究线注册表（topic registry） -> <topic_id>/<topic_slug>`
- wave1_deepen_focus:
- evidence_priority:
- difficulty_focus:
- trend_question:
- stop_assessment_focus:

## 成功标准（post-pass success state）

达到下面状态，才算真正满足目标：

- `<REFERENCE_DIR>` 中有一批高可信、可追溯的 ground truth 文档
- 每条研究线至少形成一组可复用证据包，而不是临时搜索结果
- 对每条研究线都能解释机制、趋势和难点
- 每个重要判断都能追溯到本地 reference 文档
- 对趋势、难度、争议都有专门证据，而不是顺手一提
- 可以明确说清楚“哪些问题不是没做，而是被主动 `suspend`，以及为什么”
- 后续新的 agent 接手时，只看 `<SEED_DIR> + <REFERENCE_DIR> + <ARTIFACT_DIR> + <STATUS_PATH> + <QUEUE_PATH>` 就能继续往下研究

## Hard Gates（可选）

默认不启用；只有当 `hard_gates_enabled = yes` 时，才把它叠加到 `Readiness Check` 上。

启用时至少检查：

- 没有 P0 级结论处于“只有单一弱来源支撑”的状态
- 所有关键术语都在跨主题范围内完成口径对齐
- 所有高价值结论都已明确标注“硬事实 / 分析判断 / 趋势推测”
- 至少完成一轮针对反例和失败模式的专门检索

<!-- END PLAN SKELETON -->

---

## 配套 Status File Skeleton

复制时只取 `BEGIN STATUS SKELETON` 与 `END STATUS SKELETON` 之间内容，不包含 marker 本身。

<!-- BEGIN STATUS SKELETON -->
# <PLAN_NAME> 执行状态（Progress / State）

> 对应计划：`<PLAN_PATH>`
> 对应执行队列：`<QUEUE_PATH>`
> 本文件只记录运行态状态、阻塞、恢复上下文与分支处置；连续动作回读 `<QUEUE_PATH>`。

## 当前执行快照（Current Execution Snapshot）

- state: `not_started`
- current_mode: `instantiation_only`
- current_wave: `Instantiation`
- blocking_issue: `not_applicable`
- required_next_step: `initialize execution surfaces`
- largest_gap_if_stop_now: `execution surfaces and shared ground truth are not initialized`

## Queue Pointer

- queue_path: `<QUEUE_PATH>`
- last_queue_refill: `not_started`

When `QUEUE_PATH.Active Queue.queue_health = blocked`, sync `state = blocked`, `blocking_issue`, and `Resume Checkpoint.safe_to_interrupt` with `QUEUE_PATH.Blocked State`.

## Gate State

- current_gate: `instantiation_complete`
- next_gate: `setup_ready`
- next_scoring_action: `+index`
- stalled_scoring_actions_since_last_gap_reduction: `0`
- last_gap_reduction: `instantiation completed`

## Plan / Status Sync

- plan_placeholders_cleared: `yes`
- topology_sync_state: `synced`

## 目录与集成状态（Directory / Integration State）

- seed_readme_ready: `no`
- reference_readme_ready: `no`
- artifact_readme_ready: `no`
- reference_index_ready: `no`
- seed_backfill_status: `not_started`
- artifact_status: `not_started`

## Topology Delta / Formalization State

当前有效 topic 数量始终由 plan 中的 `topic registry` 派生；此处只记录拓扑增量、推进中的结构变化与最近一次正式化说明。plan/status 哪一侧尚待同步，不写在这里，统一写入上面的 `Plan / Status Sync.topology_sync_state`。

- new_topics: `none`
- pending_topic_candidates: `none`
- recent_change: `instantiated from current seed baseline`
- formalization_sync_note: `not_applicable`

## Wave 0：共享 Ground Truth 地基

- target_floor: `<WAVE0_SHARED_DOC_FLOOR>`
- docs_landed: `0`
- completion_status: `not_started`
- foundation_sufficiency_check: `not_started`
- gap: `shared ground truth has not started`

## Wave 1：按研究线深挖

<!-- duplicate one block per actual topic; heading must match PLAN_PATH topic registry id + slug -->
### 研究线 <topic_id>：<topic_slug>

- registry_ref: `PLAN_PATH -> 研究线注册表（topic registry） -> <topic_id>/<topic_slug>`
- topic_id: `<topic_id>`
- topic_slug: `<topic_slug>`
- doc_count: `0`
- primary_count: `0`
- primary_source_coverage: `insufficient`
- secondary_count: `0`
- recent_count: `0`
- limitation_count: `0`
- topic_stop_decision: `not_assessed`
- early_saturation_reason: `not_applicable`
- evidence_summary: `not_started`
- question_list: `not_started`
- status: `not_started`
- gap: `not_started; derive from PLAN_PATH topic registry current_hypothesis / must_answer`

When `topic_stop_decision = suspend / archive / redirect`, add or update the matching record in `Suspended Branches`. When `topic_stop_decision = early_saturation`, keep `early_saturation_reason` explicit even if no separate branch record is needed.

## Wave 2：跨主题综合

- synthesis_file: `not_started`
- cross_checks_done: `0`
- unresolved_conflicts: `not_started`
- status: `not_started`

## Readiness Check

- 30_second_local_evidence_retrieval: `fail`
- mechanism_trend_difficulty_check: `fail`
- cross_topic_synthesis_check: `fail`
- topology_stability_check: `fail`
- handoff_continuity_check: `fail`
- overall_status: `fail`

## Suspended Branches

记录所有非主线分支处置，不只包含 `suspended`。

- none_recorded_yet: `yes`

When first real disposition appears, delete `none_recorded_yet` and add exactly these fields: `branch / state / why / confirmed_so_far / still_missing / reopen_trigger`.

## Failed Explorations

只记录有代表性的失败探索，避免后续重复无效路径。

- none_recorded_yet: `yes`

When first representative miss appears, delete `none_recorded_yet` and add exactly these fields: `exploration / why_tried / what_found / why_failed / lesson`.

## Resume Checkpoint

这里记录恢复上下文；下一步动作一律回读 `QUEUE_PATH`，不要在此处复制第二份 active queue。

- last_completed_step: `instantiation completed`
- last_verified_result: `plan + status + queue created`
- safe_to_interrupt: `yes`
- queue_resume_entry: `read <QUEUE_PATH> -> Active Queue`
- resume_precheck: `confirm execution entry prerequisites before Wave 0`
- do_not_forget: `initialize README, _INDEX, reference, and artifact surfaces before Wave 0`

## Worklog

- instantiation completed in current session
<!-- END STATUS SKELETON -->

---

## 配套 Queue File Skeleton

复制时只取 `BEGIN QUEUE SKELETON` 与 `END QUEUE SKELETON` 之间内容，不包含 marker 本身。

<!-- BEGIN QUEUE SKELETON -->
# <PLAN_NAME> Execution Queue

> 对应计划：`<PLAN_PATH>`
> 对应状态：`<STATUS_PATH>`
> 本文件只记录连续执行动作、补队列候选与提升规则；不替代设计态蓝图或完整状态面。

## Active Queue

- queue_health: `ready`

### current_task

- action: `initialize execution surfaces and verify directory scaffolding`
- done_condition: `REFERENCE_DIR, ARTIFACT_DIR, SEED_DIR/README.md, REFERENCE_DIR/README.md, ARTIFACT_DIR/README.md, and REFERENCE_DIR/_INDEX.md exist or are intentionally refreshed`
- writes_to: `<SEED_DIR>/README.md; <REFERENCE_DIR>/README.md; <ARTIFACT_DIR>/README.md; <REFERENCE_DIR>/_INDEX.md; <STATUS_PATH>`
- status_sync: `set current_mode=execution, current_wave=Wave 0, current_gate=setup_ready, and update Directory / Integration State`

### next_task

- action: `create or refresh README and _INDEX entry points`
- done_condition: `30-Second Local Evidence Retrieval entry points are present and point to plan, status, queue, reference, and artifact surfaces`
- writes_to: `<SEED_DIR>/README.md; <REFERENCE_DIR>/_INDEX.md; <STATUS_PATH>`
- status_sync: `update Directory / Integration State and Resume Checkpoint`

### next_after_next

- action: `start Wave 0 by landing next high-value shared reference`
- done_condition: `one shared reference is captured as an Authoritative Copy and indexed`
- writes_to: `new 00-shared-* reference file under REFERENCE_DIR; REFERENCE_DIR/_INDEX.md; STATUS_PATH`
- status_sync: `increment Wave 0 docs_landed and update Gate State.next_scoring_action`

## Blocked State

- blocked_reason: `not_applicable`
- interrupt_condition_matched: `not_applicable`
- unblock_trigger: `not_applicable`

When this section is active, `STATUS_PATH.state` must be `blocked`, `STATUS_PATH.blocking_issue` must summarize the same blocker, and `STATUS_PATH.Resume Checkpoint.safe_to_interrupt` must match the actual interrupt safety.

## Refill Pool

Repeat the following candidate block as needed. Do not collapse multiple candidates into one comma-separated line.

### Candidate Block

- candidate: `add next Wave 0 shared reference after current task`
- done_condition: `candidate reference is landed, indexed, and reflected in Wave 0 status`
- writes_to: `<REFERENCE_DIR>; <REFERENCE_DIR>/_INDEX.md; <STATUS_PATH>`
- status_sync: `Wave 0 docs_landed / gap / next_scoring_action`
- why_next: `keep the active queue visible through execution entry`
- prerequisite: `execution entry has started`
- promotion_trigger: `current_task closes or active queue becomes thin`

## Promotion Rules

- when_current_finishes: `promote next_task, shift next_after_next, refill immediately`
- when_queue_becomes_thin: `promote highest-value ready candidate and replenish the third slot`
- when_blocked: `write blocked state explicitly and keep unblock trigger concrete`
- when_to_suspend_branch: `when a branch no longer advances the mainline or cannot be unblocked cheaply`

## No-Empty-Queue Rule

- before_closing_current_task: `refill active queue first`
- must_refill_to: `current_task / next_task / next_after_next`
- only_allowed_empty_condition: `true mainline blockage that satisfies Autonomous Execution Protocol interrupt conditions`
<!-- END QUEUE SKELETON -->

## C. Execution Protocol

这一块是 execution-only 协议层，不参与 skeleton 复制。

## Execution Protocol（执行协议）

### Execution Entry Protocol（从 instantiation 进入 execution）

进入 `Execution Mode` 后，按下面顺序启动：

1. 再次确认 `PLAN_PATH`、`STATUS_PATH` 与 `QUEUE_PATH` 已存在，且 `Instantiation Checklist` 已通过。
2. 初始化或更新 `REFERENCE_DIR`、`ARTIFACT_DIR`、`SEED_DIR/README.md`、`REFERENCE_DIR/README.md`、`ARTIFACT_DIR/README.md`、`REFERENCE_DIR/_INDEX.md`。
3. 把 status 切到执行态：
   - `current_mode = execution`
   - `current_wave = Wave 0`
   - `current_gate = setup_ready`
4. 把 queue 从 instantiation handoff seed 切换为 execution active queue，并把 `queue_health` 设为 `ready`。
5. 按 plan 中的 `Wave 0 -> Wave 1 -> Wave 2 -> Readiness Check` 推进。

Execution entry constraints：

- 在正式开始 `Wave 0` 之前，必须先创建 `REFERENCE_DIR`、`ARTIFACT_DIR`、`STATUS_PATH` 与 `QUEUE_PATH`
- 在正式开始 `Wave 0` 之前，必须先准备好 `SEED_DIR/README.md`、`REFERENCE_DIR/README.md` 与 `ARTIFACT_DIR/README.md`
- 如果没有特殊原因，`REFERENCE_DIR` 就直接使用 `<SEED_DIR>/_reference`
- 如果没有特殊原因，`ARTIFACT_DIR` 就直接使用 `<SEED_DIR>/_artifacts`
- 只有在确有必要时，才把 `REFERENCE_DIR` 或 `ARTIFACT_DIR` 放到 `SEED_DIR` 之外；一旦这样做，必须在 plan 中解释原因
- 无论目录放在哪里，都必须保证接手者能在 30 秒内定位到本轮 reference、artifacts 与 status
- `setup_ready` 表示目录初始化已经完成，下一活跃波次是 `Wave 0`；本模板没有独立的 `Setup` wave

### Autonomous Execution Protocol（自主执行协议，MUST READ）

#### 1. 默认模式：静默自主推进（MUST）

- **MUST**：按 Wave / Step 检查点持续推进，状态写入 `<STATUS_PATH>`
- **MUST NOT**：主动停下来向用户汇报或等待确认
- **MUST NOT**：在对话中重复 status 文件已经记录的内容
- **MUST**：每完成一个有意义的步骤（一份 reference 落库、一条研究线完成、一个波次达标、一个 readiness 缺口修复），更新 status 文件后立刻继续下一步
- **MUST**：默认推进粒度是“连续把整段主链往前跑”，不是“做一小步就回话”

#### 1.1 QUEUE_PATH（连续派工机制，MUST）

- **MUST**：把连续派工显式写入 `QUEUE_PATH`
- **MUST**：默认至少保持下面 3 层非空：
  - `current_task`
  - `next_task`
  - `next_after_next`
- **MUST**：在关闭 `current_task` 之前，先补齐后续队列；不要等当前任务做完后才临时想下一步
- **MUST**：如果某一步完成后会让显性待办队列变空，优先做 queue refill，而不是停下来
- **MUST**：把“下一步在哪看”设计成显式可检索入口；默认入口就是 `QUEUE_PATH`
- **MUST NOT**：让 `required_next_step` 成为唯一下一步字段；它是当前单步要求，不替代独立执行队列
- **MUST**：`required_next_step` 与 `Resume Checkpoint` 只保留摘要、恢复指针或 precheck；不要复制 `QUEUE_PATH.Active Queue`
- **MUST**：`Refill Pool` 按候选块重复追加；不要把多个候选压成一行，也不要在无说明时覆盖旧候选
- **MUST**：当 `queue_health = blocked` 时，在 `QUEUE_PATH` 显式写出 `blocked_reason`、`interrupt_condition_matched` 与 `unblock_trigger`
- **MUST**：当 `queue_health = blocked` 时，同步更新 `<STATUS_PATH>.state = blocked`、`blocking_issue`，以及 `Resume Checkpoint.safe_to_interrupt`
- **MUST NOT**：在没有满足允许中断条件时，让 `QUEUE_PATH` 的 active queue 掉空

queue 维护原则：

- `current_task`：当前应立即执行的单一动作
- `next_task`：当前动作完成后立刻接上的下一个动作
- `next_after_next`：防止局部完成后空转的第三层缓冲动作
- 每个 active task 都必须有可检查的 `done_condition / writes_to / status_sync`，否则只是提示语，不算可执行队列项
- `queue_health = ready`：三层队列完整
- `queue_health = thin`：只剩 1 到 2 层，应先补齐队列
- `queue_health = blocked`：只有满足允许中断条件时才可使用

`QUEUE_PATH` 的目标不是做完整 project plan，而是避免 agent 在局部完成后获得“喘气机会”并错误停机。

#### 2. 允许中断用户的条件（ONLY）

**ONLY interrupt when** 下面四种情况之一成立：

1. **主线阻塞且无法绕开**：整条主线被阻塞，且无法通过 `suspend`、`archive`、`redirect` 绕开。单个分支卡住不算主线阻塞。
2. **研究方向需要根本性调整**：核心假设错误、最终产出定义需要变更、或研究线注册表需要重大重构。补证据、扩对象、换搜索策略不算根本性调整。
3. **涉及高风险、不可逆或难回滚操作**：下一步会带来高风险真实动作、难以回滚的写入、外部发布、付费、删除或权限风险。
4. **用户明确要求实时协同**：用户在本轮任务中明确要求同步讨论、逐步确认或实时汇报。

#### 3. 不允许中断用户的情况（MUST NOT）

**MUST NOT interrupt for**：

- 已明确进入 `Execution Mode` 后，从 `instantiation_complete` 过渡到 `setup_ready` 的 execution entry；如果当前任务只是生成、修复或审查 `plan + status + queue`，仍必须停在 `Instantiation Mode`
- Wave 之间的过渡
- 单个研究线的配额达标或完成
- 发现某个分支需要 `suspend`、`archive` 或 `redirect`
- 证据配额全部达标
- 遇到搜索困难但可以绕开
- 发现新的高价值方向
- 某条研究线的停止条件已满足
- 某个新对象已经明确应升格为独立 topic
- Readiness Check 某项未通过但可以自主补齐

#### 4. 进度可见性靠文件，不靠对话

- `<STATUS_PATH>` 是默认状态沟通机制
- `QUEUE_PATH` 是默认“接下来干什么”的显性入口
- Worklog 必须持续追加，记录关键推进和关键判断
- 用户主动询问进度时可以简要回答，但默认不主动发起进度汇报
- 如果用户中途插入其他任务，恢复时优先读 `QUEUE_PATH`、再读 `<STATUS_PATH>` 的当前状态、Gate State、Suspended Branches、Failed Explorations 和 Resume Checkpoint

#### 5. 与 human-on-the-loop 原则的关系

- 长程任务默认按 `human-on-the-loop` 处理；高难分支优先登记后继续推进。分支处置细则见后文 `## Suspended Branch Protocol`

### Topology Formalization Gate（拓扑正式化闸门）

这一步用于处理中途 scope 扩张时的结构同步。

如果新的研究对象已经形成独立问题簇、独立对象清单或独立工件需求，就应当把它升格为新 topic。

一旦升格为新 topic，必须在进入下一波次前同步下面对象：

- `PLAN_PATH`
- `STATUS_PATH`
- `PLAN_PATH -> 研究线注册表（topic registry）`
- 输入目录中的 topic 索引文件（如 `topics/README.md`）
- 新 topic seed 文件

不允许继续一边按旧拓扑推进，一边口头承认“这其实已经是新 topic”。

### Exploration-Exploitation Decision Framework（探索 / 利用决策框架）

目的：在“探索新方向”和“深挖已知线索”之间做稳定判断，避免机械凑配额，也避免漏掉真正改变拓扑的新方向。

#### Exploration Signals

出现下面信号时，应该考虑探索新方向：

- **高频未归类概念**：连续多份 reference 指向同一个现有 topic 难以容纳的新概念
- **未建模维度**：多个来源指向同一个新的机制、风险、评价维度或生命周期阶段
- **核心问题未回答**：配额接近达标，但 `must_answer` 仍有实质性空洞
- **横向依赖变强**：新方向会影响多个 topic 的结论、推荐、baseline 或最终产出结构

#### Exploitation Signals

出现下面信号时，应该继续深挖或收束已知线索：

- **证据收敛**：新增材料大多重复已知事实
- **问题清单收敛**：旧问题逐步被回答，新问题产生速度明显下降
- **反例搜索饱和**：专门搜索限制、争议、失败模式后没有发现新的关键反例
- **机制稳定**：核心机制已经能简洁解释，并且有多个高可信来源支撑

#### Decision Rules

- **`continue`**：exploitation signals 不足，且 exploration signals 不足以改变拓扑
- **`early_saturation`**：主要来源类型或子问题已经明显饱和；继续搜索主要只会引入低质量重复材料
- **`suspend`**：当前线重要，但暂时缺材料、访问受限，或继续追踪会明显卡住主线
- **`archive`**：继续下钻边际收益低，且不太可能改变核心判断
- **`redirect`**：新方向更可能改变核心判断；当前问题重心应转移到其他研究线或新 formalized topic

如果 `redirect` 导致出现独立问题簇、独立对象清单或独立工件需求，再触发 `Topology Formalization Gate` 去做结构同步。`Formalize 新 topic` 是结构动作，不是第二套并行 decision enum。

这套框架是判断启发，不是新的硬配额。最终仍以 `FINAL_DELIVERABLE`、`must_answer` 和本地证据质量为准。

### Foundation Sufficiency Check（Wave 0 → Wave 1，地基充分性检查）

进入 Wave 1 前，必须确认 Wave 0 不是“配额达标但地基不足”。

验收标准：

- 所有 topic 的核心术语，都能在 Wave 0 文档或研究线注册表中找到工作定义
- 所有 topic 的对象分类，都能映射到共享地基里的共同层或明确说明其差异
- 每条研究线都有明确的 Wave 1 起点：优先来源、关键对象、关键问题或已知缺口
- `<REFERENCE_DIR>/_INDEX.md` 已能作为共享 ground truth 的 `30-Second Local Evidence Retrieval` 入口

如果任何一条不满足，先补 Wave 0 或研究线注册表，再进入 Wave 1；不要把共享地基债务推迟到 Wave 1 中途处理。

### Early Saturation Protocol（topic-level decision 特判）

配额是防止浅搜的下限，不是鼓励低质量凑数的上限。

当某个研究线已经满足 topic-level 停止条件，且饱和发生在某个来源类型或子问题维度上时，可以使用 `early_saturation`；但必须在 `<STATUS_PATH>.Wave 1` 中把它写成显式 `topic_stop_decision`，并记录理由。

适用条件：

- 已有来源来自权威一手来源、高可信研究或核心维护者说明
- 连续多轮搜索新增材料主要重复已知事实
- 继续搜索只会引入低质量来源，无法改变核心机制、趋势或限制判断
- 该维度的核心判断已经能被本地 reference 支撑

status 记录建议：

```md
- topic_stop_decision: `early_saturation`
- primary_count: `3`
- primary_source_coverage: `saturated`
- early_saturation_reason: `新增材料连续重复核心机制，继续搜索只会引入低质量来源；当前 3 份 primary source 已足以支撑本轮判断。`
```

其中：

- `topic_stop_decision = early_saturation` 是研究线级决策
- `primary_source_coverage = saturated` 只是 primary source 维度已经足够 / 饱和时的可选辅助标记，不是必填替代项
- 在 stop assessment 完成之前，`topic_stop_decision` 保持 `not_assessed`
- 当 `topic_stop_decision = suspend / archive / redirect` 时，应同步补一条 `Suspended Branches` 记录，写清 `why / confirmed_so_far / still_missing / reopen_trigger`

Early saturation 只能降低“继续凑数”的优先级，不能绕过 `must_answer`、失败模式覆盖、Readiness Check 或关键结论的证据要求。

### 证据采集协议

`<REFERENCE_DIR>` 里的每个 `md` 建议遵循统一结构：

```md
# 标题

- source_url:
- source_type:
- accessed_at:
- related_topic:
- trust_level: (official / academic / practitioner / community)
- why_it_matters:
- captured_excerpt: (yes / no / partial)

## 关键事实

## 核心内容摘录

## 与本研究的关系

## 可直接引用的术语 / 概念

## 风险与局限
```

#### `## 核心内容摘录` 写法规则

定位：这一节是源头内容的“硬核精华提取”，目标是让读者不回 URL 就能把这份 reference 当作该来源的本地权威替代。

写什么：

- 关键论证链条和推理逻辑
- 重要数字、参数、阈值、性能指标
- 关键表格、对比矩阵、分层结构的忠实摘录
- 方法论要点、实验设计、测试条件
- 必要的短引文，其余以结构化摘要和转述为主
- 事故 / 案例的关键时间线和因果链
- 标准 / 规范的条款级摘要

不写什么：

- 不做二次解读或评论
- 不重复 `## 关键事实` 已经覆盖的要点
- 不抄录与本研究无关的背景铺垫
- 不整段复制纯文学性描述或营销话术

篇幅指引（按来源价值弹性控制）：

- 高价值一手来源（official / academic）：500-1500 字的结构化摘要
- 中等价值来源（practitioner）：200-500 字
- 低价值来源：可留空，注明“关键事实已充分覆盖，无需额外摘录”

忠实度要求：

- 摘要和短引文必须忠实于原文，不美化、不夸大、不把推断写成原文结论
- 如果是翻译，标注原文语言
- 数字和术语必须与原文一致，不做单位换算或近似处理
- 如果原文有歧义或矛盾，如实记录，不擅自取舍
- 遵守来源许可、版权限制和合理引用边界；不要把 reference 写成原文镜像

`captured_excerpt` 字段说明：

- `yes`：核心内容已充分摘录，后续使用时不需要回看原文
- `partial`：部分关键内容已摘录，但仍有值得补充的段落
- `no`：未做摘录；仅适用于低价值来源，且 `## 关键事实` 已充分覆盖

补充建议字段：

- `claims_supported:`
- `date_scope:`
- `related_entities:`

命名建议：

- `00-shared-<source-slug>.md`
- `<NN>-<topic-slug>-<source-slug>.md`

其中 `<NN>` 与 `<topic-slug>` 来自研究线注册表。

### 已验证的高杠杆执行行为（execution-only，默认遵守）

- 以“证据落库”为单位推进：每一次有效探索都必须落为 `<REFERENCE_DIR>/*.md`，否则视为未完成
- 以“对象清单稳定”为停止前提：围绕同一研究线持续扩对象与对照面，直到核心对象清单稳定
- 以“下钻到机制”为深挖目标：关键对象不只看 README，还要沿 docs -> schema / code / issue / 反例逐级下钻
- 以“边取证边回填”避免集成债：新增证据落库后立刻回填到对应 seed 文件和 `<ARTIFACT_DIR>` 中
- 以“持续自校验”保证 `30-Second Local Evidence Retrieval`：每个波次结束后都做一次相关检查，并维护 `<REFERENCE_DIR>/_INDEX.md`
- 以“执行队列永不见底”防止中途停机：任何时刻都要让 `QUEUE_PATH` 的 active queue 保持至少 3 层可见动作，除非主线真正阻塞
- 无外部阻塞时按 Wave / Step 检查点持续自主推进

### 什么值得存进 `<REFERENCE_DIR>`

优先入库：

- 会进入后续推理链条、且会被反复复用的高价值内容
- 能补充新事实、澄清机制差异、或解释趋势 / 难点 / 争议的一手或高可信二手来源
- 能提供真实约束、真实失败模式、实践门槛或事故复盘的材料

不建议入库：

- 只重复已知结论、没有新增信息的内容
- 相关性弱、可信度低、或只做表面排名的材料
- 纯 SEO 聚合页、内容农场、无机制和证据的短帖

入库判断的硬标准：

- 能补充新事实
- 能澄清机制差异
- 能提供一手或高可信二手证据
- 能帮助解释趋势、难点或争议

如果不能满足上面任一条，就不入库。

### Suspended Branch Protocol（探索分支处置协议）

目的：

- 控制探索树扩张，只保留会推进 `must_answer / 当前 gap / FINAL_DELIVERABLE` 的分支

处理等级：

说明：

- 下面列的是协议动作名：`discard / compress / suspend / archive / redirect`
- 真正写入 `<STATUS_PATH>.Suspended Branches.state` 时，统一使用 `Canonical Enum Registry` 中的过去分词态：`discarded / compressed / suspended / archived / redirected`

- `discard`：相关性弱、可信度不足、或只重复已知结论
  - 处理：不落库、不回填 seed、不写 artifact
- `compress`：公开信息不足或边际收益低，但结论本身值得记住
  - 处理：只在 `question-list`、`status` 或综合 artifact 里留一句压缩结论
- `suspend`：问题本身重要，但当前继续追会明显卡在 `access boundary / disclosure boundary / 搜索重复 / 边际收益过低`
  - 处理：不阻塞主线，先继续推进其他高价值分支；同时必须把这个分支登记为 `suspended`
- `archive`：继续下钻边际收益低，且不太可能改变核心判断
  - 处理：封存时只写推进到哪里、为什么暂不继续、什么条件下重开
- `redirect`：其他问题更可能提升证据强度、缩小不确定性或改变核心判断时，立即转向

#### `suspend` 与 `archive` 的区别

- `suspend`：问题仍然重要，只是当前不值得继续死磕；默认期待未来可能被新线索、新资料或新访问入口重启
- `archive`：问题当前已经不值得继续投入；即使未来重开，优先级通常也低于其他未解问题

`human-on-the-loop` 提醒：高难分支优先 `suspend and continue`；需要人工同步介入时，按前文 `Autonomous Execution Protocol` 的中断条件处理。

#### Suspended Branch 最低记录格式

建议在 status、综合 artifact 或 closeout 文档里至少保留下面结构：

```md
- branch: `<topic-slug / question>`
- state: `discarded / compressed / suspended / archived / redirected`
- why: `<access boundary / disclosure gap / repeated search / low marginal return>`
- confirmed_so_far:
- still_missing:
- reopen_trigger:
```

### 并行执行建议

这件事适合并行推进，但要有明确分工。

建议分成：

- 主线程：维护总问题、统一标准、去重、综合判断、拓扑同步
- 研究线线程：每条研究线一个线程

主线程职责：

- 统一证据采集格式
- 维护 `<REFERENCE_DIR>` 命名规范
- 避免不同线程重复抓同一来源
- 在 Wave 2 做跨主题综合
- 当 scope 扩张到足以形成独立 topic 时，先做结构同步再继续推进

各研究线线程职责：

- 深挖自己主题
- 把高价值来源落为 `<REFERENCE_DIR>/*.md`
- 回填到对应 seed 文件
- 维护本研究线的 evidence summary 与 question list

为了避免写冲突，建议按前缀分工：

- 主线程写共享地基：`00-shared-*`
- 研究线 `<NN>` 只写：`<NN>-<topic-slug>-*`

### 执行节奏

推荐顺序：

1. 列权威来源优先级清单，只抓高可信来源
2. 初始化 `<REFERENCE_DIR> / <REFERENCE_DIR>/_INDEX.md / <ARTIFACT_DIR> / <STATUS_PATH> / <QUEUE_PATH>`，先建 `30-Second Local Evidence Retrieval` 与执行队列入口再写结论
3. 扩对象、案例和机制差异
4. 上升到机制抽象
5. 补趋势、难点和失败模式
6. 做跨主题综合

如果某一步还没有达到对应检查点，不要机械进入下一步。

## D. Appendix / Maintenance

这一块只服务模板维护本身，不进入实例产物。

## Appendix：Template Maintenance（模板维护附录）

### Quality Calibration Loop（四维质量校准）

这一节用于维护模板本身，不属于每轮执行态 status / queue 的必填字段。

每次迭代主模板时，先做一轮轻量质量校准，不要一上来大改结构。

校准维度：

- 系统性：关键对象、证据类型、失败模式和最终产出需求是否都被覆盖
- 结构性：topic registry、Wave、reference、artifact、status、queue 之间是否有清晰依赖关系
- 游戏性：执行者是否知道下一步怎样得分、何时升级、何时停止、何时挂起分支
- 简洁性：是否存在重复规则、过长说明、低价值约束或会让执行者跳读的噪音

迭代规则：

- 每轮只选 1 到 2 个最影响执行质量的问题修
- 优先修会改变执行行为的规则，其次修表达，最后才修版式
- 每次调整都要写清楚 `current_score`、`smallest_next_move` 和 `do_not_change_yet`
- 如果一次改动需要重排多个大章节，先暂停，把它登记为下一轮候选，而不是当场大改

## 这个模板真正要守住的东西

以后无论你研究的主题是什么，只要还是“给定一个目录，从若干 topic seed 出发，做逐轮 Deep Research，并让本地知识库继续生长”，真正不能丢的是下面这些东西：

- 输入目录必须先被建模成研究线注册表
- 每轮都必须先写清楚最终服务于什么产出
- 每轮都必须有 `Instance Config`
- 每轮都必须显式区分 `Instantiation Mode` 与 `Execution Mode`
- 每轮都必须有 Wave 0 / 1 / 2 和 Readiness Check
- 每轮都必须以本地 evidence 落库作为完成单位
- 每轮都必须要求输入目录本身生长，而不是只生成旁路报告
- 每轮都必须有明确停止条件
- 每轮都必须保留高难问题的 `suspend` 语义
- 每轮都必须做到 `30-Second Local Evidence Retrieval` 成立
- 每轮的 reference 文档都必须做到硬核内容自给自足
- 每轮都必须有独立的 `QUEUE_PATH`
- plan / status / queue / reference / artifact / navigation 的对象边界必须清楚

如果这些约束还在，这个框架就还是同一个框架。具体主题、目录名、研究线数量、配额数字，都只是实例化参数。
