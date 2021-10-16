from rest_framework.serializers import ModelSerializer


def get_model_serializer_class(
        local_models,
        local_exclude: None | list = None,
        local_fields: str | list = "__all__",
        local_depth: int = 0
):
    """
    This method made for you typical ModelSerializer class.
    If you write param local_exclude, you don't need write param local_fields,
    because this param won't used.

    :param local_models: instance of models.Model
    :param local_fields: fields of model
    :param local_exclude: fields of model, which you want exclude
    :param local_depth: depth of serializer class
    :return: ModelSerializer
    """

    class CustomModelSerializer(ModelSerializer):
        class Meta:
            model = local_models
            if local_exclude:
                exclude = local_exclude
            else:
                fields = local_fields
            depth = local_depth
    return CustomModelSerializer
