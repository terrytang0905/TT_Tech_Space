# AI PM PRD 作品集（prd/）

> **创建**: 2026-07-05
> **定位**: AI 产品经理转型的 PRD 输出作品集
> **对应技能规划**: `TT_Obsidian/2-个人成长/AI产品经理技能规划_20260705.md` M2 / M6

---

## 用途

承接 AI PM 技能规划中的**PRD 输出证据**。每份 PRD 都是可 Show 的作品，用于：
- 求职作品集（简历附件）
- MBA 论文成果转化（Ch4/5/6 → 产品文档）
- Blog 拆解素材

---

## 目录结构（建议）

```
prd/
├─ README.md                    # 本文件
├─ 01-scenario-library-mvp/     # M2：跨企业脱敏场景库 MVP（论文 Ch4 4.6 素材）
│   ├─ prd.md                   # 主 PRD
│   ├─ competitive-analysis.md  # 竞品分析
│   ├─ ab-test-plan.md          # A/B Test 方案
│   └─ user-stories.md          # 用户故事
├─ 02-mmr-console/              # 后续：MMR 检索控制台产品
├─ 03-roi-dashboard/            # 后续：ROI 健康度仪表盘
└─ templates/                   # 模板复用（软链至 product-manager.skill）
```

---

## PRD 编写规范

复用你已打包好的 `workspace/TT_Tech_Space/skill/product-manager.skill`：
- `SKILL.md` — 核心方法论
- `references/PRD-TEMPLATE.md` — PRD 模板
- `references/PRD-WRITING-GUIDE.md` — 编写指南
- `references/PM-BEST-PRACTICES.md` — 最佳实践

每份 PRD 至少覆盖：
1. 背景与目标（Why）
2. 用户与场景（Who / When）
3. 需求详述（What）
4. 交互/流程/接口（How）
5. 验收标准 & 指标（Success Metrics）
6. 风险与依赖
7. 排期与里程碑

**AI PM 特有维度**（域 4 破局点）：
- 模型选型与替换方案
- 可解释性方案（SHAP/LIME 集成路径）
- 数据依赖与冷启动策略
- 幻觉/偏差应对
- 隐私合规（数据脱敏 / 主权协议）

---

## 交付节奏

| 时间 | PRD | 状态 |
|---|---|---|
| 2026-09 | 01-scenario-library-mvp | ⏳ 计划中 |
| 2026-11 | 02-mmr-console | ⏳ 计划中 |
| 2026-12 | 03-roi-dashboard | ⏳ 计划中 |
| 2027-Q1 | 04-explainability-console | ⏳ 计划中（配合 SHAP/LIME Blog） |

---

## 上游关联

- 论文素材：`TT_Obsidian/3-论文写作/docs/thesis.md`（Ch4 商业模式 / Ch5 A/B Test / Ch6 战略保障）
- 代码：`workspace/ad-testing-data-analyst/` 提供数据支撑
- 案例库：`TT_Obsidian/4-技术库/AI产品案例库/` 提供对标参照
