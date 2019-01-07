import Vue from 'vue';
import Router from 'vue-router';

import BudgetEditor from '@/components/budget/component'
import BudgetEditorHeader from '@/components/budget/header'
import CategoryEditor from '@/components/categories/component';
import CategoryEditorHeader from '@/components/categories/header';
import ImportExport from '@/components/import-export/component';
import ImportExportHeader from '@/components/import-export/header';
import ItemList from '@/components/item-list/component';
import ItemListHeader from '@/components/item-list/header';
import store from '@/store';
import SmartImport from '@/components/smart-import/component';
import SmartImportHeader from '@/components/smart-import/header';
import TagSum from '@/components/tag-sum/component';
import TagSumHeader from '@/components/tag-sum/header';
import TagSumOverTime from '@/components/tag-sum-over-time/component';
import TagSumOverTimeHeader from '@/components/tag-sum-over-time/header'
import TotalSum from '@/components/total-sum/component';
import TotalSumHeader from '@/components/total-sum/header';

Vue.use(Router);

export default new Router({
  mode: 'hash',
  routes: [{
    name: 'index',
    path: '/',
    redirect() {
      const now = store.state.itemList.currentDate;

      return {
        name: 'item:list:year-month',
        params: {
          year: now.format('YYYY'),
          month: now.format('MM')
        }
      }
    }
  },
  {
    name: 'item:list:year-month',
    path: '/:year(\\d+)/:month(\\d+)/',
    components: {
      default: ItemList,
      header: ItemListHeader
    }
  },
  {
    name: 'graph:total-sum',
    path: '/graph/total-sum/',
    components: {
      default: TotalSum,
      header: TotalSumHeader
    }
  },
  {
    name: 'graph:tag-total',
    path: '/graph/tag-total/',
    components: {
      default: TagSum,
      header: TagSumHeader
    }
  },
  {
    name: 'graph:tag-time',
    path: '/graph/tag-sum-over-time/',
    components: {
      default: TagSumOverTime,
      header: TagSumOverTimeHeader
    }
  },
  {
    name: 'import-export',
    path: '/import-export/',
    components: {
      default: ImportExport,
      header: ImportExportHeader
    }
  },
  {
    name: 'smart-import',
    path: '/smartimport/',
    components: {
      default: SmartImport,
      header: SmartImportHeader
    }
  }, {
    name: 'category-editor',
    path: '/categories/',
    components: {
      default: CategoryEditor,
      header: CategoryEditorHeader
    }
  },
  {
    name: 'budget-editor',
    path: '/budget/',
    components: {
      default: BudgetEditor,
      header: BudgetEditorHeader
    }
  }
  ]
});
