# 术语手册

这份手册的目的只有一个：把整套报告里出现的专业术语、缩写和概念，用清楚的中文说明白。

如果你在阅读其他文档时遇到不熟悉的词，来这里查。如果你想先系统了解所有术语再开始读，也可以从这里入手。

术语按主题分组，而不是字母顺序——因为理解一个领域，更需要知道"这些词之间什么关系"，而不是"A 开头的词有哪些"。

---

## 一、需求工件术语

### User Story（用户故事）

用最简洁的方式描述"谁要什么、为什么值得做"的一种需求写法。经典格式是：

```text
As a [角色],
I want [想要什么结果],
so that [为什么值得做].
```

User Story 的工作是表达意图，不是承载完整规格。它有意留下协商空间，让工程、设计、测试可以在这个方向上共同细化。

### INVEST

User Story 的质量评判框架，由 Bill Wake 提出，被 Martin Fowler、Mike Cohn 等人广泛引用。六个字母分别代表：

| 字母 | 英文 | 中文 | 含义 |
|------|------|------|------|
| I | Independent | 独立 | 不同 Story 之间不要强耦合，最好能单独排优先级 |
| N | Negotiable | 可协商 | 留下对话空间，不要把实现写死在 Story 里 |
| V | Valuable | 有价值 | 让真实受益方能从中得到价值，不是内部技术目标 |
| E | Estimable | 可估算 | 让团队能大致判断规模、风险和优先级 |
| S | Small | 足够小 | 控制在一个迭代内可讨论并推进 |
| T | Testable | 可确认 | 让团队能想象后续如何验证它是否成立 |

实际使用时，优先守住 V、S、T 三项，其他是进一步优化目标。

### Acceptance Criteria（AC，验收标准）

说明一个功能或行为"在什么条件下算完成"的验收边界。AC 的工作是接住 User Story 故意留白的部分——Story 说方向，AC 说判断标准。

好的 AC 通常要讲清楚：在什么条件下触发、系统给出什么响应、异常时如何降级。

### Examples（示例）

用具体场景把需求边界说清楚的工具。比 AC 更具体，通常用一个完整的输入-动作-输出结构来消除歧义。Examples 让团队"无法各自脑补"。

### Gherkin（小黄瓜语言）

一种用于编写可执行验收场景的结构化语言，通常配合 BDD 工具使用。经典格式是：

```gherkin
Given [前置状态]
When [触发动作]
Then [期望结果]
```

Gherkin 属于验证层，它的职责是把已经明确的意图和契约变成可检查、可运行的场景。它不是需求本体，也不能替代上游的 Story 和契约层。

### BDD（Behavior-Driven Development，行为驱动开发）

一种把需求描述和测试场景连接起来的开发方式。BDD 鼓励用可读的自然语言（通常是 Gherkin 格式）写出系统行为，让开发人员、测试人员和业务方能共同理解同一份"行为定义"。

BDD 最擅长验证层——用示例场景确认系统行为是否符合预期，而不是用来替代需求分析。

### PRD（Product Requirements Document，产品需求文档）

说明业务背景、产品目标、功能范围、优先级和约束环境的文档。PRD 负责讲清楚"我们为什么要做这件事，范围是什么"，不应该承担逐条行为契约的职责。

---

## 二、契约层术语

### EARS（Easy Approach to Requirements Syntax，简易需求句法）

由 Alistair Mavin 等人提出的一种受控自然语言写法，专门用于把系统行为边界写清楚。EARS 的核心是用特定句型结构把"在什么条件下、哪个系统、必须做什么"说明白。

五种核心模式：

