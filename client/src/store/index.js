import Vue from 'vue';
import Vuex from 'vuex';

import app from './app';
import categories from './categories';
import categoriesImportExport from './categories-import-export';
import smartImport from './smartImport';
import totalSum from './total-sum';
import tagSumOverTime from './tag-sum-over-time';
import tagSum from './tag-sum';
import itemList from './item-list';
import tags from './tags';
import ui from './ui';
import importExport from './import-export';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    app,
    categories,
categoriesImportExport,
    importExport,
    itemList,
    smartImport,
    tags,
    tagSum,
    tagSumOverTime,
    totalSum,
    ui
  }
});
