[file name]: SubtitlePreviewPlayer.vue
[file content begin]
<template>
  <div class="preview-player">
    <!-- Simplified playback controls -->
    <div class="player-controls">
      <button @click="togglePlay" class="play-button">
        <div v-html="isPlaying ? icons.pauseIcon : icons.playIcon"></div>
      </button>
      <span class="time-display">{{ formatTime(currentTime) }}</span>
      <input 
        type="range" 
        v-model="seekTime"
        min="0"
        :max="duration"
        step="0.1"
        @input="seekAudio"
        class="seek-bar"
      />
      <span class="time-display">{{ formatTime(duration) }}</span>
    </div>

    <!-- Hidden audio element -->
    <audio 
      ref="audioPlayer"
      :src="audioUrl"
      @timeupdate="updateTime"
      @loadedmetadata="updateDuration"
      class="hidden-audio"
    />
  </div>
</template>

<script>
  import { formatTime } from '../scripts/subtitleUtils';
  import {icons} from '../assets/icons.js';

  export default {
    props: {
      subtitleEntries: Array,
      audioFile: File
    },

    data() {
      return {
        isPlaying: false,
        currentTime: 0,
        duration: 0,
        seekTime: 0,
        audioUrl: '',
        icons,
      };
    },

    watch: {
      audioFile: {
        immediate: true,
        handler(newVal) {
          if (newVal) {
            this.audioUrl = URL.createObjectURL(newVal);
            this.$nextTick(() => {
              this.$refs.audioPlayer.load();
            });
          }
        }
      }
    },

    methods: {
      formatTime,

      togglePlay() {
        const audio = this.$refs.audioPlayer;
        if (this.isPlaying) {
          audio.pause();
        } else {
          audio.play();
        }
        this.isPlaying = !this.isPlaying;
      },

      updateTime() {
        const audio = this.$refs.audioPlayer;
        this.currentTime = audio.currentTime;
        this.seekTime = audio.currentTime;
        this.$emit('time-update', this.currentTime);
      },

      updateDuration() {
        this.duration = this.$refs.audioPlayer.duration;
      },

      seekAudio() {
        this.$refs.audioPlayer.currentTime = this.seekTime;
        this.currentTime = this.seekTime;
      },
    
      seekToTime(time) {
        const audio = this.$refs.audioPlayer;
        if (audio) {
          audio.currentTime = time;
          this.currentTime = time;
          this.seekTime = time;
          
          if (!this.isPlaying) {
            audio.play().then(() => {
              this.isPlaying = true;
              setTimeout(() => {
                audio.pause();
                this.isPlaying = false;
              }, 100);
            });
          }
        }
      }
    },
    // eslint-disable-next-line vue/no-deprecated-destroyed-lifecycle
    beforeDestroy() {
      URL.revokeObjectURL(this.audioUrl);
    }
  };
</script>

<style scoped>
</style>
[file content end]