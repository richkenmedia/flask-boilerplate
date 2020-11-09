# flask-boilerplate

1. Install All packages in requirements.txt file -> pip install -r requirements.txt
2. Rename local.env to env
3. To Run -> flask run
4. Database
   -> for migrate - flask db upgrade (this will add changes in migration folder)
5. If migration folder is not exist in this prject then do the following steps
   -> flask db init
   -> flask db migrate -m "Migration Message"
   -> flask db upgrade

6. Role Permission seeder run - python manage.py seeder
