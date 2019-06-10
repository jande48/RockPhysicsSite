$('#loading').hide();
$('#graph').hide();
function isNumberKey(evt)
{
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if(charCode == 45) return true;
    if (charCode != 46 && charCode > 31 
    && (charCode < 48 || charCode > 57))
        return false;
    return true;
}

function showFrequency(){
    $("#ricker").hide();
    $("#ormsby").hide();
    $("#klauder").hide();
    let wavelet_type = $("#wavelet_type").val();
    if(wavelet_type === 'Ricker'){
        $("#ricker").show();
        $("#ricker_frequency").val(30);
    }else if(wavelet_type === 'Ormsby'){
        $("#ormsby").show();
        $("#low_cut_frequency").val(5);
        $("#low_pass_frequency").val(10);
        $("#high_pass_frequency").val(40);
        $("#high_cut_frequency").val(45);
    }else if(wavelet_type === 'Klauder'){
        $("#klauder").show();
        $("#upper_frequency").val(10);
        $("#lower_frequency").val(100);
    }
}

function setDefaultValue(){
    $("#K0_quartz").val(37);
    $("#K0_plag_feldspar").val(75.6);
    $("#K0_dolomite").val(94.6);
    $("#K0_clay").val(25);

    // Fluid Properties
    $("#K_brine").val(3.1);
    $("#K_gas").val(0.25);
    $("#rho_brine").val(1);
    $("#rho_gas").val(0.25);

    // Rock Properties
    $("#Porosity").val();
    $("#rhob_rock").val(2.3);
    $("#grain_density").val(2.65);
    $("#Vp_rock").val(3.5);
    $("#Vs_rock").val(1.8);
    $("#sp_shale_cutoff").val(50);

    // Calculating Minteralogy K Matrix
    $("#Percent_quartz").val(0.75);
    $("#Percent_plag_feldspar").val(0.1);
    $("#Percent_dolomite").val(0.1);
    $("#Percent_clay").val(0.05);
    $("#Porosity").val(20);

    // Seismic Constants
    $("#sampling_interval_dt").val(0.02);

}

setDefaultValue();
showFrequency();

function onFieldChange(id) {
    $("#"+id+"-error").remove();
    let field_val = $("#"+id).val();
    if(field_val === ""){
        $('#'+id).after('<span class="error" id="'+id+'-error">This field is required!</span>');
        return;
    }
}

function toggleIcon(e) {
    $(e.target)
        .prev('.panel-heading')
        .find(".more-less")
        .toggleClass('fa-plus fa-minus');
}

