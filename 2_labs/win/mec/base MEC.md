### **Roteiro Técnico e Conciso para Restaurar o `.BAK`**

---

### **1. Pré-requisitos**
- SQL Server instalado (ex.: `SQL Server Express 2022`).
- SSMS instalado.
- Arquivo `MEC_BK.BAK` disponível.

---

### **2. Preparar o Arquivo**
1. Salve `MEC_BK.BAK` em:
   ```plaintext
   C:\Backup
   ```
2. **Garantir acesso**: Certifique-se de que o serviço SQL Server (`MSSQL$SQLEXPRESS`) tem permissão de leitura na pasta.

---

### **3. Restaurar no SSMS**
1. Abra o **SSMS** e conecte-se a:
   ```plaintext
   Server: localhost\SQLEXPRESS
   Authentication: Windows Authentication
   ```

2. No **Object Explorer**:
   - Clique com o botão direito em **Databases** > **Restore Database...**.
   - Em **Source**, selecione **Device** > `...` > **Add** > Selecione `C:\Backup\MEC_BK.BAK`.

3. Certifique-se de que:
   - **Destination Database**: `GATEC_MEC`.
   - **Backup sets to restore** está marcado.

4. Clique em **OK** para iniciar a restauração.

---

### **4. Validar**
1. Atualize os bancos de dados no Object Explorer.
2. Execute:
   ```sql
   USE GATEC_MEC;
   SELECT TOP 10 * FROM NomeDaTabela;
   ```

---

### **Logs e Diagnóstico**
- Logs de erro:
  ```plaintext
  C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\Log
  ```

--- 

Esse roteiro assume proficiência técnica e omite detalhes básicos. Avise se ajustes forem necessários!