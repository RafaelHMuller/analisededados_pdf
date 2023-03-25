#!/usr/bin/env python
# coding: utf-8

# # Análise de Dados PDF:
# 
# ### Separar algumas páginas de um pdf e salvar em um novo pdf -1
# Vamos avaliar o Release de Resultados do 3º e 4º Trimestre de 2020 da Magazine Luiza; queremos conseguir separar apenas o DRE Consolidado e o Balanço do Release de Resultados (Páginas 14 e 16) para enviar para a Diretoria, como fazemos?
# 
# ### Juntar os dois pdfs -2
# Para facilitar a comparação entre os trimestres pela diretoria
# 
# ### Textos dentro do pdf -3
# Como foram as Despesas com Vendas da MGLU (página ?)
# 
# ### Tabela dentro do pdf -4
# Criar tabela para analisar as Despesas Operacionais (tabela na página 5)
# 
# ### Tabela dentro do pdf -5
# Analisar o Capital de Giro (tabela na página 12)

# In[1]:


#importar a base de dados
import PyPDF2 as pyf
from pathlib import Path
import tabula
import pandas as pd

mglu3 = pyf.PdfReader('MGLU_ER_3T20_POR.pdf')
mglu4 = pyf.PdfReader('MGLU_ER_4T20_POR.pdf')


# In[2]:


#1 - separar páginas 14 e 16 (mglu3)
i=1
for pagina in mglu3.pages:
    mglu3_pagina = pyf.PdfWriter()     
    mglu3_pagina.add_page(pagina)
    with Path(f'pasta mglu3/Pdf da Página {i}.pdf').open(mode='wb') as mglu3_final:    
        mglu3_pagina.write(mglu3_final)
        i+=1

#2 - salvar as páginas em 1 pdf
mglu3_14 = pyf.PdfReader('pasta mglu3/Pdf da Página 14.pdf')
mglu3_16 = pyf.PdfReader('pasta mglu3/Pdf da Página 16.pdf')
mglu3_1416 = pyf.PdfMerger()
mglu3_1416.append(mglu3_14)
mglu3_1416.append(mglu3_16)
with Path(f'pasta mglu3/Pdf das Páginas 14 e 16.pdf').open(mode='wb') as mglu3_1416final:    
    mglu3_1416.write(mglu3_1416final)


# In[3]:


#3 - separar o texto referente às despesas de vendas (mglu3)

for pagina in mglu3.pages:
    texto = pagina.extract_text()
    if '| Despesas com Vendas' in texto:
        textodesejado = texto


posicaoinicial = textodesejado.index('| Despesas com Vendas') 
posicaofinal = textodesejado.index('| Despesas Gerais e Administrativas')
despesas_de_vendas_mglu3 = textodesejado[posicaoinicial:posicaofinal]
print(despesas_de_vendas_mglu3)

#3 - separar o texto referente às despesas de vendas (mglu4)
i=1
for pagina in mglu4.pages:
    texto = pagina.extract_text()
    if '| Despesas com Vendas' in texto:
        textodesejado = texto
    i+=1

posicaoinicial = textodesejado.index('| Despesas com Vendas') 
posicaofinal = textodesejado.index('| Despesas Gerais e Administrativas')
despesas_de_vendas_mglu4 = textodesejado[posicaoinicial:posicaofinal]
print(despesas_de_vendas_mglu4)


# In[4]:


#4 - analisar tabela de despesas operacionais (página 5)
#importar o df
df1 = tabula.read_pdf('MGLU_ER_3T20_POR.pdf', pages=5)
df1 = df1[0]

#tratamento do df
df1 = df1.dropna(axis=1, how='all')
df1 = df1.dropna(axis=0, how='all')
df1.columns = df1.loc[0, :]
df1 = df1.drop(0, axis=0)
df1 = df1.set_index('R$ milhões (exceto quando indicado)')
display(df1)


# In[5]:


#5 - analisar a tabela do capital de giro (pagina 12)
df2 = tabula.read_pdf('MGLU_ER_3T20_POR.pdf', pages=12)
tabela1 = df2[0]
tabela2 = df2[1]

#tratamentos dos dfs
tabela1 = tabela1.dropna(axis=0, how='all')
tabela2 = tabela2.dropna(axis=0, how='all')

lista=['R$ milhões', 'Dif 12UM', 'set-20', 'jun-20', 'mar-20', 'dez-19', 'set-19']
i=0
for col in tabela1.columns:
    tabela1 = tabela1.rename(columns = {col: lista[i]})
    i+=1
    
tabela1['Dif 12UM'] = tabela1['Dif 12UM'].str.replace('(', '').str.replace(')', '')
tabela1.loc[16,:] = tabela1.loc[16,:].str.replace('(', '').str.replace(')', '')

display(tabela1)
tabela1.info()
display(tabela2)
tabela2.info()


# In[6]:


tabela2 = tabela2.set_index('R$ milhões')

for col in tabela2.columns:
    tabela2[col] = tabela2[col].str.replace(',', '.')
    tabela2[col] = pd.to_numeric(tabela2[col], errors = 'coerce')
    
display(tabela2)
tabela2.info()


# In[ ]:




