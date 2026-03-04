# --- CALCULADORA DE PROBABILIDADES SMILES/GOL ---

media_atual = float(input("Qual sua média atual? (Ex: 8.4): "))
total_avaliacoes = int(input("Total de avaliações atual: "))

print(f"\n📊 ANÁLISE DE IMPACTO (Para mudar 0.1 na média)")
print("="*60)
print(f"{'NOTA RECEBIDA':<20} | {'PARA SUBIR (+0.1)':<20} | {'PARA CAIR (-0.1)':<20}")
print("-" * 60)

# Alvos
alvo_subir = media_atual + 0.1
alvo_cair = media_atual - 0.1

# Testando cada nota de 0 a 10
for nota in range(11):
    # Cálculo para Subir
    if nota > alvo_subir:
        n_subir = (total_avaliacoes * (alvo_subir - media_atual)) / (nota - alvo_subir)
        txt_subir = f"{int(n_subir) + 1} notas"
    else:
        txt_subir = "---" # Nota não é alta o suficiente para subir a média

    # Cálculo para Cair
    if nota < alvo_cair:
        n_cair = (total_avaliacoes * (media_atual - alvo_cair)) / (alvo_cair - nota)
        txt_cair = f"{int(n_cair) + 1} notas"
    else:
        txt_cair = "---" # Nota não é baixa o suficiente para derrubar a média

    print(f"Se receber nota {nota:<7} | {txt_subir:<20} | {txt_cair:<20}")

print("="*60)
print("📌 Obs: '---' significa que essa nota sozinha não tem força para atingir o alvo.")
