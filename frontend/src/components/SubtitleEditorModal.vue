// frontend/src/components/SubtitleEditorModal.vue

[file name]: SubtitleEditorModal.vue
[file content begin]
<template>
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <h3 class="d-flex align-items-center justify-content-start gap-2"><div v-html="icons.subtIcon"></div>Edit Subtitles</h3>
      <SubtitlePreviewPlayer 
        v-if="showModal && audioFile"
        :subtitleEntries="subtitleEntries"
        :audioFile="audioFile"
        @time-update="handleTimeUpdate"
        ref="previewPlayer"
      />
      <div class="scrollable-container" ref="scrollContainer">
        <div class="subtitle-list">
          <div 
            v-for="(entry, index) in subtitleEntries" 
            :key="index" 
            class="subtitle-entry"
            :ref="el => { entryElements[index] = el }"
            :class="{ 'active-entry': isActiveEntry(index) }"
            @click="seekToSegment(index)"
          >
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
              
              <div class="d-flex align-items-center justify-content-end gap-3">              
                <button @click="addNewLineAtIndex(index + 1)" class="add-button"><div v-html="icons.deleteIcon"></div></button>
                <button v-if="index > 0" @click="joinSegments(index)" class="join-button"><div v-html="icons.joinIcon"></div></button>
                <button @click="deleteLine(index)" class="delete-button"><div v-html="icons.addIcon"></div></button>
              </div>
            </div>
            <textarea
              v-model="entry.text"
              @keydown.enter="handleTextareaEnter(index, $event)"
              class="text-input"
            ></textarea>          
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
    joinSegments,
  } from '../scripts/subtitleUtils';
  import {icons} from '../assets/icons.js';
  import SubtitlePreviewPlayer from './SubtitlePreviewPlayer.vue';
  import { throttle } from 'lodash';
  
  export default {
    components: {
      SubtitlePreviewPlayer,
    },
    name: 'SubtitleEditorModal',
    props: {
      subtitles: String,
      showModal: Boolean,
      audioFile: File,
    },
    data() {
      return {
        subtitleEntries: [],
        icons,
        currentAudioTime: 0,
        entryElements: [],
        scrollThrottle: null
      };
    },
    watch: {
      subtitles(newVal) {
        if (newVal) {
          const parsed = parseSubtitles(newVal);
          // Para cada entrada, reemplazamos "\n" (literal) por un salto de línea real
          this.subtitleEntries = parsed.map(entry => ({
            ...entry,
            text: entry.text.replace(/\\n/g, '\n')
          }));
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
          .map((entry) => {
            const timeTag = `[${this.formatTime(entry.startTime)}]`;
            // Reemplazar saltos de línea reales por "\n" escapado
            const escapedText = entry.text.replace(/\n/g, '\\n'); 
            return `${timeTag}${escapedText}`;
          })
          .join('\n');
        
        this.$emit('save-changes', updatedSubtitles);
      },
      handleTextareaEnter(index, event) {
        if (event.shiftKey) {
          event.preventDefault();
          this.splitLine(index, event);
        }
        // Enter sin Shift inserta nueva línea (comportamiento por defecto)
      },
  
      closeModal() {
        this.$emit('close-modal');
      },
      addNewLineAtIndex(index) {
        this.subtitleEntries = addNewLineAtIndex(this.subtitleEntries, index);
      },
      joinSegments(index) {
        this.subtitleEntries = joinSegments(this.subtitleEntries, index);
      },
      deleteLine(index) {
        this.subtitleEntries = deleteLine(this.subtitleEntries, index);
      },
      splitLine(index, event) {
        const cursorPosition = event.target.selectionStart;
        this.subtitleEntries = splitLine(this.subtitleEntries, index, cursorPosition);
      },
      handleTimeUpdate(time) {
        this.currentAudioTime = time;
        this.scrollToActiveEntry();
      },
      isActiveEntry(index) {
        const entry = this.subtitleEntries[index];
        const nextEntry = this.subtitleEntries[index + 1];
        
        // Si es el último segmento, solo comparamos con el tiempo de inicio
        if (!nextEntry) {
          return this.currentAudioTime >= entry.startTime;
        }        
        // Para los segmentos intermedios, usamos un rango exclusivo
        return this.currentAudioTime >= entry.startTime && 
              this.currentAudioTime < nextEntry.startTime;
      },
      
      seekToSegment(index) {
        const startTime = this.subtitleEntries[index].startTime;
        if (this.$refs.previewPlayer) {
          this.$refs.previewPlayer.seekToTime(startTime);
        }
        this.scrollToEntry(index);
      },

      scrollToEntry(index) {
        if (this.entryElements[index]) {
          const container = this.$refs.scrollContainer;
          const element = this.entryElements[index];
          const containerHeight = container.clientHeight;
          const elementTop = element.offsetTop - container.offsetTop;
          
          container.scrollTo({
            top: elementTop - containerHeight * 0.3,
            behavior: 'smooth'
          });
        }
      },
      scrollToActiveEntry: throttle(function() {
        const activeIndex = this.subtitleEntries.findIndex(entry => 
          this.currentAudioTime >= entry.startTime && 
          this.currentAudioTime <= entry.endTime
        );
        
        if (activeIndex !== -1 && this.entryElements[activeIndex]) {
          const container = this.$refs.scrollContainer;
          const element = this.entryElements[activeIndex];
          const containerHeight = container.clientHeight;
          const elementTop = element.offsetTop - container.offsetTop;
          const elementBottom = elementTop + element.clientHeight;
          
          if (elementTop < container.scrollTop) {
            container.scrollTo({
              top: elementTop - 10,
              behavior: 'smooth'
            });
          } else if (elementBottom > container.scrollTop + containerHeight) {
            container.scrollTo({
              top: elementBottom - containerHeight + 10,
              behavior: 'smooth'
            });
          }
        }
      }, 300),
    },
    mounted() {
      this.scrollThrottle = throttle(this.scrollToActiveEntry, 300);
    },
    beforeUnmount() {
      if (this.scrollThrottle) {
        this.scrollThrottle.cancel();
      }
    }
  };
</script>

[file content end]