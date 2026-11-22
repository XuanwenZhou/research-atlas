<p align="center">
  <img src="assets/research-atlas-logo.svg" width="72" height="72" alt="Research Atlas Logo">
</p>

<h1 align="center">Research Atlas</h1>

<p align="center">
  <strong>从综述论文到技术演进图</strong><br>
  让 Codex 阅读综述和原始论文，整理方法、技术分类和有依据的演进关系，<br>
  交付可以搜索、筛选和追踪技术路径的独立 HTML 图谱。
</p>

<p align="center">
  <a href="SKILL.md"><img src="docs/brand/badge-codex.svg" alt="Codex Skill" height="28"></a>
  <a href="#本地构建与校验"><img src="docs/brand/badge-python.svg" alt="Python 3.10+" height="28"></a>
  <a href="examples/3dgs/README.md"><img src="docs/brand/badge-html.svg" alt="HTML 离线浏览" height="28"></a>
  <a href="references/paper-extraction-schema.md"><img src="docs/brand/badge-exports.svg" alt="导出 JSON、CSV、BibTeX 和 SVG" height="28"></a>
</p>

<p align="center">
  <a href="https://htmlpreview.github.io/?https://github.com/XuanwenZhou/research-atlas/blob/main/examples/3dgs/index.html"><img src="docs/brand/button-demo.svg" alt="在线体验 3DGS 示例" height="42"></a>
  <a href="#安装"><img src="docs/brand/button-start.svg" alt="安装与使用" height="42"></a>
  <a href="SKILL.md"><img src="docs/brand/button-docs.svg" alt="查看使用规范" height="42"></a>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/images/readme-catalog-dark.png">
    <img src="docs/images/readme-catalog-light.png" width="820" alt="真实 3DGS 方法合集：按技术分类浏览方法，搜索论文并查看机制与来源">
  </picture>
</p>

<p align="center">
  <picture><source media="(prefers-color-scheme: dark)" srcset="docs/images/readme-graph-dark.png"><img src="docs/images/readme-graph-light.png" width="405" alt="全部方法的技术演进图：时间轴、技术方向和关系连线"></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="docs/images/readme-evidence-dark.png"><img src="docs/images/readme-evidence-light.png" width="405" alt="搜索 Endo-4DGS 后点击连线，查看技术关系和原论文依据"></picture>
</p>

<p align="center"><sub>上图均来自实际示例。在线体验使用 GitHub HTML Preview，也可下载后直接打开 <code>examples/3dgs/index.html</code>。</sub></p>

<a name="为什么使用"></a>

## 为什么使用

综述中的分类、论文列表和技术关系往往分散在不同章节。只整理标题和摘要，还不足以看清方法之间的联系。

> **这些方法分别解决什么问题？采用了什么机制？哪些技术关系有文献依据？**

Research Atlas 将这些信息整理进同一份数据：用方法合集检索和比较，用时间轴浏览技术路线，点击节点或连线回到论文与来源。研究其他领域时，使用相同流程和通用模板即可。

<a name="主要功能"></a>

## <img src="docs/brand/icon-stack-2.svg" width="24" height="24" alt=""> 主要功能

| 能力 | 你能得到什么 |
|---|---|
| <img src="docs/brand/icon-book-2.svg" width="20" height="20" alt=""> **文献提取** | 从综述追溯原始论文，记录综述来源、引用编号和原文位置；区分阅读全文、摘要和转述。 |
| <img src="docs/brand/icon-stack-2.svg" width="20" height="20" alt=""> **方法合集** | 去重并统一论文信息，区分论文和方法，支持一文多法、机制检索与方法比较。 |
| <img src="docs/brand/icon-sitemap.svg" width="20" height="20" alt=""> **技术分类** | 根据研究问题和核心机制归纳分类，保留主要归属、辅助标签和分类依据。 |
| <img src="docs/brand/icon-git-branch.svg" width="20" height="20" alt=""> **演进分析** | 区分直接继承、框架扩展、机制借鉴和同方向研究；查看已有技术关系中的前驱与后续路径。 |
| <img src="docs/brand/icon-search.svg" width="20" height="20" alt=""> **文献补充** | 沿分类和技术路线查找后续研究，记录检索范围和截止日期，增量更新时保留已有 ID。 |
| <img src="docs/brand/icon-file-export.svg" width="20" height="20" alt=""> **交互交付** | 独立 HTML、完整 JSON、分类和关系数据、CSV/BibTeX，以及检索核验报告；图谱可导出 SVG。 |

<a name="安装"></a>

## <img src="docs/brand/icon-terminal-2.svg" width="24" height="24" alt=""> 安装

将完整仓库放入用户级 Skill 目录，确保 `SKILL.md` 位于该目录根部：

```bash
git clone https://github.com/XuanwenZhou/research-atlas.git ~/.agents/skills/research-evolution-map
```

Windows 用户目录通常为 `%USERPROFILE%/.agents/skills/research-evolution-map`。也可将仓库放入项目的 `.agents/skills/research-evolution-map`。如果已有同名 Skill，请先备份或在原目录更新，避免重复安装。

