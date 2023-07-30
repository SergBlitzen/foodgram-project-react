from rest_framework.response import Response
from rest_framework import status


# Функции создания и удаления объектов.
def create_instance(
        model, serializer, context, message, instance, objects
) -> Response:
    """
    Кастомная функция создания объекта связанной модели для
    существующего объекта исходной модели с учётом спецификации проекта.

    :param model: Модель объекта для создания.
    :param serializer: Сериализатор исходного объекта.
    :param context: Контекст сериализатора.
    :param str message: Сообщение об ошибке.
    :param str instance: Ключ от словаря objects, в котором
    хранится исходный объект вьюсета.
    :param dict objects: Исходные объекты для создания объекта
    связанной модели в виде словаря с ключами в виде названия
    полей связанной модели и значениями в виде объектов.
    :return Response: Респонс со статусом 201 или 400.
    """

    if model.objects.filter(**objects):
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        model.objects.create(**objects)
        serializer = serializer(objects[instance], context=context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_instance(model, message, objects) -> Response:
    """
    Кастомная функция удаления объекта связанной модели для
    существующего объекта исходной модели.

    :param model: Модель объекта для удаления.
    :param message: Сообщение об ошибке.
    :param objects: Объекты для получения объекта связанной модели.
    :return Response: Респонс со статусом 201 или 400.
    """

    if obj := model.objects.filter(**objects):
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