| 模式 | 英文 | 典型句型 | 适用场景 |
|------|------|--------|--------|
| Ubiquitous（普遍型） | 无条件约束 | `[系统] shall [动作]` | 全局政策、基础约束 |
| Event-driven（事件触发型） | 事件触发 | `When [事件], [系统] shall [响应]` | 用户操作、外部事件 |
| State-driven（状态驱动型） | 持续状态 | `While [状态], [系统] shall [行为]` | 登录态、运行模式 |
| Unwanted（异常型） | 异常/不期望事件 | `If [异常条件], then [系统] shall [降级/恢复]` | 故障、超时、错误输入 |
| Optional（可选功能型） | 配置/功能开关 | `Where [特性启用], [系统] shall [行为]` | 可选功能、平台差异 |

EARS 不是万能格式。当条件组合超过 3 个、或者出现规则网时，应该换用 decision table 或 DMN。

### Requirement Quality（需求质量）

评判一条需求是否"写好了"的质量框架。对 EARS 一类契约层需求，最重要的质量属性包括：

- **Verifiable / Validatable（可验证）**：能被测试、检查或证明
- **Measurable Performance（可量化）**：有明确的阈值、统计口径或判据
- **Explicit Conditions（显式条件）**：触发条件和状态边界写清楚，不靠上下文猜
- **Pattern Conformance（模式合规）**：句子结构符合批准的模式，如 EARS 的五种模式

### Decision Table（决策表）

用表格形式表达多条件、多规则组合的决策逻辑。当一条 EARS 句子里开始塞进三四个前置条件时，应该换用决策表。决策表的优势是让所有条件组合一目了然，方便验证覆盖完整性。

### DMN（Decision Model and Notation，决策模型与标记法）

OMG（Object Management Group）制定的面向业务决策的建模标准。DMN 比决策表更正式，支持可复用的决策逻辑组件，适合多准则、可组合的业务规则建模。

DMN 适合回答"多输入条件下输出什么结果"，EARS 适合回答"在某种状态下系统必须如何响应"。两者定位不同，不是替代关系。

### NFR（Non-Functional Requirements，非功能需求）

描述系统"如何工作"而不是"做什么"的需求，包括性能、安全、可靠性、可用性、可维护性等维度。

NFR 最容易被写成空洞愿望（"系统要快、要安全、要稳定"），正确做法是把关键指标写进 AC 或 EARS 中，给出可测的阈值和统计口径。

---

## 三、验证层术语

### Acceptance Tests（验收测试）

验证系统是否满足验收标准的一组测试。通常由 AC 和 Examples 转化而来，可以是手工执行的检查清单，也可以是自动化测试用例。

### Traceability（可追溯性）

在需求、验证场景、任务和变更之间建立可追踪关系的能力。有了可追溯性，团队可以知道：
- 这条需求来自哪个上游目标
- 用什么方式证明它已经满足
- 它改动时哪些测试和任务需要一起变

Traceability 不是装饰性文档，而是高风险、多团队、长周期项目的必要能力。

---

## 四、执行层术语

### feature workflow（功能工作流）

某个功能从需求分析到实现交付的完整工件链，通常包括 requirements / design / tasks 或 spec / plan / tasks 的分层组织。

feature workflow 解决的是"需求明确后，如何把工作稳定分配给工程师和 agent"的问题。它应该与 team context 文件（如 AGENTS.md）严格分层：team context 放长期稳定约束，feature workflow 放某个功能的具体边界和任务。

### AGENTS.md / CLAUDE.md（agent 上下文文件）

放在仓库中的 Markdown 文件，供 coding agent 启动时读取，用于传递团队的共享约束、代码库导航、工作方式和守则。

不同工具对这类文件的命名和加载机制有所不同：
- **OpenAI Codex** 使用 `AGENTS.md`，按目录层级链式加载
- **Claude Code** 使用 `CLAUDE.md` 家族和 `.claude/rules/` 路径规则文件
- **Kiro** 使用 steering 体系，同时兼容 `AGENTS.md`

这类文件的共同原则是：适合承载**稳定的团队级约束**，不适合堆进特定功能的详细边界和任务分解（那些应该进入 feature workflow）。

