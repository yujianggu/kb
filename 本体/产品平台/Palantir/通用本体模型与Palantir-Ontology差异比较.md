# 通用本体模型与 Palantir Ontology 的差异比较

## 结论

通用本体模型是一种知识表示与领域建模方法；Palantir Ontology 是 Palantir Foundry/AIP 中的一套企业级运营实现。

```text
通用本体：定义业务世界如何被理解
Palantir Ontology：让业务世界可以被查询、计算、改变和治理
```

## 核心差异

| 维度 | 通用本体模型 | Palantir Ontology |
|---|---|---|
| 定位 | 建模方法和知识表示框架 | 企业运营平台中的本体系统 |
| 核心对象 | 类、实例、属性、关系、约束、规则 | Object Type、Object、Property、Link Type、Function、Action Type |
| 数据连接 | 通常需要另行实现数据接入 | 可映射数据集、虚拟表、流、模型等企业资产 |
| 逻辑 | 依赖规则引擎、推理机或应用代码 | Function、业务规则、机器学习模型、优化器和 AIP Logic |
| 行动 | 通常需要外接工作流 | Action Type 原生定义参数、校验、变更和副作用 |
| 写回 | 取决于具体实现 | 支持 Ontology 编辑、writeback 和外部系统集成 |
| 安全 | 常由数据库、IAM 或应用提供 | 可治理对象、属性、函数和行动的访问与执行 |
| 应用接入 | 需要自行设计 API 和适配层 | 可通过 Ontology SDK、应用和 Foundry 工具使用 |
| AI 支持 | 需要自行设计 Agent 工具和权限 | AI 可在受授权的对象、函数和行动边界内运行 |
| 运行方式 | 可以是静态知识模型 | 面向实时查询、事务变更、自动化和人机协作 |

## 概念映射

| 通用本体概念 | Palantir Ontology |
|---|---|
| 类 / 概念 | Object Type |
| 实例 | Object |
| 属性 | Property |
| 关系 | Link Type |
| 关系实例 | Link |
| 共性能力 | Interface |
| 规则和计算 | Function、Ontology Rules、Submission Criteria |
| 操作 / 命令 | Action Type |
| 访问控制 | Object、Property、Action Security |

## 同一业务问题的表达差异

以“重新分配订单”为例。

### 通用本体模型

```text
概念：订单、仓库、产品
关系：订单分配到仓库，订单需要产品
规则：库存不足的仓库不能分配订单
```

该模型能够表达业务知识，但实际修改订单、通知物流系统等能力需要外部应用或工作流支持。

### Palantir Ontology

```text
Object Types：Order、Warehouse、Product、Inventory
Links：Order allocatedTo Warehouse
Function：findAlternativeWarehouses(order)
Action Type：ReallocateOrder
Submission Criteria：用户角色、订单状态、库存数量、运输能力
Side Effects：通知 WMS、更新 TMS、创建审计记录
Security：限制可见订单、可用仓库和可执行动作
```

此时模型已经从“描述事实”扩展为“支持并治理决策”。

## Palantir Ontology 的侧重点

1. 从语义模型走向运营模型：不仅描述对象，还描述如何改变对象状态。
2. 从读模型走向读写闭环：分析结果可以通过受治理的行动写回业务系统。
3. 把安全绑定到业务动作：动作提交时重新验证用户、对象和实时条件。
4. 为应用和 AI 提供统一接口：同一对象、函数和行动可被多个应用复用。
5. 支持企业级治理：覆盖数据血缘、权限、审计、版本和跨系统同步。

## 常见误解

- Palantir Ontology 不是唯一的行业本体标准；企业仍需自行定义领域概念。
- Palantir Ontology 不等于 RDF/OWL 或普通知识图谱。
- 使用平台不会自动产生正确模型，主键、关系、权限和规则仍需领域专家设计。
- Function 负责计算和判断，Action Type 负责经过治理的业务状态变更。
- Ontology 可以约束 AI 的对象、工具和权限边界，但不能保证数据或模型结果绝对正确。

## 选择建议

如果目标是统一业务词汇、建设知识图谱或制定数据标准，通用本体建模方法通常已经足够。

如果还需要连接 ERP、MES、CRM、IoT 和模型，并让应用、AI Agent 和自动化流程在同一模型上查询、决策、审批、执行和写回，那么 Palantir Ontology 这类运营型实现更适合。

## 官方参考

- [Ontology overview](https://www.palantir.com/docs/foundry/ontology/overview)
- [Why create an Ontology?](https://www.palantir.com/docs/foundry/ontology/why-ontology)
- [The Ontology system](https://www.palantir.com/docs/foundry/architecture-center/ontology-system)
- [Action types overview](https://www.palantir.com/docs/foundry/action-types/overview)

[返回本目录](README.md)
