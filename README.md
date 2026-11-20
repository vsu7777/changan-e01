# 长安易主 · 第一场《前771年 · 犬戎攻周》

立体地图解说纪录片系列《长安易主》的第 1 集（共 50 集，每集约 60 秒）。
用 [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) 的 `map-explainer`
风格纯代码渲染：3D 地形 + 发光路线 + 阵营名牌 + 情报卡，无视频模型、无脸可漂。

- **成片**：60 秒，1920×1080，24 fps，h264 + AAC（旁白 + 配乐）
- **旁白**：3 号年轻女声（Xiaoxiao 因网络代理拦住 WebSocket 握手，暂用 3 号；Xiaoxiao 可日后替换）
- **配乐**：60 BPM 低拨弦脉冲（古琴物理建模）+ 大提琴短弓 + 框鼓（t=24 换旗、t=30 东迁两个 downbeat）

## 本集内容

前 771 年，犬戎攻周。申侯联军自西而来，幽王败死于骊山，宗周失守，西周终结；
周室东迁，政治中心东移洛邑。

**五条红线**（全片死守，见 `FACTS.md`）：

1. 烽火戏诸侯是传说，不作事实呈现；
2. 入侵路线未经核实——不画分步路线（尤其不走萧关），联军接近只用一条标「示意」的示意箭头；
3. 不画具体建筑焚烧，失守只用旗帜更换 + 标记变暗表现；
4. 纪年只写「前771年（传统纪年）」，不写月日；
5. 不写兵力、伤亡数字。

## 目录

| 文件 | 说明 |
|---|---|
| `index.html` | 全片画面代码（DUR=60，含东迁路线、洛邑标记、结尾卡、机位轨迹） |
| `post.js` | 后期（字幕烧录等） |
| `mix.py` | 配乐 + 旁白混音（古琴/大提琴/框鼓 + 6 句旁白，输出 `mix.wav`） |
| `cues.json` | 7 条字幕/旁白时槽 |
| `TREATMENT.md` | 分镜与节奏方案 |
| `FACTS.md` | 事实核查（坐标、红线、东迁路线示意的 caveat） |
| `NARRATION_60s.md` | 60 秒旁白稿（6 拍，红线逐句核过） |
| `CORRECTIONS.md` | 试段修正记录（删 800 km 俯冲、丰镐纯白、删咸阳等） |
| `CREDITS` | 素材来源与授权 |
| `assets/` | 地形元数据（`meta.json`）；地形贴图/高程由 `tools/fetch.py` 拉取 |
| `raw/` | 原始瓦片清单与范围（`bbox.json` / `manifest.jsonl`） |
| `tools/` | 取数与预处理脚本（`fetch.py` / `prep.py` / `bake.py` 等） |
| `voice/` | 旁白文案（`lines.json`）与 TTS 包装（`run_tts.py`） |
| `build.sh` | 构建入口（注意：先确认其中引用的临时文件路径） |

## 复现

1. 按 Lemo-Opuscar 的说明装好环境（Node、ffmpeg、Python venv、Playwright
   chromium-headless-shell），并装 voice + music 两档依赖。
2. `tools/fetch.py` 拉取地形与影像瓦片（来源见 `CREDITS`：地形 AWS Terrain Tiles，
   影像 Sentinel-2 Cloudless 2016），`tools/prep.py` / `bake.py` 预处理；
   字体由 `tools/fonts.py` 取 Noto Sans CJK SC 子集。
3. 渲染画面（单 worker，降质 `?ssaa=1&maxcoc=0`，约 8 秒/帧；30 秒约 98 分钟。
   本机无 GPU，WebGL 走 SwiftShader 软件渲染；3 worker 并行会内存不足，务必单 worker）：
   `node core/render/video.mjs films/changan-e01 --size 1920x1080 --fps 24 --workers 1 --q 'ssaa=1&maxcoc=0'`
   长片建议拆成 10 秒一段分开渲（整段被虚拟机重启打断会全丢，分段只丢一段）。
4. 旁白：`voice/lines.json` 用 TTS 生成（本集用 3 号声线）；`mix.py` 混配乐与旁白。
5. 合成：`ffmpeg` 拼画面 + `mix.wav`，`-movflags +faststart`。

## 备注

- 本仓库只含文本工程文件（代码、文档、配置、脚本）。二进制素材（地形贴图/高程、
  旁白音频、字体子集、成片 mp4）不入库，按上节步骤拉取或生成；成片另行分发。
- `voice/combined-ca.pem`（本机代理 CA 束）未入库，Xiaoxiao TTS 的代理绕法见 `voice/run_tts.py` 注释。
- 系列分集表（94 项年表筛出的 50 场城池易主）不在本仓库。
