import msgspec


class BaseMessage(msgspec.Struct, kw_only=True, forbid_unknown_fields=True, frozen=True):
    def validate(self):
        return bool(msgspec.json.decode(msgspec.json.encode(self), type=type(self)))
