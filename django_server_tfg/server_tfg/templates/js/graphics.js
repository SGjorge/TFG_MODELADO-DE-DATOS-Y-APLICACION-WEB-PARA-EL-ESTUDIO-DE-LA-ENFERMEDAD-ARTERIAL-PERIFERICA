var boxplotGraph = function(id,title,xCategories,xTitle,yAxis,mean,seriesVal){
    Highcharts.chart(id, {
        chart: {
            type: 'boxplot'
        },
        title: {
            text: title
        },
        legend: {
            enabled: false
        },
        xAxis: {
            categories: xCategories,
            title: {
                text: xTitle
            }
        },
        yAxis: {
            title: {
                text: yAxis
            },
            plotLines: [{
                value: 932,
                color: 'red',
                width: 1,
                label: {
                    text: mean,
                    align: 'center',
                    style: {
                        color: 'gray'
                    }
                }
            }]
        },
        series: [{
            name: 'Observations',
            data: seriesVal
        }]

    });
};
//////////////////////////////////////////////////////////////////////
var barGraph = function(id,title,subtitle,yTitle,seriesVal){
    Highcharts.chart(id, {
        chart: {
            type: 'column'
        },
        title: {
            text: title
        },
        subtitle: {
            text: subtitle
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
                text: yTitle
            }

        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                }
            }
        },
        series: [seriesVal],
    });
};

var getBarSerie = function(seriesName,data) {
    s = []
    series = {} ;
    series.name = seriesName ;
    series.colorByPoint = true ;
    series.data = data;
    return series;
}

var getBarData = function(dataArrayVal){
    dataArray = []
    for (var i = 0; i < dataArrayVal.length; i++) {
        d = {}
        d.name = dataArrayVal[i].name
        d.y = dataArrayVal[i].value
        d.drilldown = dataArrayVal[i].name
        dataArray.push(d)
    };
    return dataArray
};

/**
 * Get histogram data out of xy data
 * @param   {Array} data  Array of tuples [x, y]
 * @param   {Number} step Resolution for the histogram
 * @returns {Array}       Histogram data
 */
var histogram = function(data, step){
    var histo = {},
        x,
        i,
        arr = [];

    // Group down
    for (i = 0; i < data.length; i++) {
        x = Math.floor(data[i][0] / step) * step;
        if (!histo[x]) {
            histo[x] = 0;
        }
        histo[x]++;
    }

    // Make the histo group into an array
    for (x in histo) {
        if (histo.hasOwnProperty((x))) {
            arr.push([parseFloat(x), histo[x]]);
        }
    }

    // Finally, sort the array
    arr.sort(function (a, b) {
        return a[0] - b[0];
    });

    return arr;
}

var histoGraph = function(id,title,dataArray) {
Highcharts.chart(id, {
    chart: {
        type: 'column'
    },
    title: {
        text: title
    },
    xAxis: {
        gridLineWidth: 1
    },
    legend: {
        enabled: false
    },
    series: [{
        name: 'Histogram',
        type: 'column',
        data: histogram(dataArray, 10),
        pointPadding: 0,
        groupPadding: 0,
        pointPlacement: 'between'
    }]
});
}

var getHistoData = function(arrayObject){
    var d = []
    for(i = 0; i < arrayObject.length;i++){
        var val = [];
        if(isNaN(arrayObject[i].value)){
            var val = [0,0];
        }else{
            var val = [arrayObject[i].value,0];
        }
        d.push(val)
    }
    return d
}

///////////////////////////////////////////////////////////////////////
var getDataObjects = function(id){
    var selector = "#"+ id + " p";
    var element = $(selector);
    var array = new Array;
    for (var i = 0; i < element.length; i++) {
        var a = {};
        a.name = element[i].id.replace(new RegExp("_", 'g')," ");
        a.value = parseInt(element[i].innerHTML);
        array.push(a);
    };  
    return array;
};
var arrayStringToInt = function(arr) {
    auxArr = []; 
    for(var i = 0; i < arr.length; i++){
        n = parseInt(arr[i]);
        if(isNaN(n)){
            n = 0;
        }
        auxArr.push(n);
    }
    return auxArr;
}

