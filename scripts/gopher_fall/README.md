# gopher_fall

PNG 画像を元に、上から下へ落下するアニメーション GIF を生成するスクリプト。

## 依存

- Python 3
- [Pillow](https://python-pillow.org/)
- [gifsicle](https://www.lcdf.org/gifsicle/)

```bash
pip install pillow
brew install gifsicle
```

## 使い方

```bash
python3 gen_gopher_fall_gif.py <src.png> <out.gif>
```

## 実行例

`go-gopher/` 配下の画像を上書きする場合:

```bash
python3 gen_gopher_fall_gif.py ../../assets/go-gopher/gopher_fall_color.png ../../assets/go-gopher/gopher_fall_color.gif
python3 gen_gopher_fall_gif.py ../../assets/go-gopher/gopher_fall_white.png ../../assets/go-gopher/gopher_fall_white.gif
```
