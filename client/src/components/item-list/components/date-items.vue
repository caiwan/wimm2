<template>
  <div class="date-items">
    <div class="numeric date-items-head">
      <div class="date">{{ date }}</div>
      <div
        class="daily-expense"
        v-if="dailyExpense"
      >
        {{ dailyExpense | money }}
      </div>
      <div v-else>
        &nbsp;
      </div>
    </div>
    <ul class="items">
      <li
        v-for="(item, itemIndex) of items"
        :key="item.id"
        :id="'item-' + item.id"
        :class="{selected: isSelected(item.id), submitting: submitting[item.id]}"
        @click="selectSelf(item.id)"
      >
        <div class="item">
          <template v-if="editors[item.id]">
            <item-form
              :id="'item-form-' + item.id"
              :tags="item.tags"
              :price="Number(item.price) < 0 ? -1 * Number(item.price) : '+' + item.price"
              :date="item.date"
              :category="item.category"
              :disabled="submitting[item.id]"
              @submit="submit(itemIndex, item, $event)"
            ></item-form>
          </template>
          <template v-else>
            <div class="category">
              {{item.category ? item.category.title : "Unassigned"}}&nbsp;
            </div>
            <div class="tag-list">
              <span
                v-for="(tag, index) in item.tags"
                :key="index"
              >{{ tag }}</span>
            </div>
            <span
              class="numeric price"
              :class="{positive: item.price > 0}"
            >
              {{ item.price | money }}
            </span>
          </template>
        </div>

        <div
          class="button-group"
          v-if="isDeleting || isEditing"
        >
          <button
            class="i selected"
            v-if="isDeleting"
            :class="{'i-check_box_outline_blank': !isSelected(item.id), 'i-check_box': isSelected(item.id)}"
          ></button>

          <button
            class="i"
            :class="{'i-mode_edit': !editors[item.id], 'i-close': editors[item.id]}"
            v-if="isEditing"
            @click="editSelf(item.id, $event)"
          ></button>

          <button
            type="submit"
            class="i i-save"
            v-if="editors[item.id]"
            :form="'item-form-' + item.id"
            :disabled="submitting[item.id]"
          ></button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import ItemForm from '@/components/item-form';
import { mapActions, mapGetters, mapState } from "vuex";

let formatter = Intl.NumberFormat();

export default {
  props: {
    index: Number
  },
  components: {
    ItemForm
  },
  data() {
    return {
      editors: {},
      submitting: {}
    }
  },
  computed: {
    ...mapState('itemList', {
      model: function (state) {
        return state.dates[this.index]
      },
      isEditing: 'isEditing',
      isDeleting: 'isDeleting'
    }),
    ...mapGetters('itemList', [
      'isSelected'
    ]),
    date() {
      return this.model.date
    },
    items() {
      return this.model.items;
    },
    dailyExpense() {
      return this.items.reduce((sum, item) =>
        item.price < 0 ? sum + Number(item.price) : sum,
        0);
    }
  },
  methods: {
    ...mapActions('itemList', [
      'selectItem', 'editItem'
    ]),

    // -- these should be in the state manager instead

    selectSelf(id) {
      if (this.isDeleting) {
        this.selectItem(id)
      }
      else if (this.isEditing) {
        if (!this.editors[id]) {
          this.$set(this.editors, id, true);
        }
      }
    },
    editSelf(id, e) {
      if (this.isEditing) {
        e.stopPropagation();

        if (this.editors[id]) {
          this.$delete(this.editors, id);
        }
        else {
          this.$set(this.editors, id, true);
        }
      }
    },
    async submit(itemIndex, oldItem, { item }) {
      let { id } = oldItem;

      this.$set(this.submitting, id, true);
      await this.editItem({ itemIndex, dateIndex: this.index, model: { id, ...item } });
      this.$delete(this.submitting, id);
      this.$delete(this.editors, id);
    }
  },

  // ---

  filters: {
    money(value) {
      value = formatter.format(value);

      if (value[0] !== '-') {
        value = '+' + value;
      }

      return value;
    }
  },
  watch: {
    isEditing() {
      this.editors = {};
    }
  }
}
</script>


<style lang="scss" rel="stylesheet/scss">
@import "../../../scss/consts";

.date-items {
  border: $date-items-border;
  background: $date-items-background;
  margin-bottom: $date-items-bottom-margin;

  &:last-child {
    margin: 0;
  }

  .date-items-head {
    position: relative;
    text-align: center;
    padding: $date-items-head-padding;
    border-bottom: $date-items-head-bottom-border;
    display: flex;

    .date {
      position: absolute;
      left: 0;
      right: 0;
    }

    .daily-expense {
      margin-left: auto;
      // z-index: $layer-10;
      color: royalblue;
    }
  }

  .items {
    margin: 0;
    padding: 0;
    list-style-type: none;

    & > li {
      display: flex;
      position: relative;
      padding: $date-items-li-padding;

      &.selected {
        background: $date-items-li-selected-background;
      }

      &.submitting {
        background: $date-items-li-submitting-background;
      }

      &:nth-of-type(odd) {
        background: $date-items-li-odd-background;

        &.selected {
          background: $date-items-li-selected-odd-background;
        }

        &.submitting {
          background: $date-items-li-submitting-odd-background;
        }
      }

      .item {
        flex-grow: 1;
        display: flex;
        flex-wrap: wrap;

        .category {
          color: seagreen;
        }

        .tag-list {
          flex-grow: 1;

          span {
            &::after {
              content: ", ";
            }

            &:last-child::after {
              content: "";
            }
          }
        }

        .item-form {
          flex-grow: 1;
        }

        .price {
          margin-left: auto;
        }

        .tags {
          background: $main-item-form-input-background;
          margin-bottom: $main-item-form-input-bottom-margin;

          &.disabled {
            background: #ebebe4;

            .tag {
              background: #d3d3d0;
              color: #595959;
            }
          }
        }
      }

      .button-group {
        margin: -1 * $date-items-li-padding -1 * $date-items-li-padding -1 *
          $date-items-li-padding $date-items-li-padding;
        border-left: $date-items-button-group-left-border;
        display: flex;
        flex-direction: column;

        button {
          border: none;
          outline: none;
          cursor: pointer;
          flex-grow: 1;
          -webkit-tap-highlight-color: transparent;

          background: $date-items-button-background;
          padding: $date-items-li-padding;
          font-size: $date-items-button-font-size;

          &:active {
            background: $date-items-button-active-background;
          }
        }
      }
    }
  }
}
</style>
