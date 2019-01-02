import io from '@/services/io';

export default {
  namespaced: true,
  getters: {
    autocomplete: state => term => io.tags.autocomplete(term),
    all: state => io.tags.fetchAll(),
  },

  mutations: {
    remove: state => term => io.tags.remove(term),
    merge: state => term => io.tags.merge(term, ""),
  }
}
