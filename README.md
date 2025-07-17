# 🐉 API Symbaroum

Uma API desenvolvida para praticar conhecimentos em Django e facilitar a gestão de personagens do sistema de RPG Symbaroum. O objetivo é criar uma base robusta para futuros projetos, tanto web quanto mobile, e tornar a experiência dos jogadores mais simples e intuitiva.

## 📖 Descrição
Esta API permite gerenciar informações de personagens dos jogadores, possibilitando exportação de fichas para PDF e edição completa dos dados. O projeto é ideal para quem deseja integrar sistemas de RPG a aplicações web ou mobile, servindo como base para múltiplos front-ends.

### 💡 Ideias do Projeto
- 🕸️ **Ideia 1:** Criar uma API que atenda a um sistema web onde o jogador faz login com seu perfil e gerencia seu personagem, inicialmente em uma rede local.
- 📱 **Ideia 2:** Após a interface web, desenvolver um aplicativo mobile para manipular fichas de personagem, ampliando o acesso e a praticidade.

## 🚀 Funcionalidades
- 👤 Cadastro e autenticação de usuários (JWT)
- 📝 Perfis de jogador com biografia e foto
- 🧙‍♂️ CRUD completo de personagens, com atributos, raça, ocupação, equipamentos, habilidades e poderes
- 🗃️ Catálogo de equipamentos, armas, armaduras, artefatos e elixires
- 🧠 Sistema de habilidades, qualidades e poderes
- 🔗 Relacionamento entre personagens e seus itens/habilidades
- 📄 Exportação de ficha (planejado)

## 🔗 Principais Endpoints
A API segue o padrão REST e utiliza o Django REST Framework. Os principais endpoints disponíveis são:

- `/api/cadastro/` — Cadastro de usuários
- `/api/auth/token/` — Autenticação JWT
- `/api/perfil-jogador/` — Perfil do jogador
- `/api/personagens/` — CRUD de personagens
- `/api/habilidades/`, `/api/qualidades/`, `/api/equipamentos-base/`, `/api/armas-base/`, `/api/armaduras-base/`, `/api/artefatos-base/` — Catálogos do sistema
- `/api/equipamentos/`, `/api/elixires/`, `/api/armas/`, `/api/armaduras/`, `/api/artefatos/`, `/api/poderes/`, `/api/aprendizados/` — Itens e poderes específicos de cada personagem

## 🛠️ Tecnologias Utilizadas
- 🐍 **Python 3.11+**
- 🌐 **Django 5.2**
- 🔗 **Django REST Framework**
- 🔒 **SimpleJWT** (autenticação)
- 🧪 **pytest** e **pytest-django** (testes automatizados)
- 🗄️ **SQLite** (banco de dados padrão, facilmente adaptável)
- 📦 Outras libs: Pillow, django-cors-headers, django-extensions, python-decouple, dotenv, etc.

Veja o arquivo `requirements.txt` para a lista completa de dependências.

## 🗂️ Estrutura do Projeto
- 📦 App principal: `api`
- 🧑‍💻 Modelos: Usuário, JogadorPerfil, Personagem, Equipamento, Habilidade, Qualidade, Artefato, Poder, etc.
- 🛠️ Serializers e ViewSets para todos os modelos principais
- 🧪 Testes automatizados em `symbaproject/api/tests/`
- 🗃️ Migrações já preparadas em `symbaproject/api/migrations/`

## ▶️ Como Executar
1. Clone o repositório e instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure as variáveis de ambiente (`.env` ou exporte `SECRET_KEY` e `DEBUG`):
   ```env
   SECRET_KEY=sua_secret_key
   DEBUG=True
   ```
3. Realize as migrações:
   ```bash
   python symbaproject/manage.py migrate
   ```
4. Execute o servidor de desenvolvimento:
   ```bash
   python symbaproject/manage.py runserver
   ```
5. Acesse a API em: `http://localhost:8000/api/`

## 🧪 Como Rodar os Testes
Execute os testes automatizados com:
```bash
pytest
```

## 🔮 Planos Futuros
- 🖥️ Completar a API para suportar múltiplos front-ends (Angular, Ionic, etc.)
- 🎲 Implementar sistema do Mestre (GM)
- 📚 Gerar tutoriais e documentação detalhada
- 📝 Exportação de ficha para PDF
- 🔐 Melhorar autenticação e permissões

## 💬 Observações
- O projeto está em desenvolvimento e aberto a contribuições.

---

**Pensamentos para aplicações:**
Atualmente, planejo criar um sistema que funcione tanto para web quanto para mobile, utilizando tecnologias como Dart ou Ionic (provavelmente Ionic, para trabalhar diretamente com JavaScript).