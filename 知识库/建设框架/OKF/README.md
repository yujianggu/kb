# Google Cloud Open Knowledge Format（OKF）完整解读

**OKF 是面向人与 Agent 的知识交换格式：以目录组织知识，用 Markdown 表达内容，用 YAML frontmatter 表达可查询的元数据，再通过链接、索引、来源和验证记录帮助消费。**

本文以 **OKF v0.2** 为基准，核对日期为 **2026-10-15**，固定上游提交为 `ad30107c31c06aec8a7d5636e0d1058118604e6f`。规范解释依据 [GoogleCloudPlatform 官方仓库的 SPEC.md](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/ad30107c31c06aec8a7d5636e0d1058118604e6f/SPEC.md)；中文说明、业务与 AI Coding 用法是本库整理，不是官方中文译本或完整逐句翻译。

[摘要](摘要.md) · [业务与 AI Coding 教学案例](案例-业务问答与AI-Coding.md) · [英文规范离线快照](上游规范/SPEC.md) · [来源与适用边界](来源与适用边界.md)

## 1. 来源、版本和定位

Google Cloud 于 **2026-06-12** 在官方博客介绍 OKF v0.1，作者为 Sam McVeety 和 Amir Hormati，目标是将 LLM Wiki 的组织方式整理为可移植、可互操作的格式。[Google Cloud 发布介绍](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)

当前核对的独立仓库为 `GoogleCloudPlatform/open-knowledge-format`，其规范明确标为 v0.2。早期资料常指向 `GoogleCloudPlatform/knowledge-catalog` 下的 `okf/SPEC.md`；不能仅按旧文章的字段实现当前格式。上游仓库同时提供生成 Agent 和可视化工具，它们是参考实现，不是使用 OKF 的前提。[上游 README 离线副本](上游规范/README.md)

| OKF 解决的事情 | OKF 不负责的事情 |
|---|---|
| 不同生产者和消费者交换知识文件 | 指定数据库、向量库、服务端或检索产品 |
| 记录文档类型、资源、来源与验证信号 | 自动保证知识真实、完整、实时 |
| 支持目录浏览、按需读取与文档交叉引用 | 规定所有公司的业务分类、领域本体 |
| 约定受认可计算的描述与核验接口 | 自动执行脚本，提供完整权限与运行时协议 |

不需要绑定某种模型、框架或 Google 服务。它也不替代 OpenAPI、Protobuf、Avro 等领域契约，而是可以描述或引用这些资产。

## 2. 核心术语与知识包结构

| 术语 | 含义 |
|---|---|
| Knowledge Bundle | 自包含、分层组织的知识目录，是分发单位 |
| Concept | 一个知识单元，由一份 Markdown 文档承载；可描述表、接口、指标、流程或抽象概念 |
| Concept ID | 相对 bundle 根目录的文件路径，去掉 `.md` 后缀 |
| Frontmatter | 文件开头以独立 `---` 行包围的 YAML 元数据 |
| Body | frontmatter 后的 Markdown 正文 |
| Link | 文档之间的标准 Markdown 链接 |
| Source／Provenance | 概念依赖的材料，以及这些材料形成的来源关系 |
| Actor | 记录生成者、验证者等身份的字符串约定 |
| Attested Computation | 带有受认可计算定义、执行与核验约定的独立概念 |

```text
bundle/
  index.md                 可选导航
  log.md                   可选变更记录
  business/
    refund-policy.md       Concept ID: business/refund-policy
  engineering/
    refund-api.md          Concept ID: engineering/refund-api
  computations/
    refund-count.md
  references/
    approved-change.md
```

以上目录分类是本库示例。OKF 不规定 `business/`、`engineering/` 或四类知识目录；生产者可以按领域、资产类型或任务组织。

**保留文件名只有 `index.md` 和 `log.md`**，在目录树任意层级都不能拿来作为普通 Concept。其他 `.md` 文件按 Concept 处理，必须提供 frontmatter。因此，把无 frontmatter 的 `README.md`、许可说明或随手笔记一起放入 bundle，会影响符合性；应转换为 Concept 或放在 bundle 外。

