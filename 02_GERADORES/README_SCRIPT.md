# Script de Geração de Currículos

## 📋 Descrição

Este script Python lê o arquivo `dados_estruturados.yaml` e gera currículos personalizados em Markdown focados em áreas específicas de sua carreira.

## 🚀 Instalação

### Requisitos
- Python 3.7+
- PyYAML

### Instalação de dependências

```bash
pip install pyyaml
```

## 💻 Uso

### Gerar currículo completo

```bash
python gerar_curriculo.py
```

Gera: `03_SAIDAS/Curriculo_Completo.md`

### Gerar currículo focado em Músico

```bash
python gerar_curriculo.py --tipo musico
```

Gera: `03_SAIDAS/Curriculo_Musico.md`

Incluirá apenas projetos com as competências:
- `baterista`
- `percussionista`

### Gerar currículo focado em Técnico de Som

```bash
python gerar_curriculo.py --tipo tecnico
```

Gera: `03_SAIDAS/Curriculo_Tecnico.md`

Incluirá apenas projetos com as competências:
- `tecnico_som`
- `tecnico_pa`
- `tecnico_monitor`

### Gerar currículo focado em Produtor Musical

```bash
python gerar_curriculo.py --tipo produtor
```

Gera: `03_SAIDAS/Curriculo_Produtor.md`

Incluirá apenas projetos com as competências:
- `produtor_musical`
- `tecnico_gravacao`
- `mixagem`

### Gerar currículo focado em Diretor de Palco

```bash
python gerar_curriculo.py --tipo diretor
```

Gera: `03_SAIDAS/Curriculo_Diretor.md`

Incluirá apenas projetos com as competências:
- `diretor_de_palco`
- `gestao_palco`
- `coordenacao_equipe`

### Filtrar pelos últimos N anos

```bash
python gerar_curriculo.py --tipo tecnico --anos 5
```

Gera: `03_SAIDAS/Curriculo_Tecnico_Ultimos5Anos.md`

### Ver estatísticas

```bash
python gerar_curriculo.py --tipo musico --stats
```

Mostra no terminal:
- Total de projetos
- Total de shows
- Competências mais usadas
- Distribuição por escala (local, regional, nacional, internacional)

### Listar tipos disponíveis

```bash
python gerar_curriculo.py --listar-tipos
```

Mostra todos os tipos de currículo disponíveis e suas competências associadas.

## 📝 Estrutura de Saída

Todos os currículos gerados ficam em `03_SAIDAS/` com a seguinte estrutura:

```markdown
# Currículo - Valderval de Oliveira Filho
**TIPO**

**Área de Atuação:** Produção Musical e Eventos Culturais
**Localização:** Curitiba/PR

## Formação
- **Musicoterapeuta** - Faculdade de Artes do Paraná

## 🏆 Destaques (apenas no currículo completo)

## Experiência Profissional

### Projeto 1
**Período:** Janeiro 2023 - Presente
**Cliente/Local:** Cliente | Local
**Competências:** Competência 1, Competência 2

Descrição do projeto...

### Projeto 2
...
```

## 🔄 Fluxo de Atualização

### Quando você fizer um novo projeto:

1. **Edite** `00_BASE_DADOS/dados_estruturados.yaml`
2. **Adicione** uma nova entrada na seção `projetos:`
3. **Rode** `python gerar_curriculo.py` (ou com `--tipo` específico)
4. **Pronto!** Os arquivos em `03_SAIDAS/` serão atualizados automaticamente

## 📊 Campos do YAML

Cada projeto deve ter:

```yaml
- id: "identificador_unico"
  data_inicio: "YYYY-MM-DD"
  data_fim: "YYYY-MM-DD" (ou null para "Presente")
  titulo: "Título do Projeto"
  cliente: "Nome do cliente ou instituição"
  local: "Cidade/Estado"
  competencias:
    - "competencia_id_1"
    - "competencia_id_2"
  descricao: |
    Descrição em múltiplas linhas.
    Pode ter vários parágrafos.
  num_shows: 5 (ou null)
  escala: "regional" (local, regional, nacional, internacional)
  destaque: true (ou false)
  status: "completo" (ou ativo)
  categoria: "tecnico" (tecnico, musico, produtor, diretor)
  evidencias: [] (lista de evidências/documentos)
  links_audio_video: [] (links para Spotify, YouTube, etc)
```

## 🎵 Competências Disponíveis

Ao adicionar um projeto, use os `id` das competências:

- `diretor_de_palco` - Diretor de Palco
- `tecnico_som` - Técnico de Som
- `tecnico_pa` - Técnico de PA
- `tecnico_monitor` - Técnico de Monitor
- `produtor_musical` - Produtor Musical
- `tecnico_gravacao` - Técnico de Gravação
- `mixagem` - Mixagem
- `baterista` - Baterista
- `percussionista` - Percussionista
- `gestao_palco` - Gestão de Palco
- `coordenacao_equipe` - Coordenação de Equipe
- `gravacao_estudio` - Gravação em Estúdio

## 🤔 Dúvidas Frequentes

**P: Onde fico os arquivos gerados?**
R: Em `03_SAIDAS/` na raiz do repositório.

**P: Posso editar os arquivos gerados em `03_SAIDAS/`?**
R: Não recomendado! Qualquer vez que você roda o script, eles são regenerados. Sempre edite `dados_estruturados.yaml`.

**P: Posso adicionar novas competências?**
R: Sim! Edite a seção `competencias_principais:` em `dados_estruturados.yaml`.

**P: Como adiciono links de áudio/vídeo?**
R: No campo `links_audio_video:` de cada projeto, adicione:
```yaml
links_audio_video:
  - plataforma: "spotify"
    url: "https://..."
  - plataforma: "youtube"
    url: "https://..."
```

## 📞 Suporte

Se encontrar problemas, verifique:
1. Python 3.7+ está instalado
2. PyYAML está instalado (`pip install pyyaml`)
3. O arquivo `dados_estruturados.yaml` está em `00_BASE_DADOS/`
4. O YAML está bem formado (sem indentações erradas)
