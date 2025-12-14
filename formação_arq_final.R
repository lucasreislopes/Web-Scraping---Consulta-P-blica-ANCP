library(tidyverse)

ancp <- read.csv2(file = "ancp4ag.csv", dec = ".")

ancp <- ancp %>% 
  rename("DPG.DEP" = DPG_DEP, "DPG.acc" = DPG_acc, "DPG.percentil" = DPG_percentil)

# identifica colunas com G antes do _
cols_G <- grep("G_.*", names(ancp), value = TRUE)

ancp <- ancp %>%
  mutate(genotipados = if_else(
    rowSums(!is.na(select(., all_of(cols_G)))) > 0,
    "G",
    "N"
  ))

####
# remove o G do nome das colunas
cols_G <- grep("G_.*", names(ancp), value = TRUE)
cols_G_novo <- str_replace(cols_G, "G_", "_")

# percorre cada par coluna G -> coluna final
for(i in seq_along(cols_G)){
  col_G <- cols_G[i]
  col_novo <- cols_G_novo[i]
  
  # se a coluna final não existir, cria com valor da coluna G
  if(!col_novo %in% names(ancp)){
    ancp <- ancp %>%
      rename("{col_novo}" := all_of(col_G))
  } else {
    # combina valores: pega o valor da coluna G se não for NA, senão mantém o antigo
    ancp <- ancp %>%
      mutate("{col_novo}" := coalesce(.data[[col_G]], .data[[col_novo]]))
  }
}

# opcional: remove as colunas originais com G
ancp <- ancp %>% select(-any_of(cols_G))


####  fenotipo integrado
cols_G <- grep("G._.*", names(ancp), value = TRUE)
cols_G_novo <- str_replace(cols_G, "G._", "_")

ancp <- ancp %>%
  mutate(asterisco = if_else(
    rowSums(!is.na(select(., all_of(cols_G)))) > 0,
    "tem_asterisco",
    "N"
  ))


# percorre cada par coluna G -> coluna final
for(i in seq_along(cols_G)){
  col_G <- cols_G[i]
  col_novo <- cols_G_novo[i]
  
  # se a coluna final não existir, cria com valor da coluna G
  if(!col_novo %in% names(ancp)){
    ancp <- ancp %>%
      rename("{col_novo}" := all_of(col_G))
  } else {
    # combina valores: pega o valor da coluna G se não for NA, senão mantém o antigo
    ancp <- ancp %>%
      mutate("{col_novo}" := coalesce(.data[[col_G]], .data[[col_novo]]))
  }
}

#### fenotipo integrado
# Seleciona colunas que têm "._" mas que não têm G imediatamente antes
cols_G <- names(ancp)[
  str_detect(names(ancp), "(?<!G)\\._")
]

# Testa selecionando essas colunas
cols_G_novo <- str_replace(cols_G, "._", "_")

ancp <- ancp %>%
  mutate(asterisco1 = if_else(
    rowSums(!is.na(select(., all_of(cols_G)))) > 0,
    "tem_asterisco",
    "N"
  ))

ancp <- ancp %>% 
  mutate(Consaguinidade = str_replace(Consaguinidade, "%", "")) %>% 
  mutate(Consaguinidade = as.numeric(Consaguinidade))

ancp$asterisco[ancp$asterisco == "N" & ancp$asterisco1 == "tem_asterisco"] <- "tem_asterisco"
ancp$DPG_DEP[is.na(ancp$DPG_DEP) & !is.na(ancp$DPG.DEP)] <- ancp$DPG.DEP[is.na(ancp$DPG_DEP) & !is.na(ancp$DPG.DEP)]
ancp$DPG_acc[is.na(ancp$DPG_acc) & !is.na(ancp$DPG.acc)] <- ancp$DPG.acc[is.na(ancp$DPG_acc) & !is.na(ancp$DPG.acc)]
ancp$DPG_percentil[is.na(ancp$DPG_percentil) & !is.na(ancp$DPG.percentil)] <-  ancp$DPG.percentil[is.na(ancp$DPG_percentil) & !is.na(ancp$DPG.percentil)]
ancp <- ancp %>% select(-c(DPG.DEP, DPG.acc, DPG.percentil))
                                                         
# percorre cada par coluna G -> coluna final
for(i in seq_along(cols_G)){
  col_G <- cols_G[i]
  col_novo <- cols_G_novo[i]
  
  # se a coluna final não existir, cria com valor da coluna G
  if(!col_novo %in% names(ancp)){
    ancp <- ancp %>%
      rename("{col_novo}" := all_of(col_G))
  } else {
    # combina valores: pega o valor da coluna G se não for NA, senão mantém o antigo
    ancp <- ancp %>%
      mutate("{col_novo}" := coalesce(.data[[col_G]], .data[[col_novo]]))
  }
}

# opcional: remove as colunas originais com G
# ancp <- ancp %>% select(-any_of(cols_G))

ancp <- ancp %>% select(-c(pagina, nome, asterisco1))

