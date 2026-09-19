# 按需加载约定

本约定面向引用本库的项目、工具及 AI 助手。它控制进入任务上下文的内容；不要求仅下载这些文件，也不意味着引用本库后所有工具会自动遵守。消费项目必须显式接入本约定或解析工具。

## 分层与停止条件

| 层级 | 文件 | 何时读取 |
|---|---|---|
| L0 仓库 | 根 README、根 catalog.json | 首次接入，选择领域 |
| L1 导航 | 选中领域及分类的 catalog.json | 从用途摘要中选择主题 |
| L2 摘要 | topic.json 的 brief 入口 | 判断主题是否适用；足够回答时停止 |
| L3 正文 | detail 入口 | 实际运用方法、解释约束或建模时 |
| L4 支撑 | examples、sources、assets 入口 | 需要示例、来源核验或视觉解释时 |

不要递归读取所有 README 或 Markdown。只沿选中领域的 `groups[].catalog` 下钻，在 `topics` 中按用途选择。未命中的分类不读取。人工阅读入口和机器索引共享内容，但不要求将机器索引全部注入上下文。

摘要中的链接和图片不触发自动展开；需要图示才读取资产。`sources` 是来源说明所在的本地页面，可能与正文共存，不代表已下载或重新核验外部原始材料。`assets` 当前为 SVG 源图入口；相关 PNG 保留供人工阅读。

## 路径与身份

- 所有生成的 `catalog.json`、`index/topics.json` 和解析结果中的路径，均相对**知识库根目录**。
- `topic.json` 的 `entrypoints` 路径相对**该 topic.json 所在目录**，允许在库内使用 `../` 复用旧正文，不允许越出本库。
- ID 是主题身份，一经发布不随分类或目录名称修改。部分主题使用 `thinking.model-NNN`；序号只是持久标识，不是排序或优先级。
- `index/topics.json` 是程序使用的完整 ID 地址表，不是模型启动时应读取的总目录。
- `requires` 是必需依赖，`related` 是相关推荐。只有前者自动展开，按 ID 和文件路径去重；依赖循环报错。

## 内容层级解析

```bash
python3 scripts/kb.py resolve thinking.five-whys --layer brief
python3 scripts/kb.py resolve thinking.five-whys --layer detail
python3 scripts/kb.py resolve thinking.five-whys --layer examples
python3 scripts/kb.py resolve ontology.modeling reporting.business --layer detail
```

`brief` 只选择主题及必需依赖的摘要。`detail` 选择摘要和正文。`examples`、`sources`、`assets` 选择目标主题的摘要、正文及指定支撑入口，必需依赖读到正文即可。不存在所选层级时明确报错，不用其他文件冒充。多主题输出合并、去重，并先列必需依赖。

实际应用不能只取概念定义而跳过适用边界。加载预算以 UTF-8 文件字节数计，不等于模型 token 数，也不包含图片渲染消耗：

```bash
python3 scripts/kb.py resolve ontology.modeling --layer detail --max-bytes 50000
```

超预算时整个操作失败，不输出缺少必要约束的部分清单。调用方可以缩小主题集合；若任务只需概念说明，也可改读摘要。不能为了省预算省略实际使用所需的条件。

## 内容性质与可选扩展

- `status: general` 表示一般知识条目，不是科学有效性或内容已复核的认证。
- `status: reference` 表示原义待核实的主题参考版。必须显式加 `--allow-reference`，使用时保留这一限制。
- `status: example` 表示教学／设计示例，不可作为企业事实或通用标准。
- `kind: reference` 仅表示资料类型，与 `status: reference` 的待核实状态不同。
- `scope` 区分通用、行业和公司适用范围。当前通用注册表不收录公司子仓库内容。
- 公司子仓库、建设记录、验收记录、完整视频清单及图片不默认加载。需公司资料时依照[公司扩展入口](本体/公司业务/README.md)显式获取。

本次组织调整未重新核验知识事实或厂商版本。具体主题原有来源、日期、争议与适用限制继续有效。

## 跨项目引用

在消费项目中固定本知识库的 Git 提交。若使用子模块，其提交指针即可固定版本；否则在项目依赖记录中保存实际提交 SHA。不要只记录会变动的分支名。

消费项目可保存如下约定（示例字段，由消费项目管理，不是本工具的输入文件）：

```json
{
  "repository": "项目配置的知识库来源",
  "revision": "接入时记录的实际 Git 提交 SHA",
  "topics": ["thinking.five-whys", "reporting.business"],
  "layer": "detail"
}
```

从任意工作目录调用固定版本知识库中的工具，保存输出作为本次任务的读取记录：

```bash
python3 /path/to/kb/scripts/kb.py resolve thinking.five-whys --layer detail
```

输出包括 `revision`、`dirty`、主题 ID、层级和文件清单。`dirty: true` 表示工作区有未提交变动，此时提交 SHA 不能复现本地状态；可用于试用，正式复用应固定干净的提交。非 Git 副本的版本字段为 `null`，调用方需另外记录来源版本。本工具不自动切换版本或执行 Git 下载操作。

消费项目可将以下指引写入自己的项目约定：

> 使用基础知识库时，先读取其 README.md 和 LOADING.md，再沿 catalog.json 选择领域及主题。禁止全库展开；通过主题 ID 获取所需层级，保留来源、示例和待核实标记。公司扩展显式选用。记录知识库版本和实际读取清单。

## 当前兼容边界

旧正文路径全部保留。本体长文新增独立摘要，正文暂保留整篇；因此当前已支持主题及摘要层级的按需加载，尚未提供长文内部章节级解析。未来拆分正文时，应保留旧入口，并同步迁移文内锚点及外部引用；不能假定 Markdown 会自动重定向。
