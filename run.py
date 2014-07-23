from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import formcheck
import cippcalc

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def start_html():
    design_condition = 'Fully Deteriorated'
    submitted_data={
        'design_condition':'Fully Deteriorated', 'location':'Highway'
        }
    return render_template('index.html',return_vars=submitted_data)

@app.route('/', methods=['GET', 'POST'])
def run_cippcalc():
    input = {}
    hard_error_msg = None
    soft_error_msg = None
    errors = formcheck.ErrorValidation(request.form)
    warnings = formcheck.WarningValidation(request.form)
    if request.method == 'POST' and errors.validate():
        for k in request.form.keys():
            input[k] = request.form[k]
        warnings.validate()
        soft_error_msg = warnings.errors
        if soft_error_msg:
            soft_errors = {}
            for j in soft_error_msg.keys():
                soft_errors[j] = request.form[j]
    else:
        hard_error_msg = errors.errors
        
    if hard_error_msg is None:
        thickness, area_lost, submitted_data = cippcalc.LM_run(input)
        thickness = str(thickness)
        area_lost = str(round(area_lost))+'%'
        return render_template('index.html', thickness=thickness, area_lost=area_lost, return_vars=submitted_data, warning=soft_error_msg, messages=soft_error_msg)
    else:
        submitted_data = request.form
        return render_template('index.html', thickness='Error', return_vars=submitted_data, error=hard_error_msg)

if __name__ == '__main__':
    app.debug = True
    app.run()