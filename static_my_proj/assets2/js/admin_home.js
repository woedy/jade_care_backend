 document.addEventListener("DOMContentLoaded", () => {

    echarts.init(document.querySelector("#trafficChart")).setOption({
      tooltip: {
      trigger: 'item'
      },
      legend: {
        top: '5%',
        left: 'center'
      },
      series: [{
        name: 'All Patients Gender %',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: true
        },
        data: [
            {
                value: 1048,
                name: 'Male'
            },
                {
            value: 735,
            name: 'Female'
          }
        ]
      }]
    });
});

