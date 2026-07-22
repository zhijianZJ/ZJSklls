# ZJSkills

[English](README.en.md)

**版本 [3.1.0](VERSION) **

把你真实的 AI 职业或学习处境告诉 ZJSkills。它会诊断当前问题，说明证据边界，并给出一个有用的下一步。

ZJSkills 3.1.0 是一个轻量、AI 优先的职业、创业、副业诊断 Skill。它先读取对话中已有的目标、经验、约束和反馈，拆解真正的问题，再给出适合当前阶段的判断、学习路线或解题行动。证据足够就直接行动，只有一个缺失事实会改变判断时，才问**零个或一个**决定性问题。

## 职业/创业/副业诊断

适合“不知道往哪里走”“两个方向怎么选”“我是否适合”“现在是否值得投入”等问题。诊断会把已经展示的经历翻译成可迁移资产和可测试的机会假设，区分仍待验证的边界，并给出一个最小体验任务，而不是把兴趣、学历、证书或自信直接当作能力证明。带着体验结果回来后，它会复用原诊断并作出当前阶段选择；只有“可以进入路线”才衔接学习路线。

支持的方向：

- AIAgent应用/大模型开发
- Vibe Coding
- AI 产品经理
- AI 运营（内容/增长、业务效率两个分支）
- AI 工具与职场应用
- FED
- 创业/副业

## 快速开始

在支持 Skill 的平台输入 `$zjskills` 或 `/zjskills`，也可以直接说真实情况：

```text
我想进入 AI 行业，但不知道 Agent、Vibe Coding、AI 产品还是 AI 运营更适合我。
```
```
我目前做运营，会用 AI 写内容，但没有编程项目，每周能投入 6 小时。
```
```
我是小白，想做AI博主
```

完整复制提示词和逐步示例见[新手入门](docs/getting-started.md)，详细规则见[完整使用手册](docs/usage-guide.md)。

## 安装与平台

技术名称保持为 `zjskills`，仓库地址为：

```bash
git clone https://github.com/zhijianZJ/ZJSkills.git
```

WorkBuddy 已上架技能广场，搜索智建skills使用

ZJSkills 支持 Codex 和 Claude Code 的原生 Skill 安装；在 Tencent WorkBuddy、豆包以及通用宿主中，当前这个六文件包按手动文件/上下文使用。请按[多平台安装与使用指南](docs/platform-installation.md)完成接入与验收。

## 文档

- [新手入门](docs/getting-started.md)
- [完整使用手册](docs/usage-guide.md)
- [十二个使用场景与提示词](docs/examples.md)
- [多平台安装与使用](docs/platform-installation.md)
- [贡献指南](CONTRIBUTING.md)

## 公开支持说明

使用 ZJSkills 时如遇到使用问题、规划疑问或其他未解决问题，可联系智建进入答疑群交流。


