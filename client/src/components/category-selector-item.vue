<template>
  <li
    class="selector-item zebra"
    v-if="maxDepth<0 || lod<=maxDepth"
  >
    <span
      :class="{folder: hasChildren, selected: model === selectedItem}"
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
        :selectedItem="selectedItem"
        :lod="lod+1"
      />
    </ul>
  </li>
</template>

<script>
export default {
  name: "CategoryItem",
  props: {
    model: { required: true, type: Object },
    maxDepth: { default: -1, type: Number },
    lod: { default: 0, type: Number },
    selectedItem: { default: null, type: Object }
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
  // watch: {
  //   model(vOld, vNew) {
  //     console.log('Lolz 2 updated', this.maxDepth);
  //   },
  //   maxDepth(vold, vnew) {
  //     console.log('Lolz updated', this.maxDepth);
  //   }
  // },

  // updated() {
  //   console.log('Lolz3 updated', this.maxDepth);
  // }
};
</script>

<style lang="scss" scoped>
.selector-item {
  .selected {
    color: red;
  }
}
</style>
