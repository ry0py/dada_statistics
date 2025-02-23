from PIL import Image, ImageFilter, ImageOps
import pytesseract
# extract系はすべてまとめられるけど面倒だからいいや
def extract_expedition_name_images(image):
    step_height = 130
    step_width = 510
    init_width = 290
    images =[]
    for i in range (7):
        init_height = 700 + i*210
        images.append(image.crop((init_width, init_height, init_width + step_width, init_height + step_height)))
    return images
def extract_expedition_score_images(image):
    step_height = 120
    step_width = 100
    init_width = 925
    images =[]
    for i in range (7):
        init_height = 700 + i*210
        images.append(image.crop((init_width, init_height, init_width + step_width, init_height + step_height)))
    return images


def pre_treatment(image):
    # 1. グレースケール化
    new_image = image.convert("L")
    # 2. 二値化（しきい値を調整）
    threshold = 120
    new_image = new_image.point(lambda x: 255 if x > threshold else 0, mode="1")
    # 3. シャープ化 (ノイズが多い場合はMedianFilterなども試す)
    new_image = new_image.filter(ImageFilter.SHARPEN)
    # 4. 反転
    new_image_invert = ImageOps.invert(new_image.convert('RGB'))
    return new_image_invert
def ocr_name(image):
    # Tesseract の設定
    # --psm 7: ブロック単位での認識を想定
    # --oem 3: LSTMベースエンジンのみを使用 (バージョンにより挙動が変わる)
    custom_config = r'--oem 3 --psm 7'
    # 日本語の言語データがインストールされている場合、lang="jpn" を指定
    text = pytesseract.image_to_string(image, lang="jpn", config=custom_config)
    return text