import io from '@/services/io';

function copyObject (target, source) {
  for (const key in source) {
    if (source.hasOwnProperty(key)) {
      if (typeof source[key] === 'function') continue;
      else if (typeof source[key] === 'object' && target[key] != null) copyObject(target[key], source[key]); // If there's any loop in there, well ...
      // TODO Array?
      else target[key] = source[key];
    }
  }
  return target;
}

export default {
  namespaced: true,
  state: {
    isImporting: false,
    importResponse: {}
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

    editResponse: (state, item) => {
      const stateItems = state.importResponse.items;
      const index = stateItems.findIndex((elem) => {
        return elem.id === item.id;
      });
      // we get back a new object, and we need to get setters to be invoked
      var storedItem = stateItems[index];
      copyObject(storedItem, item);
    },

    hideUi: state => {
      state.importResponse = {};
    }
  },

  actions: {
    setProperty: ({
      commit
    }, model) => commit('setProperty', model),

    async doImport ({ commit }, { type, file }) {
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

    async continueEdit ({ commit }) {
      const model = await io.smartImport.fetchAll();
      commit('setProperty', {
        key: 'importResponse',
        value: model
      });
    },

    async saveItem ({ commit }, { item, storeItem }) {
      const model = await io.smartImport.saveItem(item, storeItem);
      commit('editResponse', model);
    },

    async deleteItem ({ commit }, { itemIndex, item }) {
      await io.smartImport.deleteItem(item);
    },

    hideUi ({
      commit
    }) {
      commit('hideUi');
    }

  }
};
