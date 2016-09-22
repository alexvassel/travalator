import factory


class BaseUserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user-{0}'.format(n))
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')


class UserFactory(BaseUserFactory):
    class Meta:
        model = 'users.User'
        django_get_or_create = ('username', )


class CompanyFactory(BaseUserFactory):
    class Meta:
        model = 'users.Company'
        django_get_or_create = ('username', )


class TouristFactory(BaseUserFactory):
    class Meta:
        model = 'users.Tourist'
        django_get_or_create = ('username', )
