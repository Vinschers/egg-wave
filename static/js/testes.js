$(function() {
    $('#uploadInput').change(function() {
      $('#upload-file-btn').removeAttr('disabled')
      $('#upload-file-btn').removeClass('btnDisabled')
      $('#upload-file-btn').addClass('bgRoxoPrimario')
      $('#upload-file-btn').attr('style', 'color: black !important')
    })
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/sendFile',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
            
                $("#graficoEmocoes").remove() 
                $("#legendaGrafico").css('display', 'inline');
                $("#wrapperEmocoes").css('display', 'block');
                $("#wrapperEmocoes").css('height', '50vh');
      
                $("#wrapperEmocoes").append("<canvas id=\"graficoEmocoes\"></canvas>");
                criarGrafico(data.results, "graficoEmocoes", "Emoções");
            },
        });
    });
});

function criarGrafico(dados, nomeGrafico, label)
{
  labelsDados = []
  for (var i = 0; i < dados.length; i++)
    labelsDados.push(i)
  var ctx = document.getElementById(nomeGrafico).getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labelsDados,
      datasets: [{ 
          data: dados,
          label: label,
          steppedLine: 'before',
          //lineTension: 0,
          borderColor: "#BB86FC",
          fill: false
        }]
    },
    options: {
      maintainAspectRatio: false,
      scales: {
        xAxes: [{ticks: {fontColor: 'white'},    gridLines: {
        color: '#1F1F1F'
      }}],
        yAxes: [{ticks: {fontColor: 'white'}, 
        afterTickToLabelConversion : function(q){
          for(var tick in q.ticks){
              q.ticks[tick] = '';
          }
          q.ticks[0] = 'Positivo';
          q.ticks[5] = 'Neutro';
          q.ticks[10] = 'Negativo';
      }, 
      gridLines: {
        color: '#1F1F1F'
      }
      }]
      },
      legend: {
        display: false,
        fontColor: 'white'
      }
    }
  });
}


/*var myLineChart = new Chart(ctx, {
    type: 'line',
    datasets: [{label: 'algumacoisapraversefunciona', data: [{
        x: 0,
        y: 0
    }, {
        x: 1,
        y: 1
    }, 
    {
        x: 2,
        y: 1
    },
    {
        x: 3,
        y: 1
    },
    {
        x: 4,
        y: 0
    },
    {
        x: 5,
        y: -1
    },
    {
        x: 6,
        y: -1
    },
    {
        x: 7,
        y: 0
    }],
    options: {
        scales: {
            yAxes: [{
                stacked: true
            }]
        }
    }
}]});*/
