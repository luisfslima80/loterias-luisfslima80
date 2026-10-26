# Loteria V3

Aplicativo estático para análise de resultados da Lotofácil, gerador de jogos e conferência. Planejado para outras loterias.

## Publicação no GitHub Pages

1. Crie um repositório **público** chamado `loterias-luisfslima80`.
2. Envie o conteúdo desta pasta **para a raiz** do repositório (inclusive `.github/workflows`).
3. Em **Settings > Pages > Build and deployment**, selecione **Deploy from a branch**, `main`, pasta `/(root)` e salve.
4. Em **Actions > Atualizar resultados da Lotofácil**, clique em **Run workflow** para buscar os primeiros resultados.
5. Acesse `https://luisfslima80.github.io/loterias-luisfslima80/` depois da publicação.

## Observações

- O GitHub Actions busca os dados da Caixa sem instalar Python no seu computador. A Caixa pode bloquear ou alterar o serviço; nesse caso o último arquivo permanece e é possível importar JSON manualmente.
- A rotina agendada pode atrasar; o botão Atualizar carrega o último arquivo publicado, não consulta a Caixa em tempo real.
- Jogos são salvos **somente no navegador** (`localStorage`), não no repositório. Faça backups periódicos. Sites públicos não oferecem login ou proteção de acesso.
- Frequência histórica não altera a probabilidade matemática de uma aposta.
- A conferência por concurso só funciona para resultados disponíveis no arquivo local/importado.
