# coding: utf-8
import os
import random
from datetime import datetime
from PIL import Image

imagefilename = "yabaiwayo.jpg"

curdir = os.path.dirname(os.path.abspath(__file__))
resultdir = curdir + "/result/"


# 横に連結
def link_image_h(i1, i2):
    linkimage = Image.new('RGB', (i1.width + i2.width, i1.height))
    linkimage.paste(i1, (0, 0))
    linkimage.paste(i2, (i1.width, 0))

    return linkimage


# 縦に連結
def link_image_v(i1, i2):
    linkimage = Image.new('RGB', (i1.width, i1.height + i2.height))
    linkimage.paste(i1, (0, 0))
    linkimage.paste(i2, (0, i1.height))

    return linkimage


# イメージを180度回転させる
def image_180_rotate(src):
    return src.rotate(180)


# 読み込んだイメージの幅と高さを返す
def get_image_size(src):
    w = src.width
    h = src.height
    return w, h


# 読み込んだイメージを4分割する
def split_quarter_image(src):
    w, h = get_image_size(src)

    i1 = src.crop((0, 0, w / 2, h / 2))
    i2 = src.crop((w / 2, 0, w, h / 2))
    i3 = src.crop((0, h / 2, w / 2, h))
    i4 = src.crop((w / 2, h / 2, w, h))

    return i1, i2, i3, i4


# ランダムで1枚返す
def rand_one_image(src):
    i = random.randint(1, 4)
    i1, i2, i3, i4 = split_quarter_image(src)
    if i == 1:
        return i1
    elif i == 2:
        return i2
    elif i == 3:
        return i3
    elif i == 4:
        return i4
    else:
        raise ValueError("何か起きました")


# 回転したりしなかったりする
def rand_rotate_image(src):
    i = random.randint(1, 2)
    if i == 1:
        return image_180_rotate(src)
    elif i == 2:
        return src
    else:
        raise ValueError("何か起きました")


# ヤバイわよ！のパーツを1つ返す
def rand_yabai_image(src):
    return rand_rotate_image(rand_one_image(src))


def main():
    try:
        yabaiwayo_time = datetime.now().strftime('%Y%m%d%H%M%S')
        # イメージファイルを開く
        im = Image.open(curdir + '/' + imagefilename)
        im_tmp1 = link_image_h(rand_yabai_image(im), rand_yabai_image(im))
        im_tmp2 = link_image_h(rand_yabai_image(im), rand_yabai_image(im))
        link_image_v(im_tmp1, im_tmp2).save(resultdir + yabaiwayo_time + '.jpg')

    except Exception as x:
        print(x)


if __name__ == "__main__":
    main()