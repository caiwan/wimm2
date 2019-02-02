<template>
  <div
    :style='styleObj'
    :draggable='isDraggable'
    @drag.stop='drag'
    @dragstart.stop='dragStart'
    @dragover.stop='dragOver'
    @dragenter.stop='dragEnter'
    @dragleave.stop='dragLeave'
    @drop.stop='drop'
    @dragend.stop='dragEnd'
    class='dnd-container zebra'
  >
    <div
      :class='{"is-clicked": isClicked,"is-hover":isHover}'
      @click="toggle"
      @mouseover='mouseOver'
      @mouseout='mouseOut'
      @dblclick="changeType"
    >
      <div
        :style="{ 'padding-left': (this.depth - 1) * 24 + 'px' }"
        :id='model.id'
        class='treeNodeText'
      >
        <span :class="[isClicked ? 'nodeClicked' : '', isFolder ? 'nodeFolderIcon' : 'nodeFolderIconPlaceholder']"></span>
        <span class='text'>{{model.name}}</span>
      </div>
    </div>
    <div
      class='treeMargin'
      v-if="isFolder"
      v-show="open"
    >
      <drag-node
        v-for="item2 in model.children"
        :allowDrag='allowDrag'
        :allowDrop='allowDrop'
        :depth='increaseDepth'
        :model="item2"
        :key='item2.id'
        :defaultText='defaultText'
        :disableDBClick='disableDBClick'
      >
      </drag-node>
    </div>
  </div>
</template>

<script>
let id = 1000
let fromData = null
let toData = null
let nodeClicked = undefined // Attention: let
let rootTree = null // vue-drag-tree

import { findRoot, exchangeData } from './drag-tree-util';
export default {
  name: 'DragNode',
  data() {
    return {
      open: false,
      isClicked: false, //
      isHover: false, // hvoer
      styleObj: {
        opacity: 1
      }
    }
  },
  props: {
    model: Object,
    allowDrag: {
      type: Function,
      default: () => true
    },
    allowDrop: {
      type: Function,
      default: () => true
    },
    defaultText: {
      //
      type: String,
      default: 'New Node'
    },
    depth: {
      type: Number,
      default: 0
    },
    disableDBClick: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    isFolder() {
      return this.model.children && this.model.children.length
    },
    increaseDepth() {
      return this.depth + 1
    },
    isDraggable() {
      return this.allowDrag(this.model, this)
    }
  },
  methods: {
    toggle() {
      if (this.isFolder) {
        this.open = !this.open
      }
      rootTree.emitCurNodeClicked(this.model, this)
      this.isClicked = !this.isClicked

      if (nodeClicked != this.model.id) {
        let treeParent = rootTree.$parent

        //
        let nodeStack = [treeParent.$children[0]]
        while (nodeStack.length != 0) {
          let item = nodeStack.shift()
          item.isClicked = false
          if (item.$children && item.$children.length > 0) {
            nodeStack = nodeStack.concat(item.$children)
          }
        }
        //
        this.isClicked = true

        //
        nodeClicked = this.model.id
      }
    },

    changeType() {

      console.log('Sup bro - this should enter edit mode ');

      if (this.disableDBClick) {
        return;
      }
      // -->
      if (this.currentHighlight) {
        nodeClicked = this.model.id;
      }
      if (!this.isFolder) {
        this.$set(this.model, 'children', []);
        this.addChild();
        this.open = true;
        this.isClicked = true;
      }
    },
    mouseOver(e) {
      this.isHover = true;
    },
    mouseOut(e) {
      this.isHover = false;
    },
    addChild() {
      this.model.children.push({
        name: this.defaultText,
        id: id++
      });
    },
    removeChild(id) {
      // model.children
      let parent_model_children = this.$parent.model.children;

      // model.children
      for (let index in parent_model_children) {
        // id
        if (parent_model_children[index].id == id) {
          parent_model_children = parent_model_children.splice(index, 1);
          break;
        }
      }
    },
    drag(e) {
      fromData = this;
      rootTree.emitDrag(this.model, this, e);
    },
    dragStart(e) {
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', 'asdad'); // LOL WUT?
      return true;
    },
    dragOver(e) {
      e.preventDefault();
      rootTree.emitDragOver(this.model, this, e);
      return true;
    },
    dragEnter(e) {
      if (this._uid !== fromData._uid) {
        this.styleObj.opacity = 0.5;
      }
      rootTree.emitDragEnter(this.model, this, e)
    },
    dragLeave(e) {
      this.styleObj.opacity = 1
      rootTree.emitDragLeave(this.model, this, e)
    },
    drop(e) {
      e.preventDefault();
      this.styleObj.opacity = 1;
      if (!this.allowDrop(this.model, this)) {
        return;
      }
      toData = this;
      exchangeData(rootTree, fromData, toData);
      rootTree.emitDrop(this.model, this, e);
    },
    dragEnd(e) {
      rootTree.emitDragEnd(this.model, this, e);
      return;
    }
  },
  updated() {
    rootTree.nodeUpdated();
  },
  created() {
    rootTree = findRoot(this);
  },
  directives: {
    focus: function (el, binding) {
      if (binding.value) {
        el.focus();
      }
    }
  }
}
</script>
