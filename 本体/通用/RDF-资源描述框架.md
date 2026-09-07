# RDF（资源描述框架）

## 一、先用一分钟理解 RDF

RDF（Resource Description Framework，资源描述框架）是一种用统一方式描述“资源及其关系”的数据模型。

它把一条事实写成三元组：

```text
主语（Subject） + 谓语（Predicate） + 宾语（Object）
```

例如：

```text
车辆 VIN123 ──安装电池──▶ 电池包 PACK001
```

在 RDF 中，它可以表示为：

```text
<车辆VIN123> <安装电池> <电池包PACK001>
```

多条三元组连接起来，就形成一个可以查询和遍历的 RDF 图。

一句话定义：

> RDF 是一种用“主语—谓语—宾语”三元组表达资源、属性和关系的开放数据模型。

---

## 二、RDF 的核心结构

### 2.1 Subject：主语

主语是正在被描述的资源，例如：

```text
车辆 VIN123
订单 ORD10086
供应商 SupplierA
```

### 2.2 Predicate：谓语

谓语表示属性或关系，例如：

```text
属于车型
安装电池
由供应商提供
生产于
```

谓语最好使用明确、可复用的业务含义，而不是 `relatedTo` 这类模糊名称。

### 2.3 Object：宾语

宾语可以是另一个资源，也可以是字面量：

```text
资源：电池包 PACK001
字符串："理想 L7"
数字：180
日期：2026-09-04
```

示例：

```text
<车辆VIN123> <座位数> "5"
<车辆VIN123> <生产日期> "2026-09-04"
<车辆VIN123> <安装电池> <电池包PACK001>
```

### 2.4 IRI：资源标识符

RDF 通常使用 IRI（Internationalized Resource Identifier）为资源和属性提供全局标识：

```text
https://example.com/vehicle/VIN123
https://example.com/ontology/hasBattery
```

IRI 的意义是：不同系统可以引用同一个概念，而不会只依赖容易冲突的本地名称。

---

## 三、一个完整 RDF 示例

使用 Turtle 语法表达新能源车质量追溯信息：

```turtle
@prefix ex: <https://example.com/ev#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:VIN123 a ex:Vehicle ;
    ex:model ex:ModelL7 ;
    ex:hasBattery ex:PACK001 ;
    ex:productionDate "2026-09-04"^^xsd:date .

ex:PACK001 a ex:BatteryPack ;
    ex:fromBatch ex:BATCH2026 ;
    ex:softwareVersion "BMS-3.2.1" .

ex:BATCH2026 a ex:PartBatch ;
    ex:suppliedBy ex:SupplierA .

ex:SupplierA a ex:Supplier ;
    ex:name "示例电池供应商" .
```

这段数据表达了：

```text
VIN123 是一辆 Vehicle
VIN123 属于 ModelL7
VIN123 安装 PACK001
PACK001 来自 BATCH2026
BATCH2026 由 SupplierA 供应
```

---

## 四、RDF 图是什么

RDF 数据可以画成节点和边：

```text
VIN123 ──hasBattery──▶ PACK001
  │                       │
  │                       └──fromBatch──▶ BATCH2026
  │                                           │
  └──model──▶ ModelL7                         └──suppliedBy──▶ SupplierA
```

其中：

- 节点表示资源或字面量；
- 边表示谓语；
- 多个来源的数据可以合并到同一张图中；
- 通过 IRI 可以把不同数据集中的同一资源连接起来。

RDF 1.1 的核心抽象是 RDF Graph，即由主语、谓语和宾语构成的三元组集合；RDF Dataset 还可以组织默认图和多个命名图。[W3C RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/)

---

## 五、RDF 的常见序列化格式

RDF 是数据模型，不等于某一种文件格式。同一组 RDF 数据可以用多种语法保存和交换：

| 格式 | 特点 | 适用场景 |
|---|---|---|
| Turtle | 简洁、适合人类阅读和编写 | 本体开发、示例、版本管理 |
| N-Triples | 每行一个三元组，结构简单 | 流式处理、调试、数据交换 |
| JSON-LD | JSON 结构，适合 Web 和 JavaScript | Web API、前端、应用集成 |
| RDF/XML | XML 表达 RDF | 传统企业系统和旧工具 |
| TriG | 支持多个命名图 | 数据集和上下文管理 |

同一事实可以写成 JSON-LD：

```json
{
  "@id": "https://example.com/vehicle/VIN123",
  "@type": "Vehicle",
  "hasBattery": {
    "@id": "https://example.com/part/PACK001"
  }
}
```

---

## 六、RDF 能做什么，不能做什么

### RDF 擅长

- 统一表达跨系统事实；
- 连接不同数据源；
- 表达对象之间的关系；
- 支持开放链接数据；
- 为知识图谱提供底层数据结构；
- 作为 OWL、RDFS、SPARQL 等技术的基础。

### RDF 本身不负责

- 定义完整的领域本体；
- 自动执行复杂逻辑推理；
- 替代数据库事务；
- 提供用户权限管理；
- 定义业务审批和工作流；
- 保证数据一定真实或完整。

RDF 主要是一个数据表示框架。推理、约束校验、查询和业务行动通常需要结合其他技术。

