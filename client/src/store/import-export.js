import moment from 'moment';

import io from '@/services/io';

export default {
  namespaced: true,
  state: {
    isExporting: false,
    isImporting: false,
    dateFrom: moment().subtract(1, 'month').format('YYYY-MM-DD'),
    dateTo: moment().format('YYYY-MM-DD'),
    exportType: 'csv',
    exportedData: [],
    importResponse: {}
  },
  getters: {
    exportFilename: state => `wimm_export_${state.dateFrom}_${state.dateTo}.${state.exportType}`,
    importError: state => state.importResponse.error,
    importCount: state => state.importResponse.imported
  },
  mutations: {
    setProperty: (state, {key, value}) => state[key] = value,
    setData: (state, {models}) =>{
      // TODO: This should be a part of some Writer class
      const data = ['date,price,tags\n'];

      if(state.exportType === 'csv'){
        for(let {date, items} of models){
          for(let {price, tags} of items){
            tags.sort();
            const tagsEscaped = JSON.stringify(tags.join(','));

            data.push(`${date},${price},${tagsEscaped}\n`);
          }
        }
      }

      state.exportedData = data;
    },
    hideUi: state => {
      state.exportedData = [];
      state.importResponse = {};
    }
  },
  actions: {
    setProperty: ({commit}, model) => commit('setProperty', model),
    async doExport({commit, state}){
      commit('setProperty', {key: 'isExporting', value: true});

      try {
        const models = await io.items.fetchRange({
          dateFrom: state.dateFrom,
          dateTo: state.dateTo
        });

        commit('setData', {models});
      }
      finally {
        commit('setProperty', {key: 'isExporting', value: false});
      }
    },
    async doImport({commit}, file){
      commit('setProperty', {key: 'isImporting', value: true});

      try {
        const model = await io.items.addFromFile(file);

        commit('setProperty', {key: 'importResponse', value: model});
      }
      finally {
        commit('setProperty', {key: 'isImporting', value: false});
      }
    },
    hideUi({commit}){
      commit('hideUi')
    }
  }
}
