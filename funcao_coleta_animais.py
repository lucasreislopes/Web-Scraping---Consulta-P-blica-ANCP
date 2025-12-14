def coletar_informacoes(html):
    
    import re
    def limpar_texto(texto):
        """Remove quebras de linha, múltiplos espaços e formata o texto."""
        texto = texto.replace("\n", " ")
        texto = texto.replace("\t", " ")
        texto = re.sub(r"\s+", " ", texto)
        return texto.strip()
    
    dados = {}

    # --- COLETAR NOME DO ANIMAL ---
    nome_tag = html.find("td", {"class": "ficha_texto_campo", "width": "39%"})
    if nome_tag:
        dados["Nome_animal"] = limpar_texto(nome_tag.text)
    else:
        dados["Nome_animal"] = None

    # --- COLETAR PROPRIETÁRIO ---
    proprietario_tag = html.find("td", {"class": "ficha_texto_campo", "width": "61%"})
    if proprietario_tag:
        dados["Proprietario"] = limpar_texto(proprietario_tag.text)
    else:
        dados["Proprietario"] = None

    # --- COLETAR Criador ---
    criador_tag = html.find("td", {"class": "ficha_texto_campo", "height": "60%"})
    if criador_tag:
        dados["Criador"] = limpar_texto(criador_tag.text)
    else:
        dados["Criador"] = None

        ### Sequência de Série, RGN, RGD, Categoria, Variedade
    # --- COLETAR BLOCO USANDO SEQUÊNCIA DE WIDTHS ---
    widths_alvo = ["62", "115", "133", "124", "124", "129"]

    # procura todos os <tr> e tenta localizar aquele que contém exatamente esses width
    for tr in html.find_all("tr"):
        tds = tr.find_all("td", class_="ficha_texto_campo")

        # extrair os widths de cada <td>
        widths_encontrados = [td.get("width", "").strip() for td in tds]

        # verificar se bate exatamente com a sequência desejada
        if widths_encontrados == widths_alvo:
            valores = [limpar_texto(td.text) for td in tds]

            dados["Série"]    = valores[0]  # ex: JHVM
            dados["RGN"] = valores[1]  # ex: 27676
            dados["RGD"]   = valores[2]  # vazio mesmo
            dados["codigo_unido"] = "".join(valores[0:3]).replace(" ", "")
            dados["Raca"]     = valores[3]  # Nelore
            dados["Categoria"]    = valores[4]  # PO
            dados["Variedade"]     = valores[5]  # Padrão
            break  # bloco localizado → encerra

    # --- COLETAR BLOCO DE TRÊS COLUNAS (MESMO COM VALORES VAZIOS) ---
    for tr in html.find_all("tr"):
        tds = tr.find_all("td", class_="ficha_texto_campo")

        # o bloco alvo possui exatamente 3 <td>
        if len(tds) == 3:
            valores = [limpar_texto(td.text) for td in tds]

            # transformar valores vazios ou "&nbsp;" em ""
            valores = [v if v not in ["", "&nbsp;"] else "" for v in valores]

            # valida que o 3º item é o percentual (critério de identificação)
            if "%" in valores[2]:
                dados["Central"] = valores[0]
                dados["Reprodução Programada"] = valores[1]
                dados["Consaguinidade"] = valores[2]
                break

    # --- COLETAR BLOCO DE CINCO COLUNAS ---
    for tr in html.find_all("tr", class_="textinho"):
        tds1 = tr.find_all("td", class_="ficha_texto_campo")
        tds2 = tr.find_all("td", class_="mgt_texto")

        # o bloco alvo possui exatamente 3 <td>
        if len(tds1) == 3:
            valores = [limpar_texto(td.text) for td in tds1]

            # valida que o 3º item é o percentual (critério de identificação)
            dados["Sexo"] = valores[0]
            dados["Situação"] = valores[1]
            dados["Data_Nasc"] = valores[2]
            
            if len(tds2) == 2:
                valores = [limpar_texto(td.text) for td in tds2]
                dados["MGTe"] = valores[0]
                dados["TOP"] = valores[1]
                break

    #### --- COLETA DEPS ---        
        
        # --- COLETA DO BLOCO ---
    lista_ids = [
        "d3p_f","dipp_f","dpe365_f","dpe450_f","dipm_f","dpg_f","dpn_f","mfpp_f","dfpp_f",
        "dstay_f","dstay54_f","mp120_f","mp210_f","mtp210_f","dp120_f","dp210_f","dp365_f",
        "dp450_f","dpav_f","dpac_f","dcar_f","dims_f","dgpr_f","daol_f","dacab_f","dmar_f",
        "dmac_f","des_f","dps_f","dms_f","dframe_f","dmocho_f","dlac_f","dlpa_f",
        "mgte_cr_f","mgte_re_f","mgte_co_f","mgte_f1_f"
    ]

    for bloco_id in lista_ids:
  
        bloco = html.find("td", id=bloco_id, align="center")

        if bloco:
            tabela = bloco.find("table")
            # prefixo = 

            if tabela:
                linhas = tabela.find_all("tr")

                # Garantir que tem as 4 linhas esperadas
                if len(linhas) >= 4:

                    # 1) Cabeçalho: D3PG
                    cabecalho = linhas[0].find("td").get_text(strip=True)
                    prefixo = cabecalho.upper()

                    # 2) Valor numérico: 87.57
                    valor = linhas[1].find("td").get_text(strip=True).replace("\xa0", "")

                    # 3) Precisão @50
                    precisao = linhas[2].find("td").get_text(" ", strip=True).replace("@\xa0", "")

                    # 4) Confiabilidade ®4%
                    confiabilidade = linhas[3].find("td").get_text(" ", strip=True).replace("®\xa0", "").replace("%", "")

                    dados[f"{prefixo}_DEP"] = valor
                    dados[f"{prefixo}_acc"] = precisao
                    dados[f"{prefixo}_percentil"] = confiabilidade
        
        
        # --- COLETA DO BLOCO ---
    lista_ids_f = [
        "nf3p_f", "nfstay_f", "nn120_f", "nrn120_f", "nf120_f", "nr120_f", "nf210_f", "nr210_f", "nf450_f", 
        "nr450_f", "nfus_f", "nrus_f", "nfsams_f"
    ]

    for bloco_id in lista_ids_f:
  
        bloco = html.find("td", id=bloco_id, align="center")

        if bloco:
            tabela = bloco.find("table")
            # prefixo = 

            if tabela:
                linhas = tabela.find_all("tr")

                # Garantir que tem as 4 linhas esperadas
                if len(linhas) >= 1:

                    linha = linhas[0]
                    fontes = linha.find_all("font")

                    if len(fontes) >= 2:
                        prefixo = fontes[0].get_text(strip=True).replace(":", "")
                        valor = fontes[1].get_text(strip=True)

                    dados[f"{prefixo}"] = valor

        # --- COLETA DO BLOCO ---
    # bloco = html.find("table", width="650", border="0", align="center")
    # 1. selecionar bloco principal
    ordem = [
        "animal", "pai", "pai_do_pai", "mae_do_pai", "mae",
        "pai_da_mae", "mae_da_mae"
    ]

    sexo_fixos = {
    "animal": "MACHO",
    "pai": "MACHO",
    "pai_do_pai": "MACHO",
    "mae_do_pai": "FEMEA",
    "mae": "FEMEA",
    "pai_da_mae": "MACHO",
    "mae_da_mae": "FEMEA"
}

    bloco = html.find("table", width="650", border="0", align="center")
    if bloco:
        tds = bloco.find_all("td", height="60")[:7]

        for idx,td in enumerate(tds):
            campo = td.find("td", class_=re.compile(r"genealogia_texto_campo"))
            if not campo:
                continue

            partes = list(campo.stripped_strings)
            prefixo = ordem[idx]

            while len(partes) < 6:
                partes.append("")

            texto_interno = limpar_texto(campo.get_text(separator=" "))

            # Regex para MGTe: aceita "MGTe = -2.29", "MGTe -2.29", "MGTe=-2.29", etc.
            m_mgte = re.search(r"MGTe\s*=?\s*([+-]?\d+(?:\.\d+)?)", texto_interno, flags=re.IGNORECASE)

            # Regex para TOP: aceita "TOP 58", "TOP 58 %", "TOP58", etc.
            m_top = re.search(r"TOP\s*[:=]?\s*([0-9]+(?:[.,][0-9]+)?)\s*%?", texto_interno, flags=re.IGNORECASE)

            # Usar sexo fixo baseado no bloco
            sexo = sexo_fixos[prefixo]

            dados[f"codigo_{prefixo}"] = partes[0]
            dados[f"codigo_unido_{prefixo}"] = partes[0].replace(" ", "").replace("/", "").replace("-","")
            dados[f"nome_{prefixo}"] = partes[1]

            dados[f"MGTe_{prefixo}"] = m_mgte.group(1) if m_mgte else ""
            dados[f"TOP_{prefixo}"]  = m_top.group(1) if m_top else ""
            dados[f"sexo_{prefixo}"] = sexo
           
    return dados