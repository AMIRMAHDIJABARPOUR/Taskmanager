from django.db.models.signals import post_save, pre_save


def task_befor_save(sender, instance, **kwargs):
    print(f" the {sender.__name__} that was {instance} was saved this befor save task")


def task_after_save(sender, instance, **kwargs):
    print(f" The{sender.__name__} that was  {instance} was saved this after save task")


