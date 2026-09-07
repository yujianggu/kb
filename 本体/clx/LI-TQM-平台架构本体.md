## 13. LI-TQM 全面质量管理平台本体

补充架构图展示了一个以 IVDP 生命周期和质量价值流为主线的 LI-TQM 平台。图中标题标注为“17 个质量系统 + 12 个低码应用”，本文将其抽象为平台能力，不将图中名称直接等同于某个已验证的产品清单。

### 13.1 平台分层

```text
生命周期层：IVDP
  G9 K0 → G8 PI → G7 PA / G6 CSO → G5 ER → G4 PPV
  → G3 PP / G2 P → G1 SOP / EOP

价值流层：
  主价值流（质量控制）：项目质量 → 研发质量 → 供应商质量 → 制造质量 → 售后质量
  主价值流（质量改进）：QTR 问题到解决、回溯和经验沉淀

应用层：质量系统、质量专项、问题闭环、AI 质量专家和低码应用

能力层：用户管理、权限管理、流程中心、DSC、帆软、PB、飞书工作台等基础能力
```

其中：

- 生命周期层回答“质量活动处于产品开发和运营的哪个阶段”；
- 价值流层回答“质量价值如何向前流动、如何从问题向后改进”；
- 应用层承载具体质量管理场景；
- 能力层提供身份、流程、数据、报表、低码和协同基础设施。

### 13.2 平台对象模型

建议新增以下平台级对象：

```text
QualityPlatform           质量管理平台
QualityApplication        质量应用
LowCodeApplication        低码应用
PlatformCapability        平台基础能力
LifecycleStage            生命周期阶段
QualityValueStream        质量价值流
QualitySystemInterface    系统接口
DataAsset                 数据资产
WorkflowDefinition        流程定义
AIQualityExpert           AI 质量专家
```

关键关系：

```text
QualityPlatform ── contains ──▶ QualityApplication
QualityApplication ── supports ──▶ QualityValueStream
QualityApplication ── operatesAt ──▶ LifecycleStage
QualityApplication ── uses ──▶ PlatformCapability
QualityApplication ── consumes ──▶ DataAsset
QualityApplication ── executes ──▶ WorkflowDefinition
QualityApplication ── integratesWith ──▶ QualitySystemInterface
AIQualityExpert ── invokes ──▶ QualityApplication / Function / Action
```

## 14. 应用层系统模型

### 14.1 PQA 主价值流应用

图中位于“PQA 端到端质量控制”区域的应用，主要支撑项目、研发、供应商、制造和售后质量。

| 应用 / 系统 | 主要能力 | 对应质量域 |
|---|---|---|
| QOM 质量目标管理系统 | 指标库、目标制定、目标分解、SOP 质量目标管理 | 项目质量 / 质量体系 |
| TPQM 试制质量管理系统 | 一车一档、任务管理、试制问题、来料和质量门管理 | 研发质量 |
| SQM 供应商质量管理系统 | 来料检验、供应商审核、QR/CR、供应商年度评审 | 供应链质量 |
| COP 质量一致性管理系统 | 过程一致性、关键特性审核、物料和颜色一致性 | 制造质量 |
| AQMS 售后质量管理系统 | 保修索赔、售后问题、IPTV/CPV、故障预测、VOC | 售后质量 |
| QKM 质量知识管理系统 | 质量知识管理与知识查询 | 质量工程 / 质量体系 |
| FMEA 失效控制管理系统 | DFMEA、PFMEA、风险管理、失效和经验库 | 设计质量 / 制造质量 |
| VAS 供应链质量外援管理系统 | 人厂流程、任务、绩效和行为管理 | 供应链质量 |
| QCAS 质量专项系统 | 专项清单、风险、模板、供应商协作和专项任务 | 质量专项 |
| QLM 质量标签管理系统 | 质量标签管理和标签类别 | 质量数据 / 制造质量 |
| MMDS 尺寸测量管理系统 | 设备、测量报告、数据分析、预警、人员和系统管理 | 质量工程 |
| PCS 零部件索赔管理系统 | 售后保修索赔、手工索赔、云仓和物流索赔 | 售后质量 / 供应链质量 |
| MES 制造执行系统 | 在线检验、设备采集、质量缺陷、返工返修、质量门和证书打印 | 制造质量 |
| QCAS 质量活动管理系统 | 工厂端技术升级、车身绑定、升级流程和查询 | 制造质量 / 售后质量 |
| USS 无人移动智能调度系统 | 检测车、Care 车、路试车、VDC 车和 JPH 工位调度 | 质量工程 / 制造质量 |

图中部分系统名称或能力可能存在企业内部缩写，落地时应为每个系统补充系统负责人、数据负责人、接口、SLA 和正式定义。

### 14.2 QTR 问题解决应用

QTR 区域由问题闭环和智能辅助两类能力构成。

#### PQCP 质量问题管理系统

```text
待办中心
流程角色管理
问题权限管理
流程模板配置
实车类问题管理
问题查询
问题类型配置
字典值管理
自定义问题管理
设计类问题管理
```

建议建模为：

