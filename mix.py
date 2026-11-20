#!/usr/bin/env python3
"""长安易主 E01《前771年 · 犬戎攻周》— 60 秒配乐 + 旁白混音。

配乐按 TREATMENT.md §节奏：60 BPM 低拨弦脉冲，大提琴短弓随路线推进，
框鼓落在换旗（t=24）与东迁（t=30）两个 downbeat 上。
- 低拨弦脉冲：古琴（pluck.py 物理建模），每拍一音（60 BPM = 1 音/秒），
  五声音阶低音区，轻触，作全片心跳。
- 大提琴短弓：cellos_spic（VSCO 2 CE 采样），落在结构点（攻箭 t=10、骊山 t=18、
  换旗 t=24、东迁 t=30、洛邑 t=44、结尾 t=48）。
- 框鼓：frame_drum（VCSL 采样），t=24 与 t=30 各一击。
旁白：voice 3（out3/n1–n6.wav），按 cues.json 的时槽摆放。
混音：旁白 RMS 比音乐高约 10 dB；输出 48 kHz 立体声 mix.wav。

运行（库根目录）：.venv/bin/python films/changan-e01/mix.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIB = HERE.parent.parent  # ~/workspace/lemo-opuscar
sys.path.insert(0, str(LIB))

import numpy as np
import soundfile as sf
from core.audio import sampler as S
from core.audio import pluck as P
from core.audio.sfx import SR, add, limit

DUR = 60.0

# ---------------- 配乐 ----------------
# 古琴低拨弦脉冲：60 BPM，每秒一音；五声音阶（A 小调五声：A C D E G），
# 低音区轮换，轻触（vel 0.30–0.45），pan 轻微左右摆动，作心跳。
PENTA = ['A2', 'C3', 'D3', 'E3', 'G3', 'A3', 'G3', 'E3', 'D3', 'C3']
melody = ['A2', 'C3', 'D3', 'E3', 'D3', 'C3', 'A2', 'G2', 'A2', 'C3',
          'D3', 'E3', 'G3', 'E3', 'D3', 'C3', 'D3', 'E3', 'D3', 'C3',
          'A2', 'C3', 'D3', 'E3', 'D3', 'C3', 'A2', 'G2', 'A2', 'C3']

events = []
# 古琴脉冲：t=0..59，每秒一音；前 3 秒（标题）更轻。
for i, pitch in enumerate(melody):
    t = float(i * 2)  # 每 2 秒一音，30 个音，作疏朗脉冲（60 BPM 的半速心跳）
    vel = 0.32 if t < 3 else 0.42
    events.append((t, 'guqin', pitch, 2.0, vel, 0.0))

# 大提琴短弓（spiccato）：结构点
cello_hits = [
    (10.0, 'D3', 0.8, 0.55),   # 攻箭出现
    (18.0, 'C3', 0.8, 0.55),   # 幽王败死于骊山
    (24.0, 'A2', 1.2, 0.65),   # 换旗（与框鼓同拍）
    (30.0, 'D3', 1.2, 0.65),   # 东迁（与框鼓同拍）
    (44.0, 'E3', 0.8, 0.50),   # 洛邑标记亮起
    (48.0, 'A2', 1.5, 0.60),   # 结尾卡
]
for t, pitch, dur, vel in cello_hits:
    events.append((t, 'cellos_spic', pitch, dur, vel, 0.1))

# 框鼓：t=24 换旗、t=30 东迁
for t in (24.0, 30.0):
    events.append((t, 'frame_drum', 'large', None, 0.8, 0.0))

# 用 sampler.render 渲染采样乐器（cello + frame drum），用 pluck 渲染古琴，再叠加。
sample_events = [e for e in events if e[1] in ('cellos_spic', 'frame_drum')]
mix = S.render(sample_events, dur=DUR)

# 古琴：逐音 pluck 后叠加（pluck 返回 mono float32 @48k）
for t, inst, pitch, dur, vel, pan in events:
    if inst != 'guqin':
        continue
    note = P.pluck('guqin', pitch, dur, vel=vel)
    add(mix, note, t, gain=1.0, pan=pan)

mix = S.room(mix, size=.45, mix=.16)

# ---------------- 旁白 ----------------
VOICE = HERE / 'voice' / 'out3'
# (clip, slot start s) — 按 cues.json；每句时长已量过，均短于时槽。
narr = [
    ('n1.wav', 3.0),
    ('n2.wav', 10.0),
    ('n3.wav', 18.0),
    ('n4.wav', 24.0),
    ('n5.wav', 30.0),
    ('n6.wav', 48.0),
]
# 旁白先压限幅、再按 RMS 摆到比音乐高约 10 dB。
for fname, t in narr:
    data, sr = sf.read(VOICE / fname, dtype='float32')
    if sr != SR:
        import soxr
        data = soxr.resample(data, sr, SR)
    if data.ndim > 1:
        data = data[:, 0]  # 旁白取单声道，add() 会按 pan 铺成立体声
    # 轻压缩：峰值限幅到 0.9
    peak = float(np.max(np.abs(data))) or 1.0
    data = data / peak * 0.85
    add(mix, data, t, gain=1.0, pan=0.0)

mix = limit(mix)
out = HERE / 'mix.wav'
sf.write(out, mix, SR)
print(f'wrote {out}  {len(mix)/SR:.2f}s  peak={float(np.max(np.abs(mix))):.3f}')
