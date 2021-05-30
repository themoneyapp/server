from pydantic import BaseConfig as PydanticBaseConfig
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Extra


class BaseConfig(PydanticBaseConfig):
    allow_mutation = False
    case_sensitive = True
    extra = Extra.forbid
    use_enum_values = True


class BaseModel(PydanticBaseModel):
    class Config(BaseConfig):
        pass
