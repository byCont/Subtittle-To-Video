// frontend/src/components/VideoUpload.vue

<template>
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <h3>Edit Subtitles</h3>
      <div class="scrollable-container">
        <div class="subtitle-list">
          <div v-for="(entry, index) in subtitleEntries" :key="index" class="subtitle-entry">
            <div class="time-column">
              <input
                type="text"
                :value="formatTime(entry.startTime)"
                @input="updateTime(index, 'start', $event.target.value)"
                class="time-input"
              />
              <input
                type="text"
                :value="formatTime(entry.endTime)"
                @input="updateTime(index, 'end', $event.target.value)"
                class="time-input"
              />
            </div>
            <input
              type="text"
              v-model="entry.text"
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
export default {
  name: 'SubtitleEditorModal',
  props: {
    subtitles: String,
    showModal: Boolean,
  },
  data() {
    return {
      subtitleEntries: [],
    };
  },
  watch: {
    subtitles(newVal) {
      if (newVal) {
        this.parseSubtitles(newVal);
      }
    },
  },
  methods: {
    parseSubtitles(subtitles) {
      const lines = subtitles.split('\n');
      const entries = [];

      for (const line of lines) {
        const trimmedLine = line.trim();
        if (trimmedLine.startsWith('[')) {
          const endBracket = trimmedLine.indexOf(']');
          if (endBracket !== -1) {
            const timeStr = trimmedLine.slice(1, endBracket);
            const text = trimmedLine.slice(endBracket + 1).trim();
            const startTime = this.parseTime(timeStr);
            
            if (!isNaN(startTime)) {
              entries.push({ startTime, text });
            }
          }
        }
      }

      for (let i = 0; i < entries.length; i++) {
        
        // eslint-disable-next-line no-unused-vars
        const { startTime, text } = entries[i];
        let endTime;
        
        if (i < entries.length - 1) {
          const nextStartTime = entries[i + 1].startTime;
          const timeDiff = nextStartTime - startTime;
          endTime = timeDiff < 7 ? nextStartTime : startTime + 5;
        } else {
          endTime = startTime + 8;
        }
        
        entries[i].endTime = endTime;
      }

      this.subtitleEntries = entries;
    },

    updateTime(index, field, value) {
      const timeInSeconds = this.parseTime(value);
      if (!isNaN(timeInSeconds)) {
        this.subtitleEntries[index][`${field}Time`] = timeInSeconds;
      }
    },

    parseTime(timeStr) {
      // Acepta tanto formato con horas como sin horas
      const timeRegex = /^(?:(\d+):)?([0-5]?\d):([0-5]\d)\.(\d{2})$/;
      const match = timeStr.match(timeRegex);
      if (!match) return NaN;

      const hours = match[1] ? parseInt(match[1], 10) : 0;
      const minutes = parseInt(match[2], 10);
      const seconds = parseInt(match[3], 10);
      const milliseconds = parseInt(match[4], 10);

      return hours * 3600 + minutes * 60 + seconds + milliseconds / 100;
    },

    formatTime(seconds) {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const remainingSeconds = Math.floor(seconds % 60);
      const milliseconds = Math.round((seconds % 1) * 100);

      // Formato mm:ss.ms (solo muestra horas si son > 0)
      return hours > 0 
        ? `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}.${String(milliseconds).padStart(2, '0')}`
        : `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}.${String(milliseconds).padStart(2, '0')}`;
    },

    saveChanges() {
      const updatedSubtitles = this.subtitleEntries
        .map((entry) => `[${this.formatTime(entry.startTime)}]${entry.text}`)
        .join('\n');
      this.$emit('save-changes', updatedSubtitles);
    },

    closeModal() {
      this.$emit('close-modal');
    },
  },
};
</script>
