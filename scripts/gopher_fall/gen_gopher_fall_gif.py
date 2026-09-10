"""
PNG 画像を元に、上から下へ落下するアニメーション GIF を生成する。

使い方:
  python3 gen_fall_gif.py <src.png> <out.gif>
"""

import argparse, sys
from PIL import Image
import math

parser = argparse.ArgumentParser(description="落下アニメーション GIF 生成")
parser.add_argument("src", help="入力 PNG ファイルパス")
parser.add_argument("out", help="出力 GIF ファイルパス")
args = parser.parse_args()

SRC = args.src
OUT = args.out

CANVAS_W = 96
CANVAS_H = 96
BG_COLOR = (255, 255, 255, 255)

NUM_FRAMES = 16
FRAME_DURATION_MS = 90

gopher_orig = Image.open(SRC).convert("RGBA")
SCALE = 1.5
gopher = gopher_orig.resize(
    (int(gopher_orig.width * SCALE), int(gopher_orig.height * SCALE)),
    Image.NEAREST,
)
gw, gh = gopher.size

frames = []

for i in range(NUM_FRAMES):
    t = i / (NUM_FRAMES - 1)  # 0.0 → 1.0

    # 上端の外（-gh）から下端の外（キャラ2体分の余白付き）まで一定速度で落下
    y = int(-gh + t * (CANVAS_H + gh * 2))
    x = (CANVAS_W - gw) // 2

    # 落下中に少し回転（最大 15 度）
    angle = math.sin(t * math.pi * 2) * 8
    rotated = gopher.rotate(angle, resample=Image.BICUBIC, expand=False)

    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    canvas.paste(rotated, (x, y), rotated)

    # 透過GIF: アルファが薄いピクセルを透明色（index 0）にする
    p = canvas.convert("P", palette=Image.ADAPTIVE, colors=255)
    # パレットに透明色を追加（index 255 を透明として使う）
    palette = p.getpalette()
    palette[255 * 3:255 * 3 + 3] = [0, 0, 0]
    p.putpalette(palette)
    # アルファ < 128 のピクセルを透明色 index に置き換え
    alpha = canvas.split()[3]
    mask = alpha.point(lambda a: 255 if a < 128 else 0)
    p.paste(255, mask=mask)
    frames.append(p)

import subprocess, os, tempfile

LINGER_MS = 300
TMPDIR = tempfile.mkdtemp()

# 各フレームを個別のGIFとして保存
frame_paths = []
for idx, frame in enumerate(frames):
    path = os.path.join(TMPDIR, f"frame_{idx:03d}.gif")
    frame.save(path, transparency=255, disposal=2)
    frame_paths.append(path)

# 余韻用の空白フレームも保存（最後のフレームをそのまま流用）
linger_path = os.path.join(TMPDIR, "linger.gif")
frames[-1].save(linger_path, transparency=255, disposal=2)

# gifsicle でフレームを結合（余韻フレームの delay だけ長く設定）
normal_delay = FRAME_DURATION_MS // 10  # gifsicle は 1/100秒単位
linger_delay = LINGER_MS // 10

cmd = ["gifsicle", "--loop", "--colors", "256"]
for path in frame_paths:
    cmd += [f"--delay={normal_delay}", path]
cmd += [f"--delay={linger_delay}", linger_path]
cmd += ["-o", OUT]

subprocess.run(cmd, check=True)

# 一時ファイル削除
for p in frame_paths + [linger_path]:
    os.remove(p)
os.rmdir(TMPDIR)

print(f"生成完了: {OUT}  ({NUM_FRAMES} フレーム + 余韻 {LINGER_MS}ms, {CANVAS_W}x{CANVAS_H}px)")
