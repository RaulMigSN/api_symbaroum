"""Uma forma de serializar os dados do projeto Symba. especificar uma classe para convertar para JSON compatível."""

from rest_framework import serializers
from .models import ArmaBase, ArmaduraBase, ArtefatoBase, EquipamentoBase, Usuario, JogadorPerfil, Habilidade, DescricaoHabilidade, Qualidade, Equipamento, Elixir, Arma, Armadura, Artefato, Poder, Personagem, Aprende
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')

        try:
            usuario = Usuario.objects.get(login=login)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Login ou senha inválidos.")

        if not usuario.check_password(password):
            raise serializers.ValidationError("Login ou senha inválidos.")

        data = super().validate({
            'username': usuario.login,  # necessário para compatibilidade do SimpleJWT
            'password': password
        })

        data['user_id'] = usuario.id
        data['login'] = usuario.login
        data['tipo'] = usuario.tipo

        return data

class UsuarioCadastroSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Usuario Geral."""
    senha = serializers.CharField(write_only=True)
    confirmar_senha = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['login', 'email', 'senha', 'confirmar_senha', 'tipo']

    def validade(self, data):
        senha = data.get('senha')
        confirmar_senha = data.get('confirmar_senha')

        if senha != confirmar_senha:
            raise serializers.ValidationError("As senhas não coincidem.")
        return data

    def create(self, validated_data):
        senha = validated_data.pop('senha')
        validated_data.pop('confirmar_senha', None)
        usuario = Usuario.objects.create_user(senha=senha, **validated_data)
        return usuario

class UsuarioSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Usuario.""" 
    class Meta:
        model = Usuario
        fields = ['id', 'login', 'email', 'tipo']
        
class HabilidadeSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Habilidade."""
    
    class Meta:
        model = Habilidade
        fields = '__all__'

class PersonagemSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Personagem."""
    
    class Meta:
        model = Personagem
        fields = '__all__'
        
class JogadorPerfilSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Jogador."""
    usuario = UsuarioSerializer(read_only=True)  # Inclui os dados do usuário relacionado ao jogador
    personagens = PersonagemSerializer(many=True, read_only=True) # Inclui os personagens relacionados ao jogador
    
    class Meta:
        model = JogadorPerfil
        fields = ['id', 'usuario', 'biografia', 'fotoDePerfil', 'personagens']

class DescricaoHabilidadeSerializer(serializers.ModelSerializer):
    """Serializador para o modelo DescricaoHabilidade."""
    
    class Meta:
        model = DescricaoHabilidade
        fields = '__all__'

class QualidadeSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Qualidade."""
    
    class Meta:
        model = Qualidade
        fields = '__all__'
        
class EquipamentoBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipamentoBase
        fields = ['id', 'nome', 'custo', 'tipo', 'descricao']

class EquipamentoSerializer(serializers.ModelSerializer):
    equipamento_base = EquipamentoBaseSerializer(read_only=True)
    equipamento_base_id = serializers.PrimaryKeyRelatedField(
        queryset=EquipamentoBase.objects.all(), source='equipamento_base', write_only=True
    )

    class Meta:
        model = Equipamento
        fields = ['id', 'personagem', 'equipamento_base', 'equipamento_base_id', 'equipado']
        read_only_fields = ['personagem']

    def create(self, validated_data):
        personagem = self.context['request'].user.jogador.listar_personagens()[0]
        validated_data['personagem'] = personagem
        return super().create(validated_data)

class ElixirSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Elixir."""
    
    class Meta:
        model = Elixir
        fields = '__all__'

class ArmaBaseSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Base de Armas (Catálogo)"""
    
    class Meta:
        model = ArmaBase
        fields = '__all__'

class ArmaSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Arma."""
    
    class Meta:
        model = Arma
        fields = '__all__'

class ArmaduraBaseSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Base de Armas (Catálogo)"""
    
    class Meta:
        model = ArmaduraBase
        fields = '__all__'
        
class ArmaduraSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Armadura."""
    
    class Meta:
        model = Armadura
        fields = '__all__'

class ArtefatoBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtefatoBase
        fields = ['id', 'titulo', 'descricao']

class ArtefatoSerializer(serializers.ModelSerializer):
    artefato_base = ArtefatoBaseSerializer(read_only=True)
    artefato_base_id = serializers.PrimaryKeyRelatedField(
        queryset=ArtefatoBase.objects.all(), source='artefato_base', write_only=True
    )

    class Meta:
        model = Artefato
        fields = ['id', 'personagem', 'artefato_base', 'artefato_base_id', 'equipado']
        read_only_fields = ['personagem']

    def create(self, validated_data):
        personagem = self.context['request'].user.jogador.listar_personagens()[0]
        validated_data['personagem'] = personagem
        return super().create(validated_data)

class PoderSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Poder."""
    
    class Meta:
        model = Poder
        fields = '__all__'
        
class AprendeSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Aprende."""
    
    class Meta:
        model = Aprende
        fields = '__all__'       