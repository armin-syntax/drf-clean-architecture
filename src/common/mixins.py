class SerializerMixin:
    serializer_class = None

    def get_serializer(self, *args, **kwargs):
        if self.serializer_class is None:
            raise ValueError("serializer_class must be set")
        return self.serializer_class(*args, **kwargs)
