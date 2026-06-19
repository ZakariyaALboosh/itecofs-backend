import json

from rest_framework import serializers

from .models import ContactForm, HomepageStats, News, NewsImage, Project, ProjectImage, Service


class HomepageStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomepageStats
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'




class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = ['id', 'name', 'email', 'phone_number', 'service', 'description', 'created_at']
        read_only_fields = ['created_at']


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['id', 'image', 'order']


class NewsSerializer(serializers.ModelSerializer):
    images = NewsImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = News
        fields = [
            'id', 'title', 'content', 'is_hidden', 'author',
            'created_at', 'updated_at', 'images', 'uploaded_images'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        news = News.objects.create(**validated_data)
        for index, image in enumerate(uploaded_images):
            NewsImage.objects.create(news=news, image=image, order=index)
        return news

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if uploaded_images is not None:
            instance.images.all().delete()
            for index, image in enumerate(uploaded_images):
                NewsImage.objects.create(news=instance, image=image, order=index)
        return instance


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'order']


class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'status', 'client', 'scope',
            'execution', 'outcome', 'images', 'uploaded_images'
        ]

    def validate_execution(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError as exc:
                raise serializers.ValidationError('execution must be valid JSON list.') from exc

        if not isinstance(value, list):
            raise serializers.ValidationError('execution must be a list.')
        return value

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        project = Project.objects.create(**validated_data)
        for index, image in enumerate(uploaded_images):
            ProjectImage.objects.create(project=project, image=image, order=index)
        return project

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if uploaded_images is not None:
            instance.images.all().delete()
            for index, image in enumerate(uploaded_images):
                ProjectImage.objects.create(project=instance, image=image, order=index)
        return instance
