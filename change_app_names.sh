## Change selia_annotator name

# Change app label in content type table
python manage.py dbshell "-c UPDATE django_content_type SET app_label='irekua_annotators' WHERE app_label='selia_annotator'"

# Change model table names
python manage.py dbshell "-c ALTER TABLE selia_annotator_annotationtoolcomponent RENAME TO irekua_annotators_annotationtoolcomponent"
python manage.py dbshell "-c ALTER TABLE selia_annotator_annotationannotator RENAME TO irekua_annotators_annotationannotator"
python manage.py dbshell "-c ALTER TABLE selia_annotator_annotator RENAME TO irekua_annotators_annotator"
python manage.py dbshell "-c ALTER TABLE selia_annotator_annotatormodule RENAME TO irekua_annotators_annotatormodule"
python manage.py dbshell "-c ALTER TABLE selia_annotator_annotatorversion RENAME TO irekua_annotators_annotatorversion"

# Update migrations
python manage.py dbshell "-c UPDATE django_migrations SET app='irekua_annotators' WHERE app='selia_annotator'"

## Change selia_visualizers name

# Change app label in content type table
python manage.py dbshell "-c UPDATE django_content_type SET app_label='irekua_visualizers' WHERE app_label='selia_visualizers'"

# Change model table names
python manage.py dbshell "-c ALTER TABLE selia_visualizers_visualizercomponent RENAME TO irekua_visualizers_visualizercomponent"
python manage.py dbshell "-c ALTER TABLE selia_visualizers_visualizercomponentitemtype RENAME TO irekua_visualizers_visualizercomponentitemtype"
python manage.py dbshell "-c ALTER TABLE selia_visualizers_annotationvisualizer RENAME TO irekua_visualizers_annotationvisualizer"
python manage.py dbshell "-c ALTER TABLE selia_visualizers_visualizer RENAME TO irekua_visualizers_visualizer"
python manage.py dbshell "-c ALTER TABLE selia_visualizers_visualizeritemtype RENAME TO irekua_visualizers_visualizeritemtype"
python manage.py dbshell "-c ALTER TABLE selia_visualizers_visualizermodule RENAME TO irekua_visualizers_visualizermodule"
python manage.py dbshell "-c ALTER TABLE selia_visualizers_visualizerversion RENAME TO irekua_visualizers_visualizerversion"

# Update migrations
python manage.py dbshell "-c UPDATE django_migrations SET app='irekua_visualizers' WHERE app='selia_visualizers'"
