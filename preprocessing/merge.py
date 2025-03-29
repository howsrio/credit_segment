import pandas as pd
import os

# monthly_merge_data 폴더 생성
os.makedirs('../data/monthly_merge_data', exist_ok=True)

# 월별 데이터 병합 함수
def merge_monthly_data(month):
    # 각 데이터프레임 로드
    member = pd.read_parquet(f'../data/train/1.회원정보/2018{month}_train_회원정보.parquet')
    credit = pd.read_parquet(f'../data/train/2.신용정보/2018{month}_train_신용정보.parquet')
    sales = pd.read_parquet(f'../data/train/3.승인매출정보/2018{month}_train_승인매출정보.parquet')
    claim = pd.read_parquet(f'../data/train/4.청구입금정보/2018{month}_train_청구정보.parquet')
    balance = pd.read_parquet(f'../data/train/5.잔액정보/2018{month}_train_잔액정보.parquet')
    channel = pd.read_parquet(f'../data/train/6.채널정보/2018{month}_train_채널정보.parquet')
    marketing = pd.read_parquet(f'../data/train/7.마케팅정보/2018{month}_train_마케팅정보.parquet')
    performance = pd.read_parquet(f'../data/train/8.성과정보/2018{month}_train_성과정보.parquet')
    
    # 데이터프레임 병합
    total = member.merge(credit, on=['기준년월', 'ID'], how='left')\
        .merge(sales, on=['기준년월', 'ID'], how='left')\
        .merge(claim, on=['기준년월', 'ID'], how='left')\
        .merge(balance, on=['기준년월', 'ID'], how='left')\
        .merge(channel, on=['기준년월', 'ID'], how='left')\
        .merge(marketing, on=['기준년월', 'ID'], how='left')\
        .merge(performance, on=['기준년월', 'ID'], how='left')
    
    # 병합된 데이터프레임 저장 경로 변경
    total.to_parquet(f'../data/monthly_merge_data/2018{month}_train_total.parquet')
    #30개의 행만 excel로 저장
    total.head(30).to_excel(f'../data/monthly_merge_data/2018{month}_train_total_example.xlsx')
    return total

# 7월부터 12월까지 데이터 병합
months = ['07', '08', '09', '10', '11', '12']
total_dfs = {}

for month in months:
    print(f'Processing month: {month}')
    total_dfs[month] = merge_monthly_data(month)
    print(f'shape: {total_dfs[month].shape}')