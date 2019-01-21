import moment from 'moment';

import io from '@/services/io';

export default {
  namespaced: true,
  state: {
    isExporting: false,
    isImporting: false,
    exportedData: [],
    importResponse: {}
  },
  getters: {
    exportFilename: state => `wimm_categories.json`,
    importError: state => state.importResponse.error,
    importCount: state => state.importResponse.imported
  },
  mutations: {
    setProperty: (state, { key, value }) => state[key] = value,
    setData: (state, { models }) => {
      // TODO: This should be a part of some Writer class

      const data = [];
      for (let item of models) {
        // console.log('Helloka', item);
        data.push({
          'id': item.id,
          'title': item.title,
          'comment': item.comment,
          'parent': item.parent ? { 'id': item.parent.id } : null
        });
      }

      state.exportedData = [JSON.stringify(data)];
    },
    hideUi: state => {
      state.exportedData = [];
      state.importResponse = {};
    }
  },
  actions: {
    setProperty: ({ commit }, model) => commit('setProperty', model),
    async doExport({ commit, state }) {
      commit('setProperty', { key: 'isExporting', value: true });

      try {
        const models = await io.categories.fetchAll()
        commit('setData', { models });
      }
      finally {
        commit('setProperty', { key: 'isExporting', value: false });
      }
    },
    async doImport({ commit, dispatch }, file) {
      commit('setProperty', { key: 'isImporting', value: true });

      try {
        const model = await io.categories.addFromFile(file);
        commit('setProperty', { key: 'importResponse', value: model });
        // TODO Put this response into the category store without 
        // requiring to reload everything once again
      }
      finally {
        commit('setProperty', { key: 'isImporting', value: false });
      }

      await dispatch('categories/reload', {}, { root: true });
    },
    hideUi({ commit }) {
      commit('hideUi')
    }
  }
}
