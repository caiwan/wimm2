import {Bar, mixins} from 'vue-chartjs';


export default Bar.extend({
  mixins: [mixins.reactiveProp],
  props: ['chartData', 'options'],
  data(){
    return {
      defaultOptions: {
        responsive: true,
        maintainAspectRatio: false,
        height: '100%',
        scales: {
          xAxes: [{
            barPercentage: 1.0,
            stacked: true,
            ticks: {
              beginAtZero: true
            },
            gridLines: {
              display: true
            }
          }],
          yAxes: [{
            stacked: true,
            ticks: {
              beginAtZero: true
            },
            gridLines: {
              display: true
            }
          }]
        }
      }
    }
  },
  mounted(){
    this.renderChart(this.chartData, this.options)
  }
});
