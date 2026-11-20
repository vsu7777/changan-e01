#!/bin/bash
# 长安易主系列 · 第 1 场《前771年 · 犬戎攻周》试段 30 s, 24 fps
# 渲染:风格帧(全质量) → 全片 30 s → faststart 封装 → 验片
#
# 机器说明:本机 WebGL 走 SwiftShader 软件渲染(无 GPU)。
#   全质量(SSAA 2× + DOF maxCoc 7)约 60 s/帧,720 帧约 12 小时,不可行。
#   视频用 ?ssaa=1&maxcoc=0 渲染(约 7.7 s/帧):DOF 在本片距离下肉眼几无差别(A/B 已验),
#   SSAA 降 1× 后 3D 边缘略粗,2D 文字不受影响(叠加层为 2× 画布)。
#   必须用 --workers 1:本机内存约 8GB,3 个 SwiftShader 浏览器同时跑会在首帧截图时
#   "Target crashed"(内存不足);单 worker 已验证稳定,720 帧约 90 分钟。
#   index.html 的默认仍是全质量(SSAA 2× + DOF 7),有 GPU 的机器按默认渲即得全风格。
#   风格帧用全质量渲(见 /tmp/render_frames.mjs,截图超时放宽到 300 s,
#   因 core/render/still.mjs 的截图默认 30 s 超时,全质量帧 capture 不了)。
set -euo pipefail
LIB=/home/hatch/workspace/lemo-opuscar
cd "$LIB"

# ---- 风格帧(3 张,全质量:开场俯冲 t=1.5 / 示意箭头+情报卡 t=14 / 标志性镜头:俯冲骊山近景 t=21) ----
node /tmp/render_frames.mjs ""

# ---- 30 s 全片(ssaa=1 + maxcoc=0,见上) ----
node core/render/video.mjs films/changan-e01 --size 1920x1080 --fps 24 --workers 1 --q 'ssaa=1&maxcoc=0' --out films/changan-e01/changan-e01_trial_30s.tmp.mp4
ffmpeg -y -i films/changan-e01/changan-e01_trial_30s.tmp.mp4 -c copy -movflags +faststart films/changan-e01/changan-e01_trial_30s.mp4
rm -f films/changan-e01/changan-e01_trial_30s.tmp.mp4

# ---- 验片(与视频同配置) ----
node core/render/still.mjs films/changan-e01 --range 0:30:0.5 --q 'ssaa=1&maxcoc=0' --out films/changan-e01/stills/sheet
python3 core/render/sheet.py films/changan-e01/stills/sheet.jpg films/changan-e01/stills/sheet/t_*.jpg --cols 4 --w 480
node core/render/readcheck.mjs films/changan-e01

echo OK
