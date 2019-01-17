<template>
  <div
    id="smart-import"
    class="content"
  >
    <section class="date-items">
      <ul class="items">
        <li
          v-for="item in importedItems"
          :key="item.id"
          :id="'item-' + item.id"
        >
          <div class="item">
            <span
              class="imported-text"
              :class="{'deleted' : deleted[item.id]}"
            >
              {{item.text}} &nbsp;
            </span>
            <template v-if="!deleted[item.id]">
              <template v-if="editors[item.id]">
                <item-form
                  :id="'item-form-' + item.id"
                  :tags="getTags(item)"
                  :price="Number(item.price) < 0 ? -1 * Number(item.price) : '+' + item.price"
                  :date="item.date"
                  :category="item | getCategory"
                  :disabled="submitting[item.id]"
                  @submit="saveItemWrapped(item, $event)"
                ></item-form>
              </template>
              <template v-else>
                <!-- TODO: fix this part  -->
                <div class="category">
                  {{ item | getCategoryTitle }}&nbsp;
                </div>
                <div class="tag-list">
                  <span
                    v-for="(tag, index) in getTags(item)"
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
            </template>
          </div>

          <!-- Submit buttons -->
          <div
            class="button-group"
            v-if="!deleted[item.id]"
          >
            <div class="gap"></div>
            <button
              class="i i-delete"
              @click="deleteItemWrapped(item.id, item, $event)"
            ></button>
            <button
              class="i"
              :class="{'i-mode_edit': !editors[item.id], 'i-close': editors[item.id]}"
              @click="editItem(item.id, $event)"
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
    </section>

    <!-- Import form and buttons -->

    <header>
      <h1>Import</h1>
      <p>Experimantal AI-assisted bulk import and tagging support
      </p>
    </header>

    <section>
      <form @submit.prevent="doImportWrapped">
        <div>
          <select v-model="selectedFormat">
            <option
              value=""
              disabled
              selected
            > -- Please select -- </option>
            <option
              v-for="format in formats"
              :key="format.id"
              :value="format"
            >{{format.name}}</option>
          </select>
          <input
            type="file"
            @change="setImportedFile($event.target.files[0])"
          >
        </div>
        <button :disabled="!importedFile || !selectedFormat || isImporting">
          Import
          <span v-if="isImporting">{{ importProgress }} </span>
        </button>
      </form>

      <div>
        ... or continue edit previous data <br />
        <button
          :disabled="isImporting"
          @click="doContinueEditWrapped"
        >Go
          <span v-if="isImporting">{{ importProgress }} </span>
        </button>
      </div>

      <div v-if="importError">
        Import failed for some with this reason:
        <pre>{{ importError }}</pre>
      </div>

      <div v-if="importCount">
        Imported {{ importCount }} items
      </div>
    </section>

  </div>

</template>

<script>
import ItemForm from '@/components/item-form';

import { mapActions, mapGetters, mapState } from "vuex";

const _progress = () => {
  setTimeout(() => {
    if (this.isImporting) {
      const dots = (this.importProgress.length + 1) % 4;

      this.importProgress = ".".repeat(dots);
      setTimeout(progress, 400);
    } else {
      this.importProgress = "";
    }
  });
};

const formatter = Intl.NumberFormat();

export default {
  components: {
    ItemForm
  },
  data() {
    return {
      // save
      editors: {},
      submitting: {},
      deleted: {},
      // import
      progress: "",
      importProgress: "",
      importedFile: null,
      // TODO: this should be loaded from the backend
      formats: [
        { id: 1, name: "OTP CSV" },
        { id: 2, name: "Regular" },
        { id: 3, name: "Mixed" },
        { id: 4, name: "RAW" },
      ],
      selectedFormat: null
    };
  },
  computed: {
    ...mapState("smartImport", [
      "isImporting"
    ]),
    ...mapGetters("smartImport", [
      "importError", "importCount", "importedItems"
    ])
  },
  methods: {
    ...mapActions("smartImport", [
      "setProperty",
      "doImport", "continueEdit",
      "saveItem", "deleteItem",
      "hideUi"
    ]),

    onChanged(key, value) {
      this.setProperty({ key, value });
    },

    setImportedFile(f) {
      this.importedFile = f;
    },

    async doContinueEditWrapped() {
      _progress();
      await this.continueEdit();
      this.editors = {};
      for (const item of this.importedItems) {
        this.editors[item.id] = item;
      }
      // console.log({ editors: this.editors });
    },

    async doImportWrapped(e) {
      _progress();
      await this.doImport({ type: this.selectedFormat.id, file: this.importedFile });
      this.editors = {};
      for (const item of this.importedItems) {
        this.editors[item.id] = item;
      }
    },

    async saveItemWrapped(item, event) {
      const itemIndex = item.id;
      this.$set(this.submitting, itemIndex, true);
      await this.saveItem({ item, storeItem: event.item });
      this.$delete(this.submitting, item.id);
      this.$delete(this.editors, item.id);
      this.$set(this.submitting, itemIndex, false);
      this.$delete(this.submitting, itemIndex);
    },

    editItem(itemIndex, event) {
      event.stopPropagation();
      if (this.editors[itemIndex]) {
        this.$delete(this.editors, itemIndex);
      }
      else {
        this.$set(this.editors, itemIndex, true);
      }
    },

    async deleteItemWrapped(itemIndex, item, event) {
      event.stopPropagation();
      this.$set(this.submitting, itemIndex, true);
      if (this.editors[itemIndex]) {
        this.$delete(this.editors, itemIndex);
      }
      this.deleteItem({ itemIndex, item });
      this.$delete(this.submitting, itemIndex);
      this.$delete(this.editors, itemIndex);
      this.$set(this.deleted, itemIndex, true);
      this.$delete(this.submitting, itemIndex);
    },

    getTags: (item) => (item.stored_item != null && item.stored_item.tags != null) ? item.stored_item.tags : (item.suggested_tags || []),

  },

  filters: {
    getCategory: (item) => (item.stored_item != null && item.stored_item.category != null) ? item.stored_item.category : (item.suggested_category || null),
    getCategoryTitle: (item) => (item.stored_item != null && item.stored_item.category != null) ? item.stored_item.category.title : (item.suggested_category || 'Unassigned'),

    money(value) {
      value = formatter.format(value);

      if (value[0] !== '-') {
        value = '+' + value;
      }

      return value;
    }
  },

  beforeRouteLeave(to, from, next) {
    this.hideUi();
    next();
  }
};
</script>

<style lang="scss" rel="stylesheet/scss">
@import "../../scss/consts";
@import "../../scss/date-items";

.content {
  // height: 100%;

  pre {
    border: $input-border;
    padding: 6px;
    background: $bg-ui;
    font-size: smaller;
  }
}

.imported-text {
  width: 100%;
  &.deleted {
    color: grey;
    text-decoration: line-through;
  }
}

.gap {
  flex-grow: 1;
}
</style>
