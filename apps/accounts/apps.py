from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = 'Аккаунты'

    def ready(self):
        """
        Подключение модуля signals
        :return:
        """
        import apps.accounts.signals