```text
PQCP ── manages ──▶ QualityProblem
QualityProblem ── classifiedBy ──▶ ProblemType
QualityProblem ── assignedTo ──▶ Role / Person
QualityProblem ── follows ──▶ WorkflowDefinition
QualityProblem ── has ──▶ PermissionPolicy
```

#### AI 质量专家（图中标注 Qivis）

图中列出的能力包括：

```text
AI 降噪
数据互联
能力集成
知识提炼
Skill 生成
工单轨迹
工单聚类
Benchmark 评测
数据集拆分
发布生效
```

建议将 AI 质量专家建模为受治理的 `AIQualityExpert`，而不是普通聊天机器人：

```yaml
AIQualityExpert:
  key: expertId
  properties:
    - name
    - modelVersion
    - promptVersion
    - allowedDataScopes
    - allowedTools
    - approvalMode
    - evaluationStatus
    - publishedAt
```

AI 质量专家可执行的典型 Function：

```text
deduplicateQualityProblems
clusterSimilarProblems
extractRootCauseCandidates
retrieveLessonsLearned
evaluateBenchmark
```

可调用的 Action 必须单独授权，例如：

```text
CreateProblemDraft
AssignProblemOwner
RecommendContainment
SubmitRootCauseAnalysis
PublishQualityKnowledge
```

AI 的推荐和正式行动应保持分离：AI 可以形成草稿或建议，但涉及停线、冻结批次、车辆放行和召回的动作必须经过明确的权限和审批。

#### QWO 质量工单系统

QWO 为问题解决提供基础工单能力：

```text
工单类型管理
快捷指令管理
售后质量工单管理
生产质量工单管理
供应链工单管理
第三方数据记录
海外质量工单
海外 DMS / ERP 集成
```

其本体对象可以包括：

```text
QualityWorkOrder
WorkOrderType
WorkOrderInstruction
WorkOrderAssignment
ExternalDataRecord
```

### 14.3 JIRA 与外部协作

图中 JIRA 位于 QTR 应用区域，可作为研发或跨团队问题协作工具。建议不要将 JIRA 问题直接当作质量问题本体，而是建立映射：

```text
QualityProblem ── synchronizedWith ──▶ JiraIssue
JiraIssue ── contains ──▶ JiraTask
```

质量本体保留问题等级、影响范围、根因、质量行动和关闭证据；JIRA 保留研发执行任务和开发协作状态。

## 15. 价值流与平台应用的映射

```text
客户需求 / 项目质量
  → QOM、QKM、质量专项

研发质量 / 试制验证
  → TPQM、FMEA、MMDS、PCS

供应商质量 / 零件质量
  → SQM、VAS、QCAS、FMEA

制造质量 / 质量安全控制
  → COP、MES、QLM、MMDS、USS

售后质量 / 生命周期运营
  → AQMS、PCS、QWO、云监控

QTR 问题闭环
  → PQCP、QWO、AI 质量专家、JIRA

质量体系与基础能力
  → 标准、审核、权限、流程中心、报表和协同平台
```

同一个质量对象应尽量跨系统复用统一主键：

```text
Vehicle VIN
Part Number / Revision
Supplier ID
Batch / Serial Number
QualityProblem ID
QualityWorkOrder ID
Design / Software Version
```

## 16. 平台级业务流程示例

### 电池包质量问题闭环

```text
1. AQMS 收到售后故障和用户投诉
2. 云端监控产生预警
3. PQCP 创建 QualityProblem
4. AI 质量专家进行降噪、聚类和相似问题检索
5. QWO 分派责任人和处理任务
6. SQM 查询供应商和批次质量记录
7. MES 查询生产工位、过程参数和质量门结果
8. FMEA 查询相关失效模式和已有控制措施
9. 质量工程师完成根因分析和遏制方案
10. 主管审批冻结批次或启动售后服务活动
11. 验证整改效果并关闭问题
12. 将经验回写知识库、FMEA、设计规范和质量标准
```

### 关键本体关系

```text
CustomerComplaint ── creates ──▶ QualityProblem
QualityProblem ── analyzedBy ──▶ AIQualityExpert / QualityEngineer
QualityProblem ── trackedBy ──▶ QualityWorkOrder
QualityProblem ── affects ──▶ Vehicle / Part / Batch / Supplier
QualityProblem ── references ──▶ FailureMode
QualityProblem ── resultsIn ──▶ CorrectiveAction
CorrectiveAction ── verifiedBy ──▶ VerificationResult
VerificationResult ── updates ──▶ FMEA / QualityStandard / KnowledgeRecord
```

## 17. 平台治理要求

1. **系统不是本体对象**：QOM、MES、AQMS 等是应用或数据来源，订单、车辆、问题和批次才是业务对象。
2. **统一主键优先**：跨系统追溯必须优先统一 VIN、零件号、批次号和问题号。
3. **应用能力与对象分离**：系统中的“问题查询”是能力，`QualityProblem` 是对象。
4. **AI 工具白名单化**：AI 只能调用被授权的函数、知识源和 Action。
5. **质量门必须有证据**：应用状态不能替代检验记录、审批记录和验证证据。
6. **保留系统边界**：本体统一语义，但不必把所有系统强行合并成一个数据库。
7. **跨域行动可审计**：冻结、放行、返工、升级和召回必须记录执行人、时间、依据和结果。
