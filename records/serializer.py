from rest_framework import serializers

from records.utils import find_data

from .models import Record
from recogniser.utils import encode

class FindImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, img):
        embeddings = encode(img)
        if len(embeddings) > 1:
            raise serializers.ValidationError("More than one face detected in image")
        
        return list(embeddings[0])
    
    def validate(self, attrs):
        embedding = attrs["image"]
        data = find_data(embedding)
        data = map(lambda el: {**el, **el["_id"]}, data)
        return list(data)

class RecordSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Record
        fields = ["name", "mobile", "image"]

    def create(self, validated_data):
        img = validated_data.pop("image")
        record = super().create(validated_data)
        record.add_images([img])
        return record


