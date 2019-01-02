<template>
  <div
    id="smart-import"
    class="content"
  >

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

    <section>
      <ul>
        <li
          v-for="item in importedItems"
          :key="item.id"
        >{{item.text}}
        </li>
      </ul>
    </section>

  </div>

</template>

<script>
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

export default {
  data() {
    return {
      progress: "",
      importProgress: "",
      importedFile: null,
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
      "hideUi"
    ]),

    onChanged(key, value) {
      this.setProperty({ key, value });
    },

    setImportedFile(f) {
      this.importedFile = f;
    },

    doContinueEditWrapped() {
      _progress();
      this.continueEdit();
    },

    doImportWrapped(e) {
      _progress();
      this.doImport({ type: this.selectedFormat.id, file: this.importedFile });
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

#import-export {
  height: 100%;

  pre {
    border: $input-border;
    padding: 6px;
    background: $bg-ui;
    font-size: smaller;
  }
}
</style>
