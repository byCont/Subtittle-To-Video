// frontend/src/components/SubtitleEditorModal.vue

<template>
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <h3 class="d-flex align-items-center justify-content-start gap-2"><div v-html="icons.subtIcon"></div>Edit Subtitles</h3>
      <div class="scrollable-container">
        <div class="subtitle-list">
          <div v-for="(entry, index) in subtitleEntries" :key="index" class="subtitle-entry">
            <div class="d-flex">
              <div class="d-flex align-items-center justify-content-start gap-2">
                <input
                type="text"
                :value="formatTime(entry.startTime)"
                @input="updateTime(index, 'start', $event.target.value)"
                class="time-input gap-3"
                />
                <input
                  type="text"
                  :value="formatTime(entry.endTime)"
                  @input="updateTime(index, 'end', $event.target.value)"
                  class="time-input"
                />
              </div>
              
              <div class="d-flex align-items-center justify-content-end gap-2">              
                <button @click="addNewLineAtIndex(index + 1)" class="add-button"><div v-html="icons.deleteIcon"></div></button>
                <button @click="deleteLine(index)" class="delete-button"><div v-html="icons.addIcon"></div></button>
              </div>
            </div>
            <input
              type="text"
              v-model="entry.text"
              @keydown.enter.prevent="splitLine(index, $event)"
              class="text-input"
            />            
          </div>
        </div>
      </div>
      <div class="modal-actions">
        <button @click="saveChanges">Save Changes</button>
        <button @click="closeModal">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
  import {
    parseSubtitles,
    formatTime,
    updateTime,
    addNewLineAtIndex,
    deleteLine,
    splitLine,
  } from '../scripts/subtitleUtils.js';
  import {icons} from '../assets/icons.js';
  export default {
    name: 'SubtitleEditorModal',
    props: {
      subtitles: String,
      showModal: Boolean,
    },
    data() {
      return {
        subtitleEntries: [],
        icons,
      };
    },
    watch: {
      subtitles(newVal) {
        if (newVal) {
          this.subtitleEntries = parseSubtitles(newVal);
        }
      },
    },
    methods: {
      formatTime,
      updateTime(index, field, value) {
        this.subtitleEntries = updateTime(this.subtitleEntries, index, field, value);
      },
      saveChanges() {
        const updatedSubtitles = this.subtitleEntries
          .map((entry) => `[${formatTime(entry.startTime)}]${entry.text}`)
          .join('\n');
        this.$emit('save-changes', updatedSubtitles);
      },
      closeModal() {
        this.$emit('close-modal');
      },
      addNewLineAtIndex(index) {
        this.subtitleEntries = addNewLineAtIndex(this.subtitleEntries, index);
      },
      deleteLine(index) {
        this.subtitleEntries = deleteLine(this.subtitleEntries, index);
      },
      splitLine(index, event) {
        const cursorPosition = event.target.selectionStart;
        this.subtitleEntries = splitLine(this.subtitleEntries, index, cursorPosition);
      },
    },
  };
</script>