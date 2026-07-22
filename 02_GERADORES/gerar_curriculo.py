#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar currículos focados a partir de dados estruturados em YAML.

Uso:
    python gerar_curriculo.py                    # Gera currículo completo
    python gerar_curriculo.py --tipo musico      # Gera currículo focado em músico
    python gerar_curriculo.py --tipo tecnico     # Gera currículo focado em técnico de som
    python gerar_curriculo.py --tipo produtor    # Gera currículo focado em produtor musical
    python gerar_curriculo.py --anos 3           # Últimos 3 anos
"""

import yaml
import json
from datetime import datetime
from pathlib import Path
import argparse
from typing import List, Dict, Any


class CurriculoGerador:
    """Classe para gerar currículos personalizados a partir de dados estruturados."""

    MAPEAMENTO_TIPOS = {
        "musico": ["baterista", "percussionista"],
        "tecnico": ["tecnico_som", "tecnico_pa", "tecnico_monitor"],
        "produtor": ["produtor_musical", "tecnico_gravacao", "mixagem"],
        "diretor": ["diretor_de_palco", "gestao_palco", "coordenacao_equipe"],
        "completo": None,  # Sem filtro
    }

    def __init__(self, arquivo_yaml: str):
        """Inicializa o gerador carregando o arquivo YAML."""
        self.arquivo_yaml = arquivo_yaml
        self.dados = self._carregar_yaml()
        self.competencias = {c["id"]: c for c in self.dados["competencias_principais"]}

    def _carregar_yaml(self) -> Dict[str, Any]:
        """Carrega o arquivo YAML."""
        with open(self.arquivo_yaml, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _filtrar_projetos(
        self, tipo: str = "completo", anos: int = None
    ) -> List[Dict[str, Any]]:
        """Filtra projetos por tipo e anos."""
        projetos = self.dados["projetos"]
        agora = datetime.now()

        # Filtro por tipo de competência
        if tipo != "completo":
            competencias_filtro = self.MAPEAMENTO_TIPOS.get(tipo, [])
            projetos = [
                p
                for p in projetos
                if any(c in p["competencias"] for c in competencias_filtro)
            ]

        # Filtro por anos
        if anos:
            data_limite = datetime(
                agora.year - anos, agora.month, agora.day
            ).isoformat()
            projetos = [p for p in projetos if p["data_inicio"] >= data_limite]

        # Ordena por data (mais recente primeiro)
        projetos.sort(key=lambda p: p["data_inicio"], reverse=True)
        return projetos

    def _formatar_data(self, data_str: str) -> str:
        """Formata data de string ISO para formato legível."""
        if not data_str:
            return ""
        try:
            data = datetime.fromisoformat(data_str)
            return data.strftime("%B %Y")
        except:
            return data_str

    def _gerar_secao_projeto(self, projeto: Dict[str, Any]) -> str:
        """Gera a seção Markdown de um projeto."""
        titulo = projeto["titulo"]
        cliente = projeto["cliente"]
        local = projeto["local"]
        descricao = projeto["descricao"].strip()
        data_inicio = self._formatar_data(projeto["data_inicio"])
        data_fim = (
            self._formatar_data(projeto["data_fim"])
            if projeto.get("data_fim")
            else "Presente"
        )
        competencias = projeto["competencias"]

        # Monta as competências com labels
        labels_competencias = [
            self.competencias[c]["label"] for c in competencias if c in self.competencias
        ]
        competencias_str = ", ".join(labels_competencias)

        # Seção
        secao = f"""### {titulo}
**Período:** {data_inicio} - {data_fim}
**Cliente/Local:** {cliente} | {local}
**Competências:** {competencias_str}

{descricao}

"""
        return secao

    def gerar_curriculo(
        self, tipo: str = "completo", anos: int = None, salvar: bool = True
    ) -> str:
        """Gera um currículo em Markdown."""
        projetos_filtrados = self._filtrar_projetos(tipo, anos)
        dados_pessoais = self.dados["dados_pessoais"]

        # Cabeçalho
        titulo_tipo = tipo.upper() if tipo != "completo" else "COMPLETO"
        cabecalho = f"""# Currículo - {dados_pessoais['nome']}
**{titulo_tipo}**

**Área de Atuação:** {dados_pessoais['area_atuacao']}
**Localização:** {dados_pessoais['localizacao']}

