from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key


# Step 1 Form: Product Information
class ProductInfoForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    version = StringField('Version (Optional)')
    launch_date = DateField('Launch Date', format='%Y-%m-%d', default=datetime.date.today, validators=[DataRequired()])
    status = SelectField('Status', choices=[('active', 'Active'), ('in_development', 'In Development')], default='active', validators=[DataRequired()])
    product_properties = SelectField('Product Properties (Optional)', choices=[('AI', 'AI'), ('GUI', 'GUI'), ('Personal Information', 'Personal Information')], widget=SelectField.widget, multiple=True)
    retirement_date = DateField('Retirement Date', format='%Y-%m-%d', default="8999-12-31", validators=[DataRequired()])
    description = StringField('Description (Max 2500 words)')
    business_value = StringField('Business Value (Max 2500 words)')
    risks = StringField('Risks (Optional, Max 2500 words)')
    additional_properties = StringField('Additional Properties (Optional, Max 2500 words)')
    documentation_url = StringField('Product Documentation URL (Optional)')
    repository_url = StringField('Repository URL (Optional)')
    metrics_dashboard = StringField('Metrics Dashboard (Optional)')
    submit = SubmitField('Next')


# Step 2 Form: Product Owners Information
class ProductOwnerForm(FlaskForm):
    product_owner_name = StringField('Product Owner Name', validators=[DataRequired()])
    product_owner_zid = StringField('Product Owner ZID', validators=[DataRequired()])
    product_owner_email = StringField('Product Owner Email', validators=[DataRequired()])
    product_owner_type = SelectField('Product Owner Type', choices=[('Owner', 'Owner')], validators=[DataRequired()])
    valid_from_date = DateField('Valid From Date', format='%Y-%m-%d', default=datetime.date.today, validators=[DataRequired()])
    valid_to_date = DateField('Valid To Date', format='%Y-%m-%d', default="8999-12-31", validators=[DataRequired()])
    submit = SubmitField('Next')
    skip = SubmitField('Skip')


# Step 3 Form: Business Owner Information
class BusinessOwnerForm(FlaskForm):
    business_contact_name = StringField('Business Contact Name', validators=[DataRequired()])
    business_owner_zid = StringField('Business Owner ZID', validators=[DataRequired()])
    business_contact_email = StringField('Business Contact Email', validators=[DataRequired()])
    business_contact_type = SelectField('Business Contact Type', choices=[('Owner', 'Owner')], validators=[DataRequired()])
    valid_from_date = DateField('Valid From Date', format='%Y-%m-%d', default=datetime.date.today, validators=[DataRequired()])
    valid_to_date = DateField('Valid To Date', format='%Y-%m-%d', default="8999-12-31", validators=[DataRequired()])
    submit = SubmitField('Next')


# Step 4 Form: Snowflake Data Information
class SnowflakeDataForm(FlaskForm):
    database_name = StringField('Database Name', validators=[DataRequired()])
    schema_name = StringField('Schema Name', validators=[DataRequired()])
    table_name = StringField('Table Name', validators=[DataRequired()])
    snowflake_data_type = SelectField('Snowflake Data Type', choices=[('Source', 'Source'), ('Output', 'Output'), ('Source and Output', 'Source and Output')], validators=[DataRequired()])
    valid_from_date = DateField('Valid From Date', format='%Y-%m-%d', default=datetime.date.today, validators=[DataRequired()])
    valid_to_date = DateField('Valid To Date', format='%Y-%m-%d', default="8999-12-31", validators=[DataRequired()])
    submit = SubmitField('Next')


# Step 5 Form: Other Data Sources/Outputs
class OtherDataForm(FlaskForm):
    dataset_name = StringField('Dataset Name', validators=[DataRequired()])
    dataset_description = StringField('Dataset Description', validators=[DataRequired()])
    dataset_type = SelectField('Dataset Type', choices=[('Source', 'Source'), ('Output', 'Output'), ('Source and Output', 'Source and Output')], validators=[DataRequired()])
    valid_from_date = DateField('Valid From Date', format='%Y-%m-%d', default=datetime.date.today, validators=[DataRequired()])
    valid_to_date = DateField('Valid To Date', format='%Y-%m-%d', default="8999-12-31", validators=[DataRequired()])
    submit = SubmitField('Next')


# Step 6 Form: Platform Information
class PlatformForm(FlaskForm):
    platform_name = StringField('Platform Name', validators=[DataRequired()])
    platform_description = StringField('Platform Description', validators=[DataRequired()])
    valid_from_date = DateField('Valid From Date', format='%Y-%m-%d', default=datetime.date.today, validators=[DataRequired()])
    valid_to_date = DateField('Valid To Date', format='%Y-%m-%d', default="8999-12-31", validators=[DataRequired()])
    submit = SubmitField('Next')


# Final Review
@app.route('/review', methods=['GET', 'POST'])
def review():
    # Collecting all data from the session and displaying it in a review page
    return render_template('review.html', data=session)


# Submit Data (to database or other storage)
@app.route('/submit_final', methods=['POST'])
def submit_final():
    # Here you would process the final submission (e.g., storing to Snowflake or another database)
    return render_template('thank_you.html', data=session)


# Route for Step 1
@app.route('/', methods=['GET', 'POST'])
def step1():
    form = ProductInfoForm()
    if form.validate_on_submit():
        # Store data in session
        session['product_name'] = form.product_name.data
        session['version'] = form.version.data
        session['launch_date'] = form.launch_date.data
        session['status'] = form.status.data
        session['product_properties'] = form.product_properties.data
        session['retirement_date'] = form.retirement_date.data
        session['description'] = form.description.data
        session['business_value'] = form.business_value.data
        session['risks'] = form.risks.data
        session['additional_properties'] = form.additional_properties.data
        session['documentation_url'] = form.documentation_url.data
        session['repository_url'] = form.repository_url.data
        session['metrics_dashboard'] = form.metrics_dashboard.data

        return redirect(url_for('step2'))  # Redirect to Step 2

    return render_template('step1.html', form=form)


# Route for Step 2
@app.route('/step2', methods=['GET', 'POST'])
def step2():
    form = ProductOwnerForm()
    if form.validate_on_submit():
        # Collect data for product owners
        num_owners = int(request.form.get('num_owners', 0))
        product_owners = []

        for i in range(num_owners):
            owner_data = {
                'name': request.form.get(f'product_owner_name_{i}'),
                'zid': request.form.get(f'product_owner_zid_{i}'),
                'email': request.form.get(f'product_owner_email_{i}'),
                'type': request.form.get(f'product_owner_type_{i}'),
                'valid_from': request.form.get(f'valid_from_date_{i}'),
                'valid_to': request.form.get(f'valid_to_date_{i}')
            }
            product_owners.append(owner_data)

        session['product_owners'] = product_owners  # Store in session

        return redirect(url_for('step3'))  # Redirect to Step 3

    return render_template('step2.html', form=form)


# Route for Step 3
@app.route('/step3', methods=['GET', 'POST'])
def step3():
    form = BusinessOwnerForm()
    if form.validate_on_submit():
        # Collect business owner data
        business_owner_data = {
            'contact_name': form.business_contact_name.data,
            'zid': form.business_owner_zid.data,
            'email': form.business_contact_email.data,
            'contact_type': form.business_contact_type.data,
            'valid_from': form.valid_from_date.data,
            'valid_to': form.valid_to_date.data
        }
        session['business_owner'] = business_owner_data  # Store in session
        return redirect(url_for('step4'))  # Redirect to Step 4

    return render_template('step3.html', form=form)


# Route for Step 4
@app.route('/step4', methods=['GET', 'POST'])
def step4():
    form = SnowflakeDataForm()
    if form.validate_on_submit():
        # Collect snowflake data
        snowflake_data = {
            'database_name': form.database_name.data,
            'schema_name': form.schema_name.data,
            'table_name': form.table_name.data,
            'data_type': form.snowflake_data_type.data,
            'valid_from': form.valid_from_date.data,
            'valid_to': form.valid_to_date.data
        }
        session['snowflake_data'] = snowflake_data  # Store in session
        return redirect(url_for('step5'))  # Redirect to Step 5

    return render_template('step4.html', form=form)


# Route for Step 5
@app.route('/step5', methods=['GET', 'POST'])
def step5():
    form = OtherDataForm()
    if form.validate_on_submit():
        # Collect other data
        other_data = {
            'dataset_name': form.dataset_name.data,
            'dataset_description': form.dataset_description.data,
            'dataset_type': form.dataset_type.data,
            'valid_from': form.valid_from_date.data,
            'valid_to': form.valid_to_date.data
        }
        session['other_data'] = other_data  # Store in session
        return redirect(url_for('step6'))  # Redirect to Step 6

    return render_template('step5.html', form=form)


# Route for Step 6
@app.route('/step6', methods=['GET', 'POST'])
def step6():
    form = PlatformForm()
    if form.validate_on_submit():
        # Collect platform data
        platform_data = {
            'platform_name': form.platform_name.data,
            'platform_description': form.platform_description.data,
            'valid_from': form.valid_from_date.data,
            'valid_to': form.valid_to_date.data
        }
        session['platform_data'] = platform_data  # Store in session
        return redirect(url_for('review'))  # Redirect to Review page

    return render_template('step6.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
