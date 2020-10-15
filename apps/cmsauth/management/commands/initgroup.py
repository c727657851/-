from django.core.management.base import BaseCommand, CommandError
from apps.news.models import News,NewsCategory,Comment
from django.contrib.auth.models import Group,ContentType,Permission
class Command(BaseCommand):
    help = '创建分组并用来分配权限'

    def handle(self, *args, **options):
        # 编辑组
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Comment)
        ]
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)
        edit_group = Group.objects.create(name='编辑')
        edit_group.permissions.set(edit_permissions)
        edit_group.save()
        self.stdout.write(self.style.SUCCESS('编辑组创建完成'))

        #评论组
        comment_content_types = [
            ContentType.objects.get_for_model(Comment),
        ]
        comment_permissions = Permission.objects.filter(content_type__in=edit_content_types)
        comment_group = Group.objects.create(name='评论组')
        comment_group.permissions.set(comment_permissions)
        comment_group.save()
        self.stdout.write(self.style.SUCCESS('评论组创建完成'))

        # 管理员组
        admin_permissions = edit_permissions.union(comment_permissions)
        admin_group = Group.objects.create(name='管理员组')
        admin_group.permissions.set(admin_permissions)
        self.stdout.write(self.style.SUCCESS('管理员组创建完成'))