# 参考附录

这份附录的职责只有三个：补术语、补可信外部入口、补标准与工具映射。它不是正文的替身，也不是理解前面几份文档的前提。

如果你只想理解整套方法，先看主文档和示例手册即可。只有当你需要回查术语、标准锚点、工作流类型或证据边界时，再回来查这份附录。

建议阅读阶段：`查阅层`

首读目标：

- 首轮阅读时知道这份文档可以整体跳过
- 需要术语、来源、标准边界时再回来查

你现在只需要记住：

- `User Story` 的正式质量锚点是 `INVEST`
- requirement / EARS 的正式质量语言更接近 `Verifiable / Measurable / Explicit Conditions / Pattern Conformance`
- `measurement` 在本包里是解释层常用词，但不是 Story 的正式总框架名词

## 关键术语表

术语按需求工程的五层结构分组，方便查阅时快速定位。

### 意图层工件

| 术语 | 本文中的含义 |
| --- | --- |
| `User Story` | 承载角色、结果和业务价值的意图层工件，不是完整规格 |
| `INVEST` | User Story 的经典质量特征集：Independent、Negotiable、Valuable、Estimable、Small、Testable |

### 契约层工件

| 术语 | 本文中的含义 |
| --- | --- |
| `EARS` | 受控自然语言需求写法，用于把系统在什么条件下必须如何响应写清楚 |
| `Explicit Conditions` | requirement 中的触发条件、状态条件必须显式写出，而不是靠上下文猜 |
| `Pattern Conformance` | requirement 应遵循批准的表达模式；对 EARS 来说就是模式合规 |

### 验证层工件

| 术语 | 本文中的含义 |
| --- | --- |
| `Acceptance Criteria (AC)` | 说明功能或行为在什么条件下算完成的验收边界 |
| `Examples` | 用具体场景消除歧义、支持验收与确认的例子 |
| `BDD / Gherkin` | 用 Given-When-Then 一类结构表达可验证场景的方式，属于验证层 |

### 执行层工件

| 术语 | 本文中的含义 |
| --- | --- |
| `agent context file` | 像 `AGENTS.md`、rules 这类 team / repo 级共享上下文文件 |
| `feature workflow` | 某个 feature 的 `requirements / design / tasks` 或 `spec / plan / tasks` 一类工件链 |

### 治理层工件

| 术语 | 本文中的含义 |
| --- | --- |
| `traceability` | 在需求、验证、任务、审查和变更之间建立可追踪关系 |

### 质量框架术语

| 术语 | 本文中的含义 |
| --- | --- |
| `Verifiable / Validatable` | requirement quality 的核心特征：要求能被验证或确认 |
| `Measurable Performance` | requirement quality 中与阈值、量化性能和统计口径相关的属性 |

### 决策与建模工具

| 术语 | 本文中的含义 |
| --- | --- |
| `decision table` | 用表格表达多条件、多规则组合的决策逻辑 |
| `DMN` | 面向 business decisions 与 business rules 的标准化建模方式 |

### 标准与锚点

| 术语 | 本文中的含义 |
| --- | --- |
| `29148` | requirements engineering 的官方 scope / lifecycle 锚点 |
| `GtWR` | INCOSE 的需求写作与质量规则 practitioner 锚点 |
| `model layer` | 文本规格之外更结构化的模型表达层，例如 SysML v2 所代表的方向 |

## 外部可信 URL 清单

下面这些外部入口，按用途分组列出。它们的作用是支撑进一步阅读，不替代正文解释。

### 标准与官方锚点

| 主题 | URL | 说明 |
| --- | --- | --- |
| ISO/IEC/IEEE 29148 | `https://www.iso.org/standard/72089.html` | requirements engineering 标准目录页 |
| IEEE 29148 官方页 | `https://standards.ieee.org/ieee/29148/6937/` | IEEE SA 官方入口 |
| OMG DMN | `https://www.omg.org/dmn/` | DMN 官方入口 |
| OMG DMN 1.5 | `https://www.omg.org/spec/DMN/1.5/About-DMN` | DMN 1.5 正式版目录 |
| INCOSE GtWR 产品页 | `https://www.incose.org/publications-library/product-details?productid=2bfc20a2-f35b-ef11-8473-002248009cd0` | GtWR 官方产品页 |
| INCOSE GtWR Webinar | `https://www.incose.org/resource/webinar-168-guide-to-writing-requirements-version-4/` | GtWR v4 官方公开讲解入口 |