var getDataBoxPlot = function(id){
    return $(id).html().replace(/'/g,"").replace(/u/g,"").replace(/ /g,"").replace(/\[/g,"").replace(/\]/g,"").split(",");
}

var getMean = function(arrM){
    t = 0;
    for(var i = 0 ; i < arrM.length ; i++){
        t += arrM[i];
    }
    return (t/arrM.length);
}

var getDataBoxPlotSex = function(){
    idSexBoxplot = 'sexGraph';
    idSexDataMale = "#" + 'maleAgeVal';
    htmlMale = getDataBoxPlot(idSexDataMale);
    htmlMale = arrayStringToInt(htmlMale);
    htmlMale = htmlMale.sort(function(a, b){return a-b});
    idSexDataFemale = "#" + 'femaleAgeVal';
    htmlFemale = getDataBoxPlot(idSexDataFemale);
    htmlFemale = arrayStringToInt(htmlFemale);
    htmlFemale = htmlFemale.sort(function(a, b){return a-b});

    bothArr = htmlMale.concat(htmlFemale);
    mean = getMean(bothArr);

    minMale = htmlMale[0];
    maxMale = htmlMale[htmlMale.length-1];
    medianMale = htmlMale[Math.floor(htmlMale.length/2)];
    firstQuartilMale = htmlMale[Math.floor((htmlMale.length+1)/4)];
    thirdQuartilMale = htmlMale[Math.floor((htmlMale.length+1)*0.75)];

    minFemale = htmlFemale[0];
    maxFemale = htmlFemale[htmlFemale.length-1];
    medianFemale = htmlFemale[Math.floor(htmlFemale.length/2)];
    firstQuartilFemale = htmlFemale[Math.floor(htmlFemale.length/4) + 1];
    thirdQuartilFemale = htmlMale[Math.floor((htmlFemale.length+1)*0.75)];

    dataBox = [
                [minMale, firstQuartilMale, medianMale, thirdQuartilMale, maxMale],
                [minFemale, firstQuartilFemale, medianFemale, thirdQuartilFemale, maxFemale]
            ]

    result = [mean,dataBox];
    return result;
}

$(document).ready(function(){
    yTitle = 'total patients'
    seriesName = 'Patients';

    idDiseasesVal = 'diseasesVal';
    idDiseasesGraph = 'diseasesGraph' ;
    titleDiseasesGraph = 'diseases per patient' ;
    subtitleDiseasesGraph = 'number of patient per disease' ;
    dataDiseases = getDataObjects(idDiseasesVal);
    barDataDiseases = getBarData(dataDiseases);
    seriesDiseases = getBarSerie(seriesName,barDataDiseases);
    
    idMedicinesVal = 'medicinesVal';
    idMedicinesGraph = 'medicinesGraph' ;
    titleMedicinesGraph = 'medicines per patient' ;
    subtitleMedicienesGraph = 'number of patient per medicine' 
    dataMedicines = getDataObjects(idMedicinesVal);
    barDataMedicines = getBarData(dataMedicines);
    seriesMedicines = getBarSerie(seriesName,barDataMedicines);

    idTypeVal = 'typeVal';
    idTypeGraph = 'typeGraph' ;
    titleTypeGraph = 'types per patient' ;
    subtitleTypeGraph = 'number of patient per medicine' 
    dataType = getDataObjects(idTypeVal);
    barDataType = getBarData(dataType);
    seriesType = getBarSerie(seriesName,barDataType);

    
    titleSexBoxplot = 'Sex age relationship';
    titleSexYAxisBoxplot = 'Age';
    xSexCategories = ['Male','Female']
    xSexTitle = 'Sex'
    dataSex = getDataBoxPlotSex()

    idLegBoxplot = 'legGraph';
    titleLegBoxplot = 'Strong leg';
    titleLegYAxisBoxplot = '';
    xLegCategories = ['Right','Left']
    xLegTitle = 'Leg'
    meanLeg = 'mean: 932'

    idSmokerBoxplot = 'smokerGraph';
    titleSmokerBoxplot = 'Smoker';
    titleSmokerYAxisBoxplot = '';
    xSmokerCategories = ['yes','no']
    xSmokerTitle = 'Smoker'
    meanSmoker = 'mean: 932'

    idAthleticBoxplot = 'athleticGraph';
    titleAthleticBoxplot = 'Athletic';
    titleAthleticYAxisBoxplot = '';
    xAthleticCategories = ['yes','no']
    xAthleticTitle = 'athletic'
    meanAthletic = 'mean: 932'

    idFootBoxplot = 'footGraph';
    titleFootBoxplot = 'Flat-concave foot';
    titleFootYAxisBoxplot = '';
    xFootCategories = ['Flat','Concave']
    xFootTitle = 'foot'
    meanFoot = 'mean: 932'

    idTemplateBoxplot = 'templateGraph';
    titleTemplateBoxplot = 'Foot Templates';
    titleTemplateYAxisBoxplot = '';
    xTemplateCategories = ['yes','no']
    xTemplateTitle = 'template'
    meanTemplate = 'mean: 932'

    idAgeHistogram = 'ageGraph'
    idAgeVal = 'ageVal'
    var ageData = getDataObjects(idAgeVal);
    var ageData = getHistoData(ageData);
    titleAgeHistogram = 'Histograma de edades'

    idHeightHistogram = 'heightGraph'
    titleHeightHistogram = 'Histograma de alturas'
    idHeigthVal = 'heightVal'
    var heigthData = getDataObjects(idHeigthVal);
    var heigthData = getHistoData(heigthData);

    idWeightHistogram = 'weightGraph'
    titleWeightHistogram = 'Histograma de pesos'
    idWeigthVal = 'weightVal'
    var weigthData = getDataObjects(idWeigthVal);
    var weigthData = getHistoData(weigthData);
    

    barGraph(idDiseasesGraph,titleDiseasesGraph,subtitleDiseasesGraph,yTitle,seriesDiseases);
    barGraph(idMedicinesGraph,titleMedicinesGraph,subtitleMedicienesGraph,yTitle,seriesMedicines);
    barGraph(idTypeGraph,titleTypeGraph,subtitleTypeGraph,yTitle,seriesType);
    
    boxplotGraph(idSexBoxplot,titleSexBoxplot,xSexCategories,xSexTitle,titleSexYAxisBoxplot,dataSex[0],dataSex[1]);
    boxplotGraph(idLegBoxplot,titleLegBoxplot,xLegCategories,xLegTitle,titleLegYAxisBoxplot,meanLeg);
    boxplotGraph(idSmokerBoxplot,titleSmokerBoxplot,xSmokerCategories,xSmokerTitle,titleSmokerYAxisBoxplot,meanSmoker);
    boxplotGraph(idAthleticBoxplot,titleAthleticBoxplot,xAthleticCategories,xAthleticTitle,titleAthleticYAxisBoxplot,meanAthletic);
    //boxplotGraph(idFootBoxplot,titleFootBoxplot,xFootCategories,xFootTitle,titleFootYAxisBoxplot,meanFoot);
    boxplotGraph(idTemplateBoxplot,titleTemplateBoxplot,xTemplateCategories,xTemplateTitle,titleTemplateYAxisBoxplot,meanTemplate);
    
    histoGraph(idAgeHistogram,titleAgeHistogram,ageData);
    histoGraph(idHeightHistogram,titleHeightHistogram,heigthData);
    histoGraph(idWeightHistogram,titleWeightHistogram,weigthData);
});