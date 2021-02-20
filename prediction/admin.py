from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import * 
# Register your models here.
@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    pass

@admin.register(MLAlgorithm)
class MLAlgorithmAdmin(admin.ModelAdmin):
    pass

@admin.register(MLAlgorithmStatus)
class MLAlgorithmStatusAdmin(admin.ModelAdmin):
    pass

@admin.register(MLRequest)
class MLRequestAdmin(admin.ModelAdmin):
    pass

@admin.register(BehaviouralScores)
class BehaviouralScoresAdmin(admin.ModelAdmin):
    pass
@admin.register(ApplicationScores)
class ApplicationScoresAdmin(admin.ModelAdmin):
    pass

@admin.register(RetentionScores)
class RetentionScoresAdmin(admin.ModelAdmin):
    pass

@admin.register(ABTest)
class ABTestAdmin(admin.ModelAdmin):
    pass