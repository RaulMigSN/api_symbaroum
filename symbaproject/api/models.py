from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password

# Enums para usar nos modelos de personagem e outros
class Raca(models.TextChoices):
    HUMANO_AMBRIANO = 'HA', 'Humano Ambriano'
    HUMANO_BARBARO = 'HB', 'Humano Bárbaro'
    CAMBIANTE = 'CA', 'Cambiante'
    GOBLIN = 'GO', 'Goblin'
    OGRO = 'OG', 'Ogro'
    ELFO = 'EL', 'Elfo'
    ANAO = 'AN', 'Anão'
    HUMANO_SEQUESTRADO = 'HS', 'Humano Sequestrado'
    TROLL = 'TR', 'Troll'
    MORTO_VIVO = 'MV', 'Morto-vivo'

# Nível da habilidade que um personagem pode atingir.
class NivelHabilidade(models.TextChoices):
    NOVATO = 'N', 'Novato'
    ADEPTO = 'A', 'Adepto'
    MESTRE = 'M', 'Mestre'


# Tipos de ações que uma habilidade, equipamento ou poder podem ter.
class TipoAcao(models.TextChoices):
    ATIVA = 'A', 'Ativa'
    LIVRE = 'L', 'Livre'
    PASSIVA = 'P', 'Passiva'
    REACAO = 'R', 'Reação'
    ESPECIAL = 'E', 'Especial'
    
    
# Tipos de habilidade que um personagem pode atingir.
class TipoHabilidade(models.TextChoices):
    HABILIDADE = 'H', 'Habilidade'
    TRACO = 'T', 'Traço'
    PODER_MISTICO = 'P', 'Poder Místico'

# Tipos dos equipamentos, essas propriedades são específicas para serem utilizadas no sistema.
class TipoEquipamento(models.TextChoices):
    ARREMESSO = 'AR', 'Arremesso'
    CURTA = 'CU', 'Curta'
    DESARMADO = 'DE', 'Desarmado'
    LONGA = 'LO', 'Longa'
    PESADA = 'PE', 'Pesada'
    PROJETIL = 'PR', 'Projetil'
    UMA_MAO = 'UM', 'Uma Mão'
    ESCUDO = 'ES', 'Escudo'
    ANTIDOTO = 'AN', 'Antídoto'
    VENENO = 'VE', 'Veneno'
    LEVE = 'LE', 'Leve'
    MEDIA = 'ME', 'Média'
    COMUM = 'CO', 'Comum'

#Classes de modelos para o sistema de RPG
class Usuario(models.Model):
    _nome = models.CharField(max_length=100)
    _login = models.CharField(max_length=10, unique=True)
    _email = models.EmailField(unique=True)
    _senha = models.CharField(max_length=128)
    
    def verificarSenha(self, senha):
        return check_password(senha, self.senha)
    
    @staticmethod
    def autenticar(login, senha):
        try:
            jogador = Jogador.objects.get(login=login)
            if jogador.verificarSenha(senha):
                return jogador
        except Jogador.DoesNotExist:
            pass
        return None
    
    def atualizarSenha(self, senha_atual, nova_senha):
        if not self.verificarSenha(senha_atual):
            raise ValidationError("Senha atual incorreta.")
        if not nova_senha or len(nova_senha) < 6:
            raise ValidationError("A nova senha deve ter pelo menos 6 caracteres.")
        self.senha = make_password(nova_senha)
        self.save()
    
    def atualizarEmail(self, novo_email):
        if not novo_email or '@' not in novo_email:
            raise ValidationError("O email deve ser válido.")
        if Usuario.objects.filter(email=novo_email).exists():
            raise ValidationError("Este email já está em uso.")
        self.email = novo_email
        self.save()
    
    class Meta:
        abstract = True
        
class Jogador(Usuario):
    _biografia = models.TextField(blank=True, null=True)
    _fotoDePerfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    
    def adicionar_personagem(self, nome_personagem):
        if not nome_personagem:
            return False
        
        Personagem.objects.create(jogador=self, nome=nome_personagem)
        return True
    
    def listar_personagens(self):
        return list(self.personagens.all())
    
    def __str__(self):
        return self.nome

class Habilidade(models.Model):
    _nome = models.CharField(max_length=100)
    _descricao_geral = models.TextField()
    _tipo = models.CharField(
        max_length=1,
        choices=TipoHabilidade.choices,
    )
    
    def __str__(self):
        return self.nome

class DescricaoHabilidade(models.Model):
    _habilidade = models.ForeignKey(
        Habilidade,
        on_delete=models.CASCADE,
        related_name='descricoes'
    )
    _nivel_habilidade = models.CharField(
        max_length=1,
        choices=NivelHabilidade.choices,
        default=NivelHabilidade.NOVATO
    )
    _tipo_acao = models.CharField(
        max_length=1,
        choices=TipoAcao.choices,
        default=TipoAcao.ATIVA
    )
    _descricao = models.TextField()
    
    class Meta:
        unique_together = ('habilidade', 'nivel_habilidade')
    
    def save(self, *args, **kwargs):
        # Se estiver criando (ou seja, ainda não existe)
        if not self.pk and self.habilidade.descricoes.count() >= 3:
            raise ValueError("Não é possível adicionar mais de 3 descrições para a mesma habilidade.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Descrição {self.get_nivel_habilidade_display()} de {self.habilidade.nome}"

class Qualidade(models.Model):
    _nome = models.CharField(max_length=100, unique=True)
    _descricao = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nome

class Equipamento(models.Model):
    _nome = models.CharField(max_length=100)
    _custo = models.JSONField(default=dict) # Ex: {'taler': 1, 'xelins': 3, 'ortegas': 20}
    _tipo = models.CharField(max_length=2, choices=TipoEquipamento.choices, default=TipoEquipamento.COMUM)
    _personagem = models.ForeignKey(
        'Personagem',
        on_delete=models.CASCADE,
        related_name='equipamentos'
    )
    
    def __str__(self):
        return f"{self.nome} ({self.tipo})"
    
class Elixir(Equipamento):
    _efeito = models.TextField()
    
    def __str__(self):
        return f"{self.nome} (Efeito: {self.efeito})"
    
class Arma(Equipamento):
    _dano = models.CharField(max_length=50)  # Ex: "1d6"
    _qualidade = models.ForeignKey(
        Qualidade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='armas'
    )
    
    def __str__(self):
        return f"{self.nome} (Dano: {self.dano})"

class Armadura(Equipamento):
    _protecao = models.CharField(max_length=50)  # Ex: "1d4"
    _qualidade = models.ForeignKey(
        Qualidade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='armaduras'
    )
    
    def __str__(self):
        return f"{self.nome} (Proteção: {self.protecao})"
    
class Artefato(models.Model):
    _titulo = models.CharField(max_length=100)
    _descricao = models.TextField()
    _personagem = models.ForeignKey(
        'Personagem',
        on_delete=models.CASCADE,
        related_name='artefatos',
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"{self.titulo} ({self.personagem.nome if self.personagem else 'Sem Personagem'})"
    
class Poder(models.Model):
    _artefato = models.ForeignKey(
        Artefato,
        on_delete=models.CASCADE,
        related_name='poderes'
    )
    _nome = models.CharField(max_length=100)
    _requesito = models.TextField()
    _descricao = models.TextField()
    _acao = models.CharField(
        max_length=1,
        choices=TipoAcao.choices,
        default=TipoAcao.ATIVA
    )
    _corrupcao = models.CharField(max_length=50)  # Ex: "1d6"
    
    def __str__(self):
        return f"{self.nome} ({self.artefato.titulo})"
    
class Personagem(models.Model):
    _jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name='personagens')
    _nome = models.CharField(max_length=100)
    _idade = models.PositiveIntegerField(default=18)
    _experiencia = models.PositiveIntegerField(default=0)
    _experiencia_nao_gasta = models.PositiveIntegerField(default=0)
    _raca = models.CharField(max_length=2, choices=Raca.choices, default=Raca.HUMANO_AMBRIANO)
    _ocupacao = models.CharField(max_length=100, blank=True, null=True)
    _vitaliade_maxima = models.PositiveIntegerField(blank=True, null=True)
    _vitalidade_atual = models.PositiveIntegerField(blank=True, null=True)
    _limiar_de_dor = models.PositiveIntegerField(blank=True, null=True)
    _corrupcao_permanente = models.PositiveIntegerField(default=0)
    _corrupcao_temporaria = models.PositiveIntegerField(default=0)
    _limiar_de_corrupcao = models.PositiveIntegerField(blank=True, null=True)
    _sombra = models.CharField(max_length=100, blank=True, null=True)
    _citacao = models.CharField(max_length=200, blank=True, null=True)
    
    # Atributos básicos do personagem, eles vão definir alguns dos atributos acima.
    _astuto = models.PositiveBigIntegerField(default=10)
    _discreto = models.PositiveBigIntegerField(default=10)
    _persuasivo = models.PositiveBigIntegerField(default=10)
    _preciso = models.PositiveBigIntegerField(default=10)
    _rapido = models.PositiveBigIntegerField(default=10)
    _resoluto = models.PositiveBigIntegerField(default=10)
    _vigilante = models.PositiveBigIntegerField(default=10)
    _vigoroso = models.PositiveBigIntegerField(default=10)
    _habilidades_e_poderes = models.ManyToManyField(
        Habilidade, 
        through='Aprende',
        related_name='personagens'
    )
    _altura = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    _peso = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    _aparencia = models.TextField(blank=True, null=True)
    _foto = models.ImageField(upload_to='fotos_personagens/', blank=True, null=True)
    _historico = models.TextField(blank=True, null=True)
    _objetivo_pessoal = models.TextField(blank=True, null=True)
    _amigos_e_companheiros = models.TextField(blank=True, null=True)
    _armadura_equipada = models.OneToOneField(
        'Armadura',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personagem_vestindo'
    )
    _armas_equipadas = models.ManyToManyField(
        'Arma',
        blank=True,
        related_name='personagem_empunhando'
    )
    _dinheiro = models.JSONField(default=dict) # Ex: {'taler': 1, 'xelins': 3, 'ortegas': 20}
    _outras_riquezas = models.TextField(blank=True, null=True)
    
    
    def equipar_armadura(self, armadura):
        if armadura.personagem != self:
            raise ValueError("Essa armadura não pertence ao personagem.")
        self.armadura_equipada = armadura
        self.save()
        
    def equipar_arma(self, arma):
        if arma.personagem != self:
            raise ValueError("Essa arma não pertence ao personagem.")
        self.armas_equipadas.add(arma)
        self.save()
        
    def ganhar_experiencia(self, quantidade):
        self.experiencia += quantidade
        self.experiencia_nao_gasta += quantidade
        self.save()
        
    def remover_experiencia(self, quantidade):
        if quantidade > self.experiencia_nao_gasta:
            raise ValueError("Não é possível remover mais experiência do que a disponível.")
        self.experiencia_nao_gasta -= quantidade
        self.save()
        
    def remover_experiencia_total(self, quantidade):
        if quantidade > self.experiencia:
            raise ValueError("Não é possível remover mais experiência do que a total.")
        self.experiencia -= quantidade
        self.experiencia_nao_gasta -= quantidade
        self.save()
        
    def listar_habilidades(self):
        habilidades = self.aprende_set.select_related('habilidade')
        resultado = []
        for aprende in habilidades:
            nivel = aprende.get_nivel_display()
            habilidade = aprende.habilidade
            resultado.append({
                'nome': habilidade.nome,
                'descricao': habilidade.descricao_geral,
                'tipo': habilidade.tipo,
                'nivel': nivel,
            })
        return resultado
    
    @classmethod
    def criar_com_padrao(cls, jogador, nome):
        return cls.objects.create(nome=nome, jogador=jogador)
        
    def __str__(self):
        return f"{self.nome} ({self.jogador.nome})"
    
class Aprende(models.Model):
    _personagem = models.ForeignKey(Personagem, on_delete=models.CASCADE)
    _habilidade = models.ForeignKey(Habilidade, on_delete=models.CASCADE)
    _nivel = models.CharField(
        max_length=1, 
        choices=NivelHabilidade.choices, 
        default=NivelHabilidade.NOVATO
    )
    
    class Meta:
        unique_together = ('personagem', 'habilidade')
    
    def promover_nivel(self):
        ordem = ['N', 'A', 'M']
        atual = ordem.index(self.nivel)
        if atual < 2:  # Se não for o nível máximo
            self.nivel = ordem[atual + 1]
            self.save()
    
    def rebaixar_nivel(self):
        ordem = ['N', 'A', 'M']
        atual = ordem.index(self.nivel)
        if atual > 0:
            self.nivel = ordem[atual - 1]
            self.save()
    
    def clean(self):
        super().clean()
        
        existe = Aprende.objects.filter(
            personagem=self.personagem, 
            habilidade=self.habilidade
        ).exclude(pk=self.pk).exists()
        
        if existe:
            raise ValidationError("Esse personagem já aprendeu essa habilidade, atualize o nível em vez de criar uma nova entrada.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.personagem.nome} - {self.habilidade.nome} ({self.get_nivel_display()})"

