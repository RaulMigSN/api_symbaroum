"""Uma forma de serializar os dados do projeto Symba. especificar uma classe para convertar para JSON compatível."""

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Usuario, Jogador, Habilidade, DescricaoHabilidade, Qualidade, Equipamento, Elixir, Arma, Armadura, Artefato, Poder, Personagem, Aprende

class UsuarioSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Usuario."""
    senha = serializers.CharField(write_only=True)  # Campo de senha, apenas para escrita
    confirmar_senha = serializers.CharField(write_only=True)  # Campo para confirmar a senha

    def validate(self, data):
        """Valida se a senha e a confirmação de senha são iguais."""
        if data['senha'] != data['confirmar_senha']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return data
    
    def create(self, validated_data):
        """Cria um novo usuário com a senha criptografada."""
        senha = validated_data.pop('senha')
        usuario = Usuario(**validated_data)
        usuario.senha = make_password(senha)  # Criptografa a senha
        usuario.save()
        return usuario
    
    def update(self, instance, validated_data):
        """Atualiza o usuário, permitindo a atualização da senha."""
        senha = validated_data.pop('senha', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if senha:
            instance.senha = make_password(senha)  # Criptografa a nova senha, se fornecida
        instance.save()
        return instance
        
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'login', 'email', 'senha', 'confirmar_senha']
        
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
        
class JogadorSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Jogador."""
    usuario = UsuarioSerializer(read_only=True)  # Inclui os dados do usuário relacionado ao jogador
    personagens = PersonagemSerializer(many=True, read_only=True) # Inclui os personagens relacionados ao jogador
    
    class Meta:
        model = Jogador
        fields = ['id', 'usuario', 'biografia', 'personagens']

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

class EquipamentoSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Equipamento."""
    
    class Meta:
        model = Equipamento
        fields = '__all__'

class ElixirSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Elixir."""
    
    class Meta:
        model = Elixir
        fields = '__all__'

class ArmaSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Arma."""
    
    class Meta:
        model = Arma
        fields = '__all__'
        
class ArmaduraSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Armadura."""
    
    class Meta:
        model = Armadura
        fields = '__all__'
        
class ArtefatoSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Artefato."""
    
    class Meta:
        model = Artefato
        fields = '__all__'

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