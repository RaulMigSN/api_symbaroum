from django.db import models

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
    nome = models.CharField(max_length=100)
    login = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)

    class Meta:
        abstract = True
        
class Jogador(Usuario):
    biografia = models.TextField(blank=True, null=True)
    fotoDePerfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    
    def __str__(self):
        return self.nome

class Habilidade(models.Model):
    nome = models.CharField(max_length=100)
    descricao_geral = models.TextField()
    tipo = models.CharField(
        max_length=1,
        choices=TipoHabilidade.choices,
    )
    
    def __str__(self):
        return self.nome

class DescricaoHabilidade(models.Model):
    habilidade = models.ForeignKey(
        Habilidade,
        on_delete=models.CASCADE,
        related_name='descricoes'
    )
    nivel_habilidade = models.CharField(
        max_length=1,
        choices=NivelHabilidade.choices,
        default=NivelHabilidade.NOVATO
    )
    tipo_acao = models.CharField(
        max_length=1,
        choices=TipoAcao.choices,
        default=TipoAcao.ATIVA
    )
    descricao = models.TextField()
    
    class Meta:
        unique_together = ('habilidade', 'nivel_habilidade')
    
    def save(self, *args, **kwargs):
        # Se estiver criando (ou seja, ainda não existe)
        if not self.pk and self.habilidade.descricoes.count() >= 3:
            raise ValueError("Não é possível adicionar mais de 3 descrições para a mesma habilidade.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Descrição {self.get_nivel_habilidade_display()} de {self.habilidade.nome}"
    
class Personagem(models.Model):
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name='personagens')
    nome = models.CharField(max_length=100)
    idade = models.PositiveIntegerField()
    experiencia = models.PositiveIntegerField(default=0)
    experiencia_nao_gasta = models.PositiveIntegerField(default=0)
    raca = models.CharField(max_length=2, choices=Raca.choices, default=Raca.HUMANO_AMBRIANO)
    ocupacao = models.CharField(max_length=100, blank=True, null=True)
    vitaliade_maxima = models.PositiveIntegerField(blank=True, null=True)
    vitalidade_atual = models.PositiveIntegerField(blank=True, null=True)
    limiar_de_dor = models.PositiveIntegerField(blank=True, null=True)
    corrupcao_permanente = models.PositiveIntegerField(default=0)
    corrupcao_temporaria = models.PositiveIntegerField(default=0)
    limiar_de_corrupcao = models.PositiveIntegerField(blank=True, null=True)
    sombra = models.CharField(max_length=100, blank=True, null=True)
    citacao = models.CharField(max_length=200, blank=True, null=True)
    
    # Atributos básicos do personagem, eles vão definir alguns dos atributos acima.
    astuto = models.PositiveBigIntegerField(default=10)
    discreto = models.PositiveBigIntegerField(default=10)
    persuasivo = models.PositiveBigIntegerField(default=10)
    preciso = models.PositiveBigIntegerField(default=10)
    rapido = models.PositiveBigIntegerField(default=10)
    resoluto = models.PositiveBigIntegerField(default=10)
    vigilante = models.PositiveBigIntegerField(default=10)
    vigoroso = models.PositiveBigIntegerField(default=10)
    habilidades_e_poderes = models.ManyToManyField(
        Habilidade, 
        through='Aprende',
        related_name='personagens'
    )
    
    
    def __str__(self):
        return f"{self.nome} ({self.jogador.nome})"
    
class Aprende(models.Model):
    personagem = models.ForeignKey(Personagem, on_delete=models.CASCADE)
    habilidade = models.ForeignKey(Habilidade, on_delete=models.CASCADE)
    nivel = models.CharField(
        max_length=1, 
        choices=NivelHabilidade.choices, 
        default=NivelHabilidade.NOVATO
    )
    
    class Meta:
        unique_together = ('personagem', 'habilidade')
        
    def __str__(self):
        return f"{self.personagem.nome} - {self.habilidade.nome} ({self.get_nivel_display()})"

