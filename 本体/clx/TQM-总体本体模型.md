# TQM（全面质量管理）业务流程本体模型

## 1. 建模依据与目标

本文根据所给业务流程图进行抽象。图中层级为：

```text
L1：2 IPD
└── L2：2.15 质量管理
    ├── L3：2.15.1 管理 PQA 产品端到端质量
    ├── L3：2.15.2 管理 QTR 问题解决及回溯
    ├── L3：2.15.3 管理质量工程
    └── L3：2.15.4 管理质量体系
```

本体模型的目标不是复制流程图，而是把流程中的**业务能力、对象、关系、规则、指标和行动**结构化，使其可用于流程治理、质量数据平台、知识图谱、AI 助手或 Palantir Ontology 建模。

## 2. 一分钟理解

TQM 质量管理本体可以概括为：

```text
质量战略定义方向
  → PQA 管理产品端到端质量
  → QTR 管理问题闭环和经验回溯
  → 质量工程提供工具、系统、设备和能力
  → 质量体系提供法规、标准、审核和治理
```

核心闭环是：

```text
质量要求 → 产品开发 → 生产交付 → 问题发现
    ↑                              ↓
    └──── 根因分析、纠正、回溯、改进 ────┘
```

## 3. 顶层本体结构

### 3.1 顶层概念

```text
QualityManagementDomain
├── QualityStrategy              质量战略
├── ProductQuality               产品质量
├── QualityProblem               质量问题
├── QualityEngineering           质量工程
├── QualitySystem                质量体系
├── QualityRequirement           质量要求
├── QualityEvidence              质量证据
├── QualityRisk                  质量风险
├── CorrectiveAction             纠正措施
└── QualityMetric                质量指标
```

### 3.2 与 IPD 的关系

质量管理不是 IPD 之外的独立环节，而是贯穿需求、设计、开发、验证、试产、量产和上市后的质量控制能力。

```text
IPDPhase
├── Concept
├── Planning
├── Development
├── Validation
├── PilotProduction
├── MassProduction
└── LifecycleOperation
```

每个 IPD 阶段都可以关联质量门、质量目标、风险、评审和放行决策。

## 4. L3 领域模型

### 4.1 2.15.1 管理 PQA 产品端到端质量

PQA 表示围绕产品全生命周期管理质量，关注“产品从需求到交付及运营是否满足质量目标”。

核心对象：

```text
ProductQualityPlan       产品质量策划
QualityObjective         质量目标
QualityGate               质量门
DesignQualityReview       设计质量评审
DevelopmentQualityCheck  开发过程质量检查
ValidationActivity       验证活动
ReleaseDecision           放行决策
LifecycleQualityRecord    生命周期质量记录
QualitySpecialProject     质量专项
```

图中 L4 能力映射：

| 编号 | 能力 | 建议本体对象 |
|---|---|---|
| 2.15.1.1 | 管理质量策略 | QualityStrategy、QualityObjective |
| 2.15.1.2 | 管理开发过程质量保证 | DevelopmentQualityCheck、QualityGate |
| 2.15.1.3 | 管理质量安全控制与验证 | SafetyControl、VerificationActivity |
| 2.15.1.4 | 管理全生命周期质量安全运营 | LifecycleQualityRecord、FieldQualityEvent |
| 2.15.1.5 | 管理质量专项 | QualitySpecialProject、SpecialTask |

关键关系：

```text
Product ── governedBy ──▶ ProductQualityPlan
ProductQualityPlan ── hasGate ──▶ QualityGate
QualityGate ── evaluates ──▶ Product / Deliverable
QualityGate ── produces ──▶ ReleaseDecision
Product ── hasLifecycleRecord ──▶ LifecycleQualityRecord
```

### 4.2 2.15.2 管理 QTR 问题解决及回溯

QTR 领域负责将质量问题从发现、分级、遏制、分析、整改、验证一直闭环到经验回溯。

核心对象：

```text
QualityProblem          质量问题
ProblemReport           问题报告
ProblemClassification   问题分类
ContainmentAction       遏制措施
RootCauseAnalysis       根因分析
CorrectiveAction        纠正措施
PreventiveAction        预防措施
VerificationResult      效果验证
TracebackRecord         问题回溯记录
LessonsLearned          经验教训
CloudMonitoringAlert    云端监控预警
IntelligentDrivingEvent 智能驾驶云安全事件
UserSafetyCase          用户安全事件
```

图中 L4 能力映射：