在 Codex 中查找 **Research Atlas｜科研技术图谱**，或输入 `$research-evolution-map` 调用。安装目录和调用名保留为 `research-evolution-map`；未显示时可重启 Codex。

| 环境 | 用途 |
|---|---|
| Codex 与可用的阅读、检索工具 | 阅读文献、分析机制、分类和技术关系 |
| Python 3.10+ | 数据校验、去重、构建和导出，仅依赖标准库 |
| 现代浏览器 | 浏览生成的 HTML，无需服务器或前端依赖 |

<a name="使用示例"></a>

## <img src="docs/brand/icon-book-2.svg" width="24" height="24" alt=""> 使用示例

```text
使用 $research-evolution-map，研究领域为【领域名称】。
请阅读【综述文件或链接】，研究时间范围为【起止时间】，
整理方法合集、技术分类和演进关系，并补充相关新文献，
最终生成交互式 HTML、JSON 数据、文献清单和核验报告。
```

你会得到可独立打开的 **HTML**、可继续更新的 **JSON 数据**、**CSV/BibTeX 文献清单**，以及检索核验报告和未核实问题清单。

更新已有项目时，可以这样提出需求：

```text
使用 $research-evolution-map，基于现有项目 JSON 和这批新增论文，
补充方法、技术分类与关系依据，保留已有 ID，并重新生成 HTML 和文献清单。
```

已有数据也可用于进一步整理专题方向。

<a name="工作流程"></a>

## <img src="docs/brand/icon-route.svg" width="24" height="24" alt=""> 工作流程

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/brand/workflow-mobile-dark.svg">
  <source media="(max-width: 600px)" srcset="docs/brand/workflow-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/brand/workflow-dark.svg">
  <img src="docs/brand/workflow-light.svg" width="100%" alt="提供综述和论文，整理方法、分类和技术关系，交付交互式 HTML 图谱">
</picture>

综述解析、方法提取、去重、分类、关系分析、沿路线补充文献和 HTML 构建连续完成。分类依据、来源位置、事实或推断及核验状态随数据保存，交付时汇总需要进一步讨论的问题。

<details>
<summary>查看数据如何生成图谱</summary>

Codex 负责文献阅读与技术判断；Python 脚本负责结构校验、HTML 构建和数据导出。

```mermaid
flowchart LR
    A["综述与原始论文"] --> B["Codex：方法提取与文献整合"]
    B --> C["技术分类与关系依据"]
    C --> D["项目 JSON"]
    D --> E["validate_data.py"]
    E --> F["build_html.py"]
    F --> G["方法合集与技术演进图"]
    F --> H["JSON / CSV / BibTeX / 核验报告"]
```

</details>

<a name="html-输出效果"></a>

## <img src="docs/brand/icon-browser.svg" width="24" height="24" alt=""> HTML 输出效果

以 **3D Gaussian Splatting** 为例，使用同一份结构化数据生成方法合集和技术演进关系图：

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/brand/3dgs-stats-mobile-dark.svg">
  <source media="(max-width: 600px)" srcset="docs/brand/3dgs-stats-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/brand/3dgs-stats-dark.svg">
  <img src="docs/brand/3dgs-stats-light.svg" width="100%" alt="3DGS 实例：493 个方法、21 个技术分类、484 条关系记录、5 篇综述来源">
</picture>

<br>

| 页面 | 主要内容 |
|---|---|
| 总方法合集 | 分类导航、名称／作者／机制搜索、年份筛选、排序分页、论文与方法详情、JSON／CSV／BibTeX 导出 |
| 技术演进关系图 | 默认展示全部方法、时间轴、起止年份、四类关系筛选、前驱／后续路径、节点与连线详情、定位高亮、缩放拖动、全屏及 SVG 导出 |

图谱首次打开和重置后均显示全部方法。搜索或筛选后可以查看局部关联；技术路径沿已有技术边展开，同方向研究不作为继承路径。

[操作指南](examples/3dgs/README.md) · [HTML 文件](examples/3dgs/index.html) · [JSON 数据](examples/3dgs/project-data.json) · [文献 CSV](examples/3dgs/bibliography.csv) · [BibTeX](examples/3dgs/bibliography.bib)

GitHub 文件页面显示 HTML 源码；首屏“在线体验”提供浏览入口，下载后的 HTML 可直接离线打开。

<details>
<summary><strong>查看完整操作演示</strong>：分类、详情、关系依据、技术路径和导出</summary>

![3DGS 实际操作：分类筛选、论文详情、节点关联、关系依据、技术路径、年份筛选和明暗主题](docs/images/3dgs-demo.gif)

可以从这些操作开始体验：

1. 在合集选择“稀疏视角重建”和“2024”，查看4个方法并导出文献。
2. 在图谱搜索 `Endo-4DGS`，点击与 `4D-GS` 的连线，阅读关系说明和原论文依据。
3. 搜索 `Deformable Radial Kernel Splatting`，选择“前驱技术路径”，浏览已有技术边中的多级前驱。
4. 组合年份和关系类型筛选；重置回全部方法后，导出完整 SVG。

