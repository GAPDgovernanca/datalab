def send_email(sender_email, sender_password, recipient_emails, output_folder):
    """
    Envia um e-mail com anexos usando uma conta Gmail.

    Parâmetros:
        sender_email (str): O endereço de e-mail do remetente (deve ser uma conta Gmail).
        sender_password (str): A senha do remetente (ou App Password se a verificação em duas etapas estiver ativada).
        recipient_emails (list): Uma lista de endereços de e-mail dos destinatários.
        output_folder (str): O caminho para a pasta onde os arquivos a serem anexados estão localizados.

    Passos:
        1. Configuração do Servidor SMTP do Gmail.
        2. Criação da Mensagem.
        3. Anexar Arquivos.
        4. Envio do E-mail.
    """
    
    # Configuração do servidor SMTP do Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # Criação da mensagem
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = "Resultados da Análise de Indicadores de Funcionários"
    
    # Corpo do e-mail
    body = "Por favor, encontre anexados os gráficos e o arquivo Excel com os resultados da análise de indicadores de funcionários."
    msg.attach(MIMEText(body, 'plain'))
    
    # Anexar arquivos da pasta de saída
    for filename in os.listdir(output_folder):
        file_path = os.path.join(output_folder, filename)
        attachment = MIMEBase('application', 'octet-stream')
        with open(file_path, 'rb') as file:
            attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(attachment)
    
    # Enviar o e-mail
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    try:
        server.login(sender_email, sender_password)
    except smtplib.SMTPAuthenticationError as e:
        print(f"Erro de autenticação: {e}")
        print("Certifique-se de que você está usando a senha correta (App Password se a verificação em duas etapas estiver ativada).")
        return
    server.sendmail(sender_email, recipient_emails, msg.as_string())
    server.quit()
    print("E-mail enviado com sucesso.")
