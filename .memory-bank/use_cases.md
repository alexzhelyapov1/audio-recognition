# Use Case Scenarios

This document outlines the primary use cases for the Voice Command Recognition System, distinguishing between Operator and Admin roles.

## Actors
- **Operator**: Users who record commands, verify results, and search history.
- **Admin**: Users who manage system access and user accounts.

## UML Use Case Diagram

```mermaid
useCaseDiagram
    actor "Operator" as Op
    actor "Admin" as Adm

    package "Voice Command Recognition System" {
        usecase "Authenticate (Login/Logout)" as UC_Auth
        usecase "Record Voice Command" as UC_Record
        usecase "Automatic Transcription (VOSK)" as UC_Transcribe
        usecase "Extract Command & ID" as UC_Extract
        usecase "Manual Result Correction" as UC_Correct
        usecase "Audio Playback" as UC_Audio
        usecase "Confirm Recognition" as UC_Confirm
        usecase "Search/Filter History" as UC_History
        usecase "Manage Users (Create/Block/Roles)" as UC_ManageUsers
    }

    Op --> UC_Auth
    Op --> UC_Record
    Op --> UC_Transcribe
    Op --> UC_Extract
    Op --> UC_Correct
    Op --> UC_Audio
    Op --> UC_Confirm
    Op --> UC_History

    Adm --|> Op
    Adm --> UC_ManageUsers
```

## Scenario 1: Operator records a command
1. **Operator** logs in to the system.
2. **Operator** opens the recording interface and speaks a command (e.g., "Зарегистрировать трубу P45345ИВ").
3. **System** transcribes audio to text using VOSK.
4. **System** extracts the key command ("Зарегистрировать") and the identifier ("P45345ИВ").
5. **System** displays the recognition results (text, command, ID) to the operator.
6. **System** saves the raw audio and metadata to the database.

## Scenario 2: Operator corrects transcription
1. **Operator** reviews the recognition result.
2. If incorrect, **Operator** clicks on the record detail/card.
3. **Operator** listens to the original audio playback.
4. **Operator** manually edits the text, command, or identifier.
5. **Operator** confirms the record.
6. **System** updates the record status and metadata (e.g., "Confirmed").

## Scenario 3: History Search & Verification
1. **Operator** opens the history page.
2. **Operator** applies filters (date range, command type, operator name, specific identifier).
3. **System** displays a list of matching records.
4. **Operator** clicks a record to view its full details and listen to the audio.

## Scenario 4: Admin User Management
1. **Admin** logs in and navigates to the user management panel.
2. **Admin** creates a new user account with the "Operator" role.
3. **Admin** resets a password or blocks an account (e.g., due to security policy).
4. **System** applies changes immediately to the authentication layer.
