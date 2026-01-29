import pandas as pd
import matplotlib.pyplot as plt
import webbrowser
import urllib.parse
import os


try:
    # Leitura do CSV, o arquivo com os dados.
    df = pd.read_csv('audiencia.csv')
    print(f"📊 Sucesso! {len(df)} jogos carregados.")
except Exception as e:
    print(f"❌ Erro ao ler o arquivo: {e}")
    exit()

# Transformação
df['data'] = pd.to_datetime(df['data'])
audiencia_por_plataforma = df.groupby('plataforma')['audiencia_pico'].sum().sort_values(ascending=False).reset_index()
jogo_maior_audiencia = df.loc[df['audiencia_pico'].idxmax()]

# Visualização (Gráfico)
plt.figure(figsize=(10, 6))
plt.bar(audiencia_por_plataforma['plataforma'], audiencia_por_plataforma['audiencia_pico'], color=['skyblue', 'lightcoral'])
plt.title('Audiência Total de Pico por Plataforma (Atualizado)')
plt.ylabel('Audiência (Milhões)')

# Formatação para milhões (M)
def format_func(value, tick_number):
    return f"{value / 1000000:.1f}M"
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_func))

plt.savefig('audiencia_por_plataforma.png')
print("✅ Gráfico 'audiencia_por_plataforma.png' atualizado!")

# Carga (Gerando o Excel)
try:
    with pd.ExcelWriter('resumo_audiencia_livemode.xlsx') as writer:
        df.to_excel(writer, sheet_name='Dados Brutos', index=False)
        audiencia_por_plataforma.to_excel(writer, sheet_name='Resumo', index=False)
    print("✅ Excel 'resumo_audiencia_livemode.xlsx' gerado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao gerar Excel: {e}. Tente instalar: pip install openpyxl")

# automação e rascunho do e-mail para o time
print("\n🚀 Preparando e-mail para o time...")
corpo_email = f"Olá time LiveMode,\n\nO relatório de audiência foi atualizado.\nO destaque foi {jogo_maior_audiencia['jogo']} com {jogo_maior_audiencia['audiencia_pico']:,} de pico.\n\nOs arquivos estão prontos para envio!"
assunto = "RELATÓRIO SEMANAL: Insights de Audiência"
url = f"https://mail.google.com/mail/?view=cm&fs=1&to=projetos@livemode.com&su={urllib.parse.quote(assunto)}&body={urllib.parse.quote(corpo_email)}"


webbrowser.open(url)
