
#include <iostream>
#include <limits> // Necessário para limpar o buffer corretamente
#include <map>
#include <sstream>
#include <string>

using namespace std;

// --- 1. FUNÇÕES AUXILIARES SEGURAS ---

// Remove espaços E caracteres de controle invisíveis como '\r' (comum no
// Windows)
string trim(const string &str) {
  const string whitespace = " \t\n\r\f\v";
  size_t start = str.find_first_not_of(whitespace);
  if (start == string::npos)
    return ""; // String vazia ou só espaços
  size_t end = str.find_last_not_of(whitespace);
  return str.substr(start, end - start + 1);
}

// Normaliza para minúsculo e remove acentos manualmente para evitar dependência
// de Locale do SO Mapeamos 'ç' e acentos comuns para seus equivalentes ASCII
string normalizarParaAscii(string texto) {
  string saida = "";
  for (size_t i = 0; i < texto.length(); ++i) {
    unsigned char c = static_cast<unsigned char>(texto[i]);

    // Converte maiúsculo para minúsculo (ASCII padrão)
    if (c >= 'A' && c <= 'Z') {
      saida += (c + 32);
    }
    // Mantém letras minúsculas e números
    else if ((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9')) {
      saida += c;
    }
    // Tenta identificar caracteres acentuados comuns (UTF-8 ou Latin1)
    // Isso é uma heurística: se não é ASCII padrão, ignoramos ou tratamos
    // Para "Março", se ignorarmos o 'ç', vira "maro". Nosso mapa vai lidar com
    // isso.
  }
  return saida;
}

int main() {
  // --- 2. MAPA DE DADOS RESILIENTE ---
  // Mapeamos variações possíveis de inputs (com e sem acento, erros de
  // encoding) Isso resolve o problema do "Março" no Windows vs Linux.
  map<string, int> mapa_meses;

  // Padrão
  mapa_meses["janeiro"] = 1;
  mapa_meses["fevereiro"] = 2;
  mapa_meses["marco"] = 3;
  mapa_meses["maro"] = 3; // 'maro' acontece se 'ç' for ignorado
  mapa_meses["abril"] = 4;
  mapa_meses["maio"] = 5;
  mapa_meses["junho"] = 6;
  mapa_meses["julho"] = 7;
  mapa_meses["agosto"] = 8;
  mapa_meses["setembro"] = 9;
  mapa_meses["outubro"] = 10;
  mapa_meses["novembro"] = 11;
  mapa_meses["dezembro"] = 12;

  while (true) { // --- 3. LOOP DE INTERAÇÃO (Evita fechar no erro) ---

    cout << "\nDigite a data (Ex: 15, Fevereiro, 1989) ou 'sair': ";

    string linha;
    if (!getline(cin, linha))
      break; // Proteção contra EOF (Ctrl+D / Ctrl+Z)

    if (trim(linha) == "sair")
      break;

    // Troca qualquer delimitador não alfanumérico por espaço
    for (char &c : linha) {
      if (!isalnum(static_cast<unsigned char>(c)))
        c = ' ';
    }

    stringstream ss(linha);
    string dia_s, mes_s, ano_s;

    // Tenta ler 3 blocos de informação
    if (ss >> dia_s >> mes_s >> ano_s) {
      try {
        int dia = stoi(dia_s);
        int ano = stoi(ano_s);
        string mes_norm = normalizarParaAscii(mes_s);

        // --- 4. VALIDAÇÃO LÓGICA RÍGIDA ---
        if (dia < 1 || dia > 31)
          throw out_of_range("Dia invalido");
        if (ano < 1900 || ano > 2100)
          throw out_of_range("Ano fora do escopo");

        int num_mes = 0;
        // Busca no mapa
        if (mapa_meses.find(mes_norm) != mapa_meses.end()) {
          num_mes = mapa_meses[mes_norm];
        }

        if (num_mes > 0) {
          cout << ">> PROCESSADO: " << dia << " " << num_mes << " " << ano
               << endl;
        } else {
          cout << ">> ERRO: Mes '" << mes_s << "' nao reconhecido." << endl;
        }

      } catch (...) {
        cout << ">> ERRO: Os dados numericos (dia/ano) sao invalidos." << endl;
      }
    } else {
      cout << ">> ERRO: Formato incompleto. Digite: Dia, Mes, Ano." << endl;
    }

    // Limpa estado de erro do cin, se houver, e garante fluxo limpo
    if (cin.fail()) {
      cin.clear();
      cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
  }

  return 0;
}