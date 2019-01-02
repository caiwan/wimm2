import moment from 'moment';
import Vue from 'vue';

import io from '@/services/io';


export default {
  namespaced: true,
  state: {
    currentDate: moment(),
    today: moment().format('YYYY-MM-DD'),

    isEditing: false,
    isDeleting: false,
    isLoading: false,
    isSubmitting: false,
    dates: [],
    selected: new Set()
  },
  getters: {
    isEditingDisabled: state => state.isDeleting,
    isDeletingDisabled: state => state.isEditing,
    canNavigate: state => !(state.isEditing || state.isDeleting),
    currentDateFormatted: state => state.currentDate ? state.currentDate.format('YYYY / MMMM') : '',
    isSelected: state => id => state.selected[id] !== undefined
  },
  mutations: {
    toggle: (state, property) => {
      state[property] = !state[property];
      state.selected = {};
    },
    setCurrentDate: (state, nextDate) => {
      state.currentDate = nextDate;

      const today = moment().format('YYYY-MM-DD');
      if (nextDate.format('YYYY-MM-DD') === today) {
        state.today = today
      }
      else {
        state.today = nextDate.date(1).format('YYYY-MM-DD');
      }
    },
    setDates: (state, dates) => {
      state.dates = dates;
      state.isEditing = false;
      state.isDeleting = false;
      state.isLoading = false;
      state.selected = {};
    },
    fetchStarted: state => state.isLoading = true,
    selectItem: (state, itemId) => {
      let isSelected = !state.selected[itemId];
      if (isSelected) {
        Vue.set(state.selected, itemId, true);
      }
      else {
        Vue.delete(state.selected, itemId);
      }
    },
    setToday: (state, date) => state.today = date,
    setBoolean: (state, { key, value }) => state[key] = value,
    cleanDates: state => {
      const { dates, selected } = state;

      for (let date of dates) {
        date.items = date.items.filter(d => selected[d.id] === undefined)
      }

      state.dates = dates.filter(d => d.items.length > 0);

      state.selected = {};
    },
    pushItem: (state, model) => {
      const [date] = state.dates.filter(d => d.date === model.item.date);
      if (date) {
        date.items.push(model.item);
      }
      else {
        if (moment(model.item.date, 'YYYY-MM-DD').format('YYYY-MM') === moment(state.today, 'YYYY-MM-DD').format('YYYY-MM')) {
          state.dates.push({
            date: model.item.date,
            items: [model.item]
          });
          state.dates.sort((left, right) => (left.date > right.date) - (left.date < right.date));
        }
      }
    },
    editItem: (state, { itemIndex, dateIndex, item }) => {
      let dateItems = state.dates[dateIndex];

      if (item.date === dateItems.date) {
        dateItems.items[itemIndex] = item;
      }
      else {
        dateItems.items.splice(itemIndex, 1);
        if (!dateItems.items.length) {
          state.dates.splice(dateIndex, 1);
        }

        [dateItems] = state.dates.filter(d => d.date === item.date);

        if (dateItems) {
          dateItems.items.push(item);
        }
        else {
          state.dates.push({
            date: item.date,
            items: [item]
          })
        }
      }

      state.dates.sort((left, right) => (left.date > right.date) - (left.date < right.date));
    }
  },
  actions: {
    toggleEditing: ({ commit }) => commit('toggle', 'isEditing'),
    toggleDeleting: ({ commit }) => commit('toggle', 'isDeleting'),
    async fetchAllByDate({ commit }, { year, month }) {
      const yearMonth = moment().year(year).month(month).subtract(1, 'month');

      commit('fetchStarted');

      const dates = await io.items.fetchMonth({ year, month });
      dates.sort((left, right) => (left.date > right.date) - (left.date < right.date))
        .forEach(date => date.items.forEach(item => {
          item.price = Number(item.price)
        }));

      commit('setDates', dates);
      commit('setCurrentDate', yearMonth)
    },
    setToday: ({ commit }, date) => commit('setToday', date),
    selectItem: ({ commit }, itemId) => commit('selectItem', itemId),
    async submit({ commit }, { item, callback }) {
      commit('setBoolean', { key: 'isSubmitting', value: true });

      const model = await io.items.add(item);
      model.item.price = Number(model.item.price);
      commit('pushItem', model);
      console.log('submitItem', { item, model });
      callback();
      commit('setBoolean', { key: 'isSubmitting', value: false });

      return model.item.id;
    },

    async deleteSelected({ commit, state }) {
      const toDelete = Object.keys(state.selected);

      commit('setBoolean', { key: 'isLoading', value: true });
      await io.items.remove(toDelete);
      commit('cleanDates');
      commit('setBoolean', { key: 'isLoading', value: false });
    },
    async editItem({ commit }, model) {
      const item = await io.items.edit(model.model);
      console.log('editItem', { item, model });
      commit('editItem', { item, ...model });
    }
  }
}
