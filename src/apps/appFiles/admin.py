from django.contrib import admin
from django import forms
from .models import File


class FileAdminForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('local_url',)

    def save(self, commit=True):
        file_instance = super().save(commit=False)

        if 'local_url' in self.changed_data:
            file = self.cleaned_data['local_url']
            extension = file.name.split('.')[-1]

            uploaded_file = File.upload(self.user.id, file, extension,False)
            file_instance.directory = uploaded_file.directory
            file_instance.url_to_upload = uploaded_file.url_to_upload

        return file_instance


class FileAdmin(admin.ModelAdmin):
    form = FileAdminForm
    list_display = ('directory', 'local_url', 'url_to_upload')

    def save_form(self, request, form, change):
        form.user = request.user  # Передаем текущего пользователя в форму
        return super().save_form(request, form, change)


admin.site.register(File, FileAdmin)