### 方法论与写法参考

| 主题 | URL | 说明 |
| --- | --- | --- |
| Martin Fowler on User Stories | `https://martinfowler.com/bliki/UserStory.html` | User Story 边界的经典参考入口 |
| Martin Fowler on Given-When-Then | `https://martinfowler.com/bliki/GivenWhenThen.html` | Given-When-Then 的简明边界入口 |
| Mountain Goat Software | `https://www.mountaingoatsoftware.com/` | User Story 与敏捷写法实践参考 |

### 工具与工作流

| 主题 | URL | 说明 |
| --- | --- | --- |
| OpenAI Codex `AGENTS.md` | `https://developers.openai.com/codex/guides/agents-md` | Codex 官方 `AGENTS.md` 分层与发现机制说明 |
| Claude Code memory / `CLAUDE.md` | `https://code.claude.com/docs/en/memory` | Claude Code 官方项目记忆与 `CLAUDE.md` 说明 |
| Amazon Kiro | `https://kiro.dev/docs/getting-started/first-project/` | `requirements / design / tasks` workflow 官方入口 |
| Kiro Steering | `https://kiro.dev/docs/steering/` | team/workspace steering 分层说明 |
| GitHub Spec Kit | `https://github.com/github/spec-kit` | `spec / plan / tasks` workflow 官方仓库 |
| OpenSpec | `https://github.com/Fission-AI/OpenSpec` | cross-tool spec workflow 官方仓库 |

### 进一步阅读

| 主题 | URL | 说明 |
| --- | --- | --- |
| ISTQB Acceptance Testing Syllabus | `https://www.istqb.org/wp-content/uploads/2024/11/ISTQB-CT-AcT_Syllabus_v1.0_2019.pdf` | requirements / AC / Gherkin / BPMN / DMN / traceability 的治理链参考 |
| OMG DMN Intro | `https://www.omg.org/intro/DMN.pdf` | DMN 官方简介 |

## 标准与工具映射表

这张表不是为了证明“每个团队都要上全套”，而是帮助你快速看清：不同锚点分别在整条链条上支持什么。

| 锚点 / 工具 | 更偏支持哪一层 | 最适合回答什么问题 |
| --- | --- | --- |
| `User Story` 方法论 | 意图层 | 为什么做、给谁做、什么结果值得做 |
| `EARS` | 行为契约层 | 系统在什么条件下必须如何响应 |
| `Gherkin / BDD` | 验证层 | 怎样把关键行为变成可检查场景 |
| `DMN / decision table` | 契约层与验证层之间的决策边界 | 多条件、多规则决策逻辑怎样表达 |
| `29148` | 治理与追溯层 | requirements engineering 的 scope 和 lifecycle 锚点是什么 |
| `GtWR` | 契约层与治理层 | 什么样的 requirement 写法更清楚、可测、可审查 |
| `Kiro` | 执行与工作流层 | 如何把 requirements / design / tasks 分层组织 |
| `Spec Kit` | 执行与工作流层 | 如何把 spec / plan / tasks 组织成 feature 工作流 |
| `OpenSpec` | 执行与工作流层 | 如何把 cross-tool 的 spec workflow 组织起来 |
| `AGENTS.md` / rules | team / repo context | 团队共享约束和导航应放在哪里 |

## Story 与 requirement 的正式质量叫法不要混

这是整包里一个很容易被说顺口、但其实必须守住的边界。

| 对象 | 更正式的质量锚点 | 更稳的理解 |
| --- | --- | --- |
| `User Story` | `INVEST` | Story 先看它是否独立、可协商、有价值、可估、够小、可确认 |
| `EARS / requirement` | `Verifiable / Measurable / Explicit Conditions / Pattern Conformance` | requirement 先看它是否满足契约层的质量特征 |

所以更稳的写法应该是：

- 不要把 `measurement` 写成 Story 的正式总框架。
- 可以把 measurement 当成 `INVEST-T = Testable` 的展开解释。
- 对 EARS / requirements，则可以把 measurement 看作 requirement quality 里 `Verifiable / Measurable` 的一部分，而不是全部。

