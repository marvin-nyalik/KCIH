from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', views.index, name='welcome'),
    path('', views.home, name='home'),
    path('login', views.login_render, name='login_render'),
    path('leader_login', views.leader_log, name='l_login_render'),
    path('my_admin', views.index, name = 'my_admin'),


    #Login & logout
    path('authentication', views.authenticate_user, name='authenticate'),
    path('logout', views.logout, name='logout'),

    #Registrations
    #registrations page rendering
    path('registrations/', views.render_home_register, name='render_home_register'),
    path('register*leader', views.render_leader_register, name='render_leader_register'),
    path('register*MP', views.render_MP_register, name='render_MP_register'),
    path('register*MCA', views.render_MCA_register, name='render_MCA_register'),
    path('register*ministry_officials', views.render_Min_Off_register, name='render_Min_Off_register'),
    path('register*union_officials', views.render_Union_Off_register, name='render_Union_Off_register'),

    #Actual registrations
    path('register_leader', views.register_leader, name='add_leader'),
    path('register_mp', views.register_MP, name='add_mp'),
    path('register_mca', views.register_MCA, name='add_mca'),
    path('register_min_off', views.register_Min_Off, name='add_min_off'),
    path('register_union_off', views.register_Union_Off, name='add_union_off'),

    #USER MANAGEMENT
    path('view_users', views.manage_home, name='view_users'),
    path('manage_leaders', views.manage_leaders, name='manage_leaders'),
    path('manage_leaders/<int:pk>/', views.reset_leader, name='reset_leader_pwd'),

    path('view_mps', views.manage_mps, name='view_mps'),
    path('manage_mps/<int:pk>/', views.reset_mp, name='reset_mp_pwd'),

    path('view_mcas', views.manage_mcas, name='view_mcas'),
    path('manage_mcas/<int:pk>/', views.reset_mca, name='reset_mca_pwd'),

    path('view_mins', views.manage_mins, name='view_mins'),
    path('manage_ministry/<int:pk>/', views.reset_ministry, name='reset_ministry_off_pwd'),

    path('view_unions', views.manage_unions, name='view_union'),
    path('manage_union/<int:pk>/', views.reset_union, name='reset_union_off_pwd'),


    #UPDATES
    path('render_leader_update', views.render_leader_update, name='render_leader_update'),
    path('create_leader_update/', views.create_update, name='create_leader_update'),
    path('view_my_leader_update/', views.my_leader_updates, name='view_leader_update'),


    path('render_mp_update', views.render_mp_update, name='render_mp_update'),
    path('create_mp_update/', views.create_MP_update, name='create_mp_update'),
    path('view_my_mp_update/', views.my_MP_updates, name='view_mp_update'),


    path('render_mca_update', views.render_mca_update, name='render_mca_update'),
    path('create_mca_update/', views.create_MCA_update, name='create_mca_update'),
    path('view_my_mca_update/', views.my_MCA_updates, name='view_mca_update'),

    path('render_ministry_update', views.render_ministry_update, name='render_ministry_update'),
    path('create_ministry_update/', views.create_MIN_update, name='create_ministry_update'),
    path('view_my_min_update/', views.my_Ministry_updates, name='view_ministry_update'),

    path('render_union_update', views.render_union_update, name='render_union_update'),
    path('create_union_update/', views.create_UNION_update, name='create_union_update'),
    path('view_my_union_update/', views.my_Union_updates, name='view_union_update'),


    #PROJECTS 
    path('render_leader_project', views.render_leader_project, name='render_leader_project'),
    path('create_leader_project/', views.create_leader_project, name='create_leader_project'),
    path('view_my_leader_project/', views.my_leader_projects, name='view_leader_project'),
    path('leader_update_proj/<int:pk>', views.lead_proj_update, name='leader_project_update'),
    path('project_update/<int:pk>', views.proj_update, name='update_project_final'),
    path('lead_proj_complete/<int:pk>', views.lead_proj_complete, name='lead_proj_complete'),


    path('render_mp_project', views.render_mp_project, name='render_mp_project'),
    path('create_mp_project/', views.create_mp_project, name='create_mp_project'),
    path('view_my_mp_project/', views.my_mp_projects, name='view_mp_project'),
    path('mp_update_proj/<int:pk>', views.MP_proj_update, name='mp_project_update'),
    path('mp_project_update/<int:pk>', views.MPproj_update, name='update_mp_project_final'),
    path('mp_proj_complete/<int:pk>', views.mp_proj_complete, name='mp_proj_complete'),

    path('render_mca_project', views.render_mca_project, name='render_mca_project'),
    path('create_mca_project/', views.create_mca_project, name='create_mca_project'),
    path('view_my_mca_project/', views.my_mca_projects, name='view_mca_project'),
    path('mca_update_proj/<int:pk>', views.MCA_proj_update, name='mca_project_update'),
    path('mca_project_update/<int:pk>', views.MCAproj_update, name='update_mca_project_final'),
    path('mca_proj_complete/<int:pk>', views.mca_proj_complete, name='mca_proj_complete'),

    path('render_ministry_project', views.render_ministry_project, name='render_ministry_project'),
    path('create_ministry_project/', views.create_ministry_project, name='create_ministry_project'),
    path('view_my_ministry_project/', views.my_ministry_projects, name='view_ministry_project'),
    path('ministry_update_proj/<int:pk>', views.MIN_proj_update, name='ministry_project_update'),
    path('ministry_project_update/<int:pk>', views.MINproj_update, name='update_ministry_project_final'),
    path('min_proj_complete/<int:pk>', views.min_proj_complete, name='min_proj_complete'),


    path('change_password', views.change_password, name='change_password'),
    path('password_change', views.render_password_change, name='render_change_password'),
    path('Lpassword_change', views.Lrender_password_change, name='Lrender_change_password'),
    path('Leader_change_password', views.Lchange_password, name='leader_change_password'),

    path('render_mp_pwd_change', views.render_mp_password_change, name='render_mp_pwd_change'),
    path('mp/change-password', views.MPchange_password, name='chage-pwd-MP'),


    path('render_mca_pwd_change', views.render_mca_password_change, name='render_mca_pwd_change'),
    path('mca/change-password', views.MCAchange_password, name='chage-pwd-MCA'),


    path('render_min_pwd_change', views.render_min_password_change, name='render_min_pwd_change'),
    path('min/change-password', views.MINchange_password, name='chage-pwd-MIN'),

    path('render_union_pwd_change', views.render_union_password_change, name='render_unino_pwd_change'),
    path('union/change-password', views.UNIONchange_password, name='chage-pwd-UNION'),


    #ARCHIVES
    path('archive', views.archive_home, name= 'archive_welcome'),

    path('archive_mp', views.archive_mp_render, name= 'archive_mp_render'),
    path('archive_mp/<int:pk>', views.archive_mp, name= 'archive_mp'),

    path('archive_leader', views.archive_leader_render, name= 'archive_leader_render'),
    path('archive_leader/<int:pk>', views.archive_leader, name= 'archive_leader'),

    path('archive_mca', views.archive_mca_render, name= 'archive_mca_render'),
    path('archive_mca/<int:pk>', views.archive_mca, name= 'archive_mca'),

    path('reports', views.report_home, name='reports_home'),
    path('leader_projects_report', views.leader_report, name='leader_projects'),

    #REPORTS
    path('render/leader_project_pdf/<int:pk>', views.Pdf.as_view(), name='leader_project_pdf'),
    path('render/mp_reports_pdf/<int:pk>', views.MpPdf.as_view(), name='mp_project_pdf'),
    path('render/mca_reports_pdf/<int:pk>', views.McaPdf.as_view(), name='mca_project_pdf'),
    path('render/min_reports_pdf/<int:pk>', views.MinPdf.as_view(), name='min_project_pdf'),
    path('render/all_reports_pdf', views.ProjectsPdf.as_view(), name='all_projects'),
    path('render/all_updates_reports_pdf', views.UpdatesPdf.as_view(), name='all_updates'),



    #PUBLIC PAGES
    path('public/leaders', views.public_leader, name='public_leader'),
    path('public/ministries', views.public_ministry, name='public_ministry'),
    path('public/', views.public_unions, name='public_unions'),

    #PUBLIC DETAIL PAGES
    path('leader_updates/<int:pk>', views.county_updates, name='leader_details'),
    path('extras/<int:pk>', views.county_ext, name='extra_updates'),

    path('mp_updates/<int:pk>', views.mp_updates, name='mp_leader_details'),
    path('mp_extras/<int:pk>', views.mp_ext, name='mp_extra_updates'),

    path('mca_updates/<int:pk>', views.mca_updates, name='mca_leader_details'),
    path('mca_extras/<int:pk>', views.mca_ext, name='mca_extra_updates'),

    path('min_updates/<int:pk>', views.min_updates, name='min_leader_details'),
    path('min_extras/<int:pk>', views.min_ext, name='min_extra_updates'),

    path('uni_updates/<int:pk>', views.uni_updates, name='uni_leader_details'),
    path('uni_extras/<int:pk>', views.uni_ext, name='uni_extra_updates'),

    #PUBLIC PROJECT PAGES
    path('leader_projects/<int:pk>', views.county_proj, name='leader_projects'),
    path('project_extras/<int:pk>', views.county_ext_proj, name='extra_projects'),

    path('mp_projects/<int:pk>', views.mp_proj, name='mp_projects'),
    path('mp_project_extras/<int:pk>', views.mp_ext_proj, name='mp_extra_projects'),

    path('mca_projects/<int:pk>', views.mca_proj, name='mca_projects'),
    path('mca_project_extras/<int:pk>', views.mca_ext_proj, name='mca_extra_projects'),

    path('min_projects/<int:pk>', views.min_proj, name='min_projects'),
    path('min_project_extras/<int:pk>', views.min_ext_proj, name='min_extra_projects'),


  

]
if settings.DEBUG:
    urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)