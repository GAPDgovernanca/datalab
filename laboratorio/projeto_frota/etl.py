# etl.py
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, Any
from sqlalchemy.orm import Session
from models import *
from config import Config

logger = logging.getLogger(__name__)

class FrotaETL:
    def __init__(self, session: Session):
        self.session = session
        self.config = Config()

    def validar_medidor(self, medidor: str) -> str:
        """Valida e normaliza o tipo de medidor"""
        medidor_norm = medidor.strip().upper()
        if medidor_norm not in self.config.MEDIDORES_VALIDOS:
            logger.warning(f"Medidor inválido encontrado: {medidor}. Usando IND.")
            return "IND"
        return medidor_norm

    def processar_equipamento(self, row: pd.Series) -> Dict:
        """Processa dados do equipamento"""
        return {
            'id': int(row['Equipamento']),
            'modelo_versao': str(row['Modelo/Versão']),
            'usuario': str(row['Usuário']),
            'classe': str(row['Classe']),
            'medidor': self.validar_medidor(str(row['Medidor']))
        }

    def processar_uso(self, row: pd.Series, equip_id: int) -> Dict:
        """Processa dados de uso"""
        return {
            'equipamento_id': equip_id,
            'uso_estimado': float(row['Uso (km ou hora) Estimado']),
            'uso_realizado': float(row['Uso (km ou hora) Realizado']),
            'uso_diferenca': float(row['Uso (km ou hora) Diferença'])
        }

    def processar_custo(self, row: pd.Series, equip_id: int) -> Dict:
        """Processa dados de custo"""
        return {
            'equipamento_id': equip_id,
            'custo_km_orcado': float(row['Custo por Km ou hora Orçado']),
            'custo_km_realizado': float(row['Custo por Km ou hora Realizado']),
            'custo_km_diferenca': float(row['Custo por Km ou hora Diferença']),
            'total_orcado': float(row['Total Orçado']),
            'total_realizado': float(row['Total Realizado']),
            'total_diferenca': float(row['Total Diferença'])
        }

    def processar_combustivel(self, row: pd.Series, equip_id: int) -> Dict:
        """Processa dados de combustível"""
        return {
            'equipamento_id': equip_id,
            'volume_orcado': float(row['Combustíveis (l) Orçado']),
            'volume_realizado': float(row['Combustíveis (l) Realizado']),
            'volume_diferenca': float(row['Combustíveis (l) Diferença']),
            'vu_orcado': float(row['VU Combustível Orçado']),
            'vu_realizado': float(row['VU Combustível Realizado']),
            'vu_diferenca': float(row['VU Combustível Diferença']),
            'total_orcado': float(row['Combustíveis Orçado']),
            'total_realizado': float(row['Combustíveis Realizado']),
            'total_diferenca': float(row['Combustíveis Diferença'])
        }

    def processar_manutencao(self, row: pd.Series, equip_id: int) -> Dict:
        """Processa dados de manutenção"""
        return {
            'equipamento_id': equip_id,
            'lubrificantes_orcado': float(row['Lubrificantes Orçado']),
            'lubrificantes_realizado': float(row['Lubrificantes Realizado']),
            'lubrificantes_diferenca': float(row['Lubrificantes Diferença']),
            'filtros_orcado': float(row['Filtros Orçado']),
            'filtros_realizado': float(row['Filtros Realizado']),
            'filtros_diferenca': float(row['Filtros Diferença']),
            'graxas_orcado': float(row['Graxas Orçado']),
            'graxas_realizado': float(row['Graxas Realizado']),
            'graxas_diferenca': float(row['Graxas Diferença']),
            'pecas_servicos_orcado': float(row['Peças, Serviços e Pneus Orçado']),
            'pecas_servicos_realizado': float(row['Peças, Serviços e Pneus Realizado']),
            'pecas_servicos_diferenca': float(row['Peças, Serviços e Pneus Diferença']),
            'reforma_orcado': float(row['Reforma Orçada']),
            'reforma_realizado': float(row['Reforma Realizada']),
            'reforma_diferenca': float(row['Reforma Diferença'])
        }

    def processar_linha(self, row: pd.Series) -> None:
        """Processa uma linha do DataFrame"""
        try:
            # Processa equipamento
            equip_data = self.processar_equipamento(row)
            equipamento = Equipamento(**equip_data)
            self.session.add(equipamento)
            self.session.flush()

            # Processa fatos
            uso = FatoUso(**self.processar_uso(row, equipamento.id))
            custo = FatoCustoOperacional(**self.processar_custo(row, equipamento.id))
            combustivel = FatoCombustivel(**self.processar_combustivel(row, equipamento.id))
            manutencao = FatoManutencao(**self.processar_manutencao(row, equipamento.id))

            self.session.add_all([uso, custo, combustivel, manutencao])
            self.session.flush()

        except Exception as e:
            logger.error(f"Erro ao processar linha: {e}")
            raise

    def executar(self) -> None:
        """Executa o processo ETL"""
        try:
            # Lê o arquivo Excel
            df = pd.read_excel(
                self.config.EXCEL_FILE,
                sheet_name=self.config.SHEET_NAME
            )
            logger.info(f"Arquivo Excel lido com sucesso. Total de registros: {len(df)}")

            # Processa cada linha
            for idx, row in df.iterrows():
                logger.info(f"Processando registro {idx + 1}/{len(df)}")
                self.processar_linha(row)

            # Commit final
            self.session.commit()
            logger.info("ETL concluído com sucesso")

        except Exception as e:
            logger.error(f"Erro durante ETL: {e}")
            self.session.rollback()
            raise