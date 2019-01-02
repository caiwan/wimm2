<template>
  <div>
    <div id="tag-sum-over-time">
      <div class="content">
        <bar-chart :chartData="chart" :styles="{height: '100%'}"></bar-chart>
      </div>
      <settings-bar :visible="isCalendarVisible" @hide="hideUi">
        <calendar :dateFrom="dateFrom" :dateTo="dateTo" :interval="interval"
                  @change="onChanged"></calendar>

        <label for="tag-sum-over-time-tags">Filter tags</label>
        <tag-input id="tag-sum-over-time-tags" :choices="autocomplete()" :tags="tags"></tag-input>

        <label for="tag-sum-over-time-base-tag">Base tag</label>
        <tag-input id="tag-sum-over-time-base-tag" :choices="autocomplete()" :tags="baseTag"></tag-input>

        <label for="tag-sum-over-time-no-base">Base tag is zero</label>
        <input type="checkbox" :checked="noBase" @change="e => setProperty({key: 'noBase', value: e.target.checked})" id="tag-sum-over-time-no-base">

        <button class="do-query" @click="doQuery">Query</button>
      </settings-bar>
    </div>
  </div>
</template>

<script>
  import {mapActions, mapGetters, mapState} from "vuex";

  import Calendar from '@/components/calendar';
  import BarChart from '@/components/charts/bar';
  import SettingsBar from '@/components/settings-bar';
  import TagInput from '@/components/tag-input';

  export default {
    components: {
      BarChart, SettingsBar, Calendar, TagInput
    },
    data(){
      return {
        chart: {},
      }
    },
    computed: {
      ...mapState('tagSumOverTime', [
        'isCalendarVisible', 'dateFrom', 'dateTo', 'interval', 'tags', 'baseTag', 'noBase'
      ]),
      ...mapGetters('tagSumOverTime', ['chartData']),
    },
    methods: {
      ...mapActions('tagSumOverTime', ['hideUi', 'setProperty', 'query']),
      ...mapGetters('tags', ['autocomplete']),
      onChanged(key, value){
        this.setProperty({key, value});
      },
      async doQuery(){
        await this.query();
        this.chart = this.chartData;
      }
    },
    async mounted(){
      await this.query();
      this.chart = this.chartData;
    },
    beforeRouteLeave(to, from, next){
      this.hideUi();
      next();
    },
    watch: {
      tags(value){
        this.setProperty({key: 'tags', value});
      },
      baseTag(value){
        this.setProperty({key: 'baseTag', value});
      }
    }
  }
</script>

<style lang="scss" rel="stylesheet/scss">
  @import '../../scss/consts';

  #tag-sum-over-time {
    height: 100%;

    .do-query {
      margin-top: 6px;
    }
  }
</style>
