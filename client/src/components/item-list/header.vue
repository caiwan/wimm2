<template>
  <div id="item-list-header">
    <div class="header-label">{{ currentDateFormatted }}</div>

    <button class="i"
            :class="{'i-mode_edit': !isEditing, 'i-close': isEditing}"
            :disabled="isEditingDisabled"
            @click="toggleEditing()">
    </button>
    <button class="i"
            :class="{'i-delete': !isDeleting, 'i-close': isDeleting}"
            :disabled="isDeletingDisabled"
            @click="toggleDeleting()">
    </button>

    <div class="fill"></div>

    <button class="i i-keyboard_arrow_left"
            v-if="canNavigate"
            @click="seekMonth(-1)">
    </button>
    <button class="i i-navigate_next"
            v-if="canNavigate"
            @click="seekMonth(1)">
    </button>
    <button id="delete-confirm" class="i i-check"
            v-if="isDeleting"
            @click="deleteSelected()">
    </button>
	<button id="save-all" class="i i-check"
            v-if="isEditing"
            @click="saveAll()">
    </button>
  </div>
</template>

<script>
  import moment from 'moment';
  import {mapActions, mapGetters, mapState} from "vuex";

  export default {
    computed: {
      ...mapState('itemList', [
        'isEditing', 'isDeleting', 'currentDate'
      ]),
      ...mapGetters('itemList', [
        'isEditingDisabled', 'isDeletingDisabled', 'canNavigate', 'currentDateFormatted'
      ])
    },
    methods: {
      ...mapActions('itemList', [
        'toggleEditing', 'saveAll', 'toggleDeleting', 'deleteSelected'
      ]),
      seekMonth(direction){
        let nextMonth = this.currentDate.clone();

        if(direction > 0){
          nextMonth.add(1, 'month');
        }
        else if(direction < 0){
          nextMonth.subtract(1, 'month');
        }
        else {
          throw new Error('direction must be +1 or -1');
        }

        this.$router.push({
          name: 'item:list:year-month', params: {
            year: nextMonth.format('YYYY'),
            month: nextMonth.format('MM')
          }
        });
      }
    }
  }
</script>


<style lang="scss" rel="stylesheet/scss">
  @import '../../scss/consts';
</style>
