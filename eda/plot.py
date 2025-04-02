import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

import platform
import matplotlib.font_manager as fm

def set_fonts():
    # OS에 따라 폰트 설정
    if platform.system() == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우: 맑은 고딕
    elif platform.system() == 'Darwin':  # macOS
        plt.rcParams['font.family'] = 'AppleGothic'
    else:  # 리눅스나 기타
        plt.rcParams['font.family'] = 'NanumGothic'

    # 마이너스 부호 깨지는 문제 해결
    plt.rcParams['axes.unicode_minus'] = False

def plot_segment_grid(dfs : list, 
                      col : str, 
                      is_categorical = True,
                      months = None, 
                      segment_col='Segment',
                      subfigsize=(4, 4),
                      numeric_plot_type = "box",
                      categorical_plot_type = "pie"):
    """
    월별 데이터프레임들에서 Segment별로 주어진 컬럼(col)의 시각화를 5xN 형태로 출력하는 함수.
    
    Parameters:
        dfs (list): 월별 데이터프레임들의 리스트
        col (str): 시각화할 컬럼 이름
        is_categorical (bool) : 해당 변수가 categorical 변수인지, else : 수치형
        months (list of str): 각 데이터프레임에 대응되는 월 이름 리스트
        segment_col (str): 세그먼트 컬럼 이름 (기본값 'Segment')
        subfigsize (tuple): 그림 하나의 크기 (가로, 세로)
        categorical_plot_type (str): "pie" or "bar"
    """

    # 폰트 설정
    set_fonts()
    
    # 입력받은 데이터프레임의 갯수 확인
    n_months = len(dfs)
    # month 값 할당
    if months is None:
        months = [f'Month {i+1}' for i in range(n_months)]
    
    segments = ['A', 'B', 'C', 'D', 'E']
    
    # 연속형 변수 전체 범위 계산
    is_numeric = all(pd.api.types.is_numeric_dtype(df[col]) for df in dfs)
    global_min = global_max = None
    if is_numeric:
        all_vals = pd.concat([df[col].dropna() for df in dfs])
        global_min, global_max = all_vals.min(), all_vals.max()
    
    # subfigsize를 통해,
    # 전체 figsize 계산
    figsize = (subfigsize[0] * n_months, subfigsize[1] * len(segments))

    fig, axes = plt.subplots(nrows = len(segments), 
                             ncols = n_months, 
                             figsize = figsize)
    fig.suptitle(f"Segment별 '{col}' 시각화 (월별)", fontsize=16)
    
    for row, segment in enumerate(segments):
        for col_idx, (df, month) in enumerate(zip(dfs, months)):
            ax = axes[row, col_idx] if n_months > 1 else axes[row]
            
            # 필터링 & NaN 제거
            sub_df = df[df[segment_col] == segment][col].dropna()
            
            if sub_df.empty:
                ax.set_title(f"{segment} - {month}")
                ax.text(0.5, 0.5, 'No Data', ha='center', va='center')
                ax.axis('off')
                continue
            
            # 연속형
            if not is_categorical:
                if numeric_plot_type == 'box':
                    sns.boxplot(y=sub_df, ax=ax)
                    if global_min is not None and global_max is not None:
                        ax.set_ylim(global_min, global_max)
                    ax.set_ylabel('')
                    ax.set_xlabel('')
            
                elif numeric_plot_type == 'hist':
                    ax.hist(sub_df, bins='auto', color='skyblue', edgecolor='black')
                    if global_min is not None and global_max is not None:
                        ax.set_xlim(global_min, global_max)
                    ax.set_ylabel('')
                    ax.set_xlabel(col)
            # 이진형, 범주형
            else:
                counts = sub_df.value_counts(normalize=True).sort_index()

                if categorical_plot_type == 'pie':
                    ax.pie(counts, 
                           labels=counts.index.astype(str), 
                           autopct='%1.1f%%', 
                           textprops={'fontsize': 18})
                    
                elif categorical_plot_type == 'bar':
                    ax.bar(counts.index.astype(str), 
                           counts.values, 
                           color=sns.color_palette("pastel", len(counts)))
                    ax.set_ylim(0, 1)
                    ax.set_xticks(range(len(counts)))
                    ax.set_xticklabels(counts.index.astype(str))

                else:
                    raise ValueError(f"cat_plot_type must be 'pie' or 'bar', but got '{categorical_plot_type}'")
            
            ax.set_title(f"{segment} - {month}", fontsize=10)
    
    # 전체 레이아웃 조정
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()