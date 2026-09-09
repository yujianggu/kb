# Palantir Ontology 总结

## 1. 核心结论

Palantir Ontology（本体论）是 Palantir AI Platform（AIP）的核心架构。它的独特之处在于：将企业的**数据、逻辑、行动和安全性**整合到一个统一的、以决策为中心的运营模型中。

它不只是存储或查询数据，而是使用企业业务语言——例如“订单”“客户”“工厂”“库存”和“航班”——构建一个实时、可操作的数字世界，让人类和 AI 智能体能够在同一个受治理的模型上理解状态、分析问题、执行动作并获得反馈。

Palantir 当前官方强调，Ontology 不只是一个“语义层”，而是一个同时具备语义建模、业务逻辑、事务动作和动态安全能力的系统。

## 2. 官方模型：四个核心层面

可以把 Ontology 理解为构造一个业务句子：对象是“名词”，动作是“动词”，逻辑负责“思考”，安全负责确保整个句子能够被合规执行。

| 组成要素 | 官方含义 | 通俗理解 |
|---|---|---|
| **数据（Data）** | 将 ERP、CRM、IoT、数据库、文档和其他来源映射为对象、属性和链接 | 业务世界的“名词” |
| **逻辑（Logic）** | 连接业务规则、函数、机器学习模型、优化算法和 LLM 能力 | 决策的“思考过程” |
| **行动（Action）** | 定义并执行创建、修改、删除、审批、调配和通知等业务操作 | 业务世界的“动词” |
| **安全（Security）** | 对对象、属性、函数、动作和数据实施细粒度、动态的权限与治理 | 决定谁能看、谁能算、谁能做 |

官方将企业决策概括为：

```text
决策 = 数据 + 逻辑 + 行动 + 安全
```

其中安全不是最后附加的控制层，而是在查询、函数执行、动作提交和 AI 工具调用时持续生效。

## 3. 核心建模元素

### 3.1 Object Type：对象类型

Object Type 定义现实实体或事件的类型，例如：

- 客户订单（Customer Order）
- 产品（Product）
- 配送中心（Distribution Center）
- 库存（Inventory）
- 飞机（Aircraft）
- 航班（Flight）

一个具体的订单或一架具体的飞机，则是该对象类型的实例。对象通常具有主键、标题键、属性、数据源映射、权限配置和可执行动作。

### 3.2 Property：属性

Property 描述对象的特征，例如：

```text
Order.orderId
Order.status
Order.requiredDeliveryDate
DistributionCenter.address
Inventory.availableQuantity
```

属性不仅有数据类型，也可以附加业务语义、枚举值、显示方式、检索配置和安全策略。

### 3.3 Link Type：链接类型

Link Type 定义对象之间的业务关系，例如：

```text
Order ── allocatedTo ──▶ DistributionCenter
DistributionCenter ── stores ──▶ Product
Order ── contains ──▶ Product
```

链接可以表示一对一、一对多、多对一或多对多关系。它的作用不只是数据库连接，还让应用、函数和 AI 能够沿着业务关系进行查询和推理。

### 3.4 Interface：接口

Interface 描述多个对象类型共同具有的结构和能力。例如，可以定义一个 `Facility` 接口，让机场、工厂、仓库和维修中心共享名称、位置和告警能力。

这样，工作流可以面向“设施”处理，而不必为每一种具体设施重复编写逻辑。

### 3.5 Function：函数

Function 用于实现可复用的业务逻辑，例如：

```text
find_alternative_centers(order_id)
```

它可以读取对象属性、遍历链接、聚合数据、调用机器学习模型或执行复杂计算，然后返回候选方案、风险分数或指标。

函数主要负责“计算和判断”，不等同于最终的业务变更动作。

### 3.6 Action Type：行动类型

Action Type 定义用户或 AI 可以执行的业务事务，例如：

- 重新分配订单
- 创建采购订单
- 调配库存
- 审批付款
- 发送告警
- 修改生产计划

一个行动类型通常包含：

1. **参数**：用户或 AI 提供的输入；
2. **提交条件**：决定动作是否允许提交；
3. **规则**：创建、修改或删除对象和链接；
4. **副作用**：通知、调用外部系统或触发后续工作流；
5. **审计与写回**：保存决策结果，并将变更同步到相关系统。

## 4. 案例：Titan 医疗用品公司的供应链应急系统

### 4.1 背景

Titan Industries 的一个配送中心因火灾停运，许多紧急订单面临延误。公司希望快速找到其他有足够库存的配送中心，并在主管批准后完成订单重新分配。

### 4.2 数据层：构建业务“名词”

定义以下对象类型：

```text
CustomerOrder
Product
DistributionCenter
Inventory
Shipment
DisruptionEvent
```

定义关键属性：

```yaml
CustomerOrder:
  orderId: "ORD-10086"
  status: "AT_RISK"
  requiredDeliveryDate: "2026-09-06"
  affectedBy: "FIRE-DC-03"

DistributionCenter:
  centerId: "DC-07"
  address: "Shanghai"
  operationalStatus: "OPEN"

Inventory:
  productId: "MED-GLOVE-L"
  availableQuantity: 85000
```

建立关系：

```text
CustomerOrder ── allocatedTo ──▶ DistributionCenter
CustomerOrder ── requires ──────▶ Product
DistributionCenter ── stores ────▶ Product
DisruptionEvent ── affects ──────▶ DistributionCenter
```

### 4.3 逻辑层：计算替代方案

定义函数：

```text
find_alternative_centers(order_id)
```

函数可以综合判断：

- 替代配送中心是否正常运营；
- 所需产品是否有足够库存；
- 到客户的运输时间；
- 当前运输容量；
- 订单优先级；
- 预计成本和延误风险。

返回结果示例：

