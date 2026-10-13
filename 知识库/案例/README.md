# AI 大模型知识库构建案例

按**方案提供方／公司或提出者**组织。当前收集十家提供方的公开技术方案，以及 Andrej Karpathy 的 LLM Wiki 模式，查阅日期：2026-10-12。案例指“提供方或作者的构建方案”，不表示已验证的客户成功案例或内部系统。

[领域入口](../README.md) · [机器索引](catalog.json) · [方案对比与选型](方案对比与选型.md)

## 按提供方阅读

| 提供方／公司或提出者 | 本次研究方案 | 阅读重点 |
|---|---|---|
| [阿里巴巴／阿里云](阿里巴巴/README.md) | 百炼知识库与知识检索服务 | 托管构建、检索服务和中国站／国际站边界 |
| [Microsoft／微软](Microsoft/README.md) | Azure AI Search 的 RAG 方案 | 检索与应用的职责、数据权限 |
| [AWS／亚马逊云科技](AWS/README.md) | Amazon Bedrock Knowledge Bases | 托管流程与不同管理方式的区别 |
| [Google Cloud](Google-Cloud/README.md) | RAG Engine | 语料导入、检索与模型接入，以及产品命名变化 |
| [Dify／LangGenius](Dify/README.md) | 知识库与 RAG 工作流 | 应用编排、检索配置和部署责任 |
| [RAGFlow／InfiniFlow](RAGFlow/README.md) | 文档解析与 RAG 引擎 | 复杂文档处理、召回与回答链路 |
| [Elastic](Elastic/README.md) | Elasticsearch 检索底座 | 混合检索与自建 RAG 的职责 |
| [Pinecone](Pinecone/README.md) | 向量检索与 RAG 组件 | 索引、检索及应用侧数据治理 |
| [Weaviate](Weaviate/README.md) | 混合检索与生成式集成 | 检索底座、模型集成与自建边界 |
| [LlamaIndex](LlamaIndex/README.md) | 数据接入与 RAG 构建框架 | 索引／检索编排和自选后端 |
| [Andrej Karpathy](Andrej-Karpathy/README.md) | LLM Wiki 持续知识整理模式 | 原始资料、整理层、维护约定和受控积累 |

## 研究口径

“最佳”按任务适配度比较，不设未经同条件测试的性能排名。入选依据是有可读取的官方技术资料、覆盖有代表性的构建方式，并能明确其负责的环节。未进行穷尽市场检索，未断言其他提供方较差。

- **官方能力**：就近引用实际读取的官方文档；不依据宣传语给出效果保证。
- **研究建议**：语料整理、配置选择、测试和运维流程，明确是本库的建议。
- **效果证据**：本次未部署、未进行统一基准测试；不比较准确率、吞吐或总拥有成本的数值。
- **版本范围**：服务、API、套餐和地域可能变化，正式实施时重新核验；价格不作为静态结论保存。

各目录包含 `README.md` 正文、`摘要.md`、`来源与适用边界.md`、`topic.json`。`kind: reference` 表示资料类型，`status: general` 不表示经过实测认证；公司方案采用 `scope: company`，通用模式采用 `scope: general`，均保留原作者及证据边界。按需阅读，不自动展开全部案例。
