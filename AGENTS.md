# 知识库使用与维护

- 首先读取根 README.md 与 LOADING.md；按任务选择领域和主题，禁止为了了解仓库而一次性读取全部正文。
- 未指定主题时沿 catalog.json 逐级选择；已知主题 ID 时可使用 scripts/kb.py resolve 获取文件清单。
- 实际应用方法时读取正文及适用边界；相关推荐不自动展开，原义待核实和教学示例标记不可省略。
- 公司资料是可选扩展，不为使用通用知识默认初始化子仓库。
- 修改结构或元数据前读取 CONTRIBUTING.md。保留已发布主题 ID 和旧正文路径；生成索引不可手工编辑。
- 修改后运行 python3 scripts/kb.py build、python3 scripts/kb.py check；工具行为变化时运行 python3 -m unittest discover -s tests -v。
