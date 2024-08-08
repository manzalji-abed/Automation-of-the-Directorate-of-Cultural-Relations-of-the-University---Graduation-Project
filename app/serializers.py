from rest_framework import serializers
from .models import *


class SerializerUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SerializerUserSynchronization(serializers.ModelSerializer):
    class Meta:
        model = UserSynchronization
        fields = '__all__'


class SerializerDeletedObjects(serializers.ModelSerializer):
    class Meta:
        model = DeletedObjects
        fields = '__all__'


class SerializerPermissions(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'


class SerializerReport(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class SerializerRegularization(serializers.ModelSerializer):
    class Meta:
        model = Regularization
        fields = '__all__'


class SerializerExtension(serializers.ModelSerializer):
    class Meta:
        model = Extension
        fields = '__all__'


class SerializerFreeze(serializers.ModelSerializer):
    class Meta:
        model = Freeze
        fields = '__all__'


class SerializerDurationChange(serializers.ModelSerializer):
    class Meta:
        model = DurationChange
        fields = '__all__'


class SerializerAlimonyChange(serializers.ModelSerializer):
    class Meta:
        model = AlimonyChange
        fields = '__all__'


class SerializerUniversityChange(serializers.ModelSerializer):
    class Meta:
        model = UniversityChange
        fields = '__all__'


class SerializerSpecializationChange(serializers.ModelSerializer):
    class Meta:
        model = SpecializationChange
        fields = '__all__'


class SerializerDispatch(serializers.ModelSerializer):
    report= SerializerReport(many=True)
    regularization= SerializerRegularization()
    extension= SerializerExtension(many=True)
    freeze= SerializerFreeze(many=True)
    durationChange= SerializerDurationChange(many=True)
    alimonyChange= SerializerAlimonyChange(many=True)
    universityChange= SerializerUniversityChange(many=True)
    specializationChange= SerializerSpecializationChange(many=True)
    
    class Meta:
        model = Dispatch
        fields = '__all__'


class SerializerDispatchSingle(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        fields = '__all__'


class SerializerGraduateStudies(serializers.ModelSerializer):
    class Meta:
        model = GraduateStudies
        fields = '__all__'


class SerializerCertificateOfExcellence(serializers.ModelSerializer):
    class Meta:
        model = CertificateOfExcellence
        fields = '__all__'


class SerializerAdjectiveChange(serializers.ModelSerializer):
    class Meta:
        model = AdjectiveChange
        fields = '__all__'


class SerializerNomination(serializers.ModelSerializer):
    class Meta:
        model = Nomination
        fields = '__all__'


class SerializerUniversityDegree(serializers.ModelSerializer):
    class Meta:
        model = UniversityDegree
        fields = '__all__'


class SerializerDemonstrator(serializers.ModelSerializer):
    universityDegree = SerializerUniversityDegree()
    nominationDecision= SerializerNomination()
    adjectiveChange= SerializerAdjectiveChange(many=True)
    certificateOfExcellence= SerializerCertificateOfExcellence(many=True)
    graduateStudies= SerializerGraduateStudies(many=True)
    dispatch = SerializerDispatch( many=True)

    class Meta:
        model = Demonstrator
        fields = '__all__'


class SerializerDemonstratorSingle(serializers.ModelSerializer):
    class Meta:
        model = Demonstrator
        fields = '__all__'