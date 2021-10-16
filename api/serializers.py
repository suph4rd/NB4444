from rest_framework.serializers import ModelSerializer


def get_model_serializer(local_models, local_fields: str | list = "__all__", local_exclude: None | list = None):
    class CustomModelSerializer(ModelSerializer):
        class Meta:
            model = local_models
            if local_exclude:
                exclude = local_exclude
            else:
                fields = local_fields
    return CustomModelSerializer

