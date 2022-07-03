from recogniser.utils import encode
from .utils import delete_imgs, get_imgs, save_embeddings, upload_img

from django.db import models

class Record(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    @property
    def images(self):
        return get_imgs(ref_no=self.id)

    def add_images(self, imgs=[]):
        for img in imgs:
            save_embeddings(
                ref_no=self.id,
                name=self.name,
                embeddings=[encode(img)[0]],
                image_uri=upload_img(img),
            )

    def delete(self, *args, **kwargs):
        ref_no = self.id
        res = super().delete(*args, **kwargs)
        delete_imgs(ref_no=ref_no)
        return res
