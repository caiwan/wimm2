<template>
  <li
    class="selector-item zebra"
    v-if="maxDepth<=0 || lod<maxDepth"
  >
    <span
      :class="{folder: hasChildren}"
      @click="select(model)"
    >{{ model.title }}
    </span>
    <ul
      class="selector-group"
      v-if="hasChildren"
    >
      <category-item
        v-for="child in model.children"
        :key="child.id"
        :model="child"
        :max-depth="maxDepth"
        v-on:itemSelected="select"
        :lod="lod+1"
      />
    </ul>
  </li>
</template>

<script>
export default {
  name: "CategoryItem",
  props: {
    model: Object,
    maxDepth: Number,
    lod: { default: 0, type: Number },
  },
  data() {
    return {
      open: false,
      isEditing: false,
      beforeEditCache: null,
      isAddingChild: false,
      newChild: '',
    }
  },
  computed: {
    hasChildren() {
      return this.model.children && this.model.children.length;
    }
  },
  methods: {
    select(item) {
      this.$emit('itemSelected', item);
    },

  },
};
</script>

<style lang="scss" scoped>
</style>
