# Google OKF：开放知识格式

## OKF 是什么

“谷歌 OKF”通常指 Google Cloud 发布的 **Open Knowledge Format（开放知识格式）**。它是一种面向人类和 AI Agent 的开放、厂商中立的知识文件规范，用于把企业知识组织成可移植、可互操作的知识包。

它不是 Open Knowledge Foundation，也不是本体论标准、数据库、知识图谱产品、LLM 框架或 Palantir Ontology 的替代品。

## 核心思想

```text
Markdown 文件 + YAML 元数据 + 标准化目录 + 文档链接
= 可被人和 AI Agent 导航的知识包
```

## 一个 OKF 知识包

```text
knowledge-bundle/
├── index.md
├── entities/
│   ├── customer.md
│   ├── order.md
│   └── supplier.md
├── processes/
│   └── order-approval.md
└── metrics/
    └── revenue.md
```

概念文件可以使用 YAML Front Matter 保存元数据：

```markdown
---
type: concept
title: 客户
description: 企业与其交易或互动的客户实体
tags:
  - CRM
  - customer
timestamp: 2026-09-04
---

# 客户

客户是向企业购买产品或服务，或与企业发生业务互动的组织或个人。

## 相关概念

- [订单](../entities/order.md)
- [合同](../entities/contract.md)
```

## OKF 与本体论的区别

| 对比项 | 本体论 | Google OKF |
|---|---|---|
| 本质 | 领域知识和语义模型 | 知识文件的组织与交换格式 |
| 主要内容 | 概念、属性、关系、约束、规则 | Markdown、YAML 元数据和文件链接 |
| 解决问题 | 领域是什么、如何关联、如何推理 | 知识如何统一存储、读取和交换 |
| 是否定义业务语义 | 是 | 不规定具体业务语义 |
| 是否定义执行动作 | 可以定义 | 主要描述知识和上下文 |

```text
本体论 = 知识的结构和含义
OKF    = 知识如何以统一文件形式保存和传递
```

## OKF 与 Palantir Ontology 的关系

```text
OKF：用 Markdown + YAML 表达和交换知识

Palantir Ontology：用 Object、Property、Link、Function、Action 和 Security
构建可查询、可计算、可执行的企业运营模型
```

OKF 可以作为本体文档、数据目录、操作手册和 AI 上下文的交换格式，但不会替代 Palantir Ontology 的实时查询、权限、事务写回和业务动作能力。

## 对当前知识库的应用

```text
本体/
├── 通用/
├── 案例/
├── palantir/
└── okf/
```

若要进一步转为 OKF 风格，可以：

1. 为每个 Markdown 文件增加 YAML Front Matter；
2. 增加 `index.md` 作为知识包入口；
3. 使用 Markdown 链接连接通用本体、行业案例、Palantir 和 OKF 文档；
4. 补充 `type`、`title`、`description`、`tags` 和 `timestamp`；
5. 约定 `concept`、`case`、`standard`、`process` 等文档类型。

## 官方资料

- [Google Cloud：Introducing the Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/how-open-knowledge-format-can-improve-data-sharing)
- [OKF Specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