## 证据强度怎么判断

这份附录不只是列链接，还要帮你判断“哪类说法能说多满”。很多 reader-facing 文档的问题，不是完全没来源，而是把不同强度的来源说成了同一种结论。

### 一张最实用的证据分层表

| 证据层级 | 典型来源 | 适合支撑什么 | 不适合支撑什么 |
| --- | --- | --- | --- |
| `official normative` | 标准正文、正式规范正文、官方 reference | 对对象边界、定义、机制做较强断言 | 不能替代本地解释与项目决策 |
| `official scope / product page` | 标准目录页、官方产品页、官方 feature 介绍页 | 说明某对象存在、定位是什么、官方把它放在哪个问题域 | 不能做 clause-level 或细语义断言 |
| `official guide / presentation` | 官方 docs、官方教程、官方 webinar、官方 best practices | 说明推荐做法、发现机制、文件分层、工作流意图 | 不该被写成跨所有工具的统一规范 |
| `supported inference` | 多份官方或高可信材料拼起来的交叉判断 | 支撑“整体趋势”“较稳实践模式”“合理对象边界” | 不该写成单条原文直述或成熟标准共识 |
| `case / ecosystem signal` | 单个工具、单个框架、单篇实践案例 | 说明某种工作流方向已经可见 | 不该直接推广成行业统一语义 |

### 这套分层怎么在本报告里用

如果一个说法只拿到了产品页或目录页支持，那么最稳的写法通常是“这是一个官方 scope / positioning anchor”，而不是“标准明确要求你必须这样做”。

如果一个说法来自官方 guide，那么你可以说“官方文档表明该工具采用这种发现或分层机制”，但不该说“所有 agent 工具都按同一机制工作”。

如果一个判断是从多份官方材料拼出来的，例如“team context 更适合放稳定约束，feature 细节更适合放到 feature workflow”，那它通常属于 `supported inference`。这种说法可以成立，但最好明确它是综合判断，而不是单条原文逐字断言。

## 风险标签与表达边界

这组标签不是给读者增加术语负担，而是帮助你判断某个结论的“稳到什么程度”。

| 标签 | 应怎样理解 |
| --- | --- |
| `official-scope-supported` | 有官方目录页、范围说明或官方文档支持该结论的对象定位 |
| `official-presentation-supported` | 有官方演示、讲解或 summary 层材料支持该结论 |
| `supported inference` | 多份官方或高可信材料共同支持的合理推论，不是单条原文逐字结论 |
| `trend signal` | 看得到趋势存在，但还不该说成成熟共识 |
| `full-text-pending` | 方向和对象定位有官方锚点，但缺少可公开取得的正文条款支持 |
| `case-claim only` | 只来自个案或单个公开案例，不能直接普遍化 |

### 证据标签与常见说法的对应方式

| 如果你想说 | 更合适的标签 | 为什么 |
| --- | --- | --- |
| `29148` 是 requirements engineering 的官方锚点 | `official-scope-supported` | 官方页能支撑对象与范围定位 |
| `GtWR` 可作为 requirement 写作质量的 practitioner 入口 | `official-presentation-supported` | 公开可得更多是产品页、webinar、summary 级材料 |
| `AGENTS.md` / `CLAUDE.md` / steering 文件都在承担 team or workspace context 角色 | `supported inference` | 多个官方文档共同支持这一分层趋势，但工具语义并不完全相同 |
| feature `spec / plan / tasks` 或 `requirements / design / tasks` 正在成为常见工作流形态 | `supported inference` 或 `trend signal` | 多个官方工具与框架都出现此方向，但不等于跨工具标准已经统一 |
| 某个工具对 `AGENTS.md` 的发现顺序、覆盖规则、文件位置有精确定义 | `official-guide-supported` 的实质用法，本文可归入 `official-presentation-supported` | 这类说法适合限定在该工具自己的官方文档范围内 |

### 这份报告中几个最重要的边界

