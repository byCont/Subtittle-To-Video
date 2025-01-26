<template>
  <div class="loading-overlay">
    <div class="loader-container">
      <div class="circle-background">
        <div class="spinner-grow" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div class="content-wrapper">
        <div class="icons-container">
          <svg
            class="animated-icon bounce"
            xmlns="http://www.w3.org/2000/svg"
            height="24px"
            viewBox="0 -960 960 960"
            width="24px"
            fill="var(--button-hover-color)"
          >
            <path
              class="line pulse"
              d="M240-320h320v-80H240v80Zm400 0h80v-80h-80v80ZM240-480h80v-80h-80v80Zm160 0h320v-80H400v80ZM160-160q-33 0-56.5-23.5T80-240v-480q0-33 23.5-56.5T160-800h640q33 0 56.5 23.5T880-720v480q0 33-23.5 56.5T800-160H160Zm0-80h640v-480H160v480Zm0 0v-480 480Z"
            />
          </svg>
          <svg
            class="animated-icon music-note scale"
            xmlns="http://www.w3.org/2000/svg"
            height="24px"
            viewBox="0 -960 960 960"
            width="24px"
            fill="var(--background-color)"
          >
            <path
              d="M400-120q-66 0-113-47t-47-113q0-66 47-113t113-47q23 0 42.5 5.5T480-418v-422h240v160H560v400q0 66-47 113t-113 47Z"
            />
          </svg>
        </div>
        <div class="loader-text fade-in">           
          <div class="dots-animation">
            <span class="dot">Genering </span>
            <span class="dot">video </span>
            <span class="dot">lyric...</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
:root {
  --primary-color: #1f2937;
  --secondary-color: #111827;
  --background-color: #374151;
  --text-color: #f9fafb;
  --button-hover-color: #25eba991;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loader-container {
  position: relative;
  text-align: center;
  background: rgba(31, 41, 55, 0.8);
  padding: 2rem;
  border-radius: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  min-width: 300px;
  min-height: 100px;
  display: flex;
  overflow: hidden;
  justify-content: center;
  align-items: center;
}

.circle-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 130%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.spinner-grow {
  width: 150%;
  height: 150%;
  overflow: hidden;
  position: absolute;
  background-color: var(--secondary-color);
  opacity: 0.2;
}

.content-wrapper {
  position: relative;
  z-index: 2;
}

.icons-container {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto 20px;
}

.animated-icon {
  width: 100px;
  height: 100px;
  position: absolute;
  top: 0;
  left: 0;
}

.music-note {
  z-index: 2;
  opacity: 0.9;
}

.bounce {
  animation: bounce 2s infinite;
}

.scale {
  animation: scale 3s infinite alternate;
}

.pulse {
  animation: pulse 1.5s infinite;
}

.loader-text {
  color: var(--text-color);
  font-size: 1.2em;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.fade-in {
  animation: fadeIn 0.5s ease-in;
}

.dots-animation {
  display: inline-block;
}

.dot {
  opacity: 0;
  animation: dotAnimation 1.4s infinite;
  margin-left: 2px;
  color: var(--text-color);
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes scale {
  0% {
    transform: scale(0.8) rotate(-10deg);
  }
  50% {
    transform: scale(1.2) rotate(10deg);
  }
  100% {
    transform: scale(0.8) rotate(-10deg);
  }
}

@keyframes pulse {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.05);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes dotAnimation {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
</style>

<script>
export default {
  name: 'CustomLoader'
}
</script>