## Formação
"""

        # Formação
        for form in dados_pessoais["formacao"]:
            cabecalho += f"- **{form['titulo']}** - {form['instituicao']}\n"
            if form.get("registro"):
                cabecalho += f"  Registro: {form['registro']}\n"

        cabecalho += "\n---\n\n"

        # Destaques
        if tipo == "completo":
            cabecalho += "## 🏆 Destaques\n\n"
            for destaque in self.dados["destaques"]:
                cabecalho += f"- **{destaque['titulo']}** ({destaque['cargo']}) - {destaque['periodo']}\n"
                cabecalho += f"  {destaque['descricao']}\n\n"
            cabecalho += "---\n\n"

        # Experiência profissional
        cabecalho += f"## Experiência Profissional\n\n"
        cabecalho += f"*Total de {len(projetos_filtrados)} projetos*\n\n"

        # Projetos
        for projeto in projetos_filtrados:
            cabecalho += self._gerar_secao_projeto(projeto)

        # Rodapé
        data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M")
        rodape = f"\n---\n**Gerado em:** {data_geracao}"

        conteudo_completo = cabecalho + rodape

        # Salva se solicitado
        if salvar:
            nome_arquivo = self._definir_nome_arquivo(tipo, anos)
            caminho = Path("03_SAIDAS") / nome_arquivo
            caminho.parent.mkdir(parents=True, exist_ok=True)
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo_completo)
            print(f"✅ Currículo salvo em: {caminho}")

        return conteudo_completo

    def _definir_nome_arquivo(self, tipo: str, anos: int) -> str:
        """Define o nome do arquivo de saída."""
        nome_base = f"Curriculo_{tipo.capitalize()}"
        if anos:
            nome_base += f"_Ultimos{anos}Anos"
        return f"{nome_base}.md"

    def gerar_estatisticas(self, tipo: str = "completo") -> Dict[str, Any]:
        """Gera estatísticas sobre projetos."""
        projetos = self._filtrar_projetos(tipo)

        stats = {
            "total_projetos": len(projetos),
            "total_shows": sum(p.get("num_shows") or 0 for p in projetos),
            "competencias_usadas": self._contar_competencias(projetos),
            "escala_distribuicao": self._contar_escala(projetos),
            "categorias": self._contar_categorias(projetos),
        }
        return stats

    def _contar_competencias(self, projetos: List) -> Dict[str, int]:
        """Conta uso de cada competência."""
        contagem = {}
        for projeto in projetos:
            for comp in projeto["competencias"]:
                contagem[comp] = contagem.get(comp, 0) + 1
        return contagem

    def _contar_escala(self, projetos: List) -> Dict[str, int]:
        """Conta distribuição por escala (local/regional/nacional/internacional)."""
        contagem = {}
        for projeto in projetos:
            escala = projeto.get("escala", "desconhecida")
            contagem[escala] = contagem.get(escala, 0) + 1
        return contagem

    def _contar_categorias(self, projetos: List) -> Dict[str, int]:
        """Conta distribuição por categoria (músico/técnico/produtor/diretor)."""
        contagem = {}
        for projeto in projetos:
            cat = projeto.get("categoria", "desconhecida")
            contagem[cat] = contagem.get(cat, 0) + 1
        return contagem

    def listar_tipos_disponiveis(self):
        """Lista todos os tipos de currículo disponíveis."""
        print("\n📋 Tipos de Currículo Disponíveis:")
        for tipo, competencias in self.MAPEAMENTO_TIPOS.items():
            if competencias:
                comp_str = ", ".join(competencias)
                print(f"  • {tipo.upper()}: {comp_str}")
            else:
                print(f"  • {tipo.upper()}: Todos os projetos")


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Gera currículos personalizados a partir de dados estruturados."
    )
    parser.add_argument(
        "--tipo",
        choices=["musico", "tecnico", "produtor", "diretor", "completo"],
        default="completo",
        help="Tipo de currículo a gerar (padrão: completo)",
    )
    parser.add_argument(
        "--anos",
        type=int,
        help="Filtrar apenas últimos N anos",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Mostrar estatísticas dos projetos",
    )
    parser.add_argument(
        "--listar-tipos",
        action="store_true",
        help="Lista todos os tipos disponíveis",
    )
    parser.add_argument(
        "--arquivo",
        default="00_BASE_DADOS/dados_estruturados.yaml",
        help="Caminho para o arquivo YAML (padrão: 00_BASE_DADOS/dados_estruturados.yaml)",
    )

    args = parser.parse_args()

    # Verifica se o arquivo existe
    if not Path(args.arquivo).exists():
        print(f"❌ Erro: Arquivo '{args.arquivo}' não encontrado.")
        return

    # Inicializa o gerador
    gerador = CurriculoGerador(args.arquivo)

    # Lista tipos disponíveis se solicitado
    if args.listar_tipos:
        gerador.listar_tipos_disponiveis()
        return

    # Gera currículo
    print(f"\n🎵 Gerando currículo ({args.tipo.upper()})...")
    gerador.gerar_curriculo(tipo=args.tipo, anos=args.anos)

    # Mostra estatísticas se solicitado
    if args.stats:
        stats = gerador.gerar_estatisticas(tipo=args.tipo)
        print(f"\n📊 Estatísticas:")
        print(f"  • Total de projetos: {stats['total_projetos']}")
        print(f"  • Total de shows: {stats['total_shows']}")
        print(f"\n  Competências mais usadas:")
        for comp, count in sorted(
            stats["competencias_usadas"].items(), key=lambda x: x[1], reverse=True
        )[:5]:
            print(f"    - {comp}: {count}")
        print(f"\n  Distribuição por escala:")
        for escala, count in stats["escala_distribuicao"].items():
            print(f"    - {escala}: {count}")


if __name__ == "__main__":
    main()
