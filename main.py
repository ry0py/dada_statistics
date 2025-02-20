import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import re
import io

st.title("画像から名前と数値を抽出するアプリ")

st.write("""
画像をアップロードすると、OCR（文字認識）で名前と数字を抽出して
表示・Excel 形式でダウンロードできるようにします。
""")

uploaded_file = st.file_uploader("画像ファイルをアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 画像読み込み
    image = Image.open(uploaded_file)
    st.write("アップロードされた画像:")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Tesseract で日本語 OCR
    # 日本語の言語データがインストールされている場合、lang="jpn" を指定
    text = pytesseract.image_to_string(image, lang="jpn")

    st.write("抽出されたテキスト:")
    st.text(text)

    # 正規表現で「名前 + 数字」を抽出
    # 例: 「たむちゃん 76」のような形を想定
    # 必要に応じてパターンは調整してください
    pattern = re.compile(r"([\u3040-\u309F\u30A0-\u30FF\uFF00-\uFF9F\u4E00-\u9FFF]+)\s*(\d+)")
    matches = pattern.findall(text)

    if matches:
        # リストを DataFrame に変換
        df = pd.DataFrame(matches, columns=["名前", "数値"])
        st.write("抽出結果:")
        st.dataframe(df)

        # Excel ファイルとしてダウンロードできるようにバイナリを用意
        # openpyxl を使って書き込む
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")

        st.download_button(
            label="Excelファイルをダウンロード",
            data=excel_buffer.getvalue(),
            file_name="extracted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # CSV ダウンロードの例 (必要なら)
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="CSVファイルをダウンロード",
            data=csv_data,
            file_name="extracted_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("名前と数字のペアが見つかりませんでした。")

