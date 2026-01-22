# JARVIS Mobile API

## Overview

REST API endpoints for mobile app integration.

## Endpoints

### Status
```
GET /api/mobile/status
```
Get JARVIS status and version.

### Execute Command
```
POST /api/mobile/command
Body: {
  "command": "create keylogger",
  "user_id": "user123"
}
```
Execute a JARVIS command from mobile.

### Voice Command
```
POST /api/mobile/voice
Body: {
  "transcript": "create keylogger"
}
```
Process voice command from mobile.

### Notifications
```
GET /api/mobile/notifications
```
Get notifications for mobile app.

### Statistics
```
GET /api/mobile/stats
```
Get statistics for mobile dashboard.

### History
```
GET /api/mobile/history?limit=50
```
Get command history.

## Usage

Start the mobile API server:
```bash
python mobile/api_endpoints.py
```

The server runs on `http://localhost:5000`

## Mobile App Integration

### iOS (Swift)
```swift
let url = URL(string: "http://your-server:5000/api/mobile/command")!
var request = URLRequest(url: url)
request.httpMethod = "POST"
request.setValue("application/json", forHTTPHeaderField: "Content-Type")
request.httpBody = try? JSONSerialization.data(withJSONObject: [
    "command": "create keylogger",
    "user_id": "user123"
])
```

### Android (Kotlin)
```kotlin
val client = OkHttpClient()
val json = JSONObject()
json.put("command", "create keylogger")
json.put("user_id", "user123")

val request = Request.Builder()
    .url("http://your-server:5000/api/mobile/command")
    .post(json.toString().toRequestBody("application/json".toMediaType()))
    .build()
```

## Next Steps

- Add authentication
- Add WebSocket support for real-time updates
- Add push notification support
- Add file upload/download
- Add voice streaming
