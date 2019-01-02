<template>
  <div>
    <div id="tag-sum">
      <div class="content">
        <horizontal-bar-chart :chartData="chart" :styles="{height: '100%'}" :options="{}"></horizontal-bar-chart>
      </div>
      <settings-bar :visible="isCalendarVisible" @hide="hideUi">
        <calendar :dateFrom="dateFrom" :dateTo="dateTo"
                  @change="onChanged"></calendar>

        <label for="tag-sum-tag-count">Top tags</label>
        <input id="tag-sum-tag-count" type="number" min="0" step="1" :value="tagCount" @input="onChanged('tagCount', $event.target.value)">

        <label for="tag-sum-negative-first">Negative first</label>
        <input id="tag-sum-negative-first" type="checkbox" :checked="negativeFirst" @change="onChanged('negativeFirst', $event.target.checked)">

        <label for="tag-sum-tags">Filter tags</label>
        <tag-input id="tag-sum-tags" :choices="autocomplete()" :tags="tags"></tag-input>

        <button class="do-query" @click="doQuery">Query</button>
      </settings-bar>
    </div>
  </div>
</template>

<script>
  import {mapActions, mapGetters, mapState} from "vuex";

  import Calendar from '@/components/calendar';
  import HorizontalBarChart from '@/components/charts/horizontal-bar';
  import IO from '@/services/io';
  import SettingsBar from '@/components/settings-bar';
  import TagInput from '@/components/tag-input';

  export default {
    components: {
      HorizontalBarChart, SettingsBar, Calendar, TagInput
    },
    data(){
      return {
        chart: {},
      }
    },
    computed: {
      ...mapState('tagSum', [
        'isCalendarVisible', 'dateFrom', 'dateTo', 'tagCount', 'negativeFirst', 'tags'
      ]),
      ...mapGetters('tagSum', ['chartData']),
    },
    methods: {
      ...mapActions('tagSum', ['hideUi', 'setProperty', 'query']),
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
      }
    }
  }
</script>

<style lang="scss" rel="stylesheet/scss">
  @import '../../scss/consts';

  #tag-sum {
    height: 100%;

    .do-query {
      margin-top: 6px;
    }
  }
</style>
