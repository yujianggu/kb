---
type: Attested Computation
title: 退款申请数量计算（教学）
description: 演示 PostgreSQL 计算定义与尚未实现的核验接口。
tags: [computation, teaching]
status: draft
runtime: postgres
parameters:
  - {name: start_at, type: string, required: true}
  - {name: end_at, type: string, required: true}
executor:
  resource: ../references/run-refund-count.md
  receipt: [execution_id, executed_sql, result]
attester:
  resource: ../references/attest-refund-count.md
generated: {by: kb-teaching/1.0, at: "2026-10-15T09:00:00+08:00"}
---

# Computation

```sql
SELECT COUNT(*) AS refund_count
FROM demo_refund_requests
WHERE requested_at >= :start_at AND requested_at < :end_at;
```

表、字段和参数均为虚构。参数是日期时间字符串，实际消费者需校验格式、时区和范围，并使用相应驱动的参数绑定；占位符不是 PostgreSQL 各客户端通用语法。禁止字符串拼接。

本概念只演示契约结构，未连接数据库；执行器和确定性核验器尚未实现，没有 receipt 或 attestation 结果。