| 主题 | 更稳的写法 | 不该写成什么 |
| --- | --- | --- |
| `29148` | requirements engineering 的 scope / lifecycle 锚点 | 不该写成已经掌握其全部 clause-level 条文 |
| `GtWR` | 需求质量与写法规则的 practitioner 锚点 | 不该和 29148 混写成同一层对象 |
| `EARS` | 强契约层写法 | 不该写成所有项目和复杂度下都最优的万能格式 |
| `Gherkin` | 验证层场景表达 | 不该写成需求本体的统一替代物 |
| `AGENTS.md` | adoption candidate / team context 文件 | 不该写成跨工具语义已经完全一致 |
| `feature spec workflow` | 官方工具中已经存在的工作流方向 | 不该写成所有团队都必须采用完整链条 |

## agent context file 的官方锚点怎么读

这一节专门补前面几份文档里经常被一句带过、但其实最容易被误读的部分：`AGENTS.md`、`CLAUDE.md`、Kiro steering 到底属于什么对象。

### 三个官方入口分别告诉了我们什么

| 工具 / 入口 | 官方明确支持的说法 | 更稳的归纳 |
| --- | --- | --- |
| OpenAI Codex `AGENTS.md` guide | Codex 会在启动时读取 `AGENTS.md`，并按 global -> project root -> 当前目录的链式方式拼接指导；更近目录的文件会覆盖更早指导 | `AGENTS.md` 在 Codex 里是一个明确的 instructions discovery 机制，适合承载可继承的工作约束和项目级上下文 |
| Claude Code memory / `CLAUDE.md` docs | Claude Code 读取 `CLAUDE.md` 与 `CLAUDE.local.md`；这些文件是 persistent instructions，按目录层级加载，还可配合 `.claude/rules/` 做 path-scoped rules | Claude 生态把 team / project context 做成 `CLAUDE.md` 家族与 rules 机制，而不是直接把 `AGENTS.md` 当原生入口 |
| Kiro steering docs | Kiro 提供 workspace / global steering，支持 foundational steering files；同时支持 `AGENTS.md`，但说明它不支持 inclusion modes 且总是被包含 | Kiro 把长期上下文放在 steering 体系中，同时兼容 `AGENTS.md` 标准作为一个输入面 |

这三组材料共同支持一个很重要的结论：不同工具都承认“长期共享上下文文件”有价值，但它们的原生文件名、发现顺序、覆盖机制和作用域并不相同。

所以更稳的写法应该是：

- 可以说 `AGENTS.md` / `CLAUDE.md` / steering files 都是在承载 team、repo 或 workspace 级共享上下文。
- 可以说不同工具越来越倾向于把长期约束与 feature 细节分层。
- 不能说这些工具已经在文件语义、优先级和加载机制上完全统一。

### 为什么这会影响本报告的结论边界

这正是为什么正文里把 `agent context file` 定义成一个“对象层概念”，而不是把某个单一文件名当成跨工具标准。对读者真正重要的，不是记住各家文件名，而是理解下面这条更稳的分层原则：

- team / repo / workspace 级文件更适合放稳定约束、共享工作方式、代码库导航和长期规则
- feature 级目标、边界、异常路径、任务分解和验证链更适合放在 feature workflow 工件里

这条原则有较强的官方与生态支持，但它仍然应该被写成 `supported inference`，而不是“已经被所有平台标准化”。

## 进一步阅读建议

如果你想继续往下钻，可以按问题来选读。

| 你的问题 | 建议先读 |
| --- | --- |
| 什么叫 requirement 的官方生命周期锚点 | `29148` 官方页 |
| 怎样判断 requirement 写得更清楚、可测、可审查 | `GtWR` 官方入口 |
| 复杂决策逻辑什么时候该脱离 EARS | `OMG DMN` |
| acceptance criteria、tests、Gherkin、BPMN/DMN 怎样连起来 | `ISTQB Acceptance Testing Syllabus` |
| `AGENTS.md`、`CLAUDE.md`、steering 文件分别是什么 | OpenAI Codex guide、Claude Code docs、Kiro Steering |
| feature spec workflow 现在有哪些官方形态 | `Kiro`、`Spec Kit`、`OpenSpec` |

最后再强调一次：附录的目标不是让你多看链接，而是帮助你在需要时找到更权威的落点。真正要读懂这套报告，前面的主文档和示例手册已经应该足够成立。
