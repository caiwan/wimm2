import moment from 'moment';

import io from '@/services/io';
import {getColor} from '@/services/palette';

export default {
  namespaced: true,
  state: {
    isCalendarVisible: false,
    dateFrom: moment().subtract(1, 'year').format('YYYY-MM-DD'),
    dateTo: moment().format('YYYY-MM-DD'),
    interval: 'weeks',
    labels: [],
    values: [],
    i: [],
    tags: [],
    baseTag: [],
    tagValues: {},
    noBase: false
  },
  mutations: {
    toggleCalendar: state => state.isCalendarVisible = !state.isCalendarVisible,
    hideUi: state => state.isCalendarVisible = false,
    setProperty: (state, {key, value}) => state[key] = value,
    setValues: (state, model) => {
      const labels = [];
      const values = [];

      const {base, tags} = model;

      for(let [date, value] of base){
        labels.push(date);
        values.push(value);
      }

      state.tagValues = tags;
      state.labels = labels;
      state.values = values;
    },
  },
  getters: {
    chartData: state => {
      const { dateFrom, dateTo, interval, tags } = state;

      const datasets = [];

      tags.forEach((tag, i) => {
        datasets.push({
          label: tag,
          backgroundColor: getColor(i),
          data: state.tagValues[tag]
        });
      });

      datasets.push(        {
          // TODO: This always triggers chart animation
          type: 'line',
          label: `${dateFrom} -- ${dateTo} (${interval})`,
          borderColor: '#286d81',
          backgroundColor: 'rgba(40, 109, 129, 0.3)',
          data: state.values,
          steppedLine: true
        });

      return {
        labels: state.labels,
        datasets
      }
    }
  },
  actions: {
    toggleCalendar: ({commit}) => commit('toggleCalendar'),
    hideUi: ({commit}) => commit('hideUi'),
    async query({commit, state}){
      const values = await io.stats.tagSumOverTime({
        dateFrom: state.dateFrom,
        dateTo: state.dateTo,
        interval: state.interval,
        tags: state.tags,
        baseTag: state.baseTag,
        noBase: state.noBase
      });

      commit('setValues', values);
    },
    setProperty: ({commit}, model) => commit('setProperty', model)
  }
}
