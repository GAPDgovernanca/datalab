### Lista de Comandos para Trabalhar no Branch `novas-funcionalidades-relatorios`

Esta lista foi revisada para incorporar melhorias de fluxo e boas práticas, assegurando uma integração mais suave com o branch principal e melhor gestão de versões.

1. **Criar e Mudar para o Novo Branch**:
   ```sh
   git checkout -b novas-funcionalidades-relatorios
   ```
   
2. **Confirmar o Branch Atual**:
   ```sh
   git branch
   ```

3. **Fazer Alterações no Código**:
   - Realize as modificações necessárias para as novas funcionalidades de relatórios no projeto.

4. **Adicionar as Alterações ao Controle de Versão**:
   - Adicione apenas os arquivos alterados para manter o histórico de commit claro e limpo.
   ```sh
   git add <caminho/dos/arquivos/modificados>
   ```

5. **Fazer o Commit das Alterações**:
   - Utilize mensagens de commit mais descritivas para garantir rastreabilidade:
   ```sh
   git commit -m "feat: Adiciona relatórios detalhados de análise de dados"
   ```

6. **Rebasing das Alterações no Branch Principal (`main`)**:
   - Antes de integrar suas mudanças, sincronize com o branch principal para evitar conflitos:
   ```sh
   git checkout main
   git pull origin main
   git checkout novas-funcionalidades-relatorios
   git rebase main
   ```

7. **Resolver Conflitos**:
   - Se houver conflitos durante o rebase, resolva-os manualmente e continue:
   ```sh
   git add <arquivos_resolvidos>
   git rebase --continue
   ```

8. **Voltar para o Branch Principal (`main`)**:
   ```sh
   git checkout main
   ```

9. **Mesclar o Novo Branch no Branch `main`**:
   - Utilize `merge --no-ff` para criar um commit de merge e manter o histórico mais claro:
   ```sh
   git merge --no-ff novas-funcionalidades-relatorios
   ```

10. **Enviar as Alterações para o Repositório Remoto**:
    ```sh
    git push origin main
    ```

11. **Criar uma Tag para Marcar uma Versão Estável**:
    - Use uma numeração de versão mais clara e, se necessário, inclua informações adicionais na mensagem:
    ```sh
    git tag -a v1.0.0 -m "Primeira versão estável com novas funcionalidades de relatórios"
    ```

12. **Enviar a Tag para o Repositório Remoto**:
    ```sh
    git push origin v1.0.0
    ```

13. **Deletar o Branch Remoto e Local Após a Mesclagem**:
    - Após a mesclagem, delete o branch para manter o repositório limpo:
    ```sh
    git branch -d novas-funcionalidades-relatorios
    git push origin --delete novas-funcionalidades-relatorios
    ```

### Notas:
- **Rebase vs. Merge**: Utilizar `git rebase` para sincronizar com o branch principal ajuda a manter um histórico de commits mais linear. É preferível ao `merge` neste contexto, principalmente quando trabalhando em branches de funcionalidades.
- **Commit Granular**: Fazer commits granulares e descritivos facilita a revisão de código e a identificação de problemas.