import axios from 'axios';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

const apiBaseUrl = "http://localhost:5000";

export default {
  data() {
    return {
      originalvideos: [],
      videos: [],
      loading: false,
      videoToRender: null,
      uploadprogress: 0,
    };
  },
  methods: {
    setRenderVideo(video, isVideoObj = true) {
      this.videoToRender = isVideoObj ? this.videos[video].file : video;
    },
    reloadOriginalVideo(videoID) {
      this.videos[videoID] = { ...this.originalvideos[videoID] };
      this.setRenderVideo(videoID);
    },
    removeVideo(videoID) {
      this.videos.splice(videoID, 1);
      this.originalvideos.splice(videoID, 1);
    },
    editVideoSubmit(videoID, actiontype) {
      if (!this.videos[videoID]?.file) return toast.error("Video is empty!");
      this.loading = true;
      const payload = {
        videofile: this.videos[videoID].file,
        ...(actiontype === 'trim' && {
          trim_start: document.getElementById(`trim_start${videoID}`).value,
          trim_end: document.getElementById(`trim_end${videoID}`).value,
        }),
      };
      axios.post(`${apiBaseUrl}/edit_video/${actiontype}`, payload)
        .then(res => {
          this.loading = false;
          if (res.data.status === "success") {
            this.videos[videoID].file = res.data.edited_videopath;
            this.setRenderVideo(videoID);
            toast.success(res.data.message);
          } else {
            toast.error("Video edit failed");
          }
        })
        .catch(() => toast.error("Error connecting to the server."));
    },
    uploadVideoFile() {
      const clipname = document.getElementById("clipname").value;
      const filedata = document.getElementById("fileinput").files[0];
      if (!filedata || !clipname) {
        return toast.warning(!filedata ? "File is empty!" : "Clip name is required!");
      }
      const data = new FormData();
      data.append("videofile", filedata);
      axios.post(`${apiBaseUrl}/upload_video`, data, {
        onUploadProgress: e => (this.uploadprogress = Math.round((e.loaded * 100) / e.total)),
      })
        .then(res => {
          const video = { name: clipname, file: res.data };
          this.originalvideos.push(video);
          this.videos.push(video);
          this.setRenderVideo(this.videos.length - 1);
          toast.success("Video uploaded!");
          this.uploadprogress = 0;
        })
        .catch(() => toast.error("Error uploading the video."));
    },
    finalrender() {
      this.loading = true;
      const payload = this.videos.reduce((acc, v, i) => ({ ...acc, [`video${i}`]: v.file }), { videoscount: this.videos.length });
      axios.post(`${apiBaseUrl}/merged_render`, payload)
        .then(res => {
          if (res.data.status === "success") {
            toast.success("Final render success!");
            this.setRenderVideo(`${apiBaseUrl}/${res.data.finalrender_videopath}`, false);
          } else {
            toast.error(`Final render failed: ${res.data.message}`);
          }
          this.loading = false;
        });
    },
    addSubtitles() {
      const subtitleFile = document.getElementById("subtitleinput").files[0];
      if (!subtitleFile || !this.videoToRender) {
        return toast.warning(!subtitleFile ? "Subtitle file is empty!" : "No video selected!");
      }
      const data = new FormData();
      data.append("videofile", this.videoToRender);
      data.append("subtitlefile", subtitleFile);
      axios.post(`${apiBaseUrl}/add_subtitles`, data)
        .then(res => {
          if (res.data.status === "success") {
            toast.success("Subtitles added!");
            this.videoToRender = res.data.subtitled_videopath;
          } else {
            toast.error(`Error adding subtitles: ${res.data.message}`);
          }
        })
        .catch(() => toast.error("Error connecting to the server."));
    },
  },
};
