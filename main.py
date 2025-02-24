import streamlit as st
import gspread
from gspread_dataframe import set_with_dataframe
from PIL import Image, ImageFilter
import pandas as pd
import re
import io
import utils
import requests

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

tab1, tab2, tab3 = st.tabs(["遠征スコア", "探索スコア", "その他"])

with tab1:
    st.write("遠征スコア")
    uploaded_file = st.file_uploader("遠征スコアの画像ファイルをアップロード", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # 画像読み込み
        base_image = Image.open(uploaded_file)
        st.image(base_image, caption="Uploaded Image")
        st.write("アップロードされた画像:")

        st.write("切り取られた画像:")
        # 名前の抽出
        extract_expedition_name_images = utils.extract_expedition_name_images(base_image)
        names = []
        for i, img in enumerate(extract_expedition_name_images):
            image = utils.pre_treatment(img)
            st.image(image, caption=f"Image {i}")
            names.append(utils.ocr_name(image))
            print(names)
        # 数字の抽出
        extract_expedition_score_images = utils.extract_expedition_score_images(base_image)
        expedition_scores = []
        for i, img in enumerate(extract_expedition_score_images):
            image = img
            image = utils.pre_treatment(img)
            st.image(image, caption=f"Image {i}")
            expedition_scores.append(utils.ocr_name(image))

        # 画像のサイズ取得（確認用）
        width, height = image.size
        st.write(f"画像のサイズ: {width} x {height}")

        # データまとめ
        df = pd.DataFrame({
            "名前": names,
            "遠征スコア": expedition_scores
        })
        st.session_state.df = df
        spreadsheet = connect_gsheet()
        worksheet = spreadsheet.sheet1
        set_with_dataframe(worksheet, df)
        st.dataframe(df)
        # リンクを張る https://docs.google.com/spreadsheets/d/1RYhxfQdzFATlLyydsCxeWcB5IIuB3vqxe5-5AymvZ3I/edit?gid=0#gid=0
        st.write(f"[スプレッドシート](https://docs.google.com/spreadsheets/d/{spreadsheet.id}/edit#gid=0)")

with tab2:
    st.title("探索スコア")
    uploaded_file = st.file_uploader("探索スコアの画像ファイルをアップロード", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # 画像読み込み
        base_image = Image.open(uploaded_file)
        st.image(base_image, caption="Uploaded Image")
        st.write("アップロードされた画像:")

        st.write("切り取られた画像:")
        # 名前の抽出
        extract_search_name_images = utils.extract_search_name_images(base_image)
        names = []
        for i, img in enumerate(extract_search_name_images):
            image = utils.pre_treatment(img)
            st.image(image, caption=f"Image {i}")
            names.append(utils.ocr_name(image))
            print(names)
        # 数字の抽出
        extract_search_score_images = utils.extract_search_score_images(base_image)
        expedition_scores = []
        for i, img in enumerate(extract_search_score_images):
            image = img
            image = utils.pre_treatment(img)
            st.image(image, caption=f"Image {i}")
            expedition_scores.append(utils.ocr_name(image))

        # 画像のサイズ取得（確認用）
        width, height = image.size
        st.write(f"画像のサイズ: {width} x {height}")

        # データまとめ
        df = pd.DataFrame({
            "名前": names,
            "遠征スコア": expedition_scores
        })
        st.session_state.df = df
        spreadsheet = connect_gsheet()
        worksheet = spreadsheet.sheet1
        set_with_dataframe(worksheet, df)
        st.dataframe(df)
        # リンクを張る https://docs.google.com/spreadsheets/d/1RYhxfQdzFATlLyydsCxeWcB5IIuB3vqxe5-5AymvZ3I/edit?gid=0#gid=0
        st.write(f"[スプレッドシート](https://docs.google.com/spreadsheets/d/{spreadsheet.id}/edit#gid=0)")
with tab3:
    st.title("猫の画像生成アプリ")

    # The Cat API を使って画像を取得
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    if response.status_code == 200:
        data = response.json()
        if data:
            # 画像のURLを取得
            image_url = data[0]["url"]
            st.write("画像URL:", image_url)
            # URLを直接st.imageに渡すか、画像をバイナリで取得して表示する方法のどちらかを選べます

            # 方法1: URLを直接渡す
            st.image(image_url, caption="Generated Cat Image", use_column_width=True)

            # 方法2: バイナリデータとして取得して表示する場合
            # image_response = requests.get(image_url)
            # if image_response.status_code == 200:
            #     image_bytes = io.BytesIO(image_response.content)
            #     image = Image.open(image_bytes)
            #     st.image(image, caption="Generated Cat Image", use_column_width=True)
    else:
        st.error("猫の画像を取得できませんでした。")