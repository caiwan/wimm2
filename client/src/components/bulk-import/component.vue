<template>
  <div>
    <div id="import-export">
      <div class="content">
        <div>
          <h1>Import</h1>
  
          <div>
            <form @submit.prevent="doImportWrapped">
              <div>
                <p>Select input format:</p>
                <select name="inportFormat"><option v-for="format in formats" :key="format.id" value:>{{format.name}}</option></select>
              </div>
              <div>
                <input type="file" @change="setImportedFile($event.target.files[0])">
              </div>
              <button :disabled="!importedFile || isImporting">
                Import Data
                <span v-if="isImporting">{{ importProgress }} </span>
              </button>
              <div v-if="importError">
                Import failed for some with this reason:
                <pre>{{ importError }}</pre>
              </div>
              <div v-if="importCount">
                Imported {{ importCount }} items
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
import FileSaver from "file-saver";

import Calendar from "@/components/calendar";

export default {
  components: {
    Calendar
  },
  data() {
    return {
      progress: "",
      importProgress: "",
      importedFile: null,
      formats: [
        { id: 1, name: "OTP CSV" },
        { id: 2, name: "Large receipt" },
        { id: 3, name: "Small receipt" },
        { id: 4, name: "Mixed" }
      ]
    };
  },
  computed: {
    ...mapState("importExport", [
      "isExporting",
      "isImporting",
      "dateFrom",
      "dateTo",
      "exportedData"
    ]),
    ...mapGetters("importExport", [
      "exportFilename",
      "importError",
      "importCount"
    ])
  },
  methods: {
    ...mapActions("importExport", [
      "doExport",
      "setProperty",
      "doImport",
      "parseFile",
      "hideUi"
    ]),
    onChanged(key, value) {
      this.setProperty({ key, value });
    },
    setImportedFile(f) {
      this.importedFile = f;
    },
    async doExportWrapped(e) {
      const progress = () => {
        setTimeout(() => {
          if (this.isExporting) {
            const dots = (this.progress.length + 1) % 4;

            this.progress = ".".repeat(dots);
            setTimeout(progress, 400);
          } else {
            this.progress = "";
          }
        });
      };

      progress();

      await this.doExport();
      const blob = new Blob(this.exportedData, {
        type: "application/octet-stream"
      });
      FileSaver.saveAs(blob, this.exportFilename);
    },
    doImportWrapped(e) {
      const progress = () => {
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

      progress();
      this.doImport(this.importedFile);
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
