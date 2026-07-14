# Agnes Studio

Agnes Studio 是一个本地运行的 AI 视频创作工作流工具。它将提示词优化、文生图、视频生成、关键帧动画和本地结果保存串成一条完整流程，在浏览器中完成从文本 / 图片到短视频的创作。

官网与 API 平台：

- [Agnes AI 官网](https://agnes-ai.com/)（**免费注册**即可获取 API Key）
- [Agnes 文档中心](https://agnes-ai.com/zh-Hans/docs)
- [Agnes Video V2.0 文档](https://agnes-ai.com/zh-Hans/docs/agnes-video-v20)
- [Agnes API 平台](https://platform.agnes-ai.com/)

> 安全提醒：不要把 API Key 写入 Git 仓库、README、截图或公开聊天记录。

---

## 功能

本项目封装 Agnes 官方文本、图片、视频 API，提供可视化操作界面：

| 能力 | 模型 | 说明 |
| --- | --- | --- |
| 提示词优化 | `agnes-2.0-flash` | 将中文描述改写为更适合视频生成的英文提示词 |
| 文生图 / 参考图 | `agnes-image-2.0-flash` | 生成公网 URL 参考图，用于图生视频或关键帧 |
| 文生视频 | `agnes-video-v2.0` | 纯文本描述生成视频 |
| 图生视频 | `agnes-video-v2.0` | 单张参考图驱动运动 |
| 关键帧动画 | `agnes-video-v2.0` | 多张关键帧之间平滑过渡 |
| 本地图片 Base64 | — | 本地上传自动转 Data URI，无需公网图床 |
| 异步任务轮询 | — | 优先使用 `video_id` 查询，自动等待并本地保存 |
| 参数可视化 | — | 分辨率、时长、帧率、seed、负向提示词等可在页面调整 |
| 样例内嵌播放 | — | 启动服务后页面底部「样例效果」直接播放；README 内嵌 WebP 动图预览 |

---

## 快速开始

### 1. 申请 Agnes API Key

1. 打开 [agnes-ai.com](https://agnes-ai.com/) 或 [platform.agnes-ai.com](https://platform.agnes-ai.com/) 注册账号（**免费**）
2. 在控制台创建并复制 API Key
3. 免费套餐有**每分钟请求次数限制**；商用或高并发场景建议升级付费方案

### 2. 安装依赖并启动

```bash
pip install flask requests
python3 server.py
```

浏览器访问：

```text
http://127.0.0.1:5000
```

页面底部 **「样例效果」** 区域可直接播放内置样例视频（锚点：`#samples`）。

### 3. 配置 API Key

**方式 A：** 填入页面「API Key」输入框

**方式 B：** 环境变量（推荐本地开发）

```bash
export AGNES_API_KEY="你的_API_Key"
export AGNES_BASE_URL="https://apihub.agnes-ai.com"   # 可选
export PORT=5000                                       # 可选
```

### 4. 开始创作

| 模式 | 操作 |
| --- | --- |
| 文生视频 | 输入描述 → 生成视频 |
| 图生视频 | 上传 1 张本地图 / 生成参考图 / 粘贴公网 URL → 生成视频 |
| 关键帧动画 | 上传 2+ 张本地图 → 选择参考图 → 生成视频 |

---

## 样例效果

启动 `python3 server.py` 后，在页面 **[样例效果](http://127.0.0.1:5000/#samples)** 区域可直接播放，无需点击文件链接。

下方为各样例的 **WebP 动图预览**（GitHub 页面可直接播放）及参数备注；完整 MP4 源文件见 `outputs/videos/`。

### 样例 1：文生视频（长视频 · 18 秒）

![样例 1：文生视频 18 秒](docs/previews/sample-1-text-18s.webp)

**源视频：** [video_task_7e0BkgnZTNAQ7jQcJUYcAvjaECHHXARs.mp4](outputs/videos/video_task_7e0BkgnZTNAQ7jQcJUYcAvjaECHHXARs.mp4)

| 项目 | 参数 |
| --- | --- |
| 生成模式 | **文生视频**（`text` / API `ti2vid`） |
| 提示词 | 写实暗黑国风仙侠场景，含分镜式运镜描述（航拍俯冲、环绕跟拍、后拉仰拍等） |
| 负向提示词 | 卡通，Q版，低幼，现代，模糊，畸形，水印文字，杂物，塑料质感，多余人物，杂乱特效 |
| 请求分辨率 | 1152×768（16:9 横屏 · 720p 预设） |
| 实际输出 | **1088×832**（API 映射为 720p / 4:3） |
| 帧数 / 帧率 | `num_frames: 441` · `frame_rate: 24` |
| 视频时长 | **约 18.4 秒** |
| 随机种子 | `seed: 43` |
| 推理步数 | `num_inference_steps: 8` |
| 任务 ID | `task_7e0BkgnZTNAQ7jQcJUYcAvjaECHHXARs` |

> 说明：请求 16:9 的 1152×768 时，Agnes 自动映射到最接近的标准档位，实际输出为 1088×832。长视频推理耗时较长（约 6 分钟），请耐心等待。

---

### 样例 2：文生视频（标准 · 约 5 秒）

![样例 2：文生视频 5 秒](docs/previews/sample-2-text-5s.webp)

**源视频：** [video_task_Q1HffJJB6mEyAykBxCqxCfu4el0zZJ4F_1783932308.mp4](outputs/videos/video_task_Q1HffJJB6mEyAykBxCqxCfu4el0zZJ4F_1783932308.mp4)

| 项目 | 参数 |
| --- | --- |
| 生成模式 | **文生视频**（`text`） |
| 参考图 | 无（纯文本输入） |
| 请求分辨率 | 1152×768（16:9 横屏 · 720p 预设） |
| 帧数 / 帧率 | `num_frames: 121` · `frame_rate: 24`（默认推荐配置） |
| 视频时长 | **约 5.0 秒** |
| 任务 ID | `task_Q1HffJJB6mEyAykBxCqxCfu4el0zZJ4F` |

> 说明：典型文生视频工作流——仅填写视频描述，无需上传图片，使用默认 5 秒 / 121 帧配置即可快速出片。

---

### 样例 3：关键帧动画（本地上传 Base64 · 约 5 秒）

![样例 3：关键帧动画 5 秒](docs/previews/sample-3-keyframes-5s.webp)

**源视频：** [video_task_Ro0HKUqg57ttpltA0z1iE4yAv4wiLMbw_1783935044.mp4](outputs/videos/video_task_Ro0HKUqg57ttpltA0z1iE4yAv4wiLMbw_1783935044.mp4)

| 项目 | 参数 |
| --- | --- |
| 生成模式 | **关键帧生成动画**（`keyframes`） |
| 参考图来源 | **本地上传 3 张**（自动转 Base64 Data URI） |
| 提示词 | 渐进式转场 |
| 请求分辨率 | 1152×768（16:9 横屏 · 720p 预设） |
| 实际输出 | **1088×832** |
| 帧数 / 帧率 | `num_frames: 121` · `frame_rate: 24` |
| 视频时长 | **约 5.0 秒** |
| API 传参 | `extra_body.image`（3 张 Base64 图片数组）+ `extra_body.mode: "keyframes"` |
| 任务 ID | `task_Ro0HKUqg57ttpltA0z1iE4yAv4wiLMbw` |

> 说明：本样例验证了**本地图片 → Base64 → 关键帧动画**的完整流程。上传 3 张截图后全选，AI 在关键帧之间生成平滑渐进式转场，无需公网图床。

---

## API 调用示例

本项目通过本地 Flask 代理 Agnes 接口。Base URL：`https://apihub.agnes-ai.com`

### 文生视频

```bash
curl -X POST http://127.0.0.1:5000/api/agnes/video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cinematic shot of a cat walking on the beach at sunset",
    "mode": "text",
    "width": 1152,
    "height": 768,
    "num_frames": 121,
    "frame_rate": 24
  }'
```

### 关键帧动画（Base64 本地图）

前端上传本地图片后会自动转为 `data:image/...;base64,...` 传入 `keyframes` 数组：

```bash
curl -X POST http://127.0.0.1:5000/api/agnes/video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "渐进式转场，保持画面风格一致",
    "mode": "keyframes",
    "keyframes": ["data:image/png;base64,...", "data:image/png;base64,..."],
    "num_frames": 121,
    "frame_rate": 24
  }'
```

### 查询视频任务

创建任务后优先使用 `video_id` 轮询（与 [agnes-ai-generation-skill](https://github.com/Yacey/agnes-ai-generation-skill) 一致）：

```bash
curl "http://127.0.0.1:5000/api/agnes/video/status?video_id=video_xxx"
```

### 默认视频参数建议

与社区最佳实践一致，推荐默认使用：

- `num_frames: 121`
- `frame_rate: 24`
- `num_frames` 须满足 **8n + 1** 且 **≤ 441**

---

## 提示词语言策略

Agnes 视频生成对**英文提示词**更稳定。本项目提供「优化提示词」按钮，会调用 `agnes-2.0-flash` 将中文描述改写为英文视频提示词。

建议保留：主体、场景、风格、光照、构图、镜头运动、动作描述、负向约束。

中文关键帧过渡示例：

```text
在关键帧之间生成平滑的渐进式转场，保持人物造型、光影风格一致，镜头运动自然流畅
```

---

## 相关资源

| 资源 | 链接 |
| --- | --- |
| Agnes 官方文档 | [agnes-ai.com/zh-Hans/docs](https://agnes-ai.com/zh-Hans/docs) |
| Agnes Video V2.0 | [文档](https://agnes-ai.com/zh-Hans/docs/agnes-video-v20) |
| Agent Skill 参考实现 | [agnes-ai-generation-skill](https://github.com/Yacey/agnes-ai-generation-skill) |
| 本项目 Web UI | `http://127.0.0.1:5000` |
| 样例播放锚点 | `http://127.0.0.1:5000/#samples` |

---

## 使用流程（Web UI）

1. 启动本地服务

```bash
python3 server.py
```

2. 打开浏览器访问：

```text
http://127.0.0.1:5000
```

3. 选择你的创作方式
   - **文本生成**：直接输入视频描述
   - **图片转视频**：上传 1 张本地图片，或生成/选择参考图，或粘贴公网 URL
   - **关键帧动画**：上传 2 张及以上本地图片，让 AI 在关键帧之间生成平滑过渡（详见下文）

4. 在「视频参数」面板中调整分辨率、时长、帧率等设置（详见下文参数说明）

5. 填写 Agnes API Key 后开始生成，结果会自动保存到本地输出目录，并可在页面内直接预览播放

---

## 本地图片生成关键帧动画（详细教程）

本项目已验证：**可以直接上传本地图片，生成关键帧过渡动画**，无需先把图片上传到 COS 或公网图床。

### 原理说明

Agnes Video V2.0 的 `extra_body.image` 字段支持两种图片输入：

| 输入方式 | 格式 | 适用场景 |
| --- | --- | --- |
| 公网 URL | `https://...` | 文生图返回的链接、已有 COS 地址 |
| **Base64 Data URI** | `data:image/png;base64,...` | **本地上传图片（本项目默认方式）** |

本地上传时，浏览器会将图片读取为 Base64 Data URI，通过后端代理原样传给 Agnes API。Agnes 服务端可直接解析 Base64，因此**不需要** `localhost` 或内网地址。

### 操作步骤（推荐流程）

以「用 3 张本地截图生成渐进式转场动画」为例：

**第 1 步：选择生成模式**

在「生成模式」下拉框中选择 **关键帧生成动画**。

**第 2 步：填写视频描述**

在「视频描述」中写清楚关键帧之间的过渡关系，例如：

```text
渐进式转场
```

更完整的提示词示例：

```text
Generate a smooth cinematic transition between the keyframes,
maintaining visual consistency and natural camera movement
```

**第 3 步：上传本地图片**

在「上传本地图片（自动转 Base64）」处，选择 **2 张及以上**图片（支持多选）。

- 上传后右侧「参考图 / 关键帧」区域会显示缩略图
- 缩略图标题带 **Base64** 标记，表示已转为 Data URI
- 底部显示：`共 N 张（本地上传 N · 文生图 0）· 已选 N 张`

**第 4 步：选择参考图**

- 关键帧动画至少需要 **2 张**图片
- 点击图片可切换选中状态（蓝色边框 = 已选中）
- 默认会全选已上传的图片；图生视频模式则默认选第 1 张

**第 5 步：调整视频参数（可选）**

在「视频参数」面板中按需设置：

| 参数 | 推荐值 | 说明 |
| --- | --- | --- |
| 分辨率 | 16:9 横屏 · 720p | 输出约 1088×832（API 自动映射） |
| 目标时长 | 约 5 秒（121 帧） | 关键帧过渡常用 5–10 秒 |
| 帧率 | 24 fps | 电影感更自然 |
| 负向提示词 | 按需填写 | 避免模糊、畸形、水印等 |

**第 6 步：生成视频**

点击 **生成视频** 或 **用参考图生成动画**，等待任务完成。

- 页面会显示进度条和轮询状态
- 完成后在「生成结果」区域直接播放视频
- 视频同时保存到 `outputs/videos/video_task_xxx.mp4`
- 「生成历史」中可回看任务状态与下载链接

### 三种图片来源对比

| 来源 | 操作 | 优点 | 适用场景 |
| --- | --- | --- | --- |
| **本地上传（Base64）** | 选择本地文件 | 最方便，无需图床，即传即用 | 已有分镜图、截图、设计稿 |
| **文生图参考图** | 点击「生成参考图」 | 从文字直接出图，返回公网 URL | 没有现成图片，需要 AI 创作 |
| **公网 URL** | 粘贴 HTTPS 链接 | 复用已有 COS / CDN 资源 | 图片已在云端 |

三种来源的图片可以**混合使用**——例如先上传 2 张本地图，再文生图补 1 张，统一在参考图区域选择后生成动画。

### 关键帧动画提示词建议

关键帧模式下，`prompt` 应描述**帧与帧之间如何过渡**，而非重复描述画面内容：

```text
[过渡方式] + [保持一致的内容] + [镜头运动]

示例：
Create a smooth progressive transition between keyframes,
maintaining character identity, consistent lighting,
and natural cinematic camera movement
```

中文示例：

```text
在关键帧之间生成平滑的渐进式转场，保持人物造型、光影风格一致，镜头运动自然流畅
```

### 图生视频 vs 关键帧动画

| 对比项 | 图生视频 | 关键帧动画 |
| --- | --- | --- |
| 参考图数量 | **1 张** | **2 张及以上** |
| API 传参 | `image` 字段 | `extra_body.image` 数组 + `mode: "keyframes"` |
| 效果 | 单图动起来 | 多图之间平滑过渡 |
| 典型用途 | 人像微动、产品旋转 | 分镜转场、状态变化、场景切换 |

### 常见问题

**Q：上传本地图片后，还需要「生成参考图」吗？**

不需要。本地上传后已具备 Base64 数据，可直接选图生成视频。只有当你没有现成图片、希望 AI 帮你出图时，才需要点「生成参考图」。

**Q：为什么历史记录里有一条 `error`，但视频实际生成成功了？**

早期版本在服务端轮询超时后，历史状态可能未及时更新。当前版本已延长轮询时间并改进结果解析；以「生成结果」区域的播放与 `outputs/videos/` 本地文件为准。

**Q：图片太大会有问题吗？**

建议单张不超过 10MB，格式使用 PNG / JPG / WebP。过大图片会导致 Base64 请求体变大、上传变慢。

**Q：输出分辨率与设置不一致？**

Agnes 会将 `width` / `height` 自动映射到最近的标准档位（480p / 720p / 1080p）。请以响应中的 `size` 字段为准，例如请求 `1152×768` 可能输出 `1088×832`。

### 快速对照表

| 模式 | 参考图要求 | 操作步骤 |
| --- | --- | --- |
| 文生视频 | 无需图片 | 输入描述 → 生成视频 |
| 图生视频 | 1 张图片 | 上传本地图 / 生成参考图 / 粘贴公网 URL → 选 1 张 → 生成视频 |
| **关键帧动画** | **2 张及以上** | **上传多张本地图 → 选 2+ 张 → 生成视频** |

---
## 技术栈

- Python / Flask
- HTML / CSS / JavaScript
- Requests
- Agnes AI 接口

## 项目结构

```text
.
├── index.html                  # 前端界面
├── server.py                   # Flask 后端与 Agnes API 代理
├── docs/
│   └── previews/               # README 样例 WebP 动图预览
├── uploads/                    # 上传图片缓存
├── outputs/
│   ├── images/                 # 本地保存的生成图片
│   └── videos/                 # 本地保存的视频（完整 MP4 源文件）
├── tests/                      # 回归测试
└── README.md                   # 项目说明
```

## 运行前准备

依赖安装与 API Key 配置见上文 **[快速开始](#快速开始)**。

```bash
pip install flask requests
```

---

## Agnes Video V2.0 参数详解

本项目通过 `POST /api/agnes/video` 代理调用 Agnes 官方接口 `POST /v1/videos`。以下参数说明基于 [Agnes Video V2.0 官方文档](https://agnes-ai.com/zh-Hans/docs/agnes-video-v20)。

### 核心请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `model` | string | 是 | `agnes-video-v2.0` | 视频生成模型名称，固定使用 Agnes Video V2.0。 |
| `prompt` | string | 是 | — | 视频内容的文本描述。建议结构：`[主体] + [动作] + [场景] + [镜头运动] + [光线] + [风格]`。 |
| `image` | string | 否 | — | **图生视频**参考图。支持公网 HTTPS URL，或 Data URI Base64（`data:image/png;base64,...`）。本地图片上传后会自动转为 Base64。 |
| `mode` | string | 否 | `text` | 前端生成模式：`text`（文生视频）、`image`（图生视频）、`keyframes`（关键帧动画）。关键帧模式实际通过 `extra_body` 传递。 |
| `height` | integer | 否 | `768` | 视频高度（像素）。与 `width` 共同决定输出分辨率；若与模型标准规格不完全匹配，API 会自动映射到最接近的标准尺寸。 |
| `width` | integer | 否 | `1152` | 视频宽度（像素）。默认组合 `1152×768` 对应 16:9 横屏 720p 档位。 |
| `num_frames` | integer | 否 | `121` | 生成视频的总帧数。必须 **≤ 441**，且遵循 **8n + 1** 规则（如 81、121、241、441）。 |
| `frame_rate` | number | 否 | `24` | 视频帧率，支持范围 **1–60**。与 `num_frames` 共同决定视频时长。 |
| `num_inference_steps` | integer | 否 | 模型默认 | 扩散推理步数。步数越高通常细节更好，但生成更慢；留空则由模型自行决定。 |
| `seed` | integer | 否 | 随机 | 随机种子。固定 seed 可在相同参数下获得可复现结果；留空则每次随机。 |
| `negative_prompt` | string | 否 | — | 负向提示词，描述需要**避免**出现在视频中的内容，如模糊、畸形、水印、低画质等。 |
| `extra_body.image` | array | 否 | — | **关键帧动画**参考图数组（至少 2 张）。支持公网 URL 或 Data URI Base64。 |
| `extra_body.mode` | string | 否 | — | 关键帧模式附加设置，使用 `keyframes` 时启用关键帧动画。 |

### 视频时长计算

视频时长由帧数和帧率决定：

```text
seconds = num_frames / frame_rate
```

| 目标时长 | 推荐 `num_frames` | 推荐 `frame_rate` | 预计秒数 |
| --- | --- | --- | --- |
| 约 3 秒 | `81` | `24` | 3.4 秒 |
| 约 5 秒 | `121` | `24` | 5.0 秒 |
| 约 10 秒 | `241` | `24` | 10.0 秒 |
| 约 18 秒 | `441` | `24` | 18.4 秒 |

> **注意**：`num_frames` 必须满足 `8n + 1`（n 为非负整数）。前端选择「自定义帧数」时会自动向下对齐到合法值。

### 分辨率与宽高比

Agnes Video V2.0 支持 **480p、720p、1080p** 三档标准分辨率。提交的 `width` / `height` 若不精确匹配，系统会自动映射到最接近的标准输出尺寸。

| 宽高比 | 推荐场景 | 本项目预设示例 |
| --- | --- | --- |
| `16:9` | 横版视频、产品演示、YouTube 风格 | 1152×768（720p）、1920×1080（1080p）、854×480（480p） |
| `9:16` | 竖版短视频、TikTok / Reels / Shorts | 768×1152（720p）、1080×1920（1080p） |
| `1:1` | 方形信息流、角色或产品展示 | 768×768（720p） |
| `4:3` | 传统横版演示 | 1024×768（720p） |
| `3:4` | 竖版肖像、产品为主内容 | 768×1024（720p） |

展示任务信息或排查问题时，请以 API 响应中的 `size`、`seconds` 字段为准，而非仅依赖请求参数。

### 三种生成模式说明

#### 1. 文生视频（text）

仅使用 `prompt` 从文字直接生成视频，无需图片输入。

**提示词示例：**

```text
A cinematic shot of a cat walking on the beach at sunset, soft ocean waves, warm golden lighting, realistic motion
```

#### 2. 图生视频（image）

上传一张参考图（本地 Base64 / 公网 URL），通过 `image` 参数传入，配合 `prompt` 描述希望发生的运动。

**提示词示例：**

```text
The woman slowly turns around and looks back at the camera, natural facial expression, cinematic camera movement
```

#### 3. 关键帧动画（keyframes）

使用 **2 张及以上**参考图，AI 会在关键帧之间生成平滑过渡动画。本项目支持直接上传本地图片（自动转 Base64），也支持公网 URL 或文生图参考图。

**本地上传关键帧动画流程：**

```text
选择「关键帧生成动画」→ 上传 2+ 张本地图片 → 选择参考图 → 填写过渡描述 → 生成视频
```

**API 请求结构（本地 Base64 示例）：**

```json
{
  "model": "agnes-video-v2.0",
  "prompt": "渐进式转场，保持画面风格一致，镜头运动自然流畅",
  "extra_body": {
    "image": [
      "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
      "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
      "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    ],
    "mode": "keyframes"
  },
  "width": 1152,
  "height": 768,
  "num_frames": 121,
  "frame_rate": 24
}
```

**提示词示例：**

```text
Generate a smooth cinematic transition between the keyframes, maintaining visual consistency and natural camera movement
```

### 任务响应字段

创建任务后，API 返回异步任务信息：

| 字段 | 说明 |
| --- | --- |
| `task_id` / `id` | 任务 ID，可用于旧版查询接口 |
| `video_id` | 视频 ID，**推荐**用于轮询结果 |
| `status` | 任务状态：`queued` → `in_progress` → `completed` / `failed` |
| `progress` | 进度百分比（0–100） |
| `seconds` | 视频时长（秒） |
| `size` | 实际输出分辨率，如 `1280x768` |
| `url` | 生成完成后的视频下载地址（仅 `completed` 时可用） |
| `error` | 失败时的错误信息 |

### 推荐参数组合

| 场景 | 推荐设置 |
| --- | --- |
| 标准横屏视频 | `width: 1152`, `height: 768`, `num_frames: 121`, `frame_rate: 24` |
| 社交短视频 | `num_frames: 81` 或 `121`, `frame_rate: 24`, 竖屏 9:16 预设 |
| 较长视频 | 增大 `num_frames`（最大 441）或适当降低 `frame_rate` |
| 更流畅运动 | `frame_rate: 24` 或 `30` |
| 可复现结果 | 设置固定 `seed` |
| 避免不良内容 | 填写 `negative_prompt` |
| 关键帧过渡 | `extra_body.mode: "keyframes"` + 多张关键帧图 |

### 前端页面对应关系

| 页面控件 | 对应 API 参数 |
| --- | --- |
| 视频描述 | `prompt` |
| 生成模式 | `mode` + `image` / `extra_body` |
| 分辨率 / 宽高比 | `width`, `height` |
| 目标时长 | `num_frames` |
| 帧率 | `frame_rate` |
| 负向提示词 | `negative_prompt` |
| 随机种子 | `seed` |
| 推理步数 | `num_inference_steps` |
| 上传本地图片 | 自动转 Base64，传入 `image` / `extra_body.image` |
| 公网图片 URL | `image` / `extra_body.image` |
| 参考图选择 | 决定传入 API 的图片列表 |
| API Key | 请求头 `Authorization`（可留空使用服务端默认） |

### 错误码

| HTTP 状态码 | 说明 |
| --- | --- |
| `400` | 请求参数无效，请检查帧数规则、必填项等 |
| `401` | API Key 无效或未授权 |
| `404` | 任务或视频未找到 |
| `500` | 服务端错误 |
| `503` | 服务繁忙，请稍后重试 |

---

## 说明

- 视频生成是**异步任务**：先创建任务，再轮询 `video_id` 获取结果；本服务会自动等待最多约 **10 分钟**（长视频如 18 秒/441 帧可能需要数分钟推理）。
- **本地图片关键帧动画**已验证可用：上传后自动转 Base64，无需公网图床。
- 生成过程可能需要一定时间，请耐心等待；完成后可在页面预览，并查看 `outputs/videos/` 本地文件。
- 如果接口返回失败，页面会显示清晰的错误提示。
- 所有生成结果都会保存在 `outputs/` 目录，便于后续下载和二次创作。

## 许可证

本项目仅用于本地演示、学习与个人创作场景。
