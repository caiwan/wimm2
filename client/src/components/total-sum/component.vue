<template>
  <div>
    <div id="total-sum">
      <div class="content">
        <line-chart :chartData="chart" :styles="{height: '100%'}"></line-chart>
      </div>
      <settings-bar :visible="isCalendarVisible" @hide="hideUi">
        <calendar :dateFrom="dateFrom" :dateTo="dateTo" :interval="interval"
                  @change="onChanged"></calendar>

        <button class="do-query" @click="doQuery">Query</button>
      </settings-bar>
    </div>
  </div>
</template>

<script>
  import {mapActions, mapGetters, mapState} from "vuex";
  import LineChart from '@/components/charts/line';

  import SettingsBar from '@/components/settings-bar';
  import Calendar from '@/components/calendar';

  export default {
    components: {
      LineChart, SettingsBar, Calendar
    },
    data(){
      return {
        chart: {}
      }
    },
    computed: {
      ...mapState('totalSum', [
        'isCalendarVisible', 'dateFrom', 'dateTo', 'interval',
      ]),
      ...mapGetters('totalSum', ['chartData'])
    },
    methods: {
      ...mapActions('totalSum', ['hideUi', 'setProperty', 'query']),
      onChanged(key, value){
        this.setProperty({key, value});
      },
      async doQuery(){
        await this.query();
        this.chart = this.chartData;
      },
    },
    async mounted(){
      await this.query();
      this.chart = this.chartData;
    },
    beforeRouteLeave(to, from, next){
      this.hideUi();
      next();
    }
  }
</script>

<style lang="scss" rel="stylesheet/scss">
  @import '../../scss/consts';

  #total-sum {
    height: 100%;

    .do-query {
      margin-top: 6px;
    }
  }
</style>