Bundle 可通过 Git 仓库、仓库子目录、ZIP 或 tar 包分发。Git 有助于版本管理，但正确性与审核仍需另外落实。

## 3. Concept 文档：最小格式与扩展

### 3.1 唯一始终必填的 frontmatter 字段

````markdown
---
type: Business Rule
---

# 退款规则

这里描述适用规则、来源与限制。
````

`type` 是非空的简短类型字符串。`Business Rule` 是自定义值，并非中央注册类型。消费者必须容忍未知类型；不能要求所有概念都属于固定枚举。

“只有 `type` 始终必填”指普通 Concept 的最低格式门槛。可选字段族出现时仍有内部约定；`Attested Computation` 还明确要求 `runtime`，见第 9 节。

### 3.2 基础字段

| 字段 | 要求 | 语义 |
|---|---|---|
| `type` | 始终必填 | 文档描述什么类型的概念 |
| `title` | 推荐 | 展示名；缺省时消费者可从文件名推导 |
| `description` | 推荐 | 一句话概要，供索引、预览与检索使用 |
| `resource` | 推荐，适用时提供 | 被描述资产的规范 URI；抽象概念不必绑定物理资源 |
| `tags` | 推荐 | YAML 字符串列表，提供跨目录分类 |
| 自定义键 | 允许 | 由生产者约定，消费者不得因不认识键而拒绝文档 |

消费者往返读写时应保留未知字段。扩展的兼容性不等于扩展的语义已被所有消费者理解。

**区分 `resource` 和 `sources[].resource`**：前者指出“本概念描述哪个资产”，后者指出“本概念依据哪些材料”。两者可以相同，也可以完全不同。

### 3.3 正文结构

正文可以自由组织，没有统一必填章节。规范建议使用标题、列表、表格与代码块；`# Schema`、`# Examples`、`# Computation` 在适用时有约定含义。不要把本库设计的“业务规则／验收／状态”模板写成 OKF 的强制章节。

## 4. 来源：`sources`、可信信号与逐条归因

```yaml
sources:
  - id: refund-change
    resource: /references/approved-change.md
    title: 退款期限变更记录
    author: human:example-reviewer
    last_modified: 2026-10-15T09:00:00+08:00
```

以上为字段教学示例，身份与记录均为虚构。

| `sources` 条目字段 | 要求／作用 |
|---|---|
| `resource` | 条目内必填；指向具体材料，也可表示无法直接打开的总体或范围描述 |
| `id` | 可选；正文引用该来源时应提供，作为稳定归因键 |
| `title` | 可选来源名称 |
| `author` | 可选来源作者信号 |
| `usage_count` | 可选使用次数信号，需结合使用窗口与使用行为解释 |
| `last_modified` | 可选，原始来源最后变更时间 |
| `usage_window` | 可在 `sources` 同级指定共同窗口 `{from, to}`，单条来源可覆盖 |

规范记录客观信号，不存储统一可信分数。查询执行次数、页面访问次数和主动查看仪表盘次数不能直接做精确横向排名；使用次数适合辅助判断活跃度和趋势，不能证明正确性。

逐条结论引用采用与 `sources[].id` 对应的 Markdown 脚注：

````markdown
目标退款期限为 14 天，尚待实现。[^refund-change]

[^refund-change]: 示例变更记录
````

脚注标签 `refund-change` 才是归因连接键，不是来源数组中的序号，也不是脚注说明文字。来源列表重新排序后，键仍可保持稳定。

来源指向另一 OKF Concept 时，消费者可以沿该概念的 `sources` 继续追溯。v0.2 没有另设通用 `derived_from` 字段来定义完整外部血缘，也不替代数据血缘系统。

## 5. 生成、验证与可信度层级

### 5.1 谁生成，与谁验证，是两回事