</details>

<details>
<summary>方法详情、搜索关联和原文依据截图</summary>

![论文信息、机制、局限与综述引用](docs/images/3dgs-method-detail.png)

![搜索 Endo-4DGS 后保留直接关联节点](docs/images/3dgs-node-relations.png)

![点击关系后查看说明与原论文链接](docs/images/3dgs-edge-evidence.png)

</details>

<details>
<summary>多级路径、年份筛选、深色主题和移动端截图</summary>

![已有技术关系中的前驱路径](docs/images/3dgs-path-tracing.png)

![年份范围与技术借鉴关系组合筛选](docs/images/3dgs-relation-filter.png)

![深色主题](docs/images/3dgs-dark.png)

<img src="docs/images/3dgs-mobile.png" alt="手机宽度下的方法合集" width="390">

</details>

示例保留实际核验状态，不代表全部信息已核实或文献收录穷尽。另有 `assets/example-data.json` 作为小型虚构数据，用于脚本和交互测试。

<a name="常见问题"></a>

## 常见问题

<details>
<summary>图谱会自动只挑选一条主线吗？</summary>

默认展示全部收录方法。搜索、技术方向、年份和关系类型筛选用于按需浏览；重置后恢复全部方法。

</details>

<details>
<summary>图中连线都表示技术继承吗？</summary>

只有 `direct`、`extension` 和 `borrow` 表示相应技术联系，`theme` 仅表示同方向研究。点击连线可查看说明和依据；事实、整理推断及核验状态保存在数据中。

</details>

<details>
<summary>生成后的 HTML 需要联网或安装前端吗？</summary>

不需要。模板的样式、脚本和项目数据内嵌在 HTML 中，下载后可离线浏览。打开论文原文或使用在线预览服务时需要联网。

</details>

<a name="本地构建与校验"></a>

## <img src="docs/brand/icon-shield-check.svg" width="24" height="24" alt=""> 本地构建与校验

<details>
<summary>展开脚本命令、构建输出和校验说明</summary>

在仓库根目录运行：

```bash
python scripts/self_test.py
python scripts/validate_data.py assets/example-data.json --report output/validation.json
python scripts/build_html.py assets/example-data.json --output output/evolution-map.html
```

打开 `output/evolution-map.html` 即可查看示例。示例中的待核警告是刻意保留的测试内容；结构校验通过不代表学术事实已核实。实际项目应按[数据契约](references/paper-extraction-schema.md)提供数据。

重新构建 3DGS 实际示例：

```bash
python scripts/build_html.py examples/3dgs/project-data.json --output output/3dgs/index.html
```

```bash
python scripts/deduplicate_papers.py project.json --report output/duplicates.json
python scripts/build_html.py project.json --output output/evolution-map.html
python scripts/export_bibliography.py project.json --output-dir output
```

构建会输出 HTML、完整 JSON、分类和关系数据、CSV/BibTeX、校验报告及待核清单。`--strict` 会把待核等警告也视为失败，适用于完成核验后的验收。

</details>

<a name="目录结构"></a>

## <img src="docs/brand/icon-folder.svg" width="24" height="24" alt=""> 目录结构

<details>
<summary>查看 Skill 文件和开发资源</summary>

```text
research-atlas/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── assets/                 # 通用 HTML 模板、虚构示例和 Skill 图标
├── references/             # 工作流、分类、关系和证据规范
├── scripts/                # 校验、去重、构建、导出及自测
├── examples/3dgs/          # 通用模板生成的 3DGS HTML 与 JSON
└── docs/                   # 真实截图、README 图标和视觉素材
```

核心执行规则见 [SKILL.md](SKILL.md)。除专门整理的示例外，私人文献库、原始论文全文及构建和测试输出均不纳入仓库；请将个人研究资料保存在单独项目目录。

</details>

## Contributors

<table>
  <tr>
    <td align="center" width="50%">
      <a href="https://github.com/XuanwenZhou">
        <img src="docs/brand/coffee-cat-avatar.png" width="64" height="64" alt="Coffee Cat 的 GitHub 头像"><br>
        <strong>Coffee Cat</strong>
      </a><br>
      <sub>项目负责人 · 需求设计与内容审阅</sub>
    </td>
    <td align="center" width="50%">
      <a href="https://github.com/openai/codex">
        <img src="docs/brand/icon-terminal-2.svg" width="64" height="64" alt="Codex AI 编程助手"><br>
        <strong>Codex</strong>
      </a><br>
      <sub>AI 辅助开发 · 文档整理与测试验证</sub>
    </td>
  </tr>
</table>

<p align="center">
  <a href="SKILL.md">Skill 使用规范</a> ·
  <a href="references/paper-extraction-schema.md">数据结构</a> ·
  <a href="references/relationship-classification.md">技术关系判断</a> ·
  <a href="docs/brand/THIRD_PARTY_NOTICES.md">图标许可</a>
</p>
