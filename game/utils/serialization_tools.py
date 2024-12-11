import importlib

from game.utils.enums import TypeData


def get_entity(data):
    cls = get_entity_type(data)

    # Проверяем, есть ли метод from_dict
    if hasattr(cls, "from_dict"):
        return cls.from_dict(data)
    else:
        raise ValueError(f"Class '{cls.__class__.__name__}' does not implement 'from_dict' method")

def get_entity_type(data):
    # Получаем полное имя класса
    type_name = data.get(TypeData.TYPE.value)
    if not type_name:
        raise ValueError("Field 'type' is missing in the data")

    # Разделяем на модуль и класс
    module_name, class_name = type_name.rsplit(".", 1)
    try:
        # Импортируем модуль
        module = importlib.import_module(module_name)
        # Получаем класс
        cls = getattr(module, class_name)
    except (ModuleNotFoundError, AttributeError) as e:
        raise ValueError(f"Error loading class '{type_name}': {e}")

    return cls
