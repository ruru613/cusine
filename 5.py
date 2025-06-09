import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from fastai.vision.all import *
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
import base64
import random
import matplotlib.pyplot as plt
import time
import shutil
import pathlib
import torch
import pickle
import asyncio

# 初始化事件循环（解决 Streamlit 异步冲突）
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# 设置页面配置
st.set_page_config(page_title="食堂菜品识别系统", layout="wide")

# 设置中文字体支持
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 初始化会话状态
if 'user_ratings' not in st.session_state:
    st.session_state.user_ratings = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = int(time.time() * 1000) % 1000000
if 'current_page' not in st.session_state:
    st.session_state.current_page = "首页"
if 'collab_model' not in st.session_state:
    st.session_state.collab_model = None

# 文件路径配置
RATINGS_FILE = Path(__file__).parent / '评分数据.xlsx'
BACKUP_DIR = Path(__file__).parent / 'ratings_backups'
DISHES_FILE = Path(__file__).parent / "菜品介绍.xlsx"

# 创建备份目录
BACKUP_DIR.mkdir(exist_ok=True)

# 加载模型和数据



@st.cache_resource
def load_model():
    model_path = pathlib.Path(__file__).parent / "dish.pkl"
    return load_learner(str(model_path))  # 显式转字符串，避免路径对象序列化

model = load_model()

st.title("菜品识别系统")