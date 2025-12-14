# Web-Scraping---Consulta-P-blica-ANCP
Uso de Web Scraping para a coleta de dados dos animais presentes na consulta pública da ANCP.

Série de arquivos necessários para a coleta dos das informações no site da consulta pública da ANCP. Recomendado seguir os 5 passos abaixo para que dê tudo certo. # Erros vão acontecer e acontecem...

. O arquivo "funcao_coleta_animais.py é requerido para realizar a coleta das informações dos animais quando o webdriver acessa as informações do animal na terceira aba da consulta pública

1. O arquivo "script_web_scraping.py" coleta os dados no site da consulta pública da ANCP e gera um arquivo .csv com os dados coletados. #### execução demorada sujeito a erros, sendo necessário alterar a página em que o script irá reinicar cada vez que ocorrer um erro ou ser fechado inesperadamente ####
2. O arquivo "coleta_total_nomes.py" coleta todos os nomes presentes no site da consulta pública. Arquivo necessário para realizar a consistência do arquivo gerado pelo web_scraping.
3. O scritp "Consistência_dos_dados.R" é necessário para verificar quantos animais do arquivo gerado "coleta_total_nomes.py" está faltando no arquivo .csv gerado pelo "script_web_scraping.py"
4. O "arquivo funcao_coleta_animais.py" deve ser executado para coletar os animais que ainda não foram coletados. E em seguida deve ser executado novamente o script "Consistência_dos_dados.R" para corrigir por completo o arquivo de .csv.
5. E por fim, o arquivo "formação_arq_final.R" arruma o ancp4ag.csv e gera um arquivo .xlsx final pronto para uso. 
