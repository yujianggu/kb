# AWS：Amazon Bedrock Knowledge Bases

## 提供方及定位

AWS 提供 Amazon Bedrock Knowledge Bases，为大模型应用接入私有知识。本案例研究公开建设方案，不代表 AWS 内部实践。当前官方区分 Managed 与 Customer-managed 两类：前者托管基础设施，后者允许用户管理向量库与处理配置；两者能力不可混用。[官方总览](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)

## 官方确认能力

- Managed 路径提供多模态摄取、智能解析和 agentic retrieval，对支持的连接器提供文档 ACL 过滤；Web Crawler 不包含该 ACL 能力。Customer-managed 路径需管理相关存储和配置。[官方总览](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- 基础 RAG 将文档块转换为嵌入并关联原始文档，查询时取回相关片段作为上下文。[工作原理](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-how-it-works.html)
- Retrieve 可独立取回证据，RetrieveAndGenerate 组合检索与生成；可配置返回数和元数据过滤。混合检索依赖支持的向量库与可过滤文本字段。[查询配置](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html)
- 服务角色需按模型、数据源与存储配置访问权限。[角色权限](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-permissions.html)

## 推荐构建流程（研究建议）

1. 明确知识对象与访问边界：先选审核过的材料集合，记录所有者、更新时间、有效状态和授权范围。历史版本保留独立标签，避免默认同时参与回答。
2. 按责任分工选路径：希望降低维护时评估 Managed；已有向量库、特定解析要求或更细存储控制时评估 Customer-managed。先列出必要权限、区域和格式要求。
3. 小样本比较解析与切分：包含普通段落、长表格、扫描件和冲突版本。检查片段能否独立解释、引用能否回到正确源文件；为摄取失败建立处理列表。
4. 先验收检索，再接生成；分别衡量证据召回率、回答忠实度和引用正确率。参数变更一次只改一个因素，保留可复现题集及配置。
5. 后端验证身份并强制访问范围；测试未授权问题、撤权和删除后的结果。前端不应凭任意知识库 ID 就可访问资料，服务角色也应仅获得必要权限。
6. 建立同步与退出流程：记录摄取完成时间，对失败任务报警。迁移或销毁时检查源副本、索引、日志和备份的保留状态。

## 适用场景

研究判断：适合已使用 AWS、希望通过统一接口向大模型供应企业文档证据的团队。产品问答、技术支持和制度助手可从受控集合起步。跨记录精确聚合或实时事务查询应另评估结构化接口，不把文档向量检索视为所有知识需求的替代。

## 限制与治理

原生支持检索与生成组合，但后端差异不可忽略。不能承诺所有向量库均支持混合检索；元数据过滤须检查类型与操作符。[配置边界](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html)

内容质量、审批、有效版本及无证据拒答仍需自行治理。Managed 的 ACL 不应推断为任意来源都自动继承；Customer-managed 不能套用其权限承诺。[类型边界](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) 上线前应测试撤权、删除同步、引用打开授权和租户隔离。


验收时建议同时保留正常问题、无答案问题和越权问题三类题集，并标注文档版本。更新后重跑旧问题，检查引用是否漂移；对不合格回答记录检索片段与生成输出，交由资料负责人和应用负责人分别处理。这是研究建议，并非产品默认提供的业务流程。

## 可借鉴点

将证据检索与回答生成独立验收，能判断错误来自资料缺失、召回失败还是模型越界。对本知识库，稳定主题 ID、来源入口和适用边界可成为内容供给契约；云服务负责检索，内容维护责任仍由知识负责人承担。

资料查阅日期：2026-10-12；未部署实测。完整证据及限制见[来源与适用边界](来源与适用边界.md)。
