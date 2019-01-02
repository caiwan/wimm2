import {Line, mixins} from 'vue-chartjs';

const {reactiveProp} = mixins;


export default Line.extend({
  mixins: [reactiveProp],
  props: ['chartData', 'options'],
  data(){
    return {
      defaultOptions: {
        responsive: true,
        maintainAspectRatio: false,
        height: '100%',
      }
    }
  },
  mounted(){
    this.renderChart(this.chartData, this.options)
  }
});
