"""
Editores de dados seguros com chaves estáveis.
Resolve o problema de perda de foco causado por chaves dinâmicas no st.data_editor.
"""

import streamlit as st
import pandas as pd


def safe_data_editor(data_list, columns, key_prefix, column_configs=None, height=None):
    """
    Editor de dados com chave estável e persistência automática.

    Args:
        data_list: lista de dicts com os dados atuais
        columns: lista de nomes de colunas
        key_prefix: string fixa e única para esta tabela (ex: "depto_financeiro_objetivos")
        column_configs: dict com st.column_config.* para cada coluna
        height: altura do editor (opcional)

    Returns:
        Lista de dicts com os dados editados (linhas vazias removidas)
    """
    if data_list:
        df = pd.DataFrame(data_list)
        for col in columns:
            if col not in df.columns:
                df[col] = ""
        df = df[columns]
    else:
        df = pd.DataFrame(columns=columns)

    # CHAVE ESTÁVEL — nunca muda durante a sessão
    editor_key = f"safe_editor_{key_prefix}"

    kwargs = {
        "num_rows": "dynamic",
        "use_container_width": True,
        "hide_index": True,
        "key": editor_key,
    }
    if column_configs:
        kwargs["column_config"] = column_configs
    if height:
        kwargs["height"] = height

    edited = st.data_editor(df, **kwargs)

    # Converte de volta para lista de dicts, ignorando linhas vazias
    if edited is not None:
        result = []
        for _, row in edited.iterrows():
            item = {col: str(row.get(col, "")).strip() for col in columns}
            if any(item.values()):  # Só inclui se pelo menos um campo preenchido
                result.append(item)
        return result
    return data_list
