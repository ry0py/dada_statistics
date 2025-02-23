import streamlit as st
import gspread
from gspread_dataframe import set_with_dataframe
from PIL import Image, ImageFilter
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

# スプレッドシートに接続
# https://docs.streamlit.io/develop/tutorials/databases/private-gsheet に書いてある
def connect_gsheet():
    creds_info = st.secrets["gcp_service_account"]
    # 認証情報を使って Google Sheets API に接続
    gc = gspread.service_account_from_dict(creds_info)
    # # 書き込み対象のスプレッドシートキーまたは URL を指定
    SPREADSHEET_KEY = creds_info["spreadsheet_key"]  # secrets.toml に設定しておく
    spreadsheet = gc.open_by_key(SPREADSHEET_KEY)
    return spreadsheet


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

    # 画像のサイズ取得（確認用）
    width, height = image.size
    st.write(f"画像のサイズ: {width} x {height}")

    # データまとめ
    df = pd.DataFrame({
        "名前": names,
        "数字": numbers
    })
    st.session_state.df = df
    spreadsheet = connect_gsheet()
    worksheet = spreadsheet.sheet1
    set_with_dataframe(worksheet, df)
    st.dataframe(df)
    # リンクを張る https://docs.google.com/spreadsheets/d/1RYhxfQdzFATlLyydsCxeWcB5IIuB3vqxe5-5AymvZ3I/edit?gid=0#gid=0
    st.write(f"[スプレッドシート](https://docs.google.com/spreadsheets/d/{spreadsheet.id}/edit#gid=0)")
