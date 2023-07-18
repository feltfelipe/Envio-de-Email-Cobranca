def enviar_email():
    '''
    Função para envio de email que está sendo utilizada no prgrama principal
    na última linha de código
    '''
    import smtplib  # para cobrir a parte de autenticação
    import email.message  # para o preenchimento do email
    #Mensagem do email com os dados extraídos da tabela
    #O texto está no formato HTML
    corpo_email = f"""
    <p>Prezado cliente,</p>
    <p>Verificamos um atraso no pagamento referente a NF {nf} com vencimento em {prazo} e valor total de R$ {valor:,.2f}</p>
    <p>Gostaríamos de verficar se há algum problema que necessite de auxílio da nossa equipe.</p>
    <p>Em caso de dúvidas, entre em contato com nosso time através do e-mail melhormaneira@gmail.com</p>
    <p>Em caso de já ter sido realizado o pagamento, pedimos que desconsidere o e-mail.</p>
    <p>Att,</p>
    <p>FelDEV Soluções</p>
    """
    #preenchimento dos campos do email da biblioteca email.message
    msg = email.message.Message()
    msg['Subject'] = "Email de Cobrança"
    msg['From'] = 'melhormaneira@gmail.com'
    msg['To'] = destinatario
    password = 'tkcnxfotwmzspndg'    #senha gerada apenas para uso do gmail no campo de 'senha de apps' do gmail
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    #
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login com as credenciais e envio do email. Imprime 'email enviado' no caso de sucesso.
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')

import pandas as pd #para leitura do banco de dados (nesse caso, uma planilha excel fornecida pela empresa)
import datetime as dt #para tratarmos os dados usando as datas como escopo pra tomada de decisão

atual = dt.datetime.now() #buscando e definindo a data atual

tabela = pd.read_excel('Contas a Receber.xlsx') #Realizei os processos de ETL(extração, tranformação e carregamento) que não estão no corpo do programa.
#Para análise primeiro imprimi a tabela e depois usei a funçao '.info()' da biblioteca do pandas,
#realizei os tratamentos necessários restou apenas produzir valor com as informações, conforme a finalidade do projeto.


#Criando uma lista apenas com os valores 'em aberto'.
#Logo depois tratando a lista para os clientes que já tiverem seu prazo de pagamento expirado.
tabela_devedores = tabela.loc[tabela['Status'] == 'Em aberto']
tabela_devedores = tabela_devedores.loc[tabela_devedores['Data Prevista para pagamento'] < atual]

#criando uma lista para cada cliente devedor
dados = tabela_devedores[['Valor em aberto', 'Data Prevista para pagamento', 'E-mail', 'NF']].values.tolist()


#um laço para lista que criei acima afim de extrair os dados para usar na minha função de envio de email
for dado in dados:
    destinatario = dado[2]
    nf = dado[3]
    prazo = dado[1]
    prazo = prazo.strftime('%d/%m/%Y') #função de tratamento da data para o formato convecional de dia/mês/ano (como está no DB)
    valor = dado[0]
enviar_email() #função e envio de email com as bibliotecas responsáveis dentro dela
