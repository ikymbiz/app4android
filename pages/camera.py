import streamlit as st
from PIL import Image
import numpy as np
import cv2
import io
import datetime
import os

# ページの設定
st.set_page_config(
    page_title="カメラアプリ",
    page_icon="📸",
    layout="wide"
)

# セッション状態の初期化
if 'captured_images' not in st.session_state:
    st.session_state.captured_images = []

if 'selected_filter' not in st.session_state:
    st.session_state.selected_filter = 'なし'


def apply_filter(image, filter_name):
    """画像にフィルターを適用する関数"""
    img_array = np.array(image)

    if filter_name == 'グレースケール':
        return cv2.cvtColor(cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB)
    elif filter_name == 'セピア':
        sepia_matrix = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ])
        sepia_img = cv2.transform(img_array, sepia_matrix)
        sepia_img[np.where(sepia_img > 255)] = 255
        return sepia_img
    elif filter_name == 'エッジ検出':
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    else:
        return img_array


def save_image(image):
    """画像を保存する関数"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.exists('captured_images'):
        os.makedirs('captured_images')
    filename = f'captured_images/image_{timestamp}.jpg'
    image.save(filename)
    return filename


# メインタイトルとサイドバー
st.title("📸 カメラアプリ")

# サイドバーでフィルターを選択
st.sidebar.header("フィルター設定")
filter_option = st.sidebar.selectbox(
    "フィルターを選択",
    ['なし', 'グレースケール', 'セピア', 'エッジ検出']
)

# カメラ入力
camera_col, preview_col = st.columns(2)

with camera_col:
    st.header("カメラ")
    camera_image = st.camera_input("写真を撮影")

    if camera_image:
        # 画像の処理
        img = Image.open(camera_image)

        # フィルター適用
        filtered_img = apply_filter(img, filter_option)

        # プレビューの表示
        with preview_col:
            st.header("プレビュー")
            st.image(filtered_img, caption=f"フィルター: {filter_option}")

            # 保存ボタン
            if st.button("画像を保存"):
                filename = save_image(Image.fromarray(filtered_img))
                st.session_state.captured_images.append(filename)
                st.success(f"画像を保存しました: {filename}")

# 保存された画像のギャラリー
if st.session_state.captured_images:
    st.header("保存された画像")
    gallery_cols = st.columns(3)

    for idx, img_path in enumerate(st.session_state.captured_images):
        try:
            with gallery_cols[idx % 3]:
                st.image(img_path, caption=f"画像 {idx + 1}")
        except Exception as e:
            st.error(f"画像の読み込みエラー: {e}")