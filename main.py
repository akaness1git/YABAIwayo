# coding: utf-8
import os
import random
from datetime import datetime
from PIL import Image

split_level = 1
# 分割レベル
# 1.....4分割
# 2....16分割
# 3....64分割
# 4...256分割
# 5..1024分割


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


# n分割用
def rand_split_yabai_image(src, split_level):
    split_level = split_level - 1
    if split_level < 0:
        return src
    image_tmp = rand_yabai_image(src)

    return rand_split_yabai_image(image_tmp, split_level)


# n分割出力用
def n_split(src, split_level):
    if len(src) == 1:
        return src[0]
    else:
        image_list_tmp = []
        for i in range(4 ** (split_level - 2)):
            j = i * 4
            im_tmp1 = link_image_h(src[j], src[j + 1])
            im_tmp2 = link_image_h(src[j + 2], src[j + 3])
            image_list_tmp.append(link_image_v(im_tmp1, im_tmp2))
        return n_split(image_list_tmp, split_level - 1)


def main():
    try:
        image_list = []
        split_num = 4 ** split_level
        split_roop = 4 ** (split_level - 1)
        print(str(split_num) + "分割スタート！")
        yabaiwayo_time = datetime.now().strftime('%Y%m%d%H%M%S')
        # イメージファイルを開く
        im = Image.open(curdir + '/' + imagefilename)
        for i in range(split_roop):
            im_tmp1 = link_image_h(rand_split_yabai_image(im, split_level), rand_split_yabai_image(im, split_level))
            im_tmp2 = link_image_h(rand_split_yabai_image(im, split_level), rand_split_yabai_image(im, split_level))
            image_list.append(link_image_v(im_tmp1, im_tmp2))

        n_split(image_list, split_level).save(resultdir + str(split_num) + 'x_' + yabaiwayo_time + '.jpg')

        print("End")

    except Exception as x:
        print(x)


if __name__ == "__main__":
    main()

