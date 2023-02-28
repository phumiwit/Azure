from django.contrib import admin
from myapp.models import Userdata,Audio,Collection,File,Valueforchart
# Register your models here.

class UserDataAdmin(admin.ModelAdmin):
    list_display=["UserName","FirstName","LastName","age","email","date"]
    
    
class AudioAdmin(admin.ModelAdmin):
    list_display=["UserName","Filename","Genre","top3_genre","Value"]
    
class CollectionAdmin(admin.ModelAdmin):
    list_display=["UserName","filename","genre","top3_genre","audio_id","collectionname"]
    
class FileAdmin(admin.ModelAdmin):
    list_display=["UserName","filename","fileurl"]

class ValueforchartAdmin(admin.ModelAdmin):
    list_display=["genre","age"]
    
admin.site.register(Userdata,UserDataAdmin)
admin.site.register(Audio,AudioAdmin)
admin.site.register(Collection,CollectionAdmin)
admin.site.register(File,FileAdmin)
admin.site.register(Valueforchart,ValueforchartAdmin)

 