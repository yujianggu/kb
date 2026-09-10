# Palantir Ontology：Interface、Function、Action 的关系与区别

## 一、核心结论

```text
Interface：规定对象应该具有什么结构和能力
Function：负责读取、计算和推理
Action：负责经过治理地改变业务状态
```

三者通常形成以下调用关系：

```text
Interface
   ↓ 定义统一能力契约
Object Type 实现 Interface
   ↓
Function 读取对象并进行计算
   ↓
Action 调用规则或 Function
   ↓
修改对象、属性、链接，并触发副作用
```

## 二、Interface：对象能力的抽象契约

Palantir 官方将 Interface 定义为描述对象类型形状和能力的 Ontology 类型。[Interfaces overview](https://www.palantir.com/docs/foundry/interfaces/interface-overview)

例如定义一个 `Facility` 接口：

```text
Facility
├── facilityName
├── location
├── operationalStatus
└── alerts
```

以下对象都可以实现它：

```text
Airport
Factory
Warehouse
MaintenanceHangar
```

应用可以面向 `Facility` 工作，而不必知道具体对象是机场、工厂还是仓库。

### Interface 的特点

- 是抽象定义，不是具体对象；
- 不直接由数据集实例化；
- 可以被多个 Object Type 实现；
- 可以定义属性；
- 可以定义链接约束；
- 可以定义 Action 能力约束；
- 支持对象类型多态；
- 适合构建跨对象类型的统一应用接口。

它可以类比为编程语言中的：

```text
interface Facility { ... }
```

而不是：

```text
class Airport { ... }
```

## 三、Function：业务逻辑和计算

Function 是运行逻辑的地方，可以：

- 读取 Object 属性；
- 遍历 Link；
- 查询对象集合；
- 聚合和计算指标；
- 调用机器学习模型；
- 查询外部系统；
- 根据复杂逻辑生成结果；
- 在特定场景中产生 Ontology 编辑。

Palantir 官方说明，Function 可以原生读取对象、遍历链接，并执行复杂业务逻辑。[Functions overview](https://www.palantir.com/docs/foundry/functions/overview)

例如：

```text
findAlternativeWarehouses(order)
```

它可以检查：

```text
订单需求量
仓库库存
运输距离
仓库当前状态
运输能力
历史延误风险
```

并返回：

```text
仓库 DC-07：推荐
仓库 DC-11：备选
仓库 DC-02：不推荐
```

Function 的主要特点：

```text
输入对象或参数
       ↓
读取对象和关系
       ↓
执行计算或判断
       ↓
返回结果
```

它通常是“计算”，不一定改变业务数据。

## 四、Action：业务状态变更

Action Type 定义一个用户或 Agent 可以执行的业务动作。

例如：

```text
ReallocateOrder
ApproveVehicleRelease
FreezePartBatch
StartCorrectiveAction
LaunchRecall
```

Palantir 官方把 Action 描述为一次可以修改一个或多个对象、属性和链接的事务，并且可以包含副作用和提交条件。[Action types overview](https://www.palantir.com/docs/foundry/action-types/overview)

一个 Action 通常包含：

```text
参数
提交条件
规则
对象修改
链接修改
通知
Webhook
审批
审计记录
```

例如：

```text
Action: FreezePartBatch

输入：
  batchId
  reason

提交条件：
  当前用户是质量负责人
  风险等级为 high 或 critical
  批次仍未完成投产

执行结果：
  批次状态 → FROZEN
  生成受影响车辆列表
  创建质量调查工单
  通知供应商
```

## 五、Function 和 Action 的区别

| 对比项 | Function | Action |
|---|---|---|
| 主要职责 | 计算、查询、判断 | 修改业务状态 |
| 是否一定改变数据 | 不一定 | 通常会产生事务变更 |
| 输出 | 值、对象集合、指标、建议 | 对象、属性、链接的变更结果 |
| 典型例子 | 计算风险分、查找替代仓库 | 冻结批次、批准放行 |
| 权限 | 函数和数据访问权限 | 动作权限和提交条件 |
| 副作用 | 可以调用外部逻辑 | 可配置通知、Webhook 等副作用 |
| 审批 | 通常不需要 | 可以要求审批或提交条件 |

## 六、Function-backed Action

复杂 Action 可以由 Function 提供具体执行逻辑，这叫 Function-backed Action。

```text
Action Type
   ├── 参数
   ├── 权限
   ├── 提交条件
   ├── 审计和副作用
   └── Function
        ├── 查询多个对象
        ├── 计算复杂逻辑
        ├── 修改多个对象
        └── 创建或连接对象
```

例如关闭一个质量问题时，需要同时：

```text
关闭 QualityProblem
关闭关联 QualityWorkOrder
更新车辆风险状态
生成验证记录
通知责任人
```

简单 Action 规则可能不够，此时可以由 Function 实现复杂编辑逻辑。[Function-backed actions](https://www.palantir.com/docs/foundry/action-types/function-actions-overview)

## 七、Interface 如何与 Function、Action 配合

以质量管理为例。

### Interface

```text
QualityIssue
├── issueId
├── severity
├── status
├── affectedAsset
├── calculateRisk
└── closeIssue
```

### Object Types 实现 Interface

```text
ProductionQualityIssue
SupplierQualityIssue
AfterSalesQualityIssue
DesignQualityIssue
```

这些具体对象都实现：

```text
QualityIssue
```

### Function

```text
calculateRisk(issue: QualityIssue)
```

它可以读取：

```text
问题严重度
影响车辆数量
是否涉及安全
供应商批次
重复发生次数
```

### Action

```text
CloseQualityIssue
StartContainment
EscalateSafetyIssue
```

最终调用链：

```text
ProductionQualityIssue
SupplierQualityIssue
AfterSalesQualityIssue
          │
          ▼
       QualityIssue Interface
          │
          ├── calculateRisk()
          ├── StartContainment Action
          └── CloseQualityIssue Action
```

## 八、完整案例：电池批次风险

### Interface

```text
SafetyIssue
├── issueId
├── severity
├── affectedVehicles
└── status
```

### Function

```text
findAffectedVehicles(issue)
```

沿着以下关系查询：

```text
QualityIssue
 → BatteryPack
 → PartBatch
 → Vehicle
```

返回：

```text
影响车辆：1,248 台
涉及工厂：2 个
涉及区域：3 个
供应商：SupplierA
```

### Action

```text
FreezeBatteryBatch
```

提交条件：

```text
severity = critical
当前用户拥有质量安全权限
影响范围分析已经完成
```

执行结果：

```text
批次状态改为 FROZEN
创建调查工单
生成影响车辆清单
通知供应商
触发售后服务活动评估
```

这里：

```text
Interface 统一“质量问题长什么样”
Function 计算“问题影响多大”
Action 执行“现在要采取什么措施”
```

## 九、容易混淆的地方

### Interface 不是父类实例

Interface 是抽象契约，不能直接作为普通对象实例使用；具体 Object Type 才有实际对象数据。

### Function 不是 Action

Function 可以返回推荐结果，但不等于已经完成业务变更：

```text
findAlternativeWarehouses()
```

只表示找到了候选仓库；

```text
ReallocateOrder
```

才表示真正修改订单分配。

### Action 不一定需要 Function

简单修改可以直接用 Action 规则：

```text
把 status 改成 Approved
```

复杂多对象修改时，才使用 Function-backed Action。

## 十、Action 中“经过治理地改变业务状态”的含义

“经过治理地改变业务状态”可以拆成两部分：

```text
改变业务状态 + 经过治理
```

### 10.1 改变业务状态

业务对象通常具有状态，例如：

```text
订单：待处理 → 已批准 → 已发运
质量问题：新建 → 分析中 → 已关闭
车辆：生产中 → 待检 → 已放行
批次：待检 → 合格 → 冻结
```

Action 负责执行这类受控状态变化：

```text
ApproveOrder
FreezePartBatch
ReleaseVehicle
CloseQualityIssue
```

### 10.2 经过治理

治理意味着不是任何人、任何时间都能直接改数据，而是必须经过预先定义的控制：

```text
谁可以执行？
执行需要什么参数？
什么条件下允许执行？
需要谁审批？
会修改哪些对象？
会触发什么副作用？
如何记录和审计？
```

### 10.3 案例：冻结电池批次

```text
Action: FreezeBatteryBatch

执行人：
  质量负责人

提交条件：
  风险等级 = high 或 critical
  批次当前不是已消耗状态
  影响范围分析已经完成

执行结果：
  批次状态 → FROZEN
  创建质量调查工单
  生成影响车辆清单
  通知供应商

审计记录：
  谁执行、何时执行、为什么执行、影响了什么
```

### 10.4 与直接数据库更新的区别

直接改数据库可能只是：

```sql
UPDATE part_batch
SET status = 'FROZEN'
WHERE batch_id = 'BATCH2026';
```

它未必检查操作人权限、风险分析是否完成、是否需要审批、是否通知供应商、是否同步其他系统，以及是否记录完整原因。

经过治理的 Action 更接近一个完整业务事务：

```text
请求
  → 权限校验
  → 参数校验
  → 提交条件校验
  → 修改对象和关系
  → 触发通知或外部系统调用
  → 保存审计记录
```

Palantir 官方将 Action 描述为一次可以修改一个或多个对象、属性和链接的事务，并可以附带提交条件和副作用。[Action types overview](https://www.palantir.com/docs/foundry/action-types/overview)

因此：

```text
普通修改：
  直接把字段改掉

经过治理的 Action：
  在明确的权限、规则、审批、审计和副作用控制下，
  执行一个完整的业务动作
```

## 十一、Interface 不等于权限

Interface 定义结构和能力；权限由 Ontology 的资源、对象、属性和 Action 安全机制控制。

## 十二、总结

```text
Interface = 统一契约
Function  = 计算逻辑
Action    = 业务变更
```

更完整地说：

```text
Interface 定义“哪些对象可以被统一处理”
Function 负责“如何查询、计算和判断”
Action    负责“如何安全、受控地改变业务世界”
```

在成熟的 Palantir Ontology 应用中，三者通常协同工作：

```text
Interface
  → 统一对象能力
  → Function 读取和计算
  → Action 执行变更
  → Security 控制谁可以调用
  → Writeback / Webhook 同步外部系统
```

[返回本目录](README.md)
