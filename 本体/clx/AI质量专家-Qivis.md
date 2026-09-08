# AI 质量专家（Qivis）

> 从 [LI-TQM 平台架构本体](./LI-TQM-平台架构本体.md) 中独立整理，保留原有能力清单、本体建模建议和权限边界。

LI-TQM 平台架构图中列出的 AI 质量专家能力包括：

```text
AI 降噪
数据互联
能力集成
知识提炼
Skill 生成
工单轨迹
工单聚类
Benchmark 评测
数据集拆分
发布生效
```

建议将 AI 质量专家建模为受治理的 `AIQualityExpert`，而不是普通聊天机器人：

```yaml
AIQualityExpert:
  key: expertId
  properties:
    - name
    - modelVersion
    - promptVersion
    - allowedDataScopes
    - allowedTools
    - approvalMode
    - evaluationStatus
    - publishedAt
```

AI 质量专家可执行的典型 Function：

```text
deduplicateQualityProblems
clusterSimilarProblems
extractRootCauseCandidates
retrieveLessonsLearned
evaluateBenchmark
```

可调用的 Action 必须单独授权，例如：

```text
CreateProblemDraft
AssignProblemOwner
RecommendContainment
SubmitRootCauseAnalysis
PublishQualityKnowledge
```

AI 的推荐和正式行动应保持分离：AI 可以形成草稿或建议，但涉及停线、冻结批次、车辆放行和召回的动作必须经过明确的权限和审批。
