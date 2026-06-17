---
obsidianUIMode: preview
cssclasses:
  - hide-properties
---
**Good Habits**
```dataviewjs
const trackerData = {
    year: 2026,
    entries: [],
    heatmapTitle: "💪 Workout Tracker",
    colorScheme: {
        paletteName: "default",
        customColors: ["#FF8C00"]
    }
}

for(let page of dv.pages('"Calendar/Journal/Daily"').where(p => p.workout)) {
    trackerData.entries.push({
        date: page.file.name,
        intensity: 1
    })
}

renderHeatmapTracker(this.container, trackerData)
```
```dataviewjs
const trackerData = {
    year: 2026,
    entries: [],
    heatmapTitle: "🥬 Dinner Vegetable",
    colorScheme: {
        paletteName: "default",
        customColors: ["#228B22"]
    }
}

for(let page of dv.pages('"Calendar/Journal/Daily"').where(p => p.vegetable)) {
    trackerData.entries.push({
        date: page.file.name,
        intensity: 1
    })
}

renderHeatmapTracker(this.container, trackerData)
```
```dataviewjs
const trackerData = {
    year: 2026,
    entries: [],
    heatmapTitle: "🔠 English Study",
    colorScheme: {
        paletteName: "default",
        customColors: ["#8470FF"]
    }
}

for(let page of dv.pages('"Calendar/Journal/Daily"').where(p => p.english)) {
    trackerData.entries.push({
        date: page.file.name,
        intensity: 1
    })
}

renderHeatmapTracker(this.container, trackerData)
```
```dataviewjs
const trackerData = {
    year: 2026,
    entries: [],
    heatmapTitle: "🪥 睡前刷牙",
    colorScheme: {
        paletteName: "default",
        customColors: ["#87CEFA"]
    }
}

for(let page of dv.pages('"Calendar/Journal/Daily"').where(p => p.teeth)) {
    trackerData.entries.push({
        date: page.file.name,
        intensity: 1
    })
}

renderHeatmapTracker(this.container, trackerData)
```