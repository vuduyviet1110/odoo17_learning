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
        'views/education_class_views.xml',
        'views/education_school.xml',
        'views/menu.xml',
        "views/template.xml",  
        'data/sequence.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],
    "assets": {
        "web.assets_frontend": [
            "/v_education/static/src/css/education_style.css",
            "/v_education/static/src/css/education_style.scss",
            "/v_education/static/src/js/education.js",
        ],
    },

    "installable": True,
    "license": "LGPL-3",
}

