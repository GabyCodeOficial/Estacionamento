import sqlite3
import datetime
import re








class Estacionamento:
  def __init__(self):
      """Inicializa conexão com o banco de dados e cria tabelas."""
      self.conn = sqlite3.connect("estacionamento.db")
      self.cursor = self.conn.cursor()
      self.criar_tabelas()




  def criar_tabelas(self):
      """Cria as tabelas no banco de dados."""
      self.cursor.execute("""
          CREATE TABLE IF NOT EXISTS clientes_mensalistas (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              nome TEXT,
              placa TEXT UNIQUE,
              modelo TEXT,
              cor TEXT,
              mensalidade REAL DEFAULT 300.00
          )
      """)




      self.cursor.execute("""
          CREATE TABLE IF NOT EXISTS veiculos_estacionados (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              nome TEXT,
              placa TEXT UNIQUE,
              modelo TEXT,
              cor TEXT,
              entrada TEXT
          )
      """)
      self.cursor.execute("""
          CREATE TABLE IF NOT EXISTS registro_historico_saidas (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              nome TEXT,
              placa TEXT,
              modelo TEXT,
              cor TEXT,
              entrada TEXT,
              saida TEXT,
              valor_pago REAL
          )
      """)




      self.conn.commit()




  def validar_placa(self, placa):
      """Valida se a placa segue o formato tradicional ou Mercosul do Brasil."""
      # Regex abrangente para placas brasileiras (tradicional e Mercosul)
      padrao = r'^[A-Z]{3}-?[0-9]{4}$|^[A-Z]{3}[0-9][A-Z][0-9]{2}$'
      return re.match(padrao, placa) is not None




  def validar_nome(self, nome):
      """Verifica se o nome contém mais de uma palavra e se cada palavra começa com maiúscula."""
      palavras = nome.split()
      if len(palavras) < 2:
          return False
      return all(palavra.istitle() and palavra.isalpha() for palavra in palavras)




  def cadastrar_cliente_mensalista(self):
      """Registra um novo cliente mensalista no banco de dados."""
      print("\n✨ **CADASTRO DE MENSALISTA** ✨")
      print("---------------------------------")
      nome = input("👤 Nome completo (ou 'v' para voltar): ")
      if nome.lower() == "v":
          print("↩️ Voltando ao menu.")
          return
      if not self.validar_nome(nome):
          print("🚫 Nome inválido! 💡 Dica: Use nome e sobrenome, com iniciais maiúsculas.")
          return




      placa = input("🚗 Placa do veículo (ou 'v' para voltar): ")
      if placa.lower() == "v":
          print("↩️ Voltando ao menu.")
          return
      if not self.validar_placa(placa):
          print("❌ Placa incorreta! 💡 Dica: Formato ABC1234 ou ABC1D23.")
          return




      modelo = input("🚘 Modelo do veículo (ou 'v' para voltar): ")
      if modelo.lower() == "v":
          print("↩️ Voltando ao menu.")
          return
      cor = input("🌈 Cor do veículo (ou 'v' para voltar): ")
      if cor.lower() == "v":
          print("↩️ Voltando ao menu.")
          return




      try:
          self.cursor.execute("INSERT INTO clientes_mensalistas (nome, placa, modelo, cor) VALUES (?, ?, ?, ?)",
                              (nome, placa, modelo, cor))
          self.conn.commit()
          print(f"✅ Cliente **{nome}** cadastrado como mensalista! Bem-vindo(a)! 🎉")
      except sqlite3.IntegrityError:
          print("⚠️ Essa placa já está cadastrada para um mensalista!")




  def registrar_entrada(self):
      """Registra a entrada de um veículo no estacionamento."""
      print("\n➡️ **REGISTRO DE ENTRADA** ➡️")
      print("-----------------------------")
      nome = input("👤 Nome completo (ou 'v' para voltar): ")
      if nome.lower() == "v":
          print("↩️ Voltando ao menu.")
          return
      if not self.validar_nome(nome):
          print("🚫 Nome inválido! 💡 Dica: Use nome e sobrenome, com iniciais maiúsculas.")
          return




      placa = input("🚗 Placa do veículo (ou 'v' para voltar): ")
      if placa.lower() == "v":
          print("↩️ Voltando ao menu.")
          return
      if not self.validar_placa(placa):
          print("❌ Placa incorreta! 💡 Dica: Formato ABC1234 ou ABC1D23.")
          return




      modelo = input("🚘 Modelo do veículo (ou 'v' para voltar): ")
      if modelo.lower() == "v":
          print("↩️ Voltando ao menu.")
          return
      cor = input("🌈 Cor do veículo (ou 'v' para voltar): ")
      if cor.lower() == "v":
          print("↩️ Voltando ao menu.")
          return
      entrada = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")




      self.cursor.execute("SELECT * FROM clientes_mensalistas WHERE placa=?", (placa,))
      cliente_mensalista = self.cursor.fetchone()




      try:
          self.cursor.execute("INSERT INTO veiculos_estacionados (nome, placa, modelo, cor, entrada) VALUES (?, ?, ?, ?, ?)",
                              (nome, placa, modelo, cor, entrada))
          self.conn.commit()
          if cliente_mensalista:
              print(f"✅ Entrada de **{nome}** (placa: {placa}) registrada. Cliente mensalista! 🅿️")
          else:
              print(f"✅ Entrada de **{nome}** (placa: {placa}) registrada. Cliente avulso. ⏱️")
      except sqlite3.IntegrityError:
          print("🚨 Opa! Este veículo já está estacionado no momento.")




  def registrar_saida(self):
      """Registra a saída de um veículo, movendo-o para o histórico e calculando valores se necessário."""
      while True: # Loop para permitir que o usuário tente novamente
          print("\n⬅️ **REGISTRO DE SAÍDA** ⬅️")
          print("----------------------------")
          placa = input("🚗 Placa do veículo (ou 'v' para voltar): ")
          if placa.lower() == "v":
              print("↩️ Voltando ao menu.")
              return




          self.cursor.execute("SELECT * FROM veiculos_estacionados WHERE placa=?", (placa,))
          dados_veiculo = self.cursor.fetchone()




          if not dados_veiculo:
              print("🤷‍♂️ Este veículo não está registrado como estacionado aqui agora.")
              continue # Volta para o início do loop para tentar outra placa




          # Exibir informações do veículo para confirmação
          print("\n--- **DETALHES DO VEÍCULO PARA SAÍDA** ---")
          print(f"Nome: {dados_veiculo[1]}")
          print(f"Placa: {dados_veiculo[2]}")
          print(f"Modelo: {dados_veiculo[3]}")
          print(f"Cor: {dados_veiculo[4]}")
          print(f"Entrada: {dados_veiculo[5]}")




          confirmacao = input("Confirmar saída deste veículo? (s/n): ").lower()




          if confirmacao == 's':
              saida = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
              valor_total = 0.0




              self.cursor.execute("SELECT * FROM clientes_mensalistas WHERE placa=?", (placa,))
              cliente_mensalista = self.cursor.fetchone()




              if cliente_mensalista:
                  print("🥳 Cliente **mensalista**! Nenhuma cobrança. Dirija com segurança! 👋")
                  valor_total = 0.0
              else:
                  entrada_str = dados_veiculo[5]
                  entrada = datetime.datetime.strptime(entrada_str, "%Y-%m-%d %H:%M:%S")
                  tempo_estacionado = (datetime.datetime.now() - entrada).total_seconds() / 3600
                  preco_por_hora = 10
                  valor_total = round(tempo_estacionado * preco_por_hora, 2)
                  print(f"💸 Cliente **avulso**! Tempo: {tempo_estacionado:.2f}h. Valor a pagar: **R${valor_total:.2f}**")




              try:
                  self.cursor.execute("INSERT INTO registro_historico_saidas (nome, placa, modelo, cor, entrada, saida, valor_pago) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                      (dados_veiculo[1], dados_veiculo[2], dados_veiculo[3], dados_veiculo[4], dados_veiculo[5], saida, valor_total))
                  self.conn.commit()
                  print("📋 Saída registrada no histórico. Obrigado(a)! ✨")
              except sqlite3.IntegrityError as e:
                  print(f"🚨 Erro ao registrar saída no histórico: {e}")




              self.cursor.execute("DELETE FROM veiculos_estacionados WHERE placa=?", (placa,))
              self.conn.commit()
              print(f"✅ Veículo **{placa}** saiu! Vaga liberada. 🚀")
              break # Sai do loop após a saída ser confirmada e processada
          elif confirmacao == 'n':
              print("❌ Saída não confirmada. Por favor, tente novamente com os dados corretos.")
              # O loop 'while True' fará com que o programa solicite a placa novamente
          else:
              print("Opção inválida. Digite 's' para sim ou 'n' para não.")
              # O loop 'while True' fará com que o programa solicite a placa novamente




  def contar_veiculos_estacionados(self):
      """Conta quantos veículos ainda estão estacionados."""
      self.cursor.execute("SELECT COUNT(*) FROM veiculos_estacionados")
      total = self.cursor.fetchone()[0]
      print(f"\n🅿️ **VAGAS OCUPADAS**: {total} veículos. 🚗💨")




# --- Rodando o Sistema ---
if __name__ == "__main__":
  estacionamento = Estacionamento()
  while True:
      print("\n" + "="*30)
      print("🌟 ESTACIONAMENTO DE VEICULOS 🌟")
      print("="*30)
      print("1️⃣ Cadastrar Cliente Mensalista")
      print("2️⃣ Registrar Entrada de Veículo")
      print("3️⃣ Registrar Saída de Veículo")
      print("4️⃣ Ver Vagas Ocupadas")
      print("5️⃣ Sair do Sistema")
      print("="*30)




      opcao = input("👉 Escolha sua opção (1-5): ")




      if opcao == "1":
          estacionamento.cadastrar_cliente_mensalista()
      elif opcao == "2":
          estacionamento.registrar_entrada()
      elif opcao == "3":
          estacionamento.registrar_saida()
      elif opcao == "4":
          estacionamento.contar_veiculos_estacionados()
      elif opcao == "5":
          print("\n👋 **SAINDO DO SISTEMA...** 👋")
          print("🚗💨 Agradecemos a preferência! Volte sempre!")
          break
      else:
          print("🤔 Opção inválida! Por favor, digite um número de 1 a 5.")

