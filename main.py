import streamlit as st
from PIL import Image, ImageFilter
import pytesseract
import pandas as pd
import re
import io
import utils

st.title("画像から名前と数値を抽出するアプリ")

st.write("""
画像をアップロードすると、OCR（文字認識）で名前と数字を抽出して
表示・Excel 形式でダウンロードできるようにします。
""")
st.write("画像には名前が7つ入っていることを前提としています")

uploaded_file = st.file_uploader("画像ファイルをアップロード", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    # 画像読み込み
    base_image = Image.open(uploaded_file)
    st.image(base_image, caption="Uploaded Image")
    st.write("アップロードされた画像:")

    st.write("切り取られた画像:")
    # 名前の抽出
    extracted_names_images = utils.extract_name_images(base_image)
    names = []
    for i, img in enumerate(extracted_names_images):
        image = utils.pre_treatment(img)
        st.image(image, caption=f"Image {i}")
        names.append(utils.ocr_name(image))
        print(names)
    # 数字の抽出
    extracted_number_images = utils.extract_number_images(base_image)
    numbers = []
    for i, img in enumerate(extracted_number_images):
        image = img
        image = utils.pre_treatment(img)
        st.image(image, caption=f"Image {i}")
        numbers.append(utils.ocr_name(image))
        print(numbers)

    # 画像のサイズ取得（確認用）
    width, height = image.size
    st.write(f"画像のサイズ: {width} x {height}")


    st.write("抽出されたテキスト:")
    for i in range(len(names)):
        st.write(f"{names[i]}:{numbers[i]}")

    # # 正規表現で「名前 + 数字」を抽出
    # # 例: 「たむちゃん 76」のような形を想定
    # # 必要に応じてパターンは調整してください
    # pattern = re.compile(r"([\u3040-\u309F\u30A0-\u30FF\uFF00-\uFF9F\u4E00-\u9FFF]+)\s*(\d+)")
    # matches = pattern.findall(text)

    # if matches:
    #     # リストを DataFrame に変換
    #     df = pd.DataFrame(matches, columns=["名前", "数値"])
    #     st.write("抽出結果:")
    #     st.dataframe(df)

    #     # Excel ファイルとしてダウンロードできるようにバイナリを用意
    #     excel_buffer = io.BytesIO()
    #     with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    #         df.to_excel(writer, index=False, sheet_name="Sheet1")

    #     st.download_button(
    #         label="Excelファイルをダウンロード",
    #         data=excel_buffer.getvalue(),
    #         file_name="extracted_data.xlsx",
    #         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    #     )

    #     # CSV ダウンロード
    #     csv_data = df.to_csv(index=False)
    #     st.download_button(
    #         label="CSVファイルをダウンロード",
    #         data=csv_data,
    #         file_name="extracted_data.csv",
    #         mime="text/csv"
    #     )
    # else:
    #     st.warning("名前と数字のペアが見つかりませんでした。")
