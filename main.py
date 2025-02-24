import streamlit as st
import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
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
# https://docs.streamlit.io/develop/tutorials/databases/vate-gsheet に書いてある
def connect_gsheet():
    creds_info = st.secrets["gcp_service_account"]
    # 認証情報を使って Google Sheets API に接続
    gc = gspread.service_account_from_dict(creds_info)
    # # 書き込み対象のスプレッドシートキーまたは URL を指定
    SPREADSHEET_KEY = creds_info["spreadsheet_key"]  # secrets.toml に設定しておく
    spreadsheet = gc.open_by_key(SPREADSHEET_KEY)
    return spreadsheet

# 初期化処理

# df = get_as_dataframe(connect_gsheet().worksheet("Template"))
# st.session_state.df = df.iloc[:40, :]

tab1, tab2, tab3, tab4 = st.tabs(["遠征スコア", "探索スコア","スプレッドシート取得","その他"])

with tab1:
    st.title("遠征スコア")
    uploaded_file = st.file_uploader("遠征スコアの画像ファイルをアップロード", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # 画像読み込み
        base_image = Image.open(uploaded_file)
        # st.image(base_image, caption="Uploaded Image")
        # 名前の抽出
        extract_expedition_name_images = utils.extract_expedition_name_images(base_image)
        names = []
        for i, img in enumerate(extract_expedition_name_images):
            image = utils.pre_treatment(img)
            names.append(utils.ocr_name(image))
        # 数字の抽出
        extract_expedition_score_images = utils.extract_expedition_score_images(base_image)
        expedition_scores = []
        for i, img in enumerate(extract_expedition_score_images):
            image = img
            image = utils.pre_treatment(img)
            expedition_scores.append(utils.ocr_name(image))

        # 画像のサイズ取得（確認用）
        width, height = image.size
        st.write(f"画像のサイズ: {width} x {height}")

        # データまとめ
        df_expedition = pd.DataFrame({
            "ユーザ名": names,
            "遠征ボス証": expedition_scores
        })
        st.session_state["df_expedition"] = df_expedition
        st.dataframe(df_expedition)

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

            names.append(utils.ocr_name(image))
        # 数字の抽出
        extract_search_score_images = utils.extract_search_score_images(base_image)
        search_scores = []
        for i, img in enumerate(extract_search_score_images):
            image = img
            image = utils.pre_treatment(img)
            search_scores.append(utils.ocr_name(image))

        # 画像のサイズ取得（確認用）
        width, height = image.size

        # データまとめ
        df_search = pd.DataFrame({
            "ユーザ名": names,
            "探索バッヂ": search_scores
        })
        st.session_state["df_search"] = df_search
        st.dataframe(df_search)

with tab3:
    st.title("スプレッドシート取得")
    if "df_expedition" not in st.session_state:
        st.write("遠征スコアのデータがありません")
    elif "df_search" not in st.session_state:
        st.write("探索スコアのデータがありません")
    else:
        if st.button("データを合体して表示"):
            df_expedition = st.session_state["df_expedition"]
            df_search = st.session_state["df_search"]
            df = pd.concat([df_expedition, df_search], axis=0)
            df = df.drop_duplicates("ユーザ名")
            st.dataframe(df)
            spreadsheet = connect_gsheet()
            worksheet_read = spreadsheet.worksheet("Template")
            df_tmp = get_as_dataframe(worksheet_read).iloc[:40, :].copy()
            st.write(df_tmp)
            min_len = min(len(df_tmp), len(df))

            df_tmp.iloc[:min_len, df_tmp.columns.get_indexer(["ユーザ名", "遠征ボス証", "探索バッヂ"])] = \
    df.iloc[:min_len, df.columns.get_indexer(["ユーザ名", "遠征ボス証", "探索バッヂ"])].values
            if len(df_tmp) > len(df):
                df_tmp.loc[len(df):, "ユーザ名"] = None
                df_tmp.loc[len(df):, "遠征ボス証"] = 0
                df_tmp.loc[len(df):, "探索バッヂ"] = 0
            st.write(df_tmp)
            worksheet_write = spreadsheet.sheet1
            set_with_dataframe(worksheet_write, df_tmp)
            st.write(f"[スプレッドシート](https://docs.google.com/spreadsheets/d/{spreadsheet.id}/edit#gid=0)")
with tab4:
    st.title("猫の画像生成アプリ")
    # ボタンを押すと猫の画像を生成
    if st.button("猫の画像を生成"):
        # The Cat API を使って画像を取得
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        if response.status_code == 200:
            data = response.json()
            if data:
                # 画像のURLを取得
                image_url = data[0]["url"]
                st.write("画像URL:", image_url)
                st.image(image_url, caption="Generated Cat Image")
        else:
            st.error("猫の画像を取得できませんでした。")