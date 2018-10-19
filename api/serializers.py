# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from api.models import (Usuario,
                        Grupo,
                        Diario, 
                        LocalDeInteresse, 
                        Relacionamento,
                        Recomendacao)


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer de exemplo
    """
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    class Meta:
        model = Usuario
        fields = ('id', 'username', 'full_name')


class PerfilSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    seguindo = serializers.SerializerMethodField()
    seguidores = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_seguindo(self, obj):
        return obj.relacionamento_set.count()

    def get_seguidores(self, obj):
        return Relacionamento.objects.filter(seguindo=obj).count()

    class Meta:
        model = Usuario
        fields = ('id', 'username', 'full_name', 
                  'email', 'foto', 'seguindo', 'seguidores')


class DetalhePerfilSerializer(PerfilSerializer):
    me_segue = serializers.BooleanField()
    sigo = serializers.BooleanField()
    classificacao_id = serializers.IntegerField()

    class Meta:
        model = Usuario
        fields = ('id', 'username', 'full_name', 
                  'email', 'foto', 'seguindo', 'seguidores',
                  'me_segue', 'sigo', 'classificacao_id')


class GrupoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Grupo
        fields = ('id', 'name', 'membros')


class DetalheGrupoSerializer(serializers.ModelSerializer):
    membros = PerfilSerializer(many=True)
    dono = PerfilSerializer()

    class Meta:
        model = Grupo
        fields = ('id', 'name', 'dono', 'membros')


class RecomendacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recomendacao
        fields = ('id', 'descricao')


class CadastroUsuariosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ('id', 'email', 'password', 'first_name', 'last_name')


class LocalDeInteresseSerializer(serializers.ModelSerializer):

    class Meta:
        model = LocalDeInteresse
        fields = ('id', 'nome', 'descricao', 'latitude', 'longitude', 'foto')


class DiarioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Diario
        fields = ('id', 'titulo')


class DetalheDiarioSerializer(serializers.ModelSerializer):
    locais_de_interesse = LocalDeInteresseSerializer(many=True, read_only=True)

    class Meta:
        model = Diario
        fields = ('id', 'titulo', 'locais_de_interesse')


class RelacionamentoSerializer(serializers.ModelSerializer):
    classificacao_id = serializers.IntegerField()

    class Meta:
        model = Relacionamento
        fields = ('classificacao_id',)