```yaml
generated:
  by: knowledge-builder/1.0
  at: 2026-10-15T09:00:00+08:00
verified:
  - by: human:example-reviewer
    at: 2026-10-15T10:00:00+08:00
  - by: process:example-contract-check
    at: 2026-10-15T10:05:00+08:00
```

该代码块只演示语法，不是本库实际审核记录。

- `generated` 记录当前内容如何产生，出现时内部的 `by` 必填；`at` 记录最后一次有意义的内容变化。
- `verified` 是验证事件列表，每条记录 `by` 与 `at`，表示曾将内容与来源或被描述资源核对。
- 只有一条验证时，也可写为单个 `{by, at}` mapping。消费者必须将其当作单元素列表。
- 内容变更时间与验证时间独立：内容可以更新但未重新验证，也可以未改写而重新核对事实。

所有表示时间戳的字段采用带显式 UTC 偏移的 ISO 8601 日期时间。只有日期或缺少时区的时间，不应当作规范要求的时间戳。

### 5.2 Actor 的规定形式

| 场景 | 形式 | 示例 |
|---|---|---|
| Agent 或工具 | `<producer>/<version>` | `knowledge-builder/1.0` |
| 人 | `human:<id>` | `human:example-reviewer` |
| 自动流程 | `process:<id>` | `process:example-contract-check` |

手工撰写或人工确认必须用 `human:` 前缀来正确表达该身份，因为可信度分类依赖该前缀。不得为了获得更高标签而伪造人工验证。

### 5.3 可信度由消费者推导

| `verified` 情况 | 推导层级 |
|---|---|
| 未提供 `verified` | `unverified` |
| 验证者全部不是 `human:` | `machine-confirmed` |
| 至少有 `human:<id>` 验证者 | `human-reviewed` |

这是咨询性信号，不是访问控制。没有验证信息的 Concept 仍可被消费，不能仅因缺少可选字段族就判格式无效。

**本库分析**：`human:` 字符串本身不认证真人身份，也不证明其有审批权；验证事件必须结合受信任的身份、流程和审计系统。内容更新后保留旧验证记录，按简单字段仍可能推导为 human-reviewed，因此消费者还应显示验证日期与版本适用性，不能将标签当成“当前版本已批准”。

## 6. 生命周期与时效

| 字段／取值 | 规范语义 | 应避免的误解 |
|---|---|---|
| `status: draft` | 未评审、可能不完整 | 不等于已批准待上线 |
| `status: stable` | 可供消费；未指定 `status` 时默认如此 | 不等于 human-reviewed 或已部署 |
| `status: deprecated` | 为历史和链接保留，已非现行内容 | 不意味着立即删除文档 |
| `stale_after` | 当 `now >= stale_after`，判定为过期 | 不应解释成从读取时刻开始计时的 TTL |

`generated.at` 是内容变更时间；`sources[].last_modified` 是来源变更时间；`verified[].at` 是验证事件时间；`stale_after` 是时效截止点。它们不能互换。

规范没有自动检测外部变更的服务，也没有定义本库需要的“待实现／已合并／已部署”等状态。可以扩展，但应另写语义说明，不要塞进 `status` 的三个约定值中冒充标准含义。

## 7. 路径、链接与图关系

Concept ID 来源于文件路径，例如 `business/refund-policy.md` 对应 `business/refund-policy`。移动或改名会改变该 ID；若业务需要永久身份，应自行维护别名或映射，不能把本库稳定主题 ID 与 OKF 路径 ID 等同。

支持两种文档链接：

- 以 `/` 开头的 **bundle 根相对路径**，例如 `/business/refund-policy.md`，是推荐形式。
- 相对当前文档的路径，例如 `../business/refund-policy.md`。

这里的 `/` 不是操作系统根目录，也不是本知识库仓库根目录，除非整个仓库本身恰好就是该 bundle。普通 Markdown 渲染器可能按网站根路径解释它，消费者需要适配；教学样例采用相对路径，便于直接在本地阅读。

`resource`、`sources[].resource`、`computation`、`executor.resource`、`attester.resource` 可表示 URL、bundle 根相对路径或相对路径。来源的范围描述例外，它不一定是可访问路径。

链接表达的关系种类由周围正文说明，不是链接语法本身提供类型。图视图通常把链接当成有向、无类型关系；不能把普通链接自动等同于本体中的已验证业务关系。

**消费者必须容忍断链**，因为目标可能尚未编写。这是 OKF 的宽容消费原则；团队仍可在发布门禁中要求关键链接完整，两种检查需要分别报告。

`references/` 是镜像外部材料、运行说明或代码的命名惯例，并非保留目录或必需目录。外部内容的权限和许可证不会因引用而消失。

## 8. 索引和变更记录

### 8.1 `index.md`

可在任意目录存在，帮助先浏览再按需打开。正文使用分组标题与链接列表，描述建议取自 Concept 的 `description`。不存在时，消费者可以临时生成。

通常无 frontmatter。**唯一例外：bundle 根 `index.md` 可以在 frontmatter 声明 `okf_version: "0.2"`**；子目录索引不能照搬这一例外。

````markdown
---
okf_version: "0.2"
---

# 业务知识

* [退款规则](business/refund-policy.md) - 示例目标规则及其来源。
````

### 8.2 `log.md`

可在任意层级记录对应范围的变更，无 frontmatter。按日期分组，最新在前；日期标题必须采用 `YYYY-MM-DD`。条目为文字，开头的 Update／Creation 等粗体标签只是惯例。

日志不替代 Git 历史、审批记录或业务审计系统。

## 9. Attested Computation：对“这次怎么算的”提供核验入口

普通来源追溯回答“定义依据什么”，Attested Computation 回答“这个结果是否按被认可的计算产生”。每个受认可计算作为独立 Concept，类型精确写为 `Attested Computation`，由指标、报表等文档链接复用。

### 9.1 契约字段

| 字段 | 作用与要求 |
|---|---|
| `runtime` | 该类型明确要求；说明计算运行方式及参数绑定语义，如 `postgres`、`bigquery`、`dbt`、`python` |
| `parameters` | 可填的具名参数列表，每项描述 `name`、`type`、`required` |
| `computation` | 可选路径；指定外部计算文件，替代正文内嵌计算 |
| `executor.resource` | 指向运行说明或执行代码 |
| `executor.receipt` | 声明一次运行需返回哪些证据字段 |
| `attester.resource` | 指向读取回执并返回判定的确定性代码，不使用 LLM 作此核验 |

除 `runtime` 的明确条件必填外，不能将所有这些字段擅自提升为普通 Concept 的必填项。要实现有效的计算核验，则需实际落实计算、执行回执及核验器之间的契约。

### 9.2 计算定义放在哪里

二选一：在正文 `# Computation` 下提供一个 fenced code block；或通过 `computation` 指向文件，并省略正文内嵌计算代码块。

````markdown
---
type: Attested Computation
title: 示例退款申请数量
runtime: postgres
parameters:
  - {name: start_at, type: string, required: true}
  - {name: end_at, type: string, required: true}
executor:
  resource: ../references/run-refund-count.md
  receipt: [execution_id, executed_sql, result]
attester:
  resource: ../references/attest-refund-count.md
status: draft
---

# Computation

```sql
SELECT COUNT(*) AS refund_count
FROM demo_refund_requests
WHERE requested_at >= :start_at AND requested_at < :end_at;
```
````

这是教学契约。参数占位符由实际消费者和驱动绑定，不声称所有 PostgreSQL 客户端都直接支持此占位语法。executor 和 attester 的目标文件在教学包中只描述待实现接口，尚无可运行核验器。

### 9.3 消费者如何处理

规范的说明性流程为：发现计算→加载定义→填参数→执行→核验→展示判定或处理失败。

关键约束是 **Agent 只能提供已声明参数的值，不得自行编写或修改受认可计算**。消费者负责生成绑定后的可执行产物，attester 独立重建相同绑定并核对实际执行证据。不能只比较 Agent 自己回传的 SQL 字符串，就声称证明数据库确实执行了它。

回执是运行时产物，不存入 bundle。核验应确认计算来源一致，并通过权威运行记录回读结果，检查展示值是否一致。规范的说明性流程建议失败时不展示为可信结果，定义已过期时警告或拒绝。

### 9.4 `verified` 与单次核验不同

- `verified` 核对计算**定义**与来源／政策的关系，记录在知识包中。
- attestation 核对**单次运行**是否遵循该计算，证据属于运行时。

过期定义也可能成功运行并通过执行一致性检查；新验证的定义也不能免除本次运行检查。

v0.2 尚未完整规定回执和 verdict 的传输格式、attester ABI、沙箱、缓存及代码打包标准。不能把 OKF 描述成已经提供通用计算执行平台、加密签名体系或全链路审计产品。

## 10. 符合性、宽容消费与版本迁移

### 10.1 最低符合性

依规范第 11 节，bundle 最低要求：非保留 `.md` 都有可解析 YAML frontmatter；frontmatter 有非空 `type`；出现的保留文件遵守索引与日志结构。

使用来源、可信、生命周期和计算字段族时，生产者应按相应章节约定填写；消费者必须处理单条 `verified` mapping，不能因缺少可选字段、未知类型、额外键、断链或缺少索引而拒绝。

因此要区分：**格式可读、团队发布质量达标、执行经过授权、业务事实正确**。本库严格链接检查属于自己的质量门禁，不应被误称为 OKF 对断链的禁止。

### 10.2 从 v0.1 到 v0.2

| 项目 | v0.1 | v0.2 |
|---|---|---|
| 内容更新时间 | `timestamp` | `generated.at`，并记录生成者 |
| 来源列表 | 正文 `# Citations` | frontmatter `sources`，逐结论用稳定 ID 脚注关联 |
| 来源信号 | 未形成该字段族 | author、usage_count、last_modified、usage_window |
| 验证 | 无该统一字段族 | `verified`，派生可信度层级 |
| 生命周期 | 无该统一字段族 | `status`、`stale_after` |
| 受认可计算 | 未定义该机制 | Attested Computation 及相关字段 |

**规范自称 minor 升级，同时明确列出两项有意的 breaking changes**：替代 `timestamp` 和正文 `# Citations`。不能将它简化为“完全没有破坏性变更”。新消费者可在没有 `generated` 时回退旧 `timestamp`，也可读取旧引用章节；旧内容可被消费，不代表已补齐 v0.2 的来源和验证信息。

Bundle 可在根索引声明版本；不认识版本的消费者应尝试尽力消费。后续版本规则以 major／minor 区分破坏性与兼容性变化，仍需检查具体变更说明。

## 11. 与 RAG、LLM Wiki、知识图谱和本体的关系

以下为本库自主分析。

| 概念 | 主要问题 | 与 OKF 的组合方式 |
|---|---|---|
| LLM Wiki | 怎样持续整理与维护知识？ | OKF 可作为 Wiki 产物的交换约定 |
| RAG | 怎样找到并向模型提供证据？ | 索引正文与 frontmatter，按来源、类型和时效辅助选择 |
| 知识图谱 | 怎样查询具体实体与关系？ | 从文档链接构建导航图，业务语义关系需额外建模和核验 |
| 知识本体 | 概念、关系、约束和行为如何共享语义？ | 用 Concept 记录或引用本体资产，OKF 本身不提供 OWL 或业务规则推理语义 |
| 行动与工具接口 | 如何在权限内执行？ | 消费者另外接入工具和执行控制，文件引用不授予执行权限 |

OKF 不保证“更低成本／更高准确率”；应在固定任务、资料与版本条件下比较效果。类型、标签与链接也不会自动建立企业统一语义。

## 12. 同时服务产品、业务与 AI Coding

以下为本库设计建议，不是 Google 规定的目录。

| 使用者与任务 | 主要需要的知识 | 应核对的属性与事实 |
|---|---|---|
| 产品人员定义新能力 | 用户问题、规则、体验要求、验收 | 是否已批准、适用范围、目标生效时间 |
| 业务人员询问当前规则 | 现行规则、例外、功能说明 | 来源、审核、当前产品与环境版本 |
| Coding Agent 实现改动 | 目标、契约、设计、实现约束 | 当前代码、依赖、兼容性与验证结果 |
| 运维与交付 | 发布、观察、恢复与故障处理 | 部署记录、环境、时间与实际运行证据 |

目录按知识内容组织，使用者通过标签和入口形成不同视图。规则要求与实现情况应关联但分别描述；产品交互要求与前端实现说明也应分别维护。`audience`、`knowledge_role`、`implementation_status` 等若采用，均是本库扩展，**不是 OKF 标准字段**。

## 13. 本仓库如何采用：先做独立样包

本库当前使用 `topic.json`＋摘要／正文＋生成的 `catalog.json`，不自动等同于 OKF。建议先输出独立 bundle，不把全库正文直接宣布为已合规。

| 当前资产 | 导出到 OKF 时的处理建议 |
|---|---|
| 稳定主题 ID | 作为自定义键保留，同时另算 OKF 路径 ID |
| `kind` | 映射成合适的 `type`；不存在自动一一对应 |
| 标题与摘要 | 映射到 `title`、`description` |
| 本地来源说明页 | 拆出可定位的 `sources`，保留原来的证据边界 |
| general／reference／example | 保留为独立扩展；不能直接映射成 stable／draft／deprecated |
| `requires`／`related` | 生成说明关系的文档链接，依赖语义仍由消费者另行实现 |
| catalog 与加载规则 | 可生成 OKF `index.md`，继续按层读取 |

扩展字段和转换语义要形成明确约定；导出时记录来源版本并做更新、删除与链接检查。本次仅新增解读、上游快照和教学 bundle，未改本库 schema、解析器或全库格式。

## 14. 实施检查与常见误区

| 检查 | 要问的问题 |
|---|---|
| 结构 | 每个 Concept 有 YAML 与 `type`？保留文件是否按约定？ |
| 语义 | 类型是否清楚，来源是否可定位，关系是否有文字说明？ |
| 时效 | 是否区分内容变更、来源变更、验证和过期？ |
| 可信 | 验证记录真实且能关联版本吗？是否把标签当作认证？ |
| 消费 | 是否容忍未知字段和类型，按需加载而非全量注入？ |
| 计算 | 参数、实际产物、权威回执和核验器是否对应？ |
| 授权 | 文件和来源是否允许当前用户读取，运行是否有独立授权？ |

常见错误包括：把有 frontmatter 的文件都当合规；把 `stable` 当人工审核；把 `generated.by: human:...` 当作已经验证；把 `source: intent/derived` 当作 OKF 规定；把断链容忍当成无需维护；把参考 Agent 或图查看器当格式必需组件；把 executor 的路径当作可以立即执行的指令。

未登记来源、未验证与已过期内容并非同一状态。消费者可以显示风险与限制；实际高风险任务是否可使用、是否可执行，仍由组织策略和授权决定。

## 15. 本地阅读清单

- [摘要](摘要.md)：快速判断用途与限制。
- [教学案例](案例-业务问答与AI-Coding.md)：跨产品、业务、研发与交付的样包阅读路线。
- [教学 bundle 根索引](示例/bundle/index.md)：可直接查看的 OKF 文件集合，所有业务内容均为虚构。
- [原始 SPEC.md](上游规范/SPEC.md)：完整英文规范，字节保持不变。
- [上游 README.md](上游规范/README.md)：参考实现使用方式，非本次运行记录。
- [Apache-2.0 许可证](上游规范/LICENSE.md)与[快照清单](上游规范/manifest.json)：上游版本及文件哈希。
- [来源与适用边界](来源与适用边界.md)：区分上游事实、设计建议和未验证能力。

[返回建设框架](../README.md) · [返回知识库](../../README.md)