### spec / plan / tasks（规格 / 计划 / 任务）

feature workflow 的一种常见组织形式：

- **spec（规格）**：这个功能的目标、关键约束和验收边界
- **plan（计划）**：实现这个功能的步骤顺序和里程碑
- **tasks（任务）**：分配给工程师或 agent 的具体执行项

这种组织方式让 agent 和人类开发者都能从明确的功能目标出发，而不是从模糊的总需求文档猜。

---

## 五、治理层术语

### ISO/IEC/IEEE 29148

全称：ISO/IEC/IEEE 29148 Systems and software engineering — Life cycle processes — Requirements engineering（系统与软件工程——生命周期过程——需求工程）

这是需求工程领域最重要的国际标准，定义了需求工程的官方范围、过程和质量属性。它不是一本写法手册，而是告诉你"需求工程包含哪些活动、这些活动如何嵌入系统生命周期、好的 requirement 应该满足什么特征"。

在这套报告里，29148 主要用作"需求工程的官方范围和 lifecycle 锚点"，不做 clause-by-clause 的逐条引用。

### INCOSE GtWR（Guide to Writing Requirements，INCOSE 需求写作指南）

INCOSE（International Council on Systems Engineering，国际系统工程协会）出版的需求写作实践指南。与 29148 不同，GtWR 更侧重 practitioner 层的写法规则和质量检查方法——如何把一条需求写得清楚、可测、可审查。

两者互补，不要混用：29148 是标准层，GtWR 是写作实践层。

---

## 六、建模与工程方法术语

### SysML（Systems Modeling Language，系统建模语言）

一种基于 UML 扩展的系统工程建模语言，由 OMG 标准化。SysML v2 是其最新版本，提供了更正式的文本语法和更强的工具互操作性。

SysML 代表的是"模型层"——在文本规格之上，用更结构化的模型表达系统架构、行为和需求的一种方式。在这套报告里，模型层是定位性说明，不是教学主题。

### MBSE（Model-Based Systems Engineering，基于模型的系统工程）

一种用模型（而非纯文本文档）作为系统设计、验证和沟通核心载体的系统工程方法。MBSE 和本报告的关系是：承认它的存在和价值，但本报告聚焦在文本层的需求表达，不展开讲 MBSE 工具链。

### BPMN（Business Process Model and Notation，业务流程建模与标记法）

OMG 制定的业务流程建模标准，用图形化方式描述业务流程的顺序、条件和参与者。在验证层的治理链讨论中，BPMN 是"把业务流程可视化"的工具锚点之一，与 DMN 配合使用。

---

## 快速查阅索引（字母顺序）

| 缩写 / 术语 | 全称 | 所属层次 | 核心职责 |
|------|------|--------|--------|
| 29148 | ISO/IEC/IEEE 29148 | 治理层 | 需求工程国际标准 |
| AC | Acceptance Criteria | 验证层 | 定义功能完成的验收边界 |
| BDD | Behavior-Driven Development | 验证层 | 用行为场景连接需求和测试 |
| BPMN | Business Process Model and Notation | 验证层 | 业务流程建模标准 |
| DMN | Decision Model and Notation | 契约层 | 业务决策逻辑建模标准 |
| EARS | Easy Approach to Requirements Syntax | 契约层 | 受控自然语言需求写法 |
| GtWR | Guide to Writing Requirements | 治理层 | INCOSE 需求写作实践指南 |
| INVEST | Independent, Negotiable, Valuable, Estimable, Small, Testable | 意图层 | User Story 质量评判框架 |
| MBSE | Model-Based Systems Engineering | 模型层 | 基于模型的系统工程 |
| NFR | Non-Functional Requirements | 契约层 + 验证层 | 性能、安全等非功能需求 |
| PRD | Product Requirements Document | 意图层 | 产品需求文档 |
| SysML | Systems Modeling Language | 模型层 | 系统建模语言 |