ancp <- ancp %>% select(Nome_animal, Proprietario, Criador, Série, RGN, RGD, codigo_unido, 
                        Raca, Categoria, Variedade, Central, Reprodução.Programada, 
                        Consaguinidade, Sexo, Situação, Data_Nasc, MGTe, TOP, genotipados, 
                        asterisco, D3P_DEP, D3P_acc, D3P_percentil, DIPP_DEP, DIPP_acc, 
                        DIPP_percentil, DPE365_DEP, DPE365_acc, DPE365_percentil, DPE450_DEP, 
                        DPE450_acc, DPE450_percentil, DIPM_DEP, DIPM_acc, DIPM_percentil, DPG_DEP, 
                        DPG_acc, DPG_percentil, DPN_DEP, DPN_acc, DPN_percentil, MFPP_DEP, 
                        MFPP_acc, MFPP_percentil, DFPP_DEP, DFPP_acc, DFPP_percentil, DSTAY_DEP, 
                        DSTAY_acc, DSTAY_percentil, DSTAY54_DEP, DSTAY54_acc, DSTAY54_percentil, 
                        MP120_DEP, MP120_acc, MP120_percentil, MP210_DEP, MP210_acc, MP210_percentil, 
                        MTP210_DEP, MTP210_acc, MTP210_percentil, DP120_DEP, DP120_acc, DP120_percentil, 
                        DP210_DEP, DP210_acc, DP210_percentil, DP365_DEP, DP365_acc, DP365_percentil, 
                        DP450_DEP, DP450_acc, DP450_percentil, DPAV_DEP, DPAV_acc, DPAV_percentil, 
                        DPAC_DEP, DPAC_acc, DPAC_percentil, DCAR_DEP, DCAR_acc, DCAR_percentil, 
                        DIMS_DEP, DIMS_acc, DIMS_percentil, DGPR_DEP, DGPR_acc, DGPR_percentil,
                        DAOL_DEP, DAOL_acc, DAOL_percentil, DACAB_DEP, DACAB_acc, DACAB_percentil, 
                        DMAR_DEP, DMAR_acc, DMAR_percentil, DMAC_DEP, DMAC_acc, DMAC_percentil, 
                        DES_DEP, DES_acc, DES_percentil, DPS_DEP, DPS_acc, DPS_percentil, DMS_DEP, 
                        DMS_acc, DMS_percentil, DFRAME_DEP, DFRAME_acc, DFRAME_percentil, 
                        DMOCHO_DEP, DMOCHO_acc, DMOCHO_percentil, DLAC_DEP, DLAC_acc, 
                        DLAC_percentil, DLPA_DEP, DLPA_acc, DLPA_percentil, MGTE_CR_DEP, 
                        MGTE_CR_acc, MGTE_CR_percentil, MGTE_RE_DEP, MGTE_RE_acc, MGTE_RE_percentil, 
                        MGTE_CO_DEP, MGTE_CO_acc, MGTE_CO_percentil, MGTE_F1_DEP, MGTE_F1_acc, 
                        MGTE_F1_percentil, NF3P, NFSTAY, NN120, NRN120, NF120, NR120, NF210, 
                        NR210, NF450, NR450, NFUS, NRUS, NFSAMS, codigo_animal, codigo_unido_animal, 
                        nome_animal, MGTe_animal, TOP_animal, sexo_animal, codigo_pai, codigo_unido_pai, 
                        nome_pai, MGTe_pai, TOP_pai, sexo_pai, codigo_pai_do_pai, codigo_unido_pai_do_pai, 
                        nome_pai_do_pai, MGTe_pai_do_pai, TOP_pai_do_pai, sexo_pai_do_pai, codigo_mae_do_pai, 
                        codigo_unido_mae_do_pai, nome_mae_do_pai, MGTe_mae_do_pai, TOP_mae_do_pai, 
                        sexo_mae_do_pai, codigo_mae, codigo_unido_mae, nome_mae, MGTe_mae, TOP_mae, 
                        sexo_mae, codigo_pai_da_mae, codigo_unido_pai_da_mae, nome_pai_da_mae, 
                        MGTe_pai_da_mae, TOP_pai_da_mae, sexo_pai_da_mae, codigo_mae_da_mae, 
                        codigo_unido_mae_da_mae, nome_mae_da_mae, MGTe_mae_da_mae, TOP_mae_da_mae, 
                        sexo_mae_da_mae, DIPMG._DEP, DAOLG._DEP, DACABG._DEP, DMARG._DEP, DCARG._DEP, 
                        DIMSG._DEP, DIPM._DEP, DAOL._DEP, DACAB._DEP, DMAR._DEP, DCAR._DEP, DIMS._DEP)

#### separar MGTe
ancp <- ancp %>%
  separate(MGTe, into = c("MGTe_DEP", "MGTe_acc"), sep = " @", convert = TRUE) %>% 
  mutate(TOP = str_replace_all(TOP, "[^0-9\\.]", ""),
         TOP = as.numeric(TOP)
         ) %>% 
  rename("MGTe_percentil" = TOP)

openxlsx::write.xlsx(ancp, "ancp_4AG.xlsx")





