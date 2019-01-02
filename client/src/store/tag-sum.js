import moment from 'moment';

import io from '@/services/io';


export default {
  namespaced: true,
  state: {
    isCalendarVisible: false,
    dateFrom: moment().subtract(1, 'year').format('YYYY-MM-DD'),
    dateTo: moment().format('YYYY-MM-DD'),
    labels: [],
    values: [],
    tagCount: 10,
    negativeFirst: true,
    tags: []
  },
  mutations: {
    toggleCalendar: state => state.isCalendarVisible = !state.isCalendarVisible,
    hideUi: state => state.isCalendarVisible = false,
    setProperty: (state, {key, value}) => state[key] = value,
    setValues: (state, model) => {
      const labels = [];
      const values = [];

      for(let [date, value] of model){
        labels.push(date);
        values.push(state.negativeFirst ? value * -1 : value);
      }

      state.labels = labels;
      state.values = values;
    }
  },
  getters: {
    chartData: state => {
      const { dateFrom, dateTo } = state;

      return {
        labels: state.labels,
        datasets: [
          {
            label: `${dateFrom} -- ${dateTo}`,
            backgroundColor: '#39a2bf',
            borderColor: '#286d81',
            data: state.values
          }
        ]
      }
    }
  },
  actions: {
    toggleCalendar: ({commit}) => commit('toggleCalendar'),
    hideUi: ({commit}) => commit('hideUi'),
    async query({commit, state}){
      const values = await io.stats.tagSum({
        dateFrom: state.dateFrom,
        dateTo: state.dateTo,
        tagCount: state.tagCount,
        negativeFirst: state.negativeFirst,
        tags: state.tags
      });

      commit('setValues', values);
    },
    setProperty: ({commit}, model) => commit('setProperty', model)
  }
}
