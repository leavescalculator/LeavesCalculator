from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import gobeacc, goremal, gorsdav, nbrjobs, nbrjob, spriden, pebempl, phraccr, perleav, perefml, perfmla, perbfml, perjtot, ptearn, pdrdedn



@admin.register(gobeacc)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(goremal)
class ViewAdmin(ImportExportModelAdmin):
    pass


@admin.register(gorsdav)
class ViewAdmin(ImportExportModelAdmin):
    pass


@admin.register(nbrjob)
class ViewAdmin(ImportExportModelAdmin):
    pass


@admin.register(spriden)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(pebempl)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(phraccr)
class ViewAdmin(ImportExportModelAdmin):
    pass


@admin.register(perleav)
class ViewAdmin(ImportExportModelAdmin):
    pass


@admin.register(perefml)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(perfmla)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(perbfml)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(perjtot)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(ptearn)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(pdrdedn)
class ViewAdmin(ImportExportModelAdmin):
    pass


