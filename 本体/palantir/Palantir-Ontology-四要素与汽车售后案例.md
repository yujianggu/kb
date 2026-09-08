# Palantir Ontology 的 Data、Logic、Action、Security

## 1. 先看结论

Palantir Ontology 的核心不是把汽车售后数据集中到一张表，而是把售后问题转化为可查询、可分析、可执行、可审计的决策闭环：

```text
Data      看清发生了什么
Logic     判断为什么发生、影响多大
Action    决定接下来做什么并改变业务状态
Security  确保谁能看、谁能判断、谁能执行
```

Palantir 官方将 Ontology 描述为组织的运营层，将现实世界对象与数据资产连接起来，并同时包含语义元素和行动、函数、动态安全等动力元素。[Ontology overview](https://www.palantir.com/docs/foundry/ontology/overview)

在汽车售后场景中，四者可以形成：

```text
车辆和故障数据
  → 故障分析与影响范围判断
  → 维修、遏制、服务活动或召回行动
  → 按区域、角色和安全等级执行权限控制
  → 结果回流到设计、供应商、制造和售后规则
```

## 2. 四要素总览

| 要素 | 核心问题 | Palantir 主要构件 | 汽车售后例子 |
|---|---|---|---|
| Data | 发生了什么？影响哪些对象？ | Object、Property、Link、数据源 | VIN、故障码、零件批次、维修记录 |
| Logic | 为什么发生？风险多大？ | Function、规则、模型、聚合 | 故障聚类、根因候选、影响范围分析 |
| Action | 下一步如何处理？ | Action Type、参数、规则、副作用 | 创建工单、冻结批次、启动服务活动 |
| Security | 谁能看、算、批、做？ | 对象、属性、函数、Action 权限 | 客服、经销商、质量和召回团队的权限差异 |

## 3. Data：把售后现实世界建模为对象和关系

### 3.1 核心对象

汽车售后至少需要以下对象：

```text
Vehicle                 车辆
Customer                客户
ServiceCenter           服务中心
CustomerComplaint       客户投诉
DiagnosticEvent         诊断事件
FaultCode               故障码
RepairOrder             维修工单
ReplacedPart            更换零件
PartBatch               零件批次
Supplier                供应商
SoftwareVersion         软件版本
ServiceCampaign         服务活动
RecallCase              召回案件
```

### 3.2 关键属性

```yaml
Vehicle:
  vin: "VIN1001"
  model: "Example-L7"
  deliveryDate: "2026-02-10"
  softwareVersion: "V3.2.1"
  region: "华东"

DiagnosticEvent:
  eventId: "D-9001"
  code: "HV_BATTERY_042"
  occurredAt: "2026-09-05T10:12:00+08:00"
  severity: "high"
  source: "vehicle-cloud"
```

### 3.3 关键关系

```text
Customer ── owns ──▶ Vehicle
Vehicle ── reports ──▶ DiagnosticEvent
DiagnosticEvent ── hasCode ──▶ FaultCode
Vehicle ── receives ──▶ RepairOrder
RepairOrder ── replaces ──▶ ReplacedPart
ReplacedPart ── fromBatch ──▶ PartBatch
PartBatch ── suppliedBy ──▶ Supplier
Vehicle ── runs ──▶ SoftwareVersion
```

Palantir 的 Object Type、Property 和 Link Type 用于把数据源映射成业务对象和关系，而不是让应用直接依赖原始系统的表名和字段名。[Object and link types](https://www.palantir.com/docs/foundry/object-link-types/type-reference)

### 3.4 Data 不只是静态主数据

售后 Data 还包括随时间变化的事件和证据：

```text
故障出现时间
车辆当时的软件版本
环境温度和行驶里程
服务中心诊断结果
维修前后零件状态
客户描述和图片
云端预警
```

这些数据需要关联 VIN、零件号、批次、时间和来源，否则很难进行可靠的追溯。

## 4. Logic：从售后事实形成判断

Logic 负责把分散的售后数据转化为风险、原因、优先级和建议。Palantir Function 可以读取对象、遍历链接、聚合数据、调用模型或执行复杂逻辑。[Functions overview](https://www.palantir.com/docs/foundry/functions/overview)

### 4.1 典型售后逻辑

```text
calculateFailureRisk(vehicle)
findSimilarComplaints(complaint)
findAffectedVehicles(partBatch)
clusterDiagnosticEvents(events)
rankRootCauseCandidates(problem)
calculateRecallPriority(scope)
```

### 4.2 逻辑不等于结论

函数可以产生候选判断，但应保留：

```text
输入数据
使用的规则或模型版本
计算时间
结果置信度
影响因素
人工复核状态
```

例如：

```yaml
RiskAssessment:
  riskLevel: critical
  score: 0.91
  modelVersion: battery-risk-v4
  evidence:
    - sameFaultCodeAcrossRegions
    - samePartBatch
    - repeatRepairWithin30Days
  reviewedBy: SafetyEngineer
```

### 4.3 影响范围分析

```text
PartBatch BATCH2026
  → ReplacedPart
  → RepairOrder
  → Vehicle
  → Customer / Region / DeliveryStatus
```

Function 可以据此回答：

- 哪些车辆使用过该批次？
- 哪些车辆已经交付？
- 哪些车辆出现过相同故障？
- 哪些车辆尚未维修？
- 哪些区域需要优先服务？

### 4.4 机器学习和规则的分工

```text
规则：涉及高压安全的故障必须升级
模型：预测车辆未来 30 天重复维修概率
优化器：安排有限服务资源的优先顺序
LLM：解释故障模式并生成调查摘要
```

模型可以参与 Logic，但不能替代明确的安全规则、审批要求和责任边界。

## 5. Action：把判断变成受治理的业务动作

Action Type 定义用户或 Agent 可以执行的业务事务。官方文档指出，Action 可以修改一个或多个对象、属性和链接，并配置提交条件与副作用。[Action types overview](https://www.palantir.com/docs/foundry/action-types/overview)

### 5.1 售后常见 Action

```text
CreateCustomerComplaint
AssignServiceCenter
CreateRepairOrder
EscalateSafetyIssue
FreezePartBatch
LaunchServiceCampaign
ApproveRecallCase
CloseQualityProblem
```

### 5.2 Action 的组成

```text
参数：车辆、故障、批次、服务中心、原因
提交条件：角色、状态、风险、证据是否完整
规则：修改对象和链接
副作用：通知、Webhook、创建工单、同步外部系统
审计：执行人、时间、原因、版本和结果
```

### 5.3 示例：启动售后服务活动

```text
Action: LaunchServiceCampaign

输入：
  faultPattern
  affectedScope
  serviceInstruction
  priority

提交条件：
  已完成影响范围分析
  风险等级为 high 或 critical
  已指定质量负责人
  服务方案已完成审批

执行结果：
  创建 ServiceCampaign
  生成受影响车辆任务
  通知服务中心
  向客户服务系统同步任务
  记录审批与执行证据
```

### 5.4 Function-backed Action

当动作需要修改多个关联对象时，可以使用 Function-backed Action。例如关闭安全质量问题可能同时需要：

```text
关闭 QualityProblem
更新 Vehicle 风险状态
关闭相关 RepairOrder
生成 VerificationResult
更新 PartBatch 调查状态
通知责任团队
```

复杂 Function 负责计算和编辑逻辑，Action 负责参数、权限、提交条件、审计和对外暴露。[Function-backed actions](https://www.palantir.com/docs/foundry/action-types/function-actions-overview)

## 6. Security：把权限嵌入数据、逻辑和行动

Security 不是只决定“用户能不能登录”，而是决定用户或 AI 在每一步能看到、调用和执行什么。

### 6.1 数据访问安全

```text
客服：查看客户、车辆和预约信息
服务中心：查看本中心车辆和维修任务
供应商质量：查看关联零件和批次质量数据
召回团队：查看全局影响范围
```

### 6.2 属性级安全

不同用户可能看到同一车辆的不同属性：

```text
客服可见：车型、交付日期、维修状态
质量工程师可见：故障码、零件批次、根因分析
安全团队可见：事故描述、敏感调查材料
```

### 6.3 Action 安全

```text
客服：可以创建投诉和预约
服务中心：可以提交诊断和维修结果
质量工程师：可以创建调查和遏制建议
质量负责人：可以冻结批次
召回委员会：可以批准召回
```

### 6.4 AI Agent 安全

AI 是否可以调用工具，需要同时检查：

```text
用户身份
Agent 身份
对象权限
属性权限
Function 权限
Action 权限
提交条件
```

例如，AI 可以推荐冻结电池批次，但不能因为生成了建议就自动执行冻结；正式 Action 仍需满足权限和审批条件。

Palantir 官方强调，Ontology 的安全控制覆盖对象、链接、Action、Function 等语义和行动原语，并在交互时进行策略判断。[The Ontology system](https://www.palantir.com/docs/foundry/architecture-center/ontology-system)

## 7. 五个典型汽车售后案例

### 案例一：重复维修问题

#### Data

```text
同一 VIN
同一故障码
30 天内两次维修
更换相同零件
```

#### Logic

```text
计算重复维修风险
识别是否属于系统性故障
```

#### Action

```text
创建重复维修调查
升级给区域质量负责人
生成技术服务指引
```

#### Security

```text
服务中心只能看本店车辆
总部质量团队可以查看跨区域聚合结果
```

### 案例二：高压电池异常

#### Data

```text
车辆 VIN
电池包序列号
电芯批次
故障码
温度、电压和绝缘数据
供应商与生产工厂
```

#### Logic

```text
聚合相同故障码
沿批次追溯影响车辆
评估热失控风险
```

#### Action

```text
冻结批次
创建专项调查
生成售后检查任务
评估服务活动或召回
```

#### Security

```text
高压安全数据仅对授权团队开放
冻结批次需要质量安全负责人批准
```

### 案例三：OTA 更新后功能异常

#### Data

```text
车辆 VIN
OTA 软件版本
更新时间
功能异常描述
云端日志
用户投诉
```

#### Logic

```text
比较升级前后故障率
识别受影响软件版本
区分版本问题与硬件问题
```

#### Action

```text
暂停版本发布
回滚软件
发布热修复
创建服务活动
通知受影响用户
```

#### Security

```text
软件发布权限与售后查询权限分离
回滚操作需要软件负责人和质量负责人联合批准
```

### 案例四：供应商批次缺陷

#### Data

```text
售后故障
维修更换件
零件序列号
供应商批次
来料检验结果
生产工位和装配时间
```

#### Logic

```text
计算同批次车辆数量
关联来料检验和制造过程
判断是否存在供应商根因
```

#### Action

```text
冻结库存
发起供应商整改
加严来料检验
启动批次遏制
```

#### Security

```text
供应商只能看到自己的问题和整改任务
跨供应商对比结果只对内部质量团队开放
```

### 案例五：安全相关召回判断

#### Data

```text
事故报告
用户投诉
故障码
维修记录
车辆配置
法规和安全要求
```

#### Logic

```text
评估严重度、发生频度和影响范围
生成召回候选车辆清单
比较服务活动和正式召回方案
```

#### Action

```text
创建召回案件
提交召回委员会审批
生成通知和维修计划
跟踪召回完成率
```

#### Security

```text
召回调查材料按案件权限控制
涉及个人信息的客户数据进行属性级限制
召回批准只能由授权委员会执行
```

## 8. 四要素如何形成闭环

```text
Data：车辆出现 HV_BATTERY_042
  ↓
Logic：发现同批次车辆存在相似故障
  ↓
Security：只有质量安全团队可以查看完整影响范围
  ↓
Action：授权负责人批准冻结批次并启动服务活动
  ↓
Data：记录执行结果、维修结果和客户反馈
  ↓
Logic：更新故障风险和供应商质量评分
```

这就是 Palantir 所强调的 read-write loop：系统不仅读取和分析运营数据，还将受治理的决策写回运营世界。

## 9. 与汽车售后系统的集成

Ontology 不必替代所有现有系统，可以将其作为统一业务层：

```text
CRM / 客诉系统       → CustomerComplaint
DMS / 经销商系统     → RepairOrder、ServiceVisit
车云平台             → DiagnosticEvent、Telemetry
MES / 制造系统       → ProductionRecord、PartBatch
PLM                   → DesignRevision、SoftwareVersion
QMS                   → QualityProblem、CorrectiveAction
ERP / WMS             → Supplier、Inventory、Shipment
```

关键是统一业务主键：

```text
VIN
零件号
零件序列号
批次号
软件版本
质量问题编号
维修工单编号
```

## 10. 实施边界

Data、Logic、Action、Security 不是自动生成的四个按钮，而是需要业务、数据、质量、安全和开发团队共同定义的模型边界。

特别需要注意：

- Ontology 不会自动消除故障数据质量问题；
- Function 的分析结果不等于经过人工确认的根因；
- AI 的推荐不等于已授权的 Action；
- Action 的执行仍必须遵守权限、审批和法规要求；
- 读取时的权限控制不一定自动保护所有下游导出数据；
- 汽车安全问题需要保留完整证据、责任和审计链。

## 11. 总结

```text
Data      把售后世界表示成车辆、零件、故障、批次和客户对象
Logic     把事实转化为风险、根因、影响范围和处置建议
Action    把建议转化为工单、冻结、服务活动和召回等业务行动
Security  控制不同角色和 AI Agent 能看什么、算什么、做什么
```

四者共同构成汽车售后质量的运营闭环：

> 从“某辆车出现了一个故障”，走到“识别根因、确定影响范围、执行受控行动，并将结果反馈给设计、供应链、制造和售后系统”。

官方参考：

- [Ontology overview](https://www.palantir.com/docs/foundry/ontology/overview)
- [Functions overview](https://www.palantir.com/docs/foundry/functions/overview)
- [Action types overview](https://www.palantir.com/docs/foundry/action-types/overview)
- [The Ontology system](https://www.palantir.com/docs/foundry/architecture-center/ontology-system)
