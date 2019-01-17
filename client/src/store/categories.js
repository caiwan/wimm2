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
    clear: (state) => { state.items = [], state.itemMap = [], state.itemTree = [] },
    put: (state, item) => {
      if (!item.hasOwnProperty('children'))
        item['children'] = []
      state.itemMap[item.id] = item;
      if (item.parent) {
        const pid = item.parent.id
        state.itemMap[pid].children.push(state.itemMap[item.id]);
      } else {
        state.itemTree.push(state.itemMap[item.id]);
      }
      state.items.push(item);
      // console.log('item', item.id);
    },

    edit: (state, item) => {
      const index = item.id;
      var storedItem = state.items[index];
      for (var key in item) {
        if (item.hasOwnProperty(key)) {
          storedItem[key] = item[key];
        }
      }
    },

    rm: (state, item) => {
      state.items.splice(state.items.indexOf(item), 1)
      state.itemTree.splice(state.itemTree.indexOf(item), 1)
    },

  },

  actions: {
    async fetchAll({ commit, state }) {
      // TODO: This shit will fetch all the things over 9000 times
      if (state.isLoading || state.isLoaded)
        return;
      state.isLoading = true;
      const categories = await io.categories.fetchAll();
      commit('clear');
      categories.forEach(category => {
        commit('put', category);
      });
      state.isLoading = false;
      state.isLoaded = true;
    },

    async addNew({ commit, state }, { parent, value }) {
      value = value && value.trim();
      if (!value) {
        return;
      }
      const item = await io.categories.add({
        title: value,
        parent: parent
      });

      commit('put', item);
    },

    async edit({ commit, state }, item) {
      item.title = item.title.trim();
      if (!item.title) {
        await io.categories.remove(item);
        commit('remove', item);
      } else {
        const edited = await io.categories.edit(item);
        commit('edit', edited);
      }
    },

    async remove({ commit, state }, category) {
      await io.categories.remove(item)
      commit('rm', item);
    }
  }
}
