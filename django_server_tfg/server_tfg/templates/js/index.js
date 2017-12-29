var areas = ["Principal","Search Patient","Calculate Risk","Sing up Patient","Graphics"];
var graf = ["diseasesGraph","medicinesGraph","typeGraph","sexGraph","ageGraph","heightGraph","weightGraph"];

var changeVisibleArea = function(visibleArea){
	areas.forEach(function(currentValue){
		element = document.getElementById(currentValue);
		$(element).attr("hidden","hidden");
	});
	area = document.getElementById(visibleArea);
	$(area).removeAttr("hidden");
};

var changeVisibleGraf = function(visibleArea){
	graf.forEach(function(currentValue){
		element = document.getElementById(currentValue);
		$(element).attr("hidden","hidden");
	});
	area = document.getElementById(visibleArea);
	$(area).removeAttr("hidden");
};

$(document).ready(function(){

	$("#P").click(function(){
		changeVisibleArea("Principal");
	});
	$("#SP").click(function(){
		changeVisibleArea("Search Patient");
	});
	$("#CR").click(function(){
		changeVisibleArea("Calculate Risk");
	});
	$("#SuP").click(function(){
		changeVisibleArea("Sing up Patient");		
	});
	$("#G").click(function(){
		changeVisibleArea("Graphics");		
	});

	$( "#graphics_select" ).change(function() {
  		val = document.getElementById('graphics_select').value;
  		switch (val){
  		case "Enfermedades":
  			changeVisibleGraf("diseasesGraph");
  			break;
        case "Medicinas":
        	changeVisibleGraf("medicinesGraph");
        	break;
        case "Tipos de paciente":
        	changeVisibleGraf("typeGraph");
        	break;
        case "Boxplot Edad según Sexo":
        	changeVisibleGraf("sexGraph");
        	break;
        case "":
        	changeVisibleGraf("legGraph");
        	break;
        case "":
        	changeVisibleGraf("smokerGraph");
        	break;
        case "":
        	changeVisibleGraf("athleticGraph");
        	break;
        case "":
        	changeVisibleGraf("footGraph");
        	break;
        case "":
        	changeVisibleGraf("templateGraph");
        	break;
        case "Histograma de Edades":
        	changeVisibleGraf("ageGraph");
        	break;
        case "Histograma de Alturas":
        	changeVisibleGraf("heightGraph");
        	break;
        case "Histograma de Pesos":
        	changeVisibleGraf("weightGraph");
        	break;
       	}
	});
});