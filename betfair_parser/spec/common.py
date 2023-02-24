import msgspec


class BaseMessage(msgspec.Struct, kw_only=True, forbid_unknown_fields=True, frozen=True):
    def validate(self):
        return bool(msgspec.json.decode(msgspec.json.encode(self), type=type(self)))

    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}