$('.panel-group').on('hidden.bs.collapse', toggleIcon);
$('.panel-group').on('shown.bs.collapse', toggleIcon);
$(document).ready(function(){

    // function submitForm(){
    $('#newForm').on('submit',function (e) {
        event.preventDefault();
        $(".error").remove();
        let valid = true;
        // Calculating Voight Reuss Mixing
        let calculation_method = $("#calculation_method").val();
        let K0_quartz = $("#K0_quartz").val();
        let K0_plag_feldspar = $("#K0_plag_feldspar").val();
        let K0_dolomite = $("#K0_dolomite").val();
        let K0_clay = $("#K0_clay").val();
    
        // Calculating Minteralogy K Matrix
        let Percent_quartz = $("#Percent_quartz").val();
        let Percent_plag_feldspar = $("#Percent_plag_feldspar").val();
        let Percent_dolomite = $("#Percent_dolomite").val();
        let Percent_clay = $("#Percent_clay").val();
    
        // Fluid Properties
        let K_brine = $("#K_brine").val();
        let K_gas = $("#K_gas").val();
        let rho_brine = $("#rho_brine").val();
        let rho_gas = $("#rho_gas").val();
        // let Sw = $("#Sw").val();
    
        // Rock Properties
        let Porosity = $("#Porosity").val();
        let rhob_rock = $("#rhob_rock").val();
        let grain_density = $("#grain_density").val();
        let Vp_rock = $("#Vp_rock").val();
        let Vs_rock = $("#Vs_rock").val();
        let sp_shale_cutoff = $("#sp_shale_cutoff").val();

        // Seismic constants
        let wavelet_type = $("#wavelet_type").val();
        if(wavelet_type === ""){
            $('#wavelet_type').after('<span class="error" id="wavelet_type-error">This field is required!</span>');
            valid = false;
        }
        let ricker_frequency = $("#ricker_frequency").val();
        let low_cut_frequency = $("#low_cut_frequency").val();
        let low_pass_frequency = $("#low_pass_frequency").val();
        let high_pass_frequency = $("#high_pass_frequency").val();
        let high_cut_frequency = $("#high_cut_frequency").val();
        let upper_frequency = $("#upper_frequency").val();
        let lower_frequency = $("#lower_frequency").val();
        let frequency;
        if(wavelet_type === 'Ricker'){
            if(ricker_frequency === ""){
                $('#ricker_frequency').after('<span class="error" id="ricker_frequency-error">This field is required!</span>');
                valid = false;
            }
            let data = parseFloat(ricker_frequency);
            frequency = data;
        }else if(wavelet_type === 'Ormsby'){
            if(low_cut_frequency === ""){
                $('#low_cut_frequency').after('<span class="error" id="low_cut_frequency-error">This field is required!</span>');
                valid = false;
            }
            if(low_pass_frequency === ""){
                $('#low_pass_frequency').after('<span class="error" id="low_pass_frequency-error">This field is required!</span>');
                valid = false;
            }
            if(high_pass_frequency === ""){
                $('#high_pass_frequency').after('<span class="error" id="high_pass_frequency-error">This field is required!</span>');
                valid = false;
            }
            if(high_cut_frequency === ""){
                $('#high_cut_frequency').after('<span class="error" id="high_cut_frequency-error">This field is required!</span>');
                valid = false;
            }
            let data = [];
            data[0] = parseFloat(low_cut_frequency);
            data[1] = parseFloat(low_pass_frequency);
            data[2] = parseFloat(high_pass_frequency);
            data[3] = parseFloat(high_cut_frequency);
            frequency = data;
        }else if(wavelet_type === 'Klauder'){
            if(upper_frequency === ""){
                $('#upper_frequency').after('<span class="error" id="upper_frequency-error">This field is required!</span>');
                valid = false;
            }
            if(lower_frequency === ""){
                $('#lower_frequency').after('<span class="error" id="lower_frequency-error">This field is required!</span>');
                valid = false;
            }
            let data = [];
            data[0] = parseFloat(upper_frequency);
            data[1] = parseFloat(lower_frequency);
            frequency = data;
        }

        
        if (!frequency){
            valid = false
        }

        let sampling_interval_dt = $("#sampling_interval_dt").val();
        if(sampling_interval_dt === ""){
            $('#sampling_interval_dt').after('<span class="error" id="sampling_interval_dt-error">This field is required!</span>');
            valid = false;
        }
    
        
        
        // formData.append('file', $('#csv_file')[0].files[0]);
        if(calculation_method === ""){
            $('#calculation_method').after('<span class="error" id="calculation_method-error">This field is required!</span>');
            valid = false;
        }
        if(K0_quartz === ""){
            $('#K0_quartz').after('<span class="error" id="K0_quartz-error">This field is required!</span>');
            valid = false;
        }
        if(K0_plag_feldspar === ""){
            $('#K0_plag_feldspar').after('<span class="error" id="K0_plag_feldspar-error">This field is required!</span>');
            valid = false;
        }
        if(K0_dolomite === ""){
            $('#K0_dolomite').after('<span class="error" id="K0_dolomite-error">This field is required!</span>');
            valid = false;
        }
        if(K0_clay === ""){
            $('#K0_clay').after('<span class="error" id="K0_clay-error">This field is required!</span>');
            valid = false;
        }
        if(Percent_quartz === ""){
            $('#Percent_quartz').after('<span class="error" id="Percent_quartz-error">This field is required!</span>');
            valid = false;
        }
        if(Percent_plag_feldspar === ""){
            $('#Percent_plag_feldspar').after('<span class="error" id="Percent_plag_feldspar-error">This field is required!</span>');
            valid = false;
        }
        if(Percent_dolomite === ""){
            $('#Percent_dolomite').after('<span class="error" id="Percent_dolomite-error">This field is required!</span>');
            valid = false;
        }
        if(Percent_clay === ""){
            $('#Percent_clay').after('<span class="error" id="Percent_clay-error">This field is required!</span>');
            valid = false;
        }
        if(K_brine === ""){
            $('#K_brine').after('<span class="error" id="K_brine-error">This field is required!</span>');
            valid = false;
        }
        if(K_gas === ""){
            $('#K_gas').after('<span class="error" id="K_gas-error">This field is required!</span>');
            valid = false;
        }
        if(rho_brine === ""){
            $('#rho_brine').after('<span class="error" id="rho_brine-error">This field is required!</span>');
            valid = false;
        }
        if(rho_gas === ""){
            $('#rho_gas').after('<span class="error" id="rho_gas-error">This field is required!</span>');
            valid = false;
        }
        // if(Sw === ""){
        //     $('#Sw').after('<span class="error" id="Sw-error">This field is required!</span>');
        //     valid = false;
        // }
        if(Porosity === ""){
            $('#Porosity').after('<span class="error" id="Porosity-error">This field is required!</span>');
            valid = false;
        }
        if(rhob_rock === ""){
            $('#rhob_rock').after('<span class="error" id="rhob_rock-error">This field is required!</span>');
            valid = false;
        }
        if(grain_density === ""){
            $('#grain_density').after('<span class="error" id="grain_density-error">This field is required!</span>');
            valid = false;
        }
        if(Vp_rock === ""){
            $('#Vp_rock').after('<span class="error" id="Vp_rock-error">This field is required!</span>');
            valid = false;
        }
        if(Vs_rock === ""){
            $('#Vs_rock').after('<span class="error" id="Vs_rock-error">This field is required!</span>');
            valid = false;
        }
        if(sp_shale_cutoff === ""){
            $('#sp_shale_cutoff').after('<span class="error" id="sp_shale_cutoff-error">This field is required!</span>');
            valid = false;
        }

        // 
        let upload_file = {}
        let csv_file = $('#csv_file')[0].files.length;
    
        if($('#csv_file')[0].files[0]){
            if($('#csv_file')[0].files[0].name.split(".")[1] === 'csv'){
                csv_file = $('#csv_file')[0].files[0];
                if(valid == true){
                    valid = true;
                }
            }else{
                $('#csv_file').after('<span class="error">Upload CSV File Only!</span>');
                valid = false;
            }
        }
        upload_file = csv_file;
    
        if(!valid){
            return;
        }
        // console.log(valid);
        let formData = new FormData();
        formData.append('file', $('#csv_file')[0].files[0]);
        formData.append("calculation_method", calculation_method);
        formData.append("sp_shale_cutoff", sp_shale_cutoff);
        formData.append("K0_quartz", K0_quartz);
        formData.append("K0_plag_feldspar", K0_plag_feldspar);
        formData.append("K0_dolomite", K0_dolomite);
        formData.append("K0_clay", K0_clay,);
        formData.append("Percent_quartz", Percent_quartz);
        formData.append("Percent_plag_feldspar", Percent_plag_feldspar);
        formData.append("Percent_dolomite", Percent_dolomite);
        formData.append("Percent_clay", Percent_clay);
        formData.append("K_brine", K_brine);
        formData.append("K_gas", K_gas);
        formData.append("rho_brine", rho_brine);
        formData.append("rho_gas", rho_gas);
        formData.append("Porosity", Porosity);
        formData.append("rhob_rock", rhob_rock);
        formData.append("grain_density", grain_density);
        formData.append("Vp_rock", Vp_rock);
        formData.append("Vs_rock", Vs_rock);
        formData.append("wavelet_type", wavelet_type);
        formData.append("frequency", frequency);
        formData.append("sampling_interval_dt", sampling_interval_dt);
        
        // let data = {
        //     "calculation_method": calculation_method,
        //     "sp_shale_cutoff": sp_shale_cutoff,
        //     "K0_quartz": K0_quartz,
        //     "K0_plag_feldspar": K0_plag_feldspar,
        //     "K0_dolomite": K0_dolomite,
        //     "K0_clay": K0_clay,
        //     "Percent_quartz": Percent_quartz,
        //     "Percent_plag_feldspar": Percent_plag_feldspar,
        //     "Percent_dolomite": Percent_dolomite,
        //     "Percent_clay": Percent_clay,
        //     "K_brine": K_brine,
        //     "K_gas": K_gas,
        //     "rho_brine": rho_brine,
        //     "rho_gas": rho_gas,
        //     // "Sw": Sw,
        //     "Porosity": Porosity,
        //     "rhob_rock": rhob_rock,
        //     "grain_density": grain_density,
        //     "Vp_rock": Vp_rock,
        //     "Vs_rock": Vs_rock,
        //     "csv_file": formData
        // }
        // console.log(data)
        $('#loading').show();
        $('#graph').hide();
        $.ajax({
            url: '/graph',
            data: formData,
            type: 'POST',
            // contentType: 'multipart/form-data',
            processData: false,
            contentType: false,
            success: function(response) {
                $('#loading').hide();
                $('#graph').show();
                $('#graph_one_image').attr('src',response.imgUrl.url_1);
                $('#graph_two_image').attr('src',response.imgUrl.url_2);
                $('html, body').animate({
                    scrollTop: $("#graph").offset().top
                }, 2000);
            },
            error: function(error) {
                $('#loading').hide();
                alert(JSON.stringify(error));
            }
        });
    })
})