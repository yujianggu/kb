# 基础知识库

供多个项目复用的知识文档库。按“领域 → 分类 → 主题摘要 → 正文 → 案例或来源”逐级读取；当前内容包含本体知识文档，不是可直接导入运行时的本体模型包。

## 从当前任务开始

| 任务 | 阅读入口 | 机器索引 |
|---|---|---|
| 理解或设计本体、研究表示格式和产品实现 | [本体](本体/README.md) | [本体索引](本体/catalog.json) |
| 分析问题、决策、学习、表达或复盘 | [思维模型](思维模型/README.md) | [思维模型索引](思维模型/catalog.json) |
| 梳理中华历史，阅读佛、道、儒的思想与历史语境 | [中国瑰宝](中国瑰宝/README.md) | [文化索引](中国瑰宝/catalog.json) |
| 研究企业经营机制、关键决策与案例 | [企业经营研究](企业经营研究/README.md) | [企业研究索引](企业经营研究/catalog.json) |
| 准备业务或技术汇报 | [汇报模板](汇报模板/README.md) | [模板索引](汇报模板/catalog.json) |
| 系统学习英语，规划阶段并练习听说读写 | [英语学习](英语学习/README.md) | [英语索引](英语学习/catalog.json) |

首次接入读取本页和[加载约定](LOADING.md)。程序入口为 [catalog.json](catalog.json)，只包含领域入口和可选扩展，不包含全部主题正文。

## 按 ID 获取文件清单

工具使用 Python 3.9 及以上版本，无第三方依赖：

```bash
python3 scripts/kb.py resolve thinking.five-whys
python3 scripts/kb.py resolve ontology.modeling --layer detail
python3 scripts/kb.py resolve reporting.business --layer detail --max-bytes 20000
```

工具输出相对于知识库根目录的文件清单及大小；由调用方读取选中的文件。不会自动读正文、渲染图片、获取子仓库或展开相关推荐。

## 多项目复用与维护

- 项目固定知识库提交版本，通过稳定主题 ID 引用内容，具体接入见[加载约定](LOADING.md#跨项目引用)。
- [公司资料](本体/公司业务/README.md)为显式选用的扩展，不进入通用知识索引。
- 新增或调整主题时维护 `topic.json`，然后运行 `python3 scripts/kb.py build` 与 `python3 scripts/kb.py check`。
- [贡献与结构维护](CONTRIBUTING.md)说明字段、路径和来源边界；生成的索引不要手工修改。
