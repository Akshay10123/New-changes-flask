from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField,SelectMultipleField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fgfdfdgdfgfdgfdgdfgfdgfdg'


# Step 1 Form (Product Information)
class ProductInfoForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()], default="")
    version = StringField('Version (Optional)', default="")
    launch_date = DateField('Launch Date', default=datetime.today().date(), format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Active', 'Active'), ('In development', 'In development')], validators=[DataRequired()])
    product_properties = SelectMultipleField('Product Properties', choices=[('AI', 'AI'), ('GUI', 'GUI'), ('Personal Information', 'Personal Information')], 
                                             validators=[DataRequired()], default=['AI','GUI','Personal Information'])  # Initialize with an empty list
    retirement_date = DateField('Retirement Date', default="9999-12-31", format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField('Description', default="")
    risks = TextAreaField('Risks (Optional)', default="")
    additional_properties = TextAreaField('Additional Properties (Optional)', default="")
    documentation_url = StringField('Product Documentation URL (Optional)', default="")
    repository_url = StringField('Repository URL (Optional)', default="")
    metrics_dashboard = StringField('Metrics Dashboard (Optional)', default="")

    # Business value sliders (can be added as range inputs directly in the HTML)
    decision_making = StringField('Decision Making (0-10)', default=0)
    monetization = StringField('Monetization (0-10)', default=0)
    time_savings = StringField('Time Savings (0-10)', default=0)
    reporting = StringField('Reporting (0-10)', default=0)
    processes = StringField('Processes (0-10)', default=0)
    collaboration = StringField('Collaboration (0-10)', default=0)
    documentation_audits = StringField('Documentation Audits (0-10)', default=0)
    
    product_owner_name = StringField('Product Owner Name', validators=[DataRequired()], default="")
    product_owner_zid = StringField('Product Owner ZID', validators=[DataRequired()], default="")
    product_owner_email = StringField('Product Owner Email', validators=[DataRequired()], default="")
    product_owner_type = SelectField('Product Owner Type', choices=[('Owner', 'Owner')], validators=[DataRequired()])
    valid_from_date = DateField('Valid From Date', default=datetime.today().date(), format='%Y-%m-%d', validators=[DataRequired()])
    valid_to_date = DateField('Valid To Date', default="9999-12-31", format='%Y-%m-%d', validators=[DataRequired()])


# Step 2 Form (Product Owner)
class ProductOwnerForm(FlaskForm):
    owner_name = StringField('Product Owner Name', validators=[DataRequired()])
    owner_zid = StringField('Product Owner ZID', validators=[DataRequired()])
    owner_email = StringField('Product Owner Email ID', validators=[DataRequired()])
    owner_type = SelectField('Product Owner Type', choices=[('Member', 'Member'), ('Owner', 'Owner')], validators=[DataRequired()])
    valid_from = DateField('Valid From', default=datetime.today().date(), format='%Y-%m-%d')
    valid_to = DateField('Valid To', default=datetime(9999, 12, 31).date(), format='%Y-%m-%d')


# Step 3 Form (Business Owner)
class BusinessOwnerForm(FlaskForm):
    contact_name = StringField('Business Contact Name', validators=[DataRequired()])
    contact_zid = StringField('Business Contact ZID', validators=[DataRequired()])
    contact_email = StringField('Business Contact Email ID', validators=[DataRequired()])
    contact_type = SelectField('Business Contact Type', choices=[('Member', 'Member'), ('Owner', 'Owner')], validators=[DataRequired()])
    valid_from = DateField('Valid From', default=datetime.today().date(), format='%Y-%m-%d')
    valid_to = DateField('Valid To', default=datetime(9999, 12, 31).date(), format='%Y-%m-%d')


# Step 4 Form (Snowflake Database)
class SnowflakeDatabaseForm(FlaskForm):
    database_name = StringField('Database Name', validators=[DataRequired()])
    schema_name = StringField('Schema Name', validators=[DataRequired()])
    table_name = StringField('Table Name', validators=[DataRequired()])
    data_type = SelectField('Data Type', choices=[('Source', 'Source'), ('Output', 'Output'), ('Source and Output', 'Source and Output')], validators=[DataRequired()])
    valid_from = DateField('Valid From', default=datetime.today().date(), format='%Y-%m-%d')
    valid_to = DateField('Valid To', default=datetime(9999, 12, 31).date(), format='%Y-%m-%d')


# Step 5 Form (Other Data Sources)
class OtherDataSourceForm(FlaskForm):
    dataset_name = StringField('Dataset Name', validators=[DataRequired()])
    dataset_description = StringField('Dataset Description', validators=[DataRequired()])
    data_set_type = SelectField('Data Set Type', choices=[('Source', 'Source'), ('Output', 'Output'), ('Source and Output', 'Source and Output')], validators=[DataRequired()])
    valid_from = DateField('Valid From', default=datetime.today().date(), format='%Y-%m-%d')
    valid_to = DateField('Valid To', default=datetime(9999, 12, 31).date(), format='%Y-%m-%d')


# Step 6 Form (Platforms)
class PlatformForm(FlaskForm):
    platform_name = StringField('Platform Name', validators=[DataRequired()])
    platform_description = StringField('Platform Description', validators=[DataRequired()])
    valid_from = DateField('Valid From', default=datetime.today().date(), format='%Y-%m-%d')
    valid_to = DateField('Valid To', default=datetime(9999, 12, 31).date(), format='%Y-%m-%d')

@app.route('/', methods=['GET', 'POST'])
def step1():
    form = ProductInfoForm()
    if form.validate_on_submit():  # Check if form is submitted
        print("Form submitted successfully!")  # Debugging line
        # Process and save data here (optional, depends on your app logic)
        return redirect(url_for('step2'))  # Redirect to Step 2
    else:
        print("Form validation failed")  # Debugging line
    return render_template('step1.html', form=form)

@app.route('/step2', methods=['GET', 'POST'])
def step2():
    form = ProductOwnerForm()
    form_count = 0
    if request.method == 'POST':
        if 'add' in request.form:
            form_count += 1
        elif 'save' in request.form:
            return redirect(url_for('step3'))  # Move to Step 3
        elif 'skip' in request.form:
            return redirect(url_for('step3'))  # Skip to Step 3
    
    return render_template('step2.html', form=form, form_count=form_count)


@app.route('/step3', methods=['GET', 'POST'])
def step3():
    form = BusinessOwnerForm()
    form_count = 0
    if request.method == 'POST':
        if 'add' in request.form:
            form_count += 1
        elif 'save' in request.form:
            return redirect(url_for('step4'))  # Move to Step 4
        elif 'skip' in request.form:
            return redirect(url_for('step4'))  # Skip to Step 4
    
    return render_template('step3.html', form=form, form_count=form_count)


@app.route('/step4', methods=['GET', 'POST'])
def step4():
    form = SnowflakeDatabaseForm()
    form_count = 0
    if request.method == 'POST':
        if 'add' in request.form:
            form_count += 1
        elif 'save' in request.form:
            return redirect(url_for('step5'))  # Move to Step 5
        elif 'skip' in request.form:
            return redirect(url_for('step5'))  # Skip to Step 5
    
    return render_template('step4.html', form=form, form_count=form_count)


@app.route('/step5', methods=['GET', 'POST'])
def step5():
    form = OtherDataSourceForm()
    form_count = 0
    if request.method == 'POST':
        if 'add' in request.form:
            form_count += 1
        elif 'save' in request.form:
            return redirect(url_for('step6'))  # Move to Step 6
        elif 'skip' in request.form:
            return redirect(url_for('step6'))  # Skip to Step 6
    
    return render_template('step5.html', form=form, form_count=form_count)


@app.route('/step6', methods=['GET', 'POST'])
def step6():
    form = PlatformForm()
    form_count = 0
    if request.method == 'POST':
        if 'add' in request.form:
            form_count += 1
        elif 'save' in request.form:
            return redirect(url_for('review'))  # Move to Review page
        elif 'skip' in request.form:
            return redirect(url_for('review'))  # Skip to Review page
    
    return render_template('step6.html', form=form, form_count=form_count)


@app.route('/review')
def review():
    return render_template('review.html')


if __name__ == "__main__":
    app.run(debug=True)
