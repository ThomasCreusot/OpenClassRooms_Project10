from django.contrib import admin
from IssueTracking_app.models import Contributor, Project, Issue, Comment, Contributor

class ProjectAdmin(admin.ModelAdmin):

    list_display = ('title',)


class IssueAdmin(admin.ModelAdmin):

    list_display = ('title', 'tag', 'priority', 'status')


class CommentAdmin(admin.ModelAdmin):

    list_display = ('description',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)

admin.site.register(Contributor)
