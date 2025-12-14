library(tidyverse)

total <- read.csv2(file = "") # caminho do arquivo gerado pelo script coleta_total_nomes.py
ancp4ag <- read.csv2(file = "") # caminho do arquivo gerado pelo script_web_scraping.py

ancp4ag[ancp4ag == ""] <- NA
total[total == ""] <- NA

# retirar animais sem registro
ancp4ag <-ancp4ag %>% 
  filter(!is.na(Nome_animal) | !is.na(codigo_unido))

# verificar animais duplicados
ancp4ag %>% 
  count(nome_animal, codigo_unido) %>% 
  filter(n > 1)

total %>% 
  count(Série, RGN, RGD) %>% 
  filter(n > 1)

total <- total %>% 
  mutate(codigo_unido = paste0(
    ifelse(!is.na(Série), Série, ""),
    ifelse(!is.na(RGN), RGN, ""),
    ifelse(!is.na(RGD), RGD, "")
  ))
total[total == ""] <- NA
    
total <- total %>% 
  filter(!is.na(Nome_animal) | !is.na(codigo_unido))

# filtrar animais que ainda faltam ser coletados #### retornar aqui para verificar se faltou algo
falta_coletar1 <- total %>%
  filter(!codigo_unido %in% ancp4ag$codigo_unido)

falta_coletar1[is.na(falta_coletar1)] <- ""

write.csv(x = falta_coletar1, file = "coleta_faltando.txt", sep = "", col.names = T, row.names = F, quote = F) # irá gerar o arquivo necesário para executar o script coletar_animais_faltantes_ancp.py
# write.csv2(x = ancp4ag, file = "ancp4ag.csv", col.names = T, row.names = F) # irá gerar o arquivo da ancp corretamente limpo.


# leitura dos dados que faltavam que foram coletados
dados_coletados <- read.csv2(file = "animais_corrigidos.csv")
dados_coletados[] <- lapply(dados_coletados, as.character)

ancp4ag[ancp4ag == ""] <- NA

dados_coletados <- dados_coletados %>% 
  distinct(Nome_animal, .keep_all = TRUE)

dados_ineditos <- dados_coletados %>% 
  filter(Nome_animal %in% total$Nome_animal)

ancp4ag <- full_join(ancp4ag, dados_ineditos)

ancp4ag[ancp4ag == ""] <- NA
ancp4ag <- distinct(ancp4ag)

### execute o código novamente até o write.csv2 para criação do arquivo de dados da ANCP