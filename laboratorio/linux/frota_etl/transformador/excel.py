# transformador/excel.py
"""
Módulo: Processador de Dados Excel
Objetivo: Transformar dados do Excel para formato dimensional
"""

import pandas as pd
from pathlib import Path
import logging
import numpy as np
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Tuple

class ProcessadorExcel:
    """Processa arquivo Excel de frotas para formato dimensional"""
    
    def __init__(self, arquivo: str, logger: logging.Logger):
        self.arquivo = Path(arquivo)
        self.logger = logger
        self.data_processamento = datetime.now()
        self.data_referencia = datetime(2024, 4, 1)
    
    def executar(self) -> Tuple[Dict, List[Dict]]:
        """
        Executa processamento completo do arquivo
        Returns:
            Tuple[Dict, List[Dict]]: Dimensões e fatos processados
        """
        try:
            self.logger.info(f"Iniciando processamento do arquivo: {self.arquivo}")
            dados = self._ler_arquivo()
            dimensoes = self._processar_dimensoes(dados)
            fatos = self._processar_fatos(dados)
            return dimensoes, fatos
        except Exception as e:
            self.logger.error(f"Erro no processamento: {str(e)}")
            raise
    
    def _ler_arquivo(self) -> pd.DataFrame:
        """Lê arquivo Excel com pandas"""
        try:
            return pd.read_excel(
                self.arquivo,
                dtype={
                    'Equipamento': int,
                    'Modelo/Versão': str,
                    'Usuário': str,
                    'Classe': str,
                    'Medidor': str
                }
            )
        except Exception as e:
            self.logger.error(f"Erro na leitura do arquivo: {str(e)}")
            raise
    
    def _processar_dimensoes(self, df: pd.DataFrame) -> Dict[str, List]:
        """Processa dimensões do dataframe"""
        try:
            dimensoes = {
                'dim_equipamento': df[['Equipamento', 'Modelo/Versão', 'Usuário', 'Classe']]
                .rename(columns={
                    'Equipamento': 'id_equipamento',
                    'Modelo/Versão': 'modelo',
                    'Usuário': 'usuario',
                    'Classe': 'classe'
                })
                .assign(data_criacao=self.data_processamento.strftime("%Y-%m-%d %H:%M:%S"))  # Converte para string compatível com SQLite
                .to_dict('records')
            }
            self.logger.info(f"Processadas {len(dimensoes['dim_equipamento'])} dimensões")
            return dimensoes
        except Exception as e:
            self.logger.error(f"Erro no processamento de dimensões: {str(e)}")
            raise
    
    def _processar_fatos(self, df: pd.DataFrame) -> List[Dict]:
        """Processa tabelas de fatos"""
        try:
            fatos = {
                'fato_uso': self._processar_fato_uso(df),
                'fato_custo': self._processar_fato_custo(df),
                'fato_combustivel': self._processar_fato_combustivel(df),
                'fato_manutencao': self._processar_fato_manutencao(df),
                'fato_reforma': self._processar_fato_reforma(df)
            }
            self.logger.info("Processamento de fatos concluído")
            return fatos
        except Exception as e:
            self.logger.error(f"Erro no processamento de fatos: {str(e)}")
            raise

    def _processar_fato_uso(self, df: pd.DataFrame) -> List[Dict]:
        """Processa fatos de uso e trata valores nulos corretamente"""
        return (df[[
            'Equipamento',
            'Medidor',
            'Uso (km ou hora) Estimado',
            'Uso (km ou hora) Realizado',
            'Uso (km ou hora) Diferença'
        ]].rename(columns={
            'Equipamento': 'id_equipamento',
            'Medidor': 'tipo_medidor',
            'Uso (km ou hora) Estimado': 'uso_estimado',
            'Uso (km ou hora) Realizado': 'uso_realizado',
            'Uso (km ou hora) Diferença': 'uso_diferenca'
        })
        .assign(
            data_referencia=self.data_referencia.strftime("%Y-%m-%d"),
            data_processamento=self.data_processamento.strftime("%Y-%m-%d %H:%M:%S")
        )
        .replace({np.nan: 0})  # Substitui NaN por 0
        .to_dict('records'))

    def _processar_fato_custo(self, df: pd.DataFrame) -> List[Dict]:
        """Processa fatos de custo"""
        return (df[[
            'Equipamento',
            'Custo por Km ou hora Orçado',
            'Custo por Km ou hora Realizado',
            'Custo por Km ou hora Diferença',
            'Total Orçado',
            'Total Realizado',
            'Total Diferença'
        ]].rename(columns={
            'Equipamento': 'id_equipamento',
            'Custo por Km ou hora Orçado': 'custo_hora_estimado',
            'Custo por Km ou hora Realizado': 'custo_hora_realizado',
            'Custo por Km ou hora Diferença': 'custo_hora_diferenca',
            'Total Orçado': 'total_estimado',
            'Total Realizado': 'total_realizado',
            'Total Diferença': 'total_diferenca'
        })
        .assign(
            data_referencia=self.data_referencia.strftime("%Y-%m-%d"),
            data_processamento=self.data_processamento.strftime("%Y-%m-%d %H:%M:%S")
        )
        .replace({np.nan: 0})  # Substitui NaN por 0
        .to_dict('records'))

    def _processar_fato_combustivel(self, df: pd.DataFrame) -> List[Dict]:
        """Processa fatos de combustível"""
        return (df[[
            'Equipamento',
            'Combustíveis (l) Orçado',
            'Combustíveis (l) Realizado',
            'Combustíveis (l) Diferença',
            'VU Combustível Orçado',
            'VU Combustível Realizado',
            'VU Combustível Diferença',
            'Combustíveis Orçado',
            'Combustíveis Realizado',
            'Combustíveis Diferença'
        ]].rename(columns={
            'Equipamento': 'id_equipamento',
            'Combustíveis (l) Orçado': 'comb_litros_estimado',
            'Combustíveis (l) Realizado': 'comb_litros_realizado',
            'Combustíveis (l) Diferença': 'comb_litros_diferenca',
            'VU Combustível Orçado': 'comb_valor_unitario_estimado',
            'VU Combustível Realizado': 'comb_valor_unitario_realizado',
            'VU Combustível Diferença': 'comb_valor_unitario_diferenca',
            'Combustíveis Orçado': 'comb_total_estimado',
            'Combustíveis Realizado': 'comb_total_realizado',
            'Combustíveis Diferença': 'comb_total_diferenca'
        })
        .assign(
            data_referencia=self.data_referencia.strftime("%Y-%m-%d"),
            data_processamento=self.data_processamento.strftime("%Y-%m-%d %H:%M:%S")
        )
        .replace({np.nan: 0})
        .to_dict('records'))

    def _processar_fato_manutencao(self, df: pd.DataFrame) -> List[Dict]:
        """Processa fatos de manutenção"""
        return (df[[
            'Equipamento',
            'Lubrificantes Orçado',
            'Lubrificantes Realizado',
            'Lubrificantes Diferença',
            'Filtros Orçado',
            'Filtros Realizado',
            'Filtros Diferença',
            'Graxas Orçado',
            'Graxas Realizado',
            'Graxas Diferença',
            'Peças, Serviços e Pneus Orçado',
            'Peças, Serviços e Pneus Realizado',
            'Peças, Serviços e Pneus Diferença'
        ]].rename(columns={
            'Equipamento': 'id_equipamento',
            'Lubrificantes Orçado': 'lubrificantes_estimado',
            'Lubrificantes Realizado': 'lubrificantes_realizado',
            'Lubrificantes Diferença': 'lubrificantes_diferenca',
            'Filtros Orçado': 'filtros_estimado',
            'Filtros Realizado': 'filtros_realizado',
            'Filtros Diferença': 'filtros_diferenca',
            'Graxas Orçado': 'graxas_estimado',
            'Graxas Realizado': 'graxas_realizado',
            'Graxas Diferença': 'graxas_diferenca',
            'Peças, Serviços e Pneus Orçado': 'pecas_servicos_estimado',
            'Peças, Serviços e Pneus Realizado': 'pecas_servicos_realizado',
            'Peças, Serviços e Pneus Diferença': 'pecas_servicos_diferenca'
        })
        .assign(
            data_referencia=self.data_referencia.strftime("%Y-%m-%d"),
            data_processamento=self.data_processamento.strftime("%Y-%m-%d %H:%M:%S")
        )
        .replace({np.nan: 0})
        .to_dict('records'))

    def _processar_fato_reforma(self, df: pd.DataFrame) -> List[Dict]:
        """Processa fatos de reforma"""
        return (df[[
            'Equipamento',
            'Reforma Orçada',
            'Reforma Realizada',
            'Reforma Diferença'
        ]].rename(columns={
            'Equipamento': 'id_equipamento',
            'Reforma Orçada': 'reforma_estimado',
            'Reforma Realizada': 'reforma_realizado',
            'Reforma Diferença': 'reforma_diferenca'
        })
        .assign(
            data_referencia=self.data_referencia.strftime("%Y-%m-%d"),
            data_processamento=self.data_processamento.strftime("%Y-%m-%d %H:%M:%S")
        )
        .replace({np.nan: 0})
        .to_dict('records'))
