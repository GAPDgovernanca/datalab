import unittest
import sqlite3
import os
from db import Database  # Importando o módulo atualizado

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Configuração inicial: conectar ao banco de dados em modo somente leitura. """
        cls.db_path = "frota.db"
        cls.db = Database(cls.db_path)

    def test_select_query(self):
        """ Testa se consultas SELECT funcionam normalmente. """
        query = "SELECT * FROM dim_equipamento LIMIT 1"
        result = self.db.execute_query(query, ())  # 🔹 Agora passamos uma tupla vazia como parâmetros
        self.assertIsInstance(result, list)  # SELECT deve retornar uma lista
        self.assertTrue(isinstance(result[0], sqlite3.Row) or len(result) == 0)  # Deve ser um Row ou lista vazia

    def test_insert_blocked(self):
        """ Testa se o INSERT é bloqueado. """
        query = "INSERT INTO dim_equipamento (modelo, usuario, classe, data_criacao) VALUES (?, ?, ?, ?)"
        params = ("TesteModelo", "TesteUsuario", "TesteClasse", "2024-02-06")
        with self.assertRaises(PermissionError):  # Deve lançar um erro de permissão
            self.db.execute_query(query, params)

    def test_update_blocked(self):
        """ Testa se o UPDATE é bloqueado. """
        query = "UPDATE dim_equipamento SET modelo = ? WHERE id_equipamento = ?"
        params = ("NovoModelo", 1)
        with self.assertRaises(PermissionError):  # Deve lançar um erro de permissão
            self.db.execute_query(query, params)

    def test_delete_blocked(self):
        """ Testa se o DELETE é bloqueado. """
        query = "DELETE FROM dim_equipamento WHERE id_equipamento = ?"
        params = (1,)
        with self.assertRaises(PermissionError):  # Deve lançar um erro de permissão
            self.db.execute_query(query, params)

if __name__ == "__main__":
    unittest.main()
