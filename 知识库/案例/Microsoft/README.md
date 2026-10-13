# Microsoft：Azure AI Search 知识检索与 RAG

## 提供方及定位

Microsoft 提供的 Azure AI Search 可作为知识库的检索层，应用将检索证据交给模型生成回答。本案例研究公开建设方案，不代表微软内部知识库实践，也不构成跨厂商最佳排名。Microsoft Foundry 是更广的 AI 应用平台；当前文档指出 Foundry IQ 的知识层由 Azure AI Search 支撑，不能将平台、检索服务和完整业务知识管理系统视为同一产品。[官方 RAG 概述](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)

## 官方确认能力

- 经典 RAG 可组合关键词、向量和语义重排；agentic retrieval 通过子查询规划与多源检索返回结构化证据，其中 LLM 查询规划仍标为预览。选型要区分这些路径。[官方 RAG 概述](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
- 集成向量化串联 indexer、skillset 和索引，在入库时分块与生成向量，在查询时由 vectorizer 转换文本；索引和查询需要匹配嵌入模型。[集成向量化](https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization)
- 无法采用内建 ACL 的场景可以保存用户／组标识，再用查询过滤裁剪结果。该过滤模式中的标识只是字符串，本身不认证调用者。[安全过滤模式](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search)

## 推荐构建流程（研究建议）

1. 先界定问题范围：从产品文档、制度或操作手册中选一个集合，确定负责人、有效日期和允许访问群体。先剔除失效材料，再进行向量化，避免放大源数据矛盾。
2. 建立可追溯内容模型：文档 ID、章节、原始链接、版本和权限标识随每个片段保存。按标题层级切分，抽样检查跨页表格、扫描件和断裂段落；不要把“导入成功”当作知识完整。
3. 用经典 RAG 建立基线，分别评估关键词、向量和组合检索。涉及精确型号、条款号的问题与自然语言问题应分别统计，再决定是否加入重排和复杂查询规划。
4. 在后端验证用户身份，生成不可由客户端任意覆盖的检索范围。对引用页面也执行权限检查，并用普通用户、管理员和离职账号测试访问边界。
5. 回答展示证据标题、版本和原文入口；没有足够证据时拒答或转人工。把误引、过期回答和漏检反馈交给内容负责人，形成更新与复验闭环。

## 适用场景

作为研究判断，适合 Azure 基础设施较完善、需要精细索引设计和可解释检索的团队。研发文档检索、产品支持、制度问答可先采用经典路径；跨资料组合的问题可在验证收益后评估 agentic retrieval。若主要诉求是多人编辑、审批发布和知识社区，还需配套内容管理系统。

## 限制与治理

原生提供检索、向量化及部分权限支持；源系统权限继承取决于数据源和接入模式，不能承诺任意连接器自动继承。安全过滤必须覆盖每次检索，隐藏字段也不能替代授权。[安全过滤模式](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search)

应用仍需自行落实内容责任、审批、删除同步、拒答政策、引用可达性和审计保留。索引与在线查询共享模型配额时应核算资源；内建重试不能解决配额耗尽。接外部模型的网络路径也须另行核验。[集成向量化限制](https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization)

## 可借鉴点

值得借鉴的是把知识内容、索引和回答分层管理：同一份内容可以支撑人工检索和 AI 问答，召回缺陷与生成缺陷可以分开定位。对本仓库而言，应保留原文路径及稳定主题身份，将来源和适用边界作为检索元数据，而不是只保存向量或最终答案。

资料查阅日期：2026-10-12；未部署实测。完整证据及限制见[来源与适用边界](来源与适用边界.md)。
