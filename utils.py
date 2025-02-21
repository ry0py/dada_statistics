from PIL import Image, ImageFilter, ImageOps
import pytesseract
def extract_name_images(image):
    step_hight = 100
    step_width = 525
    init_width = 285
    init_height = 700
    images =[]
    for i in range (7):
        images.append(image.crop((init_width, init_height, init_width + step_width, init_height + step_hight)))
        init_height += step_hight
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
    # --psm 6: ブロック単位での認識を想定
    # --oem 3: LSTMベースエンジンのみを使用 (バージョンにより挙動が変わる)
    custom_config = r'--oem 3 --psm 7'
    # 日本語の言語データがインストールされている場合、lang="jpn" を指定
    text = pytesseract.image_to_string(image, lang="jpn", config=custom_config)
    return text