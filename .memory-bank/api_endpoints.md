# API Endpoints

This document describes the Flask routes and the expected request/response payloads for the Voice Command Recognition System.

## 1. Authentication

| Method | Route | Description | Auth Required |
|---|---|---|---|
| GET | `/login` | Serves the login page. | No |
| POST | `/login` | Processes user authentication. | No |
| GET | `/register` | Serves the registration page. | No |
| POST | `/register` | Processes new user registration (default role: Operator). | No |
| GET | `/logout` | Terminates the user session. | Yes |

### POST `/login`
**Payload**: `{"username": "...", "password": "..."}` (Form-data)
**Response**: Redirect to `/` or Error flash.

### POST `/register`
**Payload**: `{"username": "...", "password": "...", "confirm_password": "..."}` (Form-data)
**Response**: Redirect to `/login` or Error flash.

---

## 2. Voice Recognition

| Method | Route | Description | Auth Required |
|---|---|---|---|
| GET | `/` | Dashboard / Recording interface. | Yes (Any) |
| POST | `/record/upload` | Handles audio upload and VOSK transcription. | Yes (Operator) |
| POST | `/record/<int:id>/confirm` | Saves manual corrections and marks as "confirmed". | Yes (Operator) |

### POST `/record/upload`
**Payload**: `multipart/form-data` with `audio_blob` file.
**Response (200 OK)**:
```json
{
  "id": 123,
  "raw_text": "зарегистрировать трубу p45345ив",
  "command": "Зарегистрировать",
  "identifier": "P45345ИВ",
  "audio_url": "/static/uploads/audio/abc-123.wav"
}
```

### POST `/record/<int:id>/confirm`
**Payload**:
```json
{
  "corrected_text": "зарегистрировать трубу p45345ив",
  "command": "Зарегистрировать",
  "identifier": "P45345ИВ"
}
```
**Response**: `{"status": "success", "record_id": 123}`.

---

## 3. History and Details

| Method | Route | Description | Auth Required |
|---|---|---|---|
| GET | `/history` | List of records with server-side filtering. | Yes (Any) |
| GET | `/record/<int:id>` | Returns details for a specific record. | Yes (Any) |

### GET `/history`
**Parameters**: `?date_from=...&date_to=...&command=...&user=...` (Query-params)
**Response**: HTML (rendered template).

---

## 4. Administration (Admin only)

| Method | Route | Description | Auth Required |
|---|---|---|---|
| GET | `/admin/users` | User management dashboard. | Yes (Admin) |
| POST | `/admin/users/create` | Creates a new system user. | Yes (Admin) |
| POST | `/admin/users/<int:id>/toggle` | Activates/Deactivates a user account. | Yes (Admin) |

### POST `/admin/users/create`
**Payload**: `{"username": "...", "password": "...", "role": "Operator"}` (Form-data)
**Response**: Redirect to `/admin/users`.
