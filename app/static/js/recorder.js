let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById('start-record');
const stopBtn = document.getElementById('stop-record');
const statusText = document.getElementById('record-status');
const processingStatus = document.getElementById('processing-status');
const resultContainer = document.getElementById('result-container');
const recordControls = document.getElementById('record-controls');

startBtn.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            await uploadAudio(audioBlob);
        };

        mediaRecorder.start();
        startBtn.classList.add('d-none');
        stopBtn.classList.remove('d-none');
        statusText.innerText = "Идет запись... Говорите";
        statusText.classList.add('text-danger');
    } catch (err) {
        console.error("Error accessing microphone:", err);
        alert("Не удалось получить доступ к микрофону. Убедитесь, что разрешили доступ в браузере.");
    }
});

stopBtn.addEventListener('click', () => {
    mediaRecorder.stop();
    mediaRecorder.stream.getTracks().forEach(track => track.stop());
    stopBtn.classList.add('d-none');
    startBtn.classList.remove('d-none');
    statusText.innerText = "Запись завершена. Обработка...";
    statusText.classList.remove('text-danger');
});

async function uploadAudio(blob) {
    processingStatus.classList.remove('d-none');
    recordControls.classList.add('d-none');

    const formData = new FormData();
    formData.append('audio_blob', blob, 'recording.webm');

    try {
        const response = await fetch('/record/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (response.ok) {
            displayResult(result);
        } else {
            alert("Ошибка при обработке: " + (result.error || "Неизвестная ошибка"));
        }
    } catch (err) {
        console.error("Upload error:", err);
        alert("Ошибка сети при отправке аудио.");
    } finally {
        processingStatus.classList.add('d-none');
        recordControls.classList.remove('d-none');
        statusText.innerText = "Нажмите для начала записи";
    }
}

function displayResult(data) {
    const html = `
        <div class="card border-primary">
            <div class="card-body">
                <h5 class="card-title text-primary">Распознанный текст:</h5>
                <p class="card-text fs-5">"${data.raw_text || 'Текст не распознан'}"</p>
                <hr>
                <div class="row">
                    <div class="col-md-6">
                        <strong>Команда:</strong> 
                        <span class="badge bg-info text-dark">${data.command || 'Не определена'}</span>
                    </div>
                    <div class="col-md-6">
                        <strong>Идентификатор:</strong> 
                        <span class="badge bg-warning text-dark">${data.identifier || 'Не найден'}</span>
                    </div>
                </div>
                <div class="mt-3">
                    <audio controls src="${data.audio_url}" class="w-100"></audio>
                </div>
                <div class="mt-4 d-flex gap-2">
                    <button class="btn btn-success flex-grow-1" onclick="confirmResult(${data.id})">
                        <i class="fa-solid fa-check me-2"></i>Подтвердить
                    </button>
                    <button class="btn btn-outline-secondary" onclick="editResult(${data.id}, '${data.command}', '${data.identifier}', '${data.raw_text}')">
                        <i class="fa-solid fa-pen"></i> Редактировать
                    </button>
                </div>
            </div>
        </div>
    `;
    resultContainer.innerHTML = html;
}

window.confirmResult = async function(id) {
    try {
        const response = await fetch(`/record/${id}/confirm`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: 'confirmed' })
        });
        if (response.ok) {
            alert("Запись подтверждена!");
            location.reload();
        }
    } catch (err) {
        console.error("Confirm error:", err);
    }
};

window.editResult = function(id, command, identifier, raw_text) {
    const modalBody = document.querySelector('#confirmModal .modal-body');
    modalBody.innerHTML = `
        <form id="edit-form">
            <div class="mb-3">
                <label class="form-label">Команда</label>
                <input type="text" class="form-control" id="edit-command" value="${command}">
            </div>
            <div class="mb-3">
                <label class="form-label">Идентификатор</label>
                <input type="text" class="form-control" id="edit-identifier" value="${identifier}">
            </div>
            <div class="mb-3">
                <label class="form-label">Полный текст</label>
                <textarea class="form-control" id="edit-text" rows="3">${raw_text}</textarea>
            </div>
            <div class="d-grid">
                <button type="button" class="btn btn-primary" onclick="submitEdit(${id})">Сохранить изменения</button>
            </div>
        </form>
    `;
    const modal = new bootstrap.Modal(document.getElementById('confirmModal'));
    modal.show();
};

window.submitEdit = async function(id) {
    const command = document.getElementById('edit-command').value;
    const identifier = document.getElementById('edit-identifier').value;
    const text = document.getElementById('edit-text').value;

    try {
        const response = await fetch(`/record/${id}/confirm`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                command: command,
                identifier: identifier,
                corrected_text: text,
                status: 'confirmed'
            })
        });
        if (response.ok) {
            alert("Изменения сохранены!");
            location.reload();
        }
    } catch (err) {
        console.error("Edit error:", err);
    }
};
