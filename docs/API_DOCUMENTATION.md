# JARVIS API Documentation

## Overview

JARVIS provides a comprehensive REST API for programmatic access to all features.

## Base URL

```
http://localhost:5000/api
```

## Authentication

Most endpoints require authentication. Include your API key in headers:

```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Mobile API

#### GET /api/mobile/status
Get JARVIS status and version.

**Response:**
```json
{
  "status": "online",
  "version": "1.0.0",
  "features": 385
}
```

#### POST /api/mobile/command
Execute a JARVIS command.

**Request:**
```json
{
  "command": "create keylogger",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Keylogger created successfully",
  "command": "create keylogger"
}
```

### Plugin Marketplace

#### GET /api/plugins/search
Search for plugins.

**Query Parameters:**
- `query` - Search query
- `category` - Filter by category

**Response:**
```json
{
  "plugins": [
    {
      "id": "plugin_id",
      "name": "Plugin Name",
      "description": "Description",
      "author": "Author",
      "version": "1.0.0",
      "downloads": 1000,
      "rating": 4.5
    }
  ]
}
```

#### POST /api/plugins/install
Install a plugin.

**Request:**
```json
{
  "plugin_id": "plugin_id"
}
```

### Collaboration

#### POST /api/collaboration/create_workspace
Create a workspace.

**Request:**
```json
{
  "workspace_id": "workspace123",
  "name": "My Workspace",
  "owner": "user123",
  "description": "Description"
}
```

#### POST /api/collaboration/share_command
Share a command with workspace.

**Request:**
```json
{
  "workspace_id": "workspace123",
  "user_id": "user123",
  "command": "create keylogger",
  "result": "Keylogger created"
}
```

### Performance

#### GET /api/performance/benchmark
Run performance benchmarks.

**Response:**
```json
{
  "startup": {
    "avg_time": 1.5,
    "avg_memory": 120
  },
  "response": {
    "overall_avg": 0.8
  },
  "cache": {
    "hit_rate": 0.75
  }
}
```

## Error Responses

All errors follow this format:

```json
{
  "success": false,
  "error": "Error message",
  "error_code": "ERROR_CODE"
}
```

## Rate Limiting

API requests are rate-limited to 100 requests per minute per API key.

## SDKs

### Python
```python
from jarvis_api import JARVISClient

client = JARVISClient(api_key="YOUR_KEY")
response = client.execute_command("create keylogger")
```

### JavaScript
```javascript
const jarvis = new JARVISClient('YOUR_KEY');
const response = await jarvis.executeCommand('create keylogger');
```

## Examples

See `examples/` directory for more examples.
