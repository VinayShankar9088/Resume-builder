// 🌟 Enhanced client-side resume preview + required toggle logic

function getFormData() {
    const form = document.getElementById('resume-form');
    const fd = new FormData(form);
    return Object.fromEntries(fd.entries());
}

function renderPreview(data) {
    const skills = (data.skills || '').split(',').map(s => s.trim()).filter(Boolean).join(', ');
    const educations = (data.education || '').split('\n').map(s => s.trim()).filter(Boolean);
    const projects = (data.projects || '').split('\n').map(s => s.trim()).filter(Boolean);
    const experiences = (data.experience || '').split('\n').map(s => s.trim()).filter(Boolean);
    const certificates = (data.certificates || '').split('\n').map(s => s.trim()).filter(Boolean);

    let html = `<div class="resume-card">`;
    html += `<header>`;

    // 📸 Image preview
    const photoInput = document.getElementById('photo');
    if (photoInput && photoInput.files[0]) {
        const imgURL = URL.createObjectURL(photoInput.files[0]);
        html += `<img src="${imgURL}" class="profile" alt="Profile Photo">`;
    }

    html += `<div>`;
    html += `<h1>${data.name || 'Your Name'}</h1>`;
    html += `<p>${data.email || ''}</p>`;
    html += `<p>${data.phone || ''}</p>`;
    html += `</div>`;
    html += `</header>`;

    if (skills) {
        html += `<h3>Skills</h3><p>${skills}</p>`;
    }

    if (educations.length) {
        html += `<h3>Education</h3><ul>${educations.map(e => `<li>${e}</li>`).join('')}</ul>`;
    }

    if (experiences.length) {
        html += `<h3>Experience</h3><ul>${experiences.map(e => `<li>${e}</li>`).join('')}</ul>`;
    }

    if (projects.length) {
        html += `<h3>Projects</h3><ul>${projects.map(p => `<li>${p}</li>`).join('')}</ul>`;
    }

    if (certificates.length) {
        html += `<h3>Certificates</h3><ul>${certificates.map(c => `<li>${c}</li>`).join('')}</ul>`;
    }

    html += `</div>`;

    document.getElementById('preview').innerHTML = html;
}

// 🔄 Toggle required fields
function toggleRequiredFields(enabled) {
    const requiredFields = document.querySelectorAll('[data-required]');
    requiredFields.forEach(field => {
        if (enabled) {
            field.setAttribute('required', 'required');
        } else {
            field.removeAttribute('required');
        }
    });
}

// 🧠 Event listeners
document.getElementById('resume-form').addEventListener('input', () => {
    const data = getFormData();
    renderPreview(data);
});

document.getElementById('toggle-required').addEventListener('change', (e) => {
    toggleRequiredFields(e.target.checked);
});
window.addEventListener('DOMContentLoaded', updatePreview);