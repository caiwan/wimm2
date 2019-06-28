export default {
  namespaced: true,
  state: {
    sidebarVisible: false
  },
  getters: {
    overlayVisible (state, getters, rootState) {
      return state.sidebarVisible ||
        rootState.app.isInitializing ||
        rootState.itemList.isLoading ||
        rootState.totalSum.isCalendarVisible ||
        rootState.tagSum.isCalendarVisible ||
        rootState.tagSumOverTime.isCalendarVisible;
    },
    spinnerVisible (state, getters, rootState) {
      return rootState.app.isInitializing ||
        rootState.itemList.isLoading;
    }
  },
  mutations: {
    toggle: (state, property) => state[property] = !state[property],
    hideUi: state => state.sidebarVisible = false
  },
  actions: {
    toggleSidebar: ({ commit }) => commit('toggle', 'sidebarVisible'),
    hideUi: ({ commit }) => commit('hideUi')
  }
};