```text
DC-07：可满足全部订单，预计延误 1 天，风险低
DC-11：只能满足 70% 数量，预计延误 2 天，风险中
DC-02：库存充足，但运输成本较高
```

AI 可以通过自然语言调用该函数，例如：

> “请为受火灾影响的紧急订单找出可行的替代配送中心，并说明推荐理由。”

LLM 负责理解问题、调用受授权的函数并解释结果；库存筛选和约束计算仍由明确的函数和业务逻辑完成。

### 4.4 行动层：定义“重新分配订单”

定义行动类型：

```text
ReallocateOrder
```

参数：

```text
order: CustomerOrder
newCenter: DistributionCenter
reason: String
```

提交条件：

```text
当前用户属于供应链主管组
AND 订单状态 = AT_RISK
AND 新配送中心状态 = OPEN
AND 新配送中心库存足够
AND 新配送中心有可用运输能力
```

执行规则：

```diff
CustomerOrder ORD-10086:
- allocatedCenter: DC-03
+ allocatedCenter: DC-07

- status: AT_RISK
+ status: REALLOCATED
```

同时可以：

- 创建一条订单重新分配记录；
- 向仓库拣货系统发送指令；
- 通知物流团队和客户服务团队；
- 同步更新运输计划；
- 将结果写回 ERP 或订单管理系统。

### 4.5 应用层：人机协作闭环

供应链主管通过基于 Ontology SDK 的应用看到：

- 地图上的受灾配送中心；
- 受影响的订单；
- 每个替代配送中心的库存和运输能力；
- AI 推荐及其理由；
- 预计成本、延误和风险。

主管审核后点击“执行重新分配”。系统会重新检查提交条件，随后执行 Action，更新 Ontology 并同步相关业务系统。

整个过程形成闭环：

```text
实时数据
  ↓
发现订单风险
  ↓
函数和 AI 生成替代方案
  ↓
主管审核
  ↓
权限与业务规则校验
  ↓
Action 执行变更
  ↓
写回 ERP / WMS / TMS
  ↓
记录结果并持续改进
```

## 5. Ontology 如何约束 AI 智能体

### 5.1 锚定在业务对象上

AI 不是对一堆未经定义的文本或数据库字段自由猜测，而是围绕明确的对象、属性和链接工作。

例如，AI 处理“订单风险”时，可以明确知道：

```text
订单有 status、priority、deliveryDate 属性
订单链接到 Product 和 DistributionCenter
```

这有助于减少字段误解和无依据推断，但不能把 Ontology 误认为可以完全消除模型幻觉。逻辑质量仍取决于数据质量、函数设计和模型表现。

### 5.2 工具必须被明确定义和授权

AI 可以调用的函数和行动必须在 Ontology 中定义，并受用户、应用和对象权限约束。

例如，AI 可以：

- 查询当前用户有权查看的订单；
- 调用“寻找替代仓库”函数；
- 推荐重新分配方案。

但它不能因为用户使用了自然语言，就自动获得财务数据权限或执行未经批准的采购动作。

### 5.3 推荐与执行分离

在高风险场景中，可以让 AI 只负责分析和推荐，而将真正的业务变更放到需要人工审批的 Action 中。

这形成一种典型的人机协作模式：

```text
AI 观察 → AI 推理 → AI 推荐 → 人员批准 → 系统执行
```

## 6. 与常见概念的区别

### 与数据库 Schema 的区别

数据库 Schema 主要描述表、字段和主外键；Ontology 进一步描述业务语义、关系、函数、动作、权限和写回流程。

### 与知识图谱的区别

知识图谱重点表达“对象—关系—对象”；Ontology 还增加了实时状态、业务逻辑、可执行动作、权限和事务写回能力。

### 与传统语义层的区别

传统语义层主要统一指标、维度和查询口径；Ontology 还负责驱动操作流程和改变企业状态。因此 Palantir 当前官方明确强调它不只是一个薄语义层。

### 与数字孪生的区别

数字孪生通常强调对现实资产的数字化表示；Ontology 在此基础上进一步表示谁可以采取什么动作、动作如何审批、如何写回以及如何形成反馈闭环。

## 7. 关键价值总结

Palantir Ontology 的价值不在于“把所有数据放到一张图里”，而在于把分散的企业数据转化为可理解、可计算、可执行、可治理的业务世界。

其核心价值可以概括为：

1. **统一业务语言**：跨 ERP、CRM、MES 和其他系统形成一致的对象模型；
2. **连接分析与行动**：分析结果可以直接转化为受治理的业务动作；
3. **支持人机协作**：人和 AI Agent 使用同一套对象、逻辑和工具；
4. **强化安全治理**：权限贯穿数据访问、函数调用和动作执行；
5. **形成运营闭环**：决策结果写回系统，并沉淀为后续分析和模型改进的数据。

## 8. 官方参考资料

- [Ontology overview](https://www.palantir.com/docs/foundry/ontology/overview)
- [Why create an Ontology?](https://www.palantir.com/docs/foundry/ontology/why-ontology)
- [The Ontology system](https://www.palantir.com/docs/foundry/architecture-center/ontology-system)
- [Types reference](https://www.palantir.com/docs/foundry/object-link-types/type-reference)
- [Action types overview](https://www.palantir.com/docs/foundry/action-types/overview)
- [Functions overview](https://www.palantir.com/docs/foundry/functions/overview)
- [Ontology SDK overview](https://www.palantir.com/docs/foundry/ontology-sdk/overview)

## 一句话总结

**Palantir Ontology 是企业的业务操作系统模型：用对象和关系描述世界，用函数和模型理解世界，用 Action 改变世界，并用安全策略确保人和 AI 都只能在被授权的边界内行动。**

[返回本目录](README.md)
