<template>
  <div>
    <div id="item-list">
      <div id="date-items">
        <date-items
          v-for="(dateItems, index) of dates"
          :key="dateItems.date"
          :index="index"
        ></date-items>
      </div>

      <div
        id="main-item-form"
        v-show="canNavigate"
      >
        <item-form
          id="item-form-0"
          :date="today"
          @dateChanged="setToday"
          :disabled="isSubmitting"
          @submit="doSubmit"
        ></item-form>
        <button
          type="submit"
          form="item-form-0"
          class="i i-add"
          :disabled="isSubmitting"
        >
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';
import store from '@/store';

import ItemForm from '../item-form';
import DateItems from './components/date-items';
import io from '@/services/io';
import { mapActions, mapGetters, mapState } from "vuex";

export default {
  components: {
    ItemForm, DateItems
  },
  computed: {
    ...mapState('itemList', [
      'isSubmitting', 'dates', 'today'
    ]),
    ...mapGetters('itemList', [
      'canNavigate'
    ]),
    ...mapState('app', ['isInitializing'])
  },
  methods: {
    ...mapActions('itemList', ['fetchAllByDate', 'setToday', 'submit']),

    async doSubmit(...args) {
      const itemId = await this.submit(...args);
      this.$nextTick(() => {
        const elem = document.getElementById(`item-${itemId}`);
        if (elem !== null) {
          elem.scrollIntoView(false);
        }
      })
    }
  },

  created() {
    this.fetchAllByDate(this.$route.params);
  },
  watch: {
    $route(route) {
      this.fetchAllByDate(route.params);
    }
  }
};
</script>

<style lang="scss" rel="stylesheet/scss">
</style>
