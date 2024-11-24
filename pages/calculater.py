import streamlit as st
import pandas as pd
import plotly.express as px

# アプリのタイトルを設定
st.set_page_config(
    page_title="シンプルなタスク管理アプリ",
    page_icon="📱",
    layout="wide"
)

# セッション状態の初期化
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# メインタイトル
st.title("📱 シンプルなタスク管理アプリ")

# タスク入力フォーム
with st.form("task_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        task = st.text_input("新しいタスク")
    with col2:
        priority = st.selectbox("優先度", ["高", "中", "低"])

    submitted = st.form_submit_button("タスクを追加")
    if submitted and task:
        st.session_state.tasks.append({"task": task, "priority": priority, "completed": False})
        st.success("タスクが追加されました！")

# タスク一覧の表示
if st.session_state.tasks:
    st.subheader("タスク一覧")
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            if st.checkbox(task["task"], key=f"task_{i}", value=task["completed"]):
                st.session_state.tasks[i]["completed"] = True
            else:
                st.session_state.tasks[i]["completed"] = False
        with col2:
            st.write(f"優先度: {task['priority']}")
        with col3:
            if st.button("削除", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()

# 統計の表示
if st.session_state.tasks:
    st.subheader("タスクの統計")
    completed_tasks = sum(1 for task in st.session_state.tasks if task["completed"])
    total_tasks = len(st.session_state.tasks)

    # 進捗状況のチャート
    progress_df = pd.DataFrame({
        "状態": ["完了", "未完了"],
        "タスク数": [completed_tasks, total_tasks - completed_tasks]
    })

    fig = px.pie(progress_df, values="タスク数", names="状態", title="タスクの進捗状況")
    st.plotly_chart(fig)