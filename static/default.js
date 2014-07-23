function loadscript() {
	if (document.getElementById("design_condition").value == "Partially Deteriorated") {
		$('.partial :input').prop("disabled", false);
		$('.partial :input').css('color', '#000');
		$('.partial').removeClass("inactive");
		$('.fully :input').prop("disabled", true);
		$('.fully :input').css('color', 'transparent');
		$('.fully').addClass("inactive");
	} else {
		$('.partial :input').prop("disabled", true);
		$('.partial :input').css('color', 'transparent');
		$('.fully :input').prop("disabled", false);
		$('.fully :input').css('color', '#000');
		$('.partial').addClass("inactive");
		$('.fully').removeClass("inactive");
	}		
}

function design_option_change(){
	if (document.getElementById("design_condition").value == "Partially Deteriorated") {
		$('.partial :input').prop("disabled", false);
		$('.partial :input').css('color', '#000');
		$('.partial').removeClass("inactive");
		$('.fully :input').prop("disabled", true);
		$('.fully :input').css('color', 'transparent');
		$('.fully').addClass("inactive");
	} else {
		$('.partial :input').prop("disabled", true);
		$('.partial :input').css('color', 'transparent');
		$('.partial').addClass("inactive");
		$('.fully :input').prop("disabled", false);
		$('.fully :input').css('color', '#000');
		$('.fully').removeClass("inactive");
	}	
}

/*function groundwater_omit(){
	if (document.getElementById("gwcb").checked == true){
		$('.gw :input').css('color', 'transparent');
		$('.gw :input').val('999');
	} else {
		$('.gw :input').css('color', '');
		$('.gw :input').val('');
	}
}*/

/*function submit_prefetch(){
	
	var defailt_inp_ids = ["design_modulus", "design_flexural_strength", "safety_factor", "ret_factor", "ovality", "enhancement_factor", "soil_density", "poissons", "soil_mod", "n_host", "n_liner", "host_age"];
	
	for (var i in defailt_inp_ids) {
		if (document.getElementById(defailt_inp_ids[i]).value == "") {
			document.getElementById(defailt_inp_ids[i]).value = document.getElementById(defailt_inp_ids[i]).placeholder;
		}
	}
	document.getElementById("input_form").submit()

}
	WE'RE GOING TO DO THIS IN PYTHON INSTEAD */