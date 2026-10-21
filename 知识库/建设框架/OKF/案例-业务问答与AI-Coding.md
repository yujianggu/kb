# 教学案例：同一份 OKF 知识包支持业务问答与 AI Coding

**本库虚构教学／设计示例**。不存在真实客户、批准需求、生产数据库或部署记录。样包用于阅读结构和字段，不用于执行操作。

## 1. 场景与样包

假设产品人员提出将退款期限从 7 天调整为 14 天，但尚未实现。业务人员想知道现在能否按 14 天处理；Coding Agent 需要知道该改什么；运维人员需要知道何时对哪个环境生效。

[打开样包根索引](示例/bundle/index.md)。仅 `示例/bundle/` 是教学 OKF bundle；上层中文解读、许可证与英文规范快照不属于这个 bundle。

```text
bundle/
  index.md
  log.md
  business/refund-policy.md
  architecture/refund-boundary.md
  engineering/refund-api.md
  operations/refund-release.md
  metrics/refund-count.md
  computations/refund-count.md
  references/
    approved-change.md
    run-refund-count.md
    attest-refund-count.md
```

各 Concept 使用 YAML frontmatter，未添加 `verified`，不表示真实人工核验。`type` 是文档类型；`knowledge_role`、`audience`、`implementation_status` 等为演示扩展。

## 2. 产品与业务阅读路线

1. 从索引进入[目标规则](示例/bundle/business/refund-policy.md)，确认这是待实现的要求。
2. 沿 `sources` 与脚注回到[虚构需求记录](示例/bundle/references/approved-change.md)。
3. 查看[交付检查](示例/bundle/operations/refund-release.md)，发现没有真实部署和运行证据。
4. 回答应明确“样例提出 14 天目标，但无法据此确认当前产品已生效”，不能把目标规则当作当前产品事实。

产品人员可在业务知识中维护用户问题、范围、例外与验收条件；页面的组件契约和技术实现通过工程知识关联，避免两套事实副本。

## 3. AI Coding 阅读路线

1. 读取目标规则，明确验收与例外仍有哪些待确认项。
2. 读取[边界设计](示例/bundle/architecture/refund-boundary.md)与[接口说明](示例/bundle/engineering/refund-api.md)。
3. 回到实际项目读取当前代码、接口契约与测试；本样包没有这些真实事实，不能直接据此改生产代码。
4. 生成候选变更与测试，按项目流程验证和审核。
5. 分别记录实现、合并、部署和环境生效，再更新知识及其来源版本。

目录有助于导航，不能替代代码核查。`status: stable` 即使存在，也不足以证明任何功能已经部署。

## 4. 计算与运行证据

[退款申请数量指标](示例/bundle/metrics/refund-count.md)链接到独立的 [Attested Computation](示例/bundle/computations/refund-count.md)。

其中只有演示 SQL、参数与接口约定：[executor 说明](示例/bundle/references/run-refund-count.md)和 [attester 说明](示例/bundle/references/attest-refund-count.md)均明确尚未实现。样包没有 receipt、判定或查询结果。

正式实现时，消费者需要安全绑定参数、执行被认可计算、获取权威运行记录，并由确定性代码核对实际产物及结果。不要把示例接口文档的存在当成核验已完成。

## 5. 可验证与不可验证的事情

| 可做的文件检查 | 不能由该检查证明 |
|---|---|
| 非保留 Markdown 含 frontmatter 和 `type` | 内容真实或通过审核 |
| YAML 可解析，路径能定位 | 被引用来源可信或可访问 |
| 生成时间与状态字段格式正确 | 目标规则当前已在系统中生效 |
| 计算字段可读取 | 数据库执行成功或单次运行已核验 |

把这些限制保留在教学样包中，正是为了避免将“格式已结构化”误认为“业务已可信、行动已授权”。

[返回完整解读](README.md)