---

## 七、RDF、RDFS、OWL 和 SPARQL 的关系

```text
RDF：     表达事实和关系
RDFS：    定义类、子类、属性、定义域和值域
OWL：     定义更丰富的本体语义和逻辑约束
SPARQL：  查询和更新 RDF 图
SHACL：   验证 RDF 数据是否满足结构约束
```

例如，RDF 可以表达：

```text
VIN123 安装 PACK001
```

RDFS 可以定义：

```text
Vehicle 是一个类
BatteryPack 是一个类
hasBattery 的主语是 Vehicle
hasBattery 的宾语是 BatteryPack
```

OWL 可以进一步表达：

```text
每辆安全车辆必须且只能有一个电池包
Vehicle 与 BatteryPack 是不同类别
两个属性具有等价或逆向关系
```

SPARQL 则负责查询：

```sparql
SELECT ?vehicle ?battery
WHERE {
  ?vehicle a ex:Vehicle .
  ?vehicle ex:hasBattery ?battery .
}
```

---

## 八、案例：追踪新能源车电池质量问题

### 8.1 初始事实

```turtle
ex:VIN1001 ex:hasBattery ex:PACK001 .
ex:VIN1002 ex:hasBattery ex:PACK002 .
ex:PACK001 ex:fromBatch ex:BATCH2026 .
ex:PACK002 ex:fromBatch ex:BATCH2026 .
ex:BATCH2026 ex:suppliedBy ex:SupplierA .
```

### 8.2 追加售后故障

```turtle
ex:Complaint9001 a ex:CustomerComplaint ;
    ex:reportedFor ex:VIN1001 ;
    ex:hasDiagnosticCode "HV_BATTERY_042" .

ex:Complaint9002 a ex:CustomerComplaint ;
    ex:reportedFor ex:VIN1002 ;
    ex:hasDiagnosticCode "HV_BATTERY_042" .
```

### 8.3 查询影响范围

通过图查询可以找到：

```text
故障投诉
  → 车辆 VIN
  → 电池包序列号
  → 电芯或电池批次
  → 供应商
  → 同批次的其他车辆
```

这使质量工程师能够识别：

- 同一批次影响了哪些车辆；
- 是否跨工厂或跨区域发生；
- 是否与某个供应商或生产时段相关；
- 是否需要冻结库存或启动调查。

### 8.4 结合 OWL / SHACL / 业务系统

RDF 可以保存事实，OWL 可以表达类别和语义，SHACL 可以校验“每个电池包必须有批次”，而真正的“冻结批次”“通知供应商”“发起召回”仍需要业务系统或 Palantir Action 等执行机制。

---

## 九、RDF 与本体论的关系

```text
本体论：定义领域概念、关系、约束和规则
RDF：   用三元组表达这些概念和关系的事实
OWL：   用形式逻辑表达本体语义
```

可以把它类比为：

```text
RDF = 句子的基本事实结构
OWL = 句子中概念和逻辑关系的正式语法
```

RDF 不等于完整本体，但可以用来表示本体；OWL 本体也可以映射成 RDF 图。

## 十、RDF 与 Palantir Ontology 的区别

| 方面 | RDF | Palantir Ontology |
|---|---|---|
| 定位 | 开放数据模型 | 企业运营平台中的本体系统 |
| 基本单元 | 三元组 | Object、Property、Link |
| 逻辑 | 需要 RDFS、OWL 或外部推理器 | Function、模型、业务规则、AIP Logic |
| 行动 | RDF 本身不定义业务行动 | Action Type 支持受治理的业务变更 |
| 查询 | 通常使用 SPARQL | Ontology API、OSDK 和平台工具 |
| 安全 | 需要外部安全机制 | 对象、属性、函数和行动均可治理 |
| 写回 | 需要外部实现 | 支持 Ontology 编辑和外部系统写回 |

简单说：RDF 是开放的底层知识表示方式，Palantir Ontology 是面向企业运营、应用、AI 和安全的完整平台实现。

## 十一、学习和应用路线

```text
1. 理解三元组：Subject / Predicate / Object
2. 学习 Turtle 和 JSON-LD
3. 使用 RDFS 定义类和属性
4. 使用 OWL 表达本体约束和推理
5. 使用 SHACL 做数据质量校验
6. 使用 SPARQL 查询 RDF 图
7. 将 RDF 图连接到业务应用和工作流
```

## 十二、总结

RDF 的核心价值是把不同来源的信息转换成统一、可链接的图结构：

```text
主语 ——谓语——> 宾语
```

它解决“如何表达和连接事实”的问题；OWL 解决“如何定义概念和推理语义”的问题；SPARQL 解决“如何查询图”的问题；SHACL 解决“数据是否满足约束”的问题。

如果要构建一个可运营的企业质量系统，还需要在 RDF 之上增加业务规则、权限、审批、行动、审计和外部系统写回能力。

官方参考：

- [W3C RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/)
- [W3C RDF 1.1 Primer](https://www.w3.org/TR/rdf11-primer/)
- [W3C OWL 2 Overview](https://www.w3.org/TR/owl2-overview/)
