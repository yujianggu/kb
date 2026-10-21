---
type: Architecture Decision
title: 退款职责边界（教学）
description: 服务端校验与页面反馈的职责示例。
tags: [architecture, teaching, refund]
status: draft
generated: {by: kb-teaching/1.0, at: "2026-10-15T09:00:00+08:00"}
sources:
  - id: target-policy
    resource: ../business/refund-policy.md
---

# 候选设计

页面表达用户操作和反馈，服务端独立校验资格、权限与状态。前端隐藏按钮不能代替服务端检查。

这是面向[目标规则](../business/refund-policy.md)的教学设计，不是从真实代码提取的系统现状。接口约定见[工程说明](../engineering/refund-api.md)。
