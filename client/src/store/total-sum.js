import moment from 'moment';

import io from '@/services/io';


export default {
  namespaced: true,
  state: {
    isCalendarVisible: false,
    dateFrom: moment().subtract(1, 'year').format('YYYY-MM-DD'),
    dateTo: moment().format('YYYY-MM-DD'),
    interval: 'weeks',
    labels: [],
    values: [],
    i: []
  },
  mutations: {
    toggleCalendar: state => state.isCalendarVisible = !state.isCalendarVisible,
    hideUi: state => state.isCalendarVisible = false,
    setProperty: (state, {key, value}) => state[key] = value,
    setValues: (state, model) => {
      const labels = [];
      const values = [];

      let sum = 0;

      for(let [date, value] of model){
        sum += value;

        labels.push(date);
        values.push(sum);
      }

      state.labels = labels;
      state.values = values;
    },
  },
  getters: {
    chartData: state => {
      const { dateFrom, dateTo, interval } = state;

      return {
        labels: state.labels,
        datasets: [
          {
            // TODO: This always triggers chart animation
            label: `${dateFrom} -- ${dateTo} (${interval})`,
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
      const values = await io.stats.totalSum({dateFrom: state.dateFrom, dateTo: state.dateTo, interval: state.interval});

      commit('setValues', values);
    },
    setProperty: ({commit}, model) => commit('setProperty', model)
  }
}
