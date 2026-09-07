## 11. 质量价值流模型

根据补充的“质量价值流”图，TQM 不只是职能分工，而是一条从客户需求到客户体验，再回流到下一轮策划的端到端价值流。

### 11.1 质量价值流的定义

质量价值流（Quality Value Stream）是指：

> 将客户和内部需求转化为质量目标、设计要求、供应商能力、制造控制和售后体验，并通过问题反馈、根因分析和经验回溯持续提升下一轮产品质量的完整流动过程。

其核心不是“完成了多少质量活动”，而是“质量价值是否沿产品生命周期持续传递”。

### 11.2 正向策划价值流：PQA 端到端质量

```text
内部 / 外部客户需求
        ↓
项目质量
        ↓
研发质量
        ↓
供应商质量
        ↓
制造质量
        ↓
售后质量
        ↓
客户体验 / 质量结果
```

对应本体对象：

```text
CustomerRequirement
→ ProjectQualityPlan
→ RnDQualityPlan
→ SupplierQualityPlan
→ ManufacturingQualityPlan
→ AfterSalesQualityPlan
→ CustomerQualityOutcome
```

对应流程能力：

| 价值流环节 | 对应能力 | 核心产出 |
|---|---|---|
| 客户需求 | 需求识别与质量目标 | CustomerRequirement、QualityObjective |
| 项目质量 | 2.15.1.1 管理质量策略 | ProjectQualityPlan、QualityTarget |
| 研发质量 | 2.15.1.2 管理开发过程质量保证 | DesignRequirement、VerificationPlan |
| 供应商质量 | APQP / PPAP、零件质量管理 | SupplierApproval、PartApproval |
| 制造质量 | 2.15.1.3 质量安全控制与验证 | ProcessControl、QualityGate、ReleaseDecision |
| 售后质量 | 2.15.1.4 生命周期质量安全运营 | FieldQualityEvent、ServiceAction |
| 客户结果 | 质量体验和结果评价 | CustomerFeedback、QualityOutcome |

### 11.3 逆向改进价值流：QTR 问题闭环

```text
客户抱怨 / 云端监控预警
        ↓
质量反馈及预分析
        ↓
根因分析及处置方案
        ↓
质量回溯
        ↓
经验沉淀与预防再发
        ↓
回流到客户需求、设计、供应链和制造策划
```

对应本体对象：

```text
CustomerComplaint / CloudMonitoringAlert
→ QualityFeedback
→ TriageAssessment
→ RootCauseAnalysis
→ TreatmentPlan
→ TracebackRecord
→ LessonsLearned
→ PreventiveAction
```

这条逆向链将“问题处理”提升为“组织学习”：

- 当前问题得到遏制；
- 根因被定位并验证；
- 影响范围被追溯；
- 经验被写入标准、FMEA、设计规范和控制计划；
- 下一轮产品和流程获得预防性改进。

### 11.4 IVDP 生命周期质量门

图中以 IVDP 生命周期为主线，列出了以下质量阶段：

```text
IVDP 生命周期
→ G9 K0
→ G8 PI
→ G7 PA / G6 CSO
→ G5 ER
→ G4 PPV
→ G3 PP / G2 P
→ G1 SOP / EOP
```

由于不同企业对阶段缩写的定义可能不同，建议将缩写作为企业配置项保存，同时为每个质量门建立统一结构：

```yaml
QualityGate:
  gateCode: G5
  lifecycle: IVDP
  phaseName: ER
  entryCriteria: []
  requiredDeliverables: []
  qualityMetrics: []
  openRisks: []
  decision: PASS / CONDITIONAL_PASS / FAIL
  approver: Person
  evidence: ComplianceEvidence
```

每个质量门都应回答：

1. 进入该阶段需要什么输入？
2. 必须完成哪些质量活动和验证？
3. 哪些风险可以接受，哪些风险必须关闭？
4. 谁拥有放行或否决权？
5. 放行结论由哪些证据支持？
6. 不通过时如何创建问题和改进任务？

### 11.5 质量价值流中的横向支撑

质量工程和质量体系不直接替代正向或逆向流程，而是为整个价值流提供横向支撑。

```text
质量工程：方法、工具、系统、设备、人员能力、度量与解析
质量体系：政策、法规、标准、审核、战略解码、问题分级
```

它们应与每个价值流节点建立支撑关系：

```text
QualityMethod ── supports ──▶ QualityActivity
QualityTool ── supports ──▶ QualityAnalysis
QualitySystem ── records ──▶ QualityEvidence
QualityStandard ── constrains ──▶ QualityGate
QualityAudit ── verifies ──▶ QualityProcess
```

### 11.6 价值流对象模型

建议新增一个 `QualityValueStream` 对象，统一管理价值流实例：

```yaml
QualityValueStream:
  key: valueStreamId
  properties:
    - productProgram
    - vehicleModel
    - lifecycle
    - startStage
    - currentStage
    - targetCustomerOutcome
    - overallQualityStatus
    - owner
```

同时增加 `ValueStreamStage`：

```yaml
ValueStreamStage:
  key: stageId
  properties:
    - stageCode
    - stageName
    - sequence
    - plannedStart
    - plannedEnd
    - actualStart
    - actualEnd
    - status
    - qualityGateDecision
```

关键关系：

```text
QualityValueStream ── hasStage ──▶ ValueStreamStage
ValueStreamStage ── governedBy ──▶ QualityGate
ValueStreamStage ── produces ──▶ QualityEvidence
QualityProblem ── interrupts ──▶ ValueStreamStage
LessonsLearned ── improves ──▶ QualityValueStream
```

### 11.7 质量价值流指标

质量价值流应同时衡量流动速度、质量结果和改进效果。

#### 流动效率

```text
质量门按期完成率
质量问题平均流转时间
等待审批时间占比
跨部门交接次数
问题从发现到遏制的时间
```

#### 质量结果

```text
质量门一次通过率
研发遗留问题数
供应商批次不良率
制造一次合格率
售后早期故障率
重大安全问题数
```

#### 闭环与学习

```text
根因确认周期
纠正措施按期完成率
措施有效率
重复问题率
经验回流覆盖率
质量改进收益
```

### 11.8 价值流案例：新车型电池系统质量改进

```text
客户提出更高续航和安全需求
  ↓
项目质量定义续航、安全和可靠性目标
  ↓
研发建立电池系统设计要求和验证计划
  ↓
供应商完成电芯和电池包 APQP / PPAP
  ↓
制造建立关键扭矩、绝缘和气密质量控制
  ↓
质量门完成 PPV、试生产和量产放行
  ↓
售后收集故障码、维修记录和用户反馈
  ↓
QTR 发现某批次电芯异常
  ↓
追溯影响车辆、供应商、工厂和设计版本
  ↓
执行批次遏制、软件修复和供应商整改
  ↓
将根因和措施回写 FMEA、设计规范和控制计划
  ↓
下一轮项目质量策划吸收经验
```

### 11.9 Palantir Ontology 映射

| 质量价值流概念 | Palantir Ontology 实现 |
|---|---|
| 价值流、阶段、质量门 | Object Type |
| 阶段状态、质量目标、门禁结论 | Property |
| 阶段包含质量门、问题影响阶段 | Link Type |
| 价值流进度、风险和指标计算 | Function |
| 放行、冻结、遏制、整改、关闭 | Action Type |
| 标准、证据、审核记录 | Object + Evidence |
| 角色、区域、项目和安全关键权限 | Security |

价值流在 Palantir Ontology 中的重点是把“流程阶段”与“实物对象、质量事实、决策行动”连接起来，而不是只做项目进度看板。

## 12. 价值流建模原则

1. **以客户结果为终点**：每一阶段都要说明最终为客户创造什么质量价值。
2. **以生命周期为主线**：设计、供应链、制造和售后共享同一产品和实物追溯链。
3. **正向策划与逆向改进必须相连**：问题经验要回流到下一轮计划、设计和标准。
4. **质量门是决策点，不是打卡点**：必须具备准入条件、证据、风险和明确决策。
5. **将等待和返工显式建模**：质量价值流不仅记录完成活动，还要识别停滞、重复和返工。
6. **区分价值活动与支撑活动**：PQA/QTR 是主要价值流，质量工程和质量体系提供横向能力。
7. **每个重大节点必须可执行**：发现风险后应能触发遏制、升级、整改、复验或放行行动。

---

