import streamlit as st

st.title("Calculadora de Farm - RubiniCoins")

st.write("Calcule quanto você farma em reais por hora.")

gold_por_hora = st.number_input("Gold farmado por hora", value=1000000)

preco_coin_gold = st.number_input("Preço de 1 RubiniCoin em gold", value=55000)

valor_1000_coins = st.number_input("Valor pago por 1000 coins (R$)", value=85.0)

# cálculos
coins_por_hora = gold_por_hora / preco_coin_gold
reais_por_coin = valor_1000_coins / 1000
reais_por_hora = coins_por_hora * reais_por_coin

st.subheader("Resultado")

st.write(f"Coins farmadas por hora: {coins_por_hora:.2f}")
st.write(f"Valor por coin: R$ {reais_por_coin:.4f}")
st.success(f"💰 Reais por hora: R$ {reais_por_hora:.2f}")
