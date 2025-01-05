# # -*- coding: utf-8 -*-
{
    "name": "Viet education",
    "version": "1.0",
    "summary": "Development education with Viet Vu",
    "description": "Update fields for product",
    "category": "zen8labs/zen8labs",
    "author": "zen8labs",
    "website": "https://www.zen8labs.com",
    "depends": ["base", "z_web", "website", "web"],
    "data": [
        'wizard/dropout_school.xml',
        "views/education_class_group.xml",
        'views/education_student_views.xml',
        'views/student_level_views.xml',
        # 'views/education_subject_views.xml',
        'views/education_class_schedule_views.xml',
        'views/education_admission_report.xml',
        'views/education_class_views.xml',
        'views/education_student_todolist.xml',
        'views/education_school.xml',
        'views/menu.xml',
        "views/template.xml",  
        'data/sequence.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],
    "assets": {
        "web.assets_frontend": [
            # "/v_education/static/src/css/education_style.css",
            # "/v_education/static/src/css/education_style.scss",
            # "/v_education/static/src/js/education.js",
            # 'v_education/static/src/components/*/*.js',
            # 'v_education/static/src/components/*/*.xml',
            # 'v_education/static/src/components/*/*.scss',
        ],
        "web.assets_backend": [
            "v_education/static/src/components/todo_list.scss",
            "v_education/static/src/components/todo_list.js",
            "v_education/static/src/components/todo_list.xml",
        ],
    },

    "installable": True,
    "license": "LGPL-3",
}

