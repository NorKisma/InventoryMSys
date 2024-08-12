@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = CompanySettingsForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            company_name = form.company_name.data
            short_name = form.short_name.data
            address = form.address.data
            email = form.email.data
            tel = form.tel.data
            website = form.website.data

            # Handle file upload
            logo = form.logo.data
            if logo:
                filename = secure_filename(logo.filename)
                logo.save(f'static/uploads/{filename}')
                logo_path = filename
            else:
                logo_path = None

            try:
                with mydb.cursor() as cursor:
                    sql = '''INSERT INTO company_settings (Company_name, ShortName, Logo, Address, Email, Tel, Website) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                    values = (company_name, short_name, logo_path, address, email, tel, website)
                    cursor.execute(sql, values)
                    mydb.commit()
                flash('Company settings updated successfully.', 'success')
                return redirect(url_for('settings'))
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'danger')

    return render_template('settings.html', form=form)