from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save


class CourseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


# Manager Model
class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()

    def get_related(self, instance):
        course_one = self.get_queryset().filter(categories__in=instance.categories.all())
        course_two = self.get_queryset().filter(default=instance.default)
        qs = (course_one | course_two).exclude(id=instance.id).distinct()

        return qs


# Course Details

class MainCategory(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Category(models.Model):
    category = models.ForeignKey(MainCategory)
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    default = models.ForeignKey('MainCategory', related_name='default_main_category', null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def get_image_url(self):
        cat_img = self.categoryimage_set.first()
        if cat_img:
            return cat_img.image.url
        return cat_img


class Course_detail(models.Model):
    Main_Category = models.ForeignKey('MainCategory', blank=True)
    categories = models.ManyToManyField('Category', blank=True)
    default = models.ForeignKey('Category', related_name='default_category', null=True, blank=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True)
    sub_title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    actual_price = models.DecimalField(null=True, decimal_places=2, max_digits=6)
    sale_price = models.DecimalField(null=True, decimal_places=2, max_digits=6)
    discount = models.PositiveIntegerField(null=True)
    review = models.BooleanField(default=True)
    url = models.URLField(blank=True, max_length=200)
    course_provider = models.CharField(max_length=50, blank=True)
    active = models.BooleanField(default=True)

    objects = CourseManager()

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(Course_detail, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-title"]

    def get_absolute_url(self):
        return reverse("single-product", kwargs={"slug": self.slug, "pk": self.pk})

    def get_image_url(self):
        img = self.courseimage_set.first()
        if img:
            return img.image.url
        return img


# Course Images
class CourseImage(models.Model):
    course = models.ForeignKey(Course_detail)
    image = models.ImageField(upload_to='media_root/')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    def __str__(self):
        return self.course.title


class CategoryImage(models.Model):
    category_image = models.ForeignKey(Category)
    image = models.ImageField(upload_to='media_root/')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    def __str__(self):
        return self.category_image.title
