# apps/accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentification
    path('login/',           views.UserLoginView.as_view(),        name='login'),
    path('register/',        views.UserRegisterView.as_view(),     name='register'),
    path('logout/',          views.UserLogoutView.as_view(),       name='logout'),

    # Réinitialisation de mot de passe
    path('password-reset/',           views.CustomPasswordResetView.as_view(),      name='password_reset'),
    path('password-reset/done/',      views.CustomPasswordResetDoneView.as_view(),  name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/',  views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # CRUD Employés
    path('employees/',        views.EmployeeListView.as_view(),      name='employee_list'),
    path('employees/add/',    views.EmployeeCreateView.as_view(),    name='employee_add'),
    path('employees/<int:pk>/',     views.EmployeeDetailView.as_view(),    name='employee_detail'),
    path('employees/<int:pk>/edit/',views.EmployeeUpdateView.as_view(),    name='employee_edit'),
    path('employees/<int:pk>/delete/',views.EmployeeDeleteView.as_view(),    name='employee_delete'),

    # CRUD Fournisseurs
    path('suppliers/',        views.SupplierListView.as_view(),      name='supplier_list'),
    path('suppliers/add/',    views.SupplierCreateView.as_view(),    name='supplier_add'),
    path('suppliers/<int:pk>/',     views.SupplierDetailView.as_view(),    name='supplier_detail'),
    path('suppliers/<int:pk>/edit/',views.SupplierUpdateView.as_view(),    name='supplier_edit'),
    path('suppliers/<int:pk>/delete/',views.SupplierDeleteView.as_view(),  name='supplier_delete'),

    # CRUD Catégories
    path('categories/',       views.CategoryListView.as_view(),      name='category_list'),
    path('categories/add/',   views.CategoryCreateView.as_view(),    name='category_add'),
    path('categories/<int:pk>/',    views.CategoryDetailView.as_view(),    name='category_detail'),
    path('categories/<int:pk>/edit/',views.CategoryUpdateView.as_view(),    name='category_edit'),
    path('categories/<int:pk>/delete/',views.CategoryDeleteView.as_view(),  name='category_delete'),

    # CRUD Produits
    path('products/',         views.ProductListView.as_view(),       name='product_list'),
    path('products/add/',     views.ProductCreateView.as_view(),     name='product_add'),
    path('products/<int:pk>/',     views.ProductDetailView.as_view(),     name='product_detail'),
    path('products/<int:pk>/edit/',views.ProductUpdateView.as_view(),     name='product_edit'),
    path('products/<int:pk>/delete/',views.ProductDeleteView.as_view(),     name='product_delete'),

    # Ventes
    path('sales/',            views.SaleListView.as_view(),          name='sale_list'),
    path('sales/bulk-delete/',views.SaleBulkDeleteView.as_view(),     name='sale_bulk_delete'),
    path('sales/add/',        views.sale_create,                     name='sale_create'),
    path('sales/<int:pk>/',   views.SaleDetailView.as_view(),        name='sale_detail'),
    path('sales/<int:pk>/edit/',views.sale_update,                   name='sale_update'),
    path('sales/<int:pk>/delete/',views.SaleDeleteView.as_view(),    name='sale_delete'),
    path('sales/<int:pk>/json/',views.sale_detail_json,               name='sale_detail_json'),

    #export ventes
    path('sales/export/pdf/', views.export_sales_pdf, name='export_pdf'),
    path('sales/export/excel/', views.export_sales_excel, name='export_excel'),
    path('sales/export/word/', views.export_sales_word, name='export_word'),
    path('sales/export/csv/', views.export_sales_csv, name='export_csv'),

    #export employés
    path('employees/export/pdf/', views.export_employees_pdf, name='export_employees_pdf'),
    path('employees/export/excel/', views.export_employees_excel, name='export_employees_excel'),
    path('employees/export/word/', views.export_employees_word, name='export_employees_word'),
    path('employees/export/csv/', views.export_employees_csv, name='export_employees_csv'),

    # Produits
    path('products/export/pdf/', views.export_products_pdf, name='export_products_pdf'),
    path('products/export/excel/', views.export_products_excel, name='export_products_excel'),
    path('products/export/word/', views.export_products_word, name='export_products_word'),
    path('products/export/csv/', views.export_products_csv, name='export_products_csv'),

    #fournisseurs
    path('suppliers/export/pdf/', views.export_suppliers_pdf,   name='export_suppliers_pdf'),
    path('suppliers/export/excel/', views.export_suppliers_excel, name='export_suppliers_excel'),
    path('suppliers/export/word/', views.export_suppliers_word,  name='export_suppliers_word'),
    path('suppliers/export/csv/',  views.export_suppliers_csv,   name='export_suppliers_csv'),

    #categories
    path('categories/export/pdf/',   views.export_categories_pdf,   name='export_categories_pdf'),
    path('categories/export/excel/', views.export_categories_excel, name='export_categories_excel'),
    path('categories/export/word/',  views.export_categories_word,  name='export_categories_word'),
    path('categories/export/csv/',   views.export_categories_csv,   name='export_categories_csv'),

    # Rapports Ventes
    path("reports/sales/pdf/",   views.export_sales_report_pdf,   name="export_sales_report_pdf"),
    path("reports/sales/excel/", views.export_sales_report_excel, name="export_sales_report_excel"),
    path("reports/sales/docx/", views.export_sales_report_docx, name="export_sales_report_docx"),
    path("reports/sales/csv/",   views.export_sales_report_csv,   name="export_sales_report_csv"),
    # Rapports Stocks
    path("reports/stock/pdf/",   views.export_stock_report_pdf,   name="export_stock_report_pdf"),
    path("reports/stock/excel/", views.export_stock_report_excel, name="export_stock_report_excel"),
    path("reports/stock/csv/",   views.export_stock_report_csv,   name="export_stock_report_csv"),
    path("reports/stock/docx/", views.export_stock_report_docx, name="export_stock_report_docx"),

]