| 编号 | 能力 | 建议本体对象 |
|---|---|---|
| 2.15.2.1 | 管理质量反馈及预分析 | Feedback、TriageAssessment |
| 2.15.2.2 | 管理根因分析及处置方案 | RootCauseAnalysis、TreatmentPlan |
| 2.15.2.3 | 管理质量回溯 | TracebackRecord、AffectedScope |
| 2.15.2.4 | 管理云端监控预警 | CloudMonitoringAlert、AlertRule |
| 2.15.2.5 | 管理智能驾驶云端安全接管 | TakeoverEvent、SafetyIntervention |
| 2.15.2.6 | 管理用户安全及案件 | UserSafetyCase、CaseInvestigation |

问题状态建议统一为：

```text
发现 → 受理 → 分级 → 遏制中 → 分析中 → 整改中 → 验证中 → 关闭 → 回溯复用
```

### 4.3 2.15.3 管理质量工程

质量工程提供质量管理所需的方法、工具、系统、设备、人员能力和度量分析。

核心对象：

```text
QualityMethod          质量方法
QualityTool            质量工具
QualitySystem          质量系统
QualityDevice          质量设备
QualityEngineer        质量人员
CompetencyRequirement  能力要求
TrainingRecord         培训记录
MeasurementSystem      测量系统
QualityMetric          质量度量
AnalyticsModel         质量分析模型
```

图中 L4 能力映射：

| 编号 | 能力 | 建议本体对象 |
|---|---|---|
| 2.15.3.1 | 管理质量工具 | QualityTool、QualityMethod |
| 2.15.3.2 | 管理质量成本 | QualityCost、CostEvent |
| 2.15.3.3 | 管理质量系统 | QualitySystem、SystemInterface |
| 2.15.3.4 | 管理质量设备 | QualityDevice、CalibrationRecord |
| 2.15.3.5 | 管理质量人员能力 | QualityEngineer、Competency、TrainingRecord |
| 2.15.3.6 | 管理质量度量及解析 | QualityMetric、AnalyticsModel、Dashboard |

### 4.4 2.15.4 管理质量体系

质量体系负责将法规、标准、审核、战略解码和问题等级转化为组织可执行的制度和控制要求。

核心对象：

```text
Regulation              法规
QualityStandard         质量标准
QualityPolicy           质量政策
QualityAudit            质量审核
AuditFinding            审核发现
QualityStrategy         质量战略
StrategyObjective       战略目标
QualityRequirement      质量要求
ProblemSeverityLevel    问题等级
ComplianceEvidence      合规证据
```

图中 L4 能力映射：

| 编号 | 能力 | 建议本体对象 |
|---|---|---|
| 2.15.4.1 | 管理政策法规研究 | Regulation、PolicyResearch |
| 2.15.4.2 | 管理质量安全体系 | QualitySafetySystem、Control |
| 2.15.4.3 | 管理质量审核 | QualityAudit、AuditFinding |
| 2.15.4.4 | 管理质量战略与解码 | QualityStrategy、StrategyObjective |
| 2.15.4.5 | 管理质量标准 | QualityStandard、StandardRequirement |
| 2.15.4.6 | 管理问题等级定义 | ProblemSeverityLevel、EscalationRule |

## 5. 跨域关系模型

```text
QualityRequirement ── constrains ──▶ Product
QualityRequirement ── derivedFrom ──▶ Regulation / QualityStandard
Product ── hasQualityPlan ──▶ ProductQualityPlan
ProductQualityPlan ── evaluatedBy ──▶ QualityGate
QualityProblem ── affects ──▶ Product / Process / Customer
QualityProblem ── detectedBy ──▶ Inspection / Monitoring / Complaint
QualityProblem ── managedBy ──▶ QTRCase
QTRCase ── contains ──▶ RootCauseAnalysis
QTRCase ── creates ──▶ CorrectiveAction
CorrectiveAction ── verifiedBy ──▶ VerificationResult
QualityTool ── supports ──▶ QualityProcess
QualityMetric ── measures ──▶ QualityProcess / Product / Supplier
QualityAudit ── verifies ──▶ QualitySystem / QualityProcess
```

## 6. 关键质量对象定义

### QualityProblem

```yaml
QualityProblem:
  key: problemId
  properties:
    - title
    - description
    - source
    - severity
    - occurrenceTime
    - discoveryTime
    - status
    - affectedScope
    - owner
    - dueDate
```

### QualityGate

```yaml
QualityGate:
  key: gateId
  properties:
    - gateType
    - ipdPhase
    - entryCriteria
    - exitCriteria
    - decision
    - approver
    - decisionTime
```

### CorrectiveAction

```yaml
CorrectiveAction:
  key: actionId
  properties:
    - actionType
    - owner
    - plannedDate
    - completedDate
    - effectivenessStatus
    - evidence
```

### QualityMetric

```yaml
QualityMetric:
  key: metricId
  properties:
    - name
    - definition
    - formula
    - unit
    - targetValue
    - threshold
    - frequency
    - owner
```

## 7. 端到端业务案例：动力电池异常

### 7.1 问题发现

云端监控发现某车型出现高压电池异常告警，售后系统同时收到多起用户投诉。

```text
CloudMonitoringAlert
  → QualityProblem
  → Vehicle
  → BatteryPack
  → PartBatch
  → Supplier
```

### 7.2 QTR 闭环

```text
1. 质量人员受理问题
2. 按用户安全影响将问题定为高等级
3. 冻结相关零件批次和在制车辆
4. 分析供应商、批次、工厂和软件版本
5. 制定来料加严、软件修复和售后检查方案
6. 验证整改效果
7. 评估是否需要服务活动或召回
8. 将根因和措施回写到 FMEA、设计规范和质量标准
```

### 7.3 本体中的关键行动

```text
CreateQualityProblem
ClassifyProblemSeverity
StartContainment
TraceAffectedVehicles
ApproveCorrectiveAction
VerifyEffectiveness
UpdateQualityStandard
LaunchServiceCampaign
```

### 7.4 质量安全规则示例

```text
如果问题涉及人身安全，则不得自动关闭
如果同一批次在多个工厂出现同类问题，则升级为供应链问题
如果质量门未通过，则车辆不能放行
如果纠正措施没有验证证据，则问题不能关闭
如果设计变更影响安全目标，则必须重新进行验证
```

## 8. 指标体系

### PQA 指标

```text
质量门一次通过率
开发阶段缺陷发现率
量产前遗留问题数
产品生命周期重大问题数
设计变更引入缺陷率
```

### QTR 指标

```text
问题响应时间
问题闭环周期
重复问题率
根因确认周期
措施按期完成率
整改有效率
高等级问题升级及时率
```

### 质量工程指标

```text
测量系统合格率
设备校准及时率
质量工具使用覆盖率
质量数据完整率
人员能力达标率
质量分析模型准确率
```

### 质量体系指标

```text
审核问题关闭率
法规要求覆盖率
标准更新及时率
质量体系成熟度
质量战略目标达成率
```

## 9. 在 Palantir Ontology 中的实现建议

如果将该模型落地到 Palantir Ontology，可采用如下映射：

| TQM 模型 | Palantir Ontology |
|---|---|
| 质量问题、质量门、审核、纠正措施 | Object Type |
| 问题状态、严重度、质量目标 | Property |
| 问题影响车辆、零件、供应商 | Link Type |
| 问题预分析、影响范围分析、指标计算 | Function |
| 冻结批次、批准放行、启动遏制、关闭问题 | Action Type |
| 质量标准、审核证据、整改证明 | Object + Evidence |
| 部门、角色、区域、问题等级权限 | Security Policy |

关键设计原则是：

```text
事实对象与判断结果分离
质量问题与行动分离
推荐结果与审批执行分离
安全关键问题与普通问题分级治理
```

## 10. 建模边界与后续工作

本文是依据流程图建立的业务本体蓝图，不等于某家企业已经认证的质量体系，也不替代其质量手册、法规符合性评估或实际 QMS 流程。

实际落地前还需要补充：

- 企业现有流程、角色和审批链；
- ERP、PLM、MES、QMS、CRM 和云监控系统字段映射；
- 质量标准和法规条款编号；
- 问题等级、升级阈值和关闭条件；
- 车辆、零件、批次、软件版本的追溯主键；
- 审核、验证和召回所需的证据模型；
- 各质量指标的正式公式、口径和数据负责人。

## 总结

TQM 本体模型把流程图中的四个能力域统一为一个质量决策系统：

```text
PQA 管产品全生命周期质量
QTR 管问题解决、回溯和改进
质量工程提供方法、工具、系统和能力
质量体系提供法规、标准、审核和治理
```

最终形成的不是一张静态流程图，而是一套能够回答以下问题的业务模型：

> 什么质量问题发生了？影响什么实物？为什么发生？谁负责处理？采取了什么行动？如何验证有效？经验如何回流到设计、供应链、制造和质量体系？

---

