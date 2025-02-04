## Video Lyric Generator

## Overview
This project is a video editing application with a **Python/Flask backend** and a **Vue.js frontend**. It allows users to upload videos, trim clips, merge multiple video clips, and add subtitles. The backend leverages **FFmpeg** and **moviepy** for video processing, while the frontend uses **Tailwind CSS** and **Wavesurfer.js** for a modern and responsive UI.

---

## Features

### Backend Features
- **Upload Videos**: Accepts video files and stores them on the server.
- **Trim Videos**: Allows trimming of video files based on user-specified start and end times.
- **Merge Videos**: Concatenates multiple video clips into one final render.
- **Add Subtitles**: Adds subtitle files (SRT/ASS) to videos with customizable styles.

### Frontend Features
- **Video Upload Interface**: Drag-and-drop functionality and file input for video upload.
- **Preview Videos**: Embedded video player for previewing uploaded or edited videos.
- **Video List Management**: Manage uploaded videos with options to edit or remove them.
- **Final Render**: Merge multiple videos into a single final clip.

---

## Technologies Used

### Backend
- **Python**
- **Flask**
- **FFmpeg**
- **moviepy**
- **Flask-CORS**

### Frontend
- **Vue.js**
- **Tailwind CSS**
- **Wavesurfer.js**
- **Vue3-Toastify**

---

## Setup Instructions

### Prerequisites
1. **Python** (3.8 or higher)
2. **Node.js** (16 or higher)
3. **FFmpeg** (Installed and available in system PATH)

### Backend Setup
1. Clone the repository.
2. Navigate to the backend folder:
   ```bash
   cd backend
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the backend server:
   ```bash
   python index.py
   ```

### Frontend Setup
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the frontend development server:
   ```bash
   npm run dev
   ```

### Access the Application
- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend: open file start-server-windows.bat

---

## API Endpoints

### General
- **`GET /`**: Returns a health check message.

### Video Management
- **`POST /upload_video`**: Uploads a video file.
- **`GET /clips/<filename>`**: Fetches a video file by name.

### Video Editing
- **`POST /edit_video/trim`**: Trims a video based on start and end times.
  - **Request Body**:
    ```json
    {
      "videofile": "path/to/video",
      "trim_start": 10,
      "trim_end": 60
    }
    ```
- **`POST /merged_render`**: Merges multiple video files.
  - **Request Body**:
    ```json
    {
      "videoscount": 3,
      "video0": "path/to/video1",
      "video1": "path/to/video2",
      "video2": "path/to/video3"
    }
    ```
- **`POST /add_subtitles`**: Adds subtitles to a video.
  - **Form Data**:
    - `videofile`: Path to the video file.
    - `subtitlefile`: Subtitle file (.srt or .ass).

---

## Project Structure

### Backend
- `index.py`: Main Flask application file.
- `video_utils.py`: Contains video editing utility functions (trimming, merging, adding subtitles).
- `config.py`: Configuration for file paths and other settings.

### Frontend
- `src/App.vue`: Main application component.
- `src/components`: Contains reusable Vue components such as `VideoUpload`, `VideoPreview`, and `VideoList`.
- `src/scripts/AppLogic.js`: Contains application logic for managing video operations.

---

## Contributing
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments
- [FFmpeg](https://ffmpeg.org/)
- [moviepy](https://zulko.github.io/moviepy/)
- [Vue3-Toastify](https://github.com/Maronato/vue-toastify)


