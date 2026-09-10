# 公司业务

按公司分别维护组织口径、业务流程、系统功能、项目规划和内部资料，避免把一家公司的做法当成行业统一定义。

| 公司目录 | 范围 |
|---|---|
| [clx](clx/README.md) | 本项目所指的特定公司业务资料；包含 TQM 实践、汽车质量业务口径、LI-TQM 应用、规划汇报及最新发布文件 |

新增公司时建立独立目录；经过核对、去除公司专有前提后，才能另行整理为通用方法或行业案例。

`clx` 通过 Git submodule 绑定到 `git@gitlab.chehejia.com:factory/qs-kb.git`，公司资料在该独立仓库中维护。

首次克隆主仓库时使用 `git clone --recurse-submodules <主仓库地址>`；已有工作区可在主仓库根目录运行：

```bash
git submodule update --init --recursive
```

修改公司资料后，先在 `本体/公司业务/clx` 中提交并推送，再回到主仓库提交 submodule 指针更新。主仓库只记录子仓库的提交位置，不直接保存其中的文档内容。

[返回项目目录](../README.md)
