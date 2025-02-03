// fontend/src/scripts/subtitleUtils.js

export function parseSubtitles(subtitles) {
  const lines = subtitles.split('\n');
  const entries = [];
  for (const line of lines) {
    const trimmedLine = line.trim();
    if (trimmedLine.startsWith('[')) {
      const endBracket = trimmedLine.indexOf(']');
      if (endBracket !== -1) {
        const timeStr = trimmedLine.slice(1, endBracket);
        const text = trimmedLine.slice(endBracket + 1).trim();
        const startTime = parseTime(timeStr);
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
  return entries;
}

export function parseTime(timeStr) {
  const timeRegex = /^(?:(\d+):)?([0-5]?\d):([0-5]\d)\.(\d{2})$/;
  const match = timeStr.match(timeRegex);
  if (!match) return NaN;
  const hours = match[1] ? parseInt(match[1], 10) : 0;
  const minutes = parseInt(match[2], 10);
  const seconds = parseInt(match[3], 10);
  const milliseconds = parseInt(match[4], 10);
  return hours * 3600 + minutes * 60 + seconds + milliseconds / 100;
}

export function formatTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  const milliseconds = Math.round((seconds % 1) * 100);
  return hours > 0
    ? `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}.${String(milliseconds).padStart(2, '0')}`
    : `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}.${String(milliseconds).padStart(2, '0')}`;
}

export function updateTime(entries, index, field, value) {
  const timeInSeconds = parseTime(value);
  if (!isNaN(timeInSeconds)) {
    entries[index][`${field}Time`] = timeInSeconds;
  }
  return entries;
}

export function addNewLineAtIndex(entries, index) {
  const previousEntry = entries[index - 1];
  const newStartTime = previousEntry ? previousEntry.endTime : 0;
  const newEndTime = newStartTime + 5; // Default duration of 5 seconds
  entries.splice(index, 0, {
    startTime: newStartTime,
    endTime: newEndTime,
    text: '',
  });
  return entries;
}

export function deleteLine(entries, index) {
  entries.splice(index, 1);
  return entries;
}

export function splitLine(entries, index, cursorPosition) {
  const entry = entries[index];
  const textBeforeCursor = entry.text.slice(0, cursorPosition);
  const textAfterCursor = entry.text.slice(cursorPosition);
  const totalTime = entry.endTime - entry.startTime;
  const splitRatio = cursorPosition / entry.text.length;
  const splitTime = entry.startTime + totalTime * splitRatio;

  entries[index] = {
    ...entry,
    text: textBeforeCursor,
    endTime: splitTime,
  };

  entries.splice(index + 1, 0, {
    startTime: splitTime,
    endTime: entry.endTime,
    text: textAfterCursor,
  });

  return entries;
}