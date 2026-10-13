# Google Cloud：RAG Engine 知识供给方案

## 提供方及定位

Google Cloud 的 RAG Engine 为大模型提供知识摄取、索引与检索框架。本条保留常见检索名称“Vertex AI RAG Engine”，但截至查阅日，原入口已重定向到 Gemini Enterprise Agent Platform 的 RAG Engine 页面；名称与 SDK 应按当前文档核验。本案例研究公开方案，不代表 Google 内部实践。[当前概述](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview)

## 官方确认能力

- 官方描述从本地文件、Cloud Storage、Google Drive 摄取，再转换、嵌入、建立 corpus、检索和生成的流程。[概述](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview)
- 快速入门演示创建 corpus、导入、配置分块和重叠、直接检索上下文，以及通过检索工具调用模型；也展示返回数与距离阈值。[快速入门](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-quickstart)
- 支持 VPC Service Controls 与 CMEK，但明确不支持 data residency 和 AXT 控制；选定资源区域不等于获得完整驻留承诺。[安全边界](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview)

## 推荐构建流程（研究建议）

1. 先确认区域、项目资格和安全约束，再决定接入。对必须具备驻留承诺的数据，先审查合同及控制要求，不仅凭部署位置判断适配。
2. 将知识治理前置：进入 corpus 前确定负责人、有效版本、许可范围和保留期限。优先选批准发布的手册，避免共享盘中重复和失效材料直接成为证据。
3. 按业务与敏感等级划分 corpus。将标题、文档 ID、原始位置、有效期和分类作为追踪信息；切分粒度应匹配典型问答证据单位，不能照抄示例参数。
4. 先验收直接检索：检查片段与原文一致性，覆盖短问、跨段问题、术语别称和无答案问题；逐步调整返回数与阈值，保存配置及测评结果。
5. 再接入模型工具调用，并展示证据位置。应用端检查回答是否被资料支持，设置无证据拒答、冲突资料提示和人工反馈。模型能调用 corpus 不代表回答一定可信。
6. 发布后建立导入状态检查、删除复验和权限回归。抽查失效资料是否仍可检索、撤权用户是否仍能通过缓存或旧引用访问，错误时回退至证据展示。

## 适用场景

研究判断：适合已采用 Google Cloud、需要将文件接入模型并保留检索配置控制的团队。开发文档助手和受控产品问答适合作为初始范围。若目标是全员知识门户或编辑审批平台，应额外评估工作流，不能从 RAG 接口推断完整知识管理能力。

## 限制与治理

区域发布状态不同，部分美国区域对新项目有 allowlist 条件。实施前检查可用性，不能将示例区域当作普遍可用承诺。[区域限制](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview)

资源角色和导入授权不应推断为源文件逐用户权限自动继承。本文未验证 Google Drive 原始 ACL 在最终回答中的效果；应用仍应定义租户隔离、访问范围和引用授权。内容审批、版本冲突处置、同步时限和审计保留同样属于建设责任。


验收时建议同时保留正常问题、无答案问题和越权问题三类题集，并标注文档版本。更新后重跑旧问题，检查引用是否漂移；对不合格回答记录检索片段与生成输出，交由资料负责人和应用负责人分别处理。这是研究建议，并非产品默认提供的业务流程。

## 可借鉴点

以 corpus 为独立管理和验收的集合，让检索先于生成验证，可缩小排查范围。对本库，可从领域和主题 ID 组织受控资料集，保留版本与来源，给不同 AI 任务提供加载范围。云索引作为派生资产，原始知识及其边界仍保留在可审查文件中。

资料查阅日期：2026-10-12；未部署实测。完整证据及限制见[来源与适用边界](来源与适用边界.md)。
