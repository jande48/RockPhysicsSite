from flask import Flask, render_template, request, jsonify
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['DEBUG'] = True

from Gassman import getGraph
import io

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        imgURL = ""
    elif request.method == 'POST':
        # calculation_method : Gardner, Castagna_1, or Castagna_2
        # SP_shale_cutoff : Any Number
        calculation_method = request.form.get("calculation_method", None)
        SP_shale_cutoff = request.form.get("sp_shale_cutoff", None)
        imgURL = getGraph(calculation_method, int(SP_shale_cutoff))
    return render_template('index.html', imgURL=imgURL)

@app.route('/graph', methods=['POST'])
def getGraphURL():
    data = {}
    if 'file' in request.form.keys():
        csv_file = None
    else:
        csv_file = io.StringIO(request.files['file'].stream.read().decode("UTF8"), newline=None)
    calculation_method = request.form["calculation_method"]
    SP_shale_cutoff = request.form["sp_shale_cutoff"]
    K0_quartz = request.form["K0_quartz"]
    K0_plag_feldspar = request.form["K0_plag_feldspar"]
    K0_dolomite = request.form["K0_dolomite"]
    K0_clay = request.form["K0_clay"]
    Percent_quartz = request.form["Percent_quartz"]
    Percent_plag_feldspar = request.form["Percent_plag_feldspar"]
    Percent_dolomite = request.form["Percent_dolomite"]
    Percent_clay = request.form["Percent_clay"]
    K_brine = request.form["K_brine"]
    K_gas = request.form["K_gas"]
    rho_brine = request.form["rho_brine"]
    rho_gas = request.form["rho_gas"]
    Sw = 1 # request.form["Sw"]
    Porosity = request.form["Porosity"]
    rhob_rock = request.form["rhob_rock"]
    grain_density = request.form["grain_density"]
    Vp_rock = request.form["Vp_rock"]
    Vs_rock = request.form["Vs_rock"]
    wavelet_type = request.form["wavelet_type"]
    frequency = request.form["frequency"].split(",")
    if len(frequency) == 1:
        frequency = float(frequency[0])
    else:
        frequency = list(map(float, frequency))
    sampling_interval_dt = request.form["sampling_interval_dt"]
    
    imgURL = getGraph(calculation_method, float(SP_shale_cutoff), float(K0_quartz), \
        float(K0_plag_feldspar), float(K0_dolomite), float(K0_clay), float(Percent_quartz), \
        float(Percent_plag_feldspar), float(Percent_dolomite), float(Percent_clay), float(K_brine), \
        float(K_gas), float(rho_brine), float(rho_gas), float(Sw), float(Porosity), float(rhob_rock), \
        float(grain_density), float(Vp_rock), float(Vs_rock), csv_file, wavelet_type, frequency, float(sampling_interval_dt))
    data['imgUrl'] = imgURL
    return jsonify(data)

if __name__ == '__main__':
    app.debug = True
    app.run()