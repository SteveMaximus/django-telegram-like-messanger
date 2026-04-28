// videoplayer.js
// Handles clicks on images, videos, and profile avatars to show a modal
// with the media and optional download link.

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('media-modal');
    const content = modal.querySelector('.media-content');
    const closeBtn = modal.querySelector('.close');
    const downloadLink = document.getElementById('media-download');

    function showModal(elementType, src) {
        // clear previous content
        content.innerHTML = '';
        downloadLink.style.display = 'none';

        if (elementType === 'img') {
            const img = document.createElement('img');
            img.src = src;
            img.style.maxWidth = '100%';
            img.style.maxHeight = '100%';
            content.appendChild(img);
            downloadLink.href = src;
            downloadLink.style.display = 'block';
        } else if (elementType === 'video') {
            const video = document.createElement('video');
            video.controls = true;
            video.autoplay = true;
            video.src = src;
            video.style.maxWidth = '100%';
            video.style.maxHeight = '100%';
            content.appendChild(video);
            downloadLink.href = src;
            downloadLink.style.display = 'block';
        }

        modal.style.display = 'block';
    }

    function hideModal() {
        modal.style.display = 'none';
        content.innerHTML = '';
    }

    // click handlers for images / videos in messages
    document.body.addEventListener('click', (ev) => {
        const img = ev.target.closest('.message-image');
        if (img) {
            showModal('img', img.src);
            return;
        }
        const video = ev.target.closest('.message-video');
        if (video) {
            showModal('video', video.querySelector('source').src);
            return;
        }
        const avatar = ev.target.closest('.account-img');
        if (avatar) {
            showModal('img', avatar.src);
            return;
        }
    });

    closeBtn.addEventListener('click', hideModal);
    modal.addEventListener('click', (ev) => {
        if (ev.target === modal) hideModal();
    });
});
