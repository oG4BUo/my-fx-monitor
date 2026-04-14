import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.title("📈 リアルタイム為替モニター")

# --- データ取得部分（ここを強化しました） ---
def get_fx_data():
    symbol = "USDJPY=X"
    # period="1d"だとデータが空になることがあるため、直近5日分を取得して最新を見るように変更
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="7d", interval="1h") 
    return df

try:
    data = get_fx_data()
    
    # 取得したデータが空っぽじゃないかチェック
    if data.empty:
        st.error("現在、為替データが取得できません。市場が閉まっているか、通信エラーの可能性があります。")
    else:
        # 最新の有効な価格を取得
        current_price = data['Close'].iloc[-1]
        last_update = data.index[-1].strftime("%Y/%m/%d %H:%M:%S")

        col1, col2 = st.columns(2)
        col1.metric("現在のドル/円", f"{current_price:.2f} 円")
        col2.metric("最終更新(日本時間)", last_update)

        # チャートの表示
        st.subheader("直近の値動き")
        # 直近100件分くらいに絞って表示
        st.line_chart(data['Close'].tail(100))

except Exception as e:
    st.error(f"エラーが発生しました: {e}")

# 自動更新の設定（1分ごと）
time.sleep(60)
st.rerun()
