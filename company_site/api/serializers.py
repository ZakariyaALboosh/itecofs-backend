import json

from rest_framework import serializers

from .models import ContactForm, HomepageStats, News, NewsImage, Project, ProjectImage, Service, SupplierRegistration


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


class SupplierRegistrationSerializer(serializers.ModelSerializer):
    vendorName = serializers.CharField(source='vendor_name')
    crNumber = serializers.CharField(source='cr_number')
    estYear = serializers.CharField(source='est_year')
    supplierType = serializers.JSONField(source='supplier_type')
    hqAddress = serializers.CharField(source='hq_address')
    operatesLibya = serializers.CharField(source='operates_libya')
    crCertificate = serializers.FileField(source='cr_certificate')
    orgChart = serializers.FileField(source='organisation_chart')
    companyProfile = serializers.FileField(source='company_profile')
    fpName = serializers.CharField(source='fp_name')
    fpPosition = serializers.CharField(source='fp_position')
    fpPhone = serializers.CharField(source='fp_phone')
    fpEmail = serializers.EmailField(source='fp_email')
    taxRegistrationCertificate = serializers.FileField(source='tax_registration_certificate')
    vatRegistrationCertificate = serializers.FileField(source='vat_registration_certificate', required=False, allow_null=True)
    bankName = serializers.CharField(source='bank_name')
    accountName = serializers.CharField(source='account_name')
    branchName = serializers.CharField(source='branch_name')
    branchAddress = serializers.CharField(source='branch_address')
    registrationType = serializers.JSONField(source='registration_type')
    productTypes = serializers.CharField(source='product_types')
    warrantyTerms = serializers.CharField(source='warranty_terms')
    supportInfo = serializers.CharField(source='support_info')
    iso9001Certificate = serializers.FileField(source='iso9001_certificate', required=False, allow_null=True)
    iso14001Certificate = serializers.FileField(source='iso14001_certificate', required=False, allow_null=True)
    iso45001Certificate = serializers.FileField(source='iso45001_certificate', required=False, allow_null=True)
    apiq1Certificate = serializers.FileField(source='apiq1_certificate', required=False, allow_null=True)
    apiq2Certificate = serializers.FileField(source='apiq2_certificate', required=False, allow_null=True)
    leadTime = serializers.CharField(source='lead_time')
    exportPorts = serializers.CharField(source='export_ports')
    logisticsAddress = serializers.CharField(source='logistics_address')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = SupplierRegistration
        fields = [
            'id', 'vendorName', 'country', 'crNumber', 'estYear', 'supplierType',
            'hqAddress', 'operatesLibya', 'crCertificate', 'orgChart', 'companyProfile',
            'fpName', 'fpPosition', 'fpPhone', 'fpEmail', 'taxRegistrationCertificate',
            'vatRegistrationCertificate', 'bankName', 'accountName', 'iban', 'swift',
            'branchName', 'branchAddress', 'currency', 'registrationType', 'productTypes',
            'warrantyTerms', 'supportInfo', 'certs', 'iso9001Certificate',
            'iso14001Certificate', 'iso45001Certificate', 'apiq1Certificate',
            'apiq2Certificate', 'leadTime', 'exportPorts', 'logisticsAddress',
            'accepted', 'representative', 'position', 'email', 'createdAt',
        ]
        read_only_fields = ['createdAt']

    def validate_supplierType(self, value):
        return self._validate_json_list(value, 'supplierType')

    def validate_registrationType(self, value):
        return self._validate_json_list(value, 'registrationType')

    def validate_certs(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError as exc:
                raise serializers.ValidationError('certs must be valid JSON object.') from exc
        if not isinstance(value, dict):
            raise serializers.ValidationError('certs must be an object.')
        return value

    def validate_accepted(self, value):
        if value is not True:
            raise serializers.ValidationError('Declaration must be accepted before submission.')
        return value

    def _validate_json_list(self, value, field_name):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError as exc:
                raise serializers.ValidationError(f'{field_name} must be valid JSON list.') from exc
        if not isinstance(value, list):
            raise serializers.ValidationError(f'{field_name} must be a list.')
        return value
