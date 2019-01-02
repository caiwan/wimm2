import io from '@/services/io';

export default {
  namespaced: true,
  state: {
    isImporting: false,
    importResponse: {},
    // type: 0,
  },
  getters: {
    importError: state => state.importResponse.error,
    importCount: state => state.importResponse.items ? state.importResponse.items.length : 0,
    importedItems: state => state.importResponse.items
  },
  mutations: {
    setProperty: (state, {
      key,
      value
    }) => state[key] = value,

    hideUi: state => {
      state.importResponse = {};
    }
  },
  actions: {
    setProperty: ({
      commit
    }, model) => commit('setProperty', model),

    async doImport({ commit }, { type, file }) {
      commit('setProperty', {
        key: 'isImporting',
        value: true
      });

      try {
        const model = await io.smartImport.addFromFile(type, file);

        commit('setProperty', {
          key: 'importResponse',
          value: model
        });
      } finally {
        commit('setProperty', {
          key: 'isImporting',
          value: false
        });
      }
    },

    // async doImport({ commit }) {
    //   commit('setProperty', {
    //     key: 'isImporting',
    //     value: true
    //   });

    //   try {
    //     const model = await io.smartImport.fetchAll();

    //     commit('setProperty', {
    //       key: 'importResponse',
    //       value: model
    //     });
    //   } finally {
    //     commit('setProperty', {
    //       key: 'isImporting',
    //       value: false
    //     });
    //   }
    // },

    async continueEdit() {
      console.error('Not implemented');
    },

    async saveItem() {
      // hello
    },

    hideUi({
      commit
    }) {
      commit('hideUi')
    }
  }
}
