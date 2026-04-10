# Resume LaTeX Reference

这份说明用于告诉本仓库里的 Codex / agent：你的简历 LaTeX 源码不在本仓库内，而在外部目录 `/Volumes/passport/简历/latex-resume`。后续如果需要根据岗位调整简历，应优先修改那套源码，而不是修改导出的 PDF 或在本仓库里另起一套简历文本。

## Source of Truth

- 简历工程目录：`/Volumes/passport/简历/latex-resume`
- 主要说明文档：`/Volumes/passport/简历/latex-resume/README.md`
- 当前仓库用途：`/Volumes/passport/简历/滴滴` 主要负责 JD 拆解、项目蓝图、面试素材；简历最终排版以外部 LaTeX 工程为准

## 关键文件

| 路径 | 作用 |
| --- | --- |
| `/Volumes/passport/简历/latex-resume/main.tex` | 统一入口，控制版式、字体回退、左右栏布局、主题装配 |
| `/Volumes/passport/简历/latex-resume/profile.tex` | 姓名、求职方向、电话、邮箱、GitHub、头像等公共字段 |
| `/Volumes/passport/简历/latex-resume/content.tex` | 教育、实习、项目、技能、匹配亮点等正文内容 |
| `/Volumes/passport/简历/latex-resume/resume-modern-blue.tex` | 蓝色主题，`ResumeMode=ai-application` |
| `/Volumes/passport/简历/latex-resume/resume-slate-gray.tex` | 灰色主题，`ResumeMode=ai-application` |
| `/Volumes/passport/简历/latex-resume/resume-classic-black.tex` | 黑色主题，`ResumeMode=ai-application` |
| `/Volumes/passport/简历/latex-resume/resume-modern-blue-ai-backend.tex` | 蓝色主题，`ResumeMode=ai-backend` |
| `/Volumes/passport/简历/latex-resume/resume-modern-blue-pure-backend.tex` | 蓝色主题，`ResumeMode=backend` |
| `/Volumes/passport/简历/latex-resume/themes/` | 各主题配色 |
| `/Volumes/passport/简历/latex-resume/vendor/altacv.cls` | AltaCV 类文件 |
| `/Volumes/passport/简历/latex-resume/out/` | PDF 输出目录 |

## 已知入口关系

这套简历工程是“薄入口 + 公共内容”的结构：

1. `resume-*.tex` 只负责设置主题和 `ResumeMode`
2. 然后统一 `\input{main.tex}`
3. `main.tex` 再加载 `profile.tex`、`content.tex` 和对应 `themes/theme-*.tex`

因此，大多数岗位适配都应该落在：

- `profile.tex`
- `content.tex`
- 必要时新增一个新的 `resume-*.tex` 入口文件

## ResumeMode 语义

当前 `profile.tex` 中的 `\TargetRole` 会根据 `ResumeMode` 自动切换标题：

- `backend` -> `后端开发工程师（Go）`
- `ai-backend` -> `后端开发工程师（AI应用方向）`
- 默认 `ai-application` -> `大模型应用算法工程师`

`content.tex` 里的技能块也会随 `ResumeMode` 变化。

这意味着，如果后续需要按岗位切换“AI 应用 / AI 后端 / 纯后端”版本，优先使用现有入口文件，而不是把所有内容混在一个版本里临时硬改。

## 后续按岗位调整时怎么改

### 1. 如果只是微调目标岗位名称、联系方式、头像

改：

- `/Volumes/passport/简历/latex-resume/profile.tex`

重点字段：

- `\CandidateName`
- `\Phone`
- `\Email`
- `\GitHubURL`
- `\GitHubDisplay`
- `\ProfilePhotoPath`
- `\ResumeMode`

### 2. 如果要改项目描述、技能标签、经历排序、岗位匹配亮点

改：

- `/Volumes/passport/简历/latex-resume/content.tex`

重点关注的正文块包括：

- `\SkillsSection`
- `\EducationSection`
- `\InternshipSection`
- `\ProjectSection`
- `\FitHighlightsSection`

### 3. 如果要为某个岗位保留一个独立入口

优先复制现有某个 `resume-*.tex` 薄入口，再只改两件事：

- `\ThemePreset`
- `\ResumeMode`

尽量不要复制整份 `main.tex` 或 `content.tex`，避免后续多版本失控。

## 编译命令

在 `/Volumes/passport/简历/latex-resume` 下执行：

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error -output-directory=out resume-modern-blue.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error -output-directory=out resume-slate-gray.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error -output-directory=out resume-classic-black.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error -output-directory=out resume-modern-blue-ai-backend.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error -output-directory=out resume-modern-blue-pure-backend.tex
```

常见输出：

- `/Volumes/passport/简历/latex-resume/out/resume-modern-blue.pdf`
- `/Volumes/passport/简历/latex-resume/out/resume-slate-gray.pdf`
- `/Volumes/passport/简历/latex-resume/out/resume-classic-black.pdf`
- `/Volumes/passport/简历/latex-resume/out/resume-modern-blue-ai-backend.pdf`
- `/Volumes/passport/简历/latex-resume/out/resume-modern-blue-pure-backend.pdf`

## 给 Codex 的操作约定

当本仓库里出现以下请求时，应默认联动这套 LaTeX 简历源码：

- “根据这个 JD 调整简历”
- “把滴滴项目写进简历”
- “给我出 AI 后端版本简历”
- “生成一个更偏后端 / 更偏算法的版本”

推荐工作流：

1. 先在本仓库中产出或更新岗位分析、项目蓝图、面试素材
2. 再把最终确认过的简历表述同步到 `/Volumes/passport/简历/latex-resume/content.tex`
3. 根据目标岗位选择合适的 `resume-*.tex` 入口编译 PDF
4. 若需要新版本，优先新增薄入口文件，不要复制整套正文

## 不建议的做法

- 不要把 PDF 当作可编辑源文件
- 不要在 `/Volumes/passport/简历/滴滴` 内再维护第二套简历正文，除非明确需要做一次性中间稿
- 不要同时修改多个版本入口里的正文；正文应尽量集中在 `content.tex`

## 当前结论

如果有人在 `滴滴` 仓库里问“简历 LaTeX 在哪里”，标准答案是：

> 简历源码在 `/Volumes/passport/简历/latex-resume`，其中 `main.tex` 是统一入口，`profile.tex` 管公共信息，`content.tex` 管正文内容，`resume-*.tex` 是不同主题/岗位版本的薄入口文件。
