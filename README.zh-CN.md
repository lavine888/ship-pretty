# Ship Pretty（中文参考）

> **AI 会生成界面，Ship Pretty 决定它是否真的准备好发布。**

Ship Pretty 是一个面向 AI 生成前端的 Agent Skill。它不把“代码能跑”当作视觉完成，而是强制执行一轮可验证的闭环：

**Render → Judge → Patch → Re-render → Quality Gate**

也就是：真实渲染、查看截图、判断最大问题、修补、再次渲染，直到通过质量门槛，或明确说明阻塞原因。

英文主文档：[README.md](README.md) · 执行规范：[skills/ship-pretty/SKILL.md](skills/ship-pretty/SKILL.md)

## 20 秒看懂

同一个 Landing Page fixture，在相同的 `1440×1000` 桌面 viewport 下：

| 没有 Ship Pretty | 使用 Ship Pretty 后 |
| --- | --- |
| ![优化前：通用 AI 营销页](assets/benchmarks/landing-page/before/desktop.png) | ![优化后：有明确层级的产品页](assets/benchmarks/landing-page/after/desktop.png) |
| 居中堆叠、等权三卡片、渐变和阴影过量 | 产品特异性层级、不对称构图、明确的质量证据 |

> **Codex 说两版都完成了。Ship Pretty 不同意。**

## 怎么使用

把 `skills/ship-pretty/` 通过你的 Agent Skill 工作流安装，或直接让 Codex 从这个仓库安装。然后对前端项目发送类似指令：

```text
使用 $ship-pretty 检查这个前端。请在桌面和移动端真实渲染，找出影响最大的视觉问题，修补后再次渲染，并持续迭代到通过质量门槛。请保存并展示 Before / After 截图。
```

重要约束：

1. 不能只看代码就宣称视觉优化完成。
2. 默认检查桌面 `1440×1000` 与移动端 `390×844`。
3. 先处理整体层级、构图和响应式问题，再处理局部装饰。
4. 每轮只选 1–3 个高杠杆问题，说明修改假设。
5. 保存实际检查过的 viewport 截图，并检查横向溢出。

## 默认质量门槛

总分至少 `80/100`，且每个维度不低于 `7/10`：

| 维度 | 要问的问题 |
| --- | --- |
| 层级 | 用户能否在三秒内看出最重要的信息或动作？ |
| 构图 | 整个画面是否有明确结构，而不是组件堆叠？ |
| 排版 | 字号、字重、行长和对比度是否形成真正的层级？ |
| 间距与密度 | 留白和间距是否在组织内容，而不是机械地到处加 padding？ |
| 色彩与效果 | 颜色、阴影、渐变和模糊是否承担了有意义的结构作用？ |
| 特异性 | 这个界面是否像为当前产品做的，而不是换个文案就能变成任意 SaaS？ |
| 响应式完整性 | 移动端是否重新编排，而不是把桌面端简单压缩？ |

完整中文门槛参考：[quality-gate.zh-CN.md](skills/ship-pretty/references/quality-gate.zh-CN.md)。

## Benchmark

- Landing Page：Hero 层级、CTA 权重、不对称构图
- Dashboard：信息密度、发布列表、移动端面板堆叠
- Mobile：任务扫描、进度反馈、底部导航可达性

截图和评分记录见：[benchmarks/results.md](benchmarks/results.md)。

## 贡献

最有价值的贡献不是再增加一条审美观点，而是一组可复现的 Before / After：包含提示词、截图、viewport、迭代记录，以及它解决了什么具体失败模式。

英文贡献指南：[CONTRIBUTING.md](CONTRIBUTING.md)。项目采用 MIT License。
