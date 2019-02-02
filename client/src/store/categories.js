import io from '@/services/io';

export default {
  namespaced: true,

  state: {
    items: [],
    itemMap: [],
    itemTree: [],
    isLoading: false,
    isLoaded: false
  },

  getters: {
  },

  mutations: {
    clear: (state) => { state.items = []; state.itemMap = []; state.itemTree = []; },
    put: (state, item) => {
      if (!item.hasOwnProperty('children')) { item['children'] = []; }
      state.itemMap[item.id] = item;
      if (item.parent) {
        const pid = item.parent.id;
        state.itemMap[pid].children.push(state.itemMap[item.id]);
      } else {
        state.itemTree.push(state.itemMap[item.id]);
      }
      state.items.push(item);
      // console.log('item', item.id);
    },

    edit: (state, item) => {
      var storedItem = state.itemMap[item.id];
      for (var key in item) {
        if (item.hasOwnProperty(key)) {
          storedItem[key] = item[key];
        }
      }
    },

    rm: (state, item) => {
      state.items.splice(state.items.indexOf(item), 1);
      state.itemTree.splice(state.itemTree.indexOf(item), 1);
    }

  },

  actions: {
    async reload({ dispatch, state }) {
      state.isLoaded = false;
      await dispatch('fetchAll');
    },
    async fetchAll({ commit, state }) {
      // TODO: This shit will fetch all the things over 9000 times
      if (state.isLoading || state.isLoaded) { return; }
      state.isLoading = true;
      const categories = await io.categories.fetchAll();
      commit('clear');
      categories.forEach(category => {
        commit('put', category);
      });
      state.isLoading = false;
      state.isLoaded = true;
    },

    async addNew({ commit, state }, { parent, name }) {
      name = name && name.trim();
      if (!name) return;
      const item = await io.categories.add({ name, parent });
      commit('put', item);
    },

    async edit({ commit, state }, item) {
      console.log('Lozl', item);
      item.name = item.name.trim();
      if (!item.name) {
        await io.categories.remove(item);
        // TODO: Sup bro, you sure?
        commit('remove', item);
      } else {
        const edited = await io.categories.edit(item);
        commit('edit', edited);
      }
    },

    async remove({ commit, state }, category) {
      await io.categories.remove(category);
      commit('rm', category);
    }
  }
};
