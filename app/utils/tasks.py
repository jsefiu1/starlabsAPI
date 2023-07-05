from fastapi_amis_admin.admin.site import AdminSite
from app.utils.database import admin_site_settings
from fastapi_scheduler import SchedulerAdmin


site = AdminSite(settings=admin_site_settings)
scheduler = SchedulerAdmin.bind(site)
