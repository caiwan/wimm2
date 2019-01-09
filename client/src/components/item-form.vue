<template>
  <form
    class="item-form"
    @submit.prevent="submit"
  >
    <categories
      class="category-selector"
      v-on:itemSelected="categorySelected"
      :category="pCategory"
    ></categories>
    <tags
      :choices="autocomplete()"
      :tags="pTags"
      :disabled="disabled"
      @blur="focusPrice()"
    ></tags>
    <input
      type="text"
      class="date numeric"
      autocomplete="off"
      placeholder="Date"
      required
      v-if="!datehidden"
      @input="dateChanged($event.target.value)"
      :value="pDate"
      :disabled="disabled"
    >
    <input
      class="price numeric"
      autocomplete="off"
      placeholder="Price"
      ref="price"
      required
      v-model="pPrice"
      :disabled="disabled"
    >
  </form>
</template>

<script>
import TagInput from './tag-input';
import CategorySelector from './category-selector';
import mathjs from 'mathjs';
import { mapGetters } from "vuex";

export default {
  components: {
    Tags: TagInput,
    Categories: CategorySelector
  },
  props: {

    date: {
      type: String,
      required: false,
      default: () => ''
    },
    price: {
      type: [Number, String],
      required: false,
      default: () => null
    },
    tags: {
      type: Array,
      required: false,
      default: () => []
    },
    category: {
      type: Object,
      required: false,
      default: () => null
    },

    disabled: Boolean,
    datehidden: String
  },
  data() {
    return {
      pPrice: this.price,
      pTags: this.tags.slice(),
      pDate: this.date,
      pCategory: this.category
    }
  },
  methods: {
    ...mapGetters('tags', ['autocomplete']),
    dateChanged(value) {
      this.pDate = value;
    },
    rawPrice() {
      let trimmedValue = String(this.pPrice).trim();
      let literalValue = mathjs.eval(trimmedValue);

      let sign = trimmedValue[0];

      if (!(sign === '+') && !(sign === '-')) {
        literalValue = -1 * literalValue;
      }

      return literalValue;
    },
    categorySelected(category) {
      console.log('Category selected', { id: category.id, title: category.title });
      this.pCategory = category;
    },
    submit(event) {
      event.preventDefault();
      if (this.pCategory == null) {
        console.error('No category selected');
        return;
      }
      let item = {
        price: this.rawPrice(),
        date: this.pDate,
        tags: this.pTags,
        category: { id: this.pCategory.id }
      };

      this.$emit('submit', {
        item,
        callback: () => {
          this.pPrice = null;
          this.pTags.splice(0, this.pTags.length);
        }
      });
    },
    focusPrice() {
      this.$refs.price.focus();
    }
  },
  watch: {
    date(nextValue) {
      this.pDate = nextValue;
    }
  }
};

</script>

<style lang="scss" scoped>
</style>
