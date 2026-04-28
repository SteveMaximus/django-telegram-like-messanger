


document.addEventListener('DOMContentLoaded', function() {
    // Auto-resize textarea and keyboard shortcuts for sending
    const textEl = document.querySelector('textarea[name="message"]') || document.querySelector('input[name="message"]');

    function autoResize(el) {
        if (!el || el.tagName !== 'TEXTAREA') return;
        el.style.height = 'auto';
        el.style.height = (el.scrollHeight) + 'px';
    }

    if (textEl) {
        if (textEl.tagName === 'TEXTAREA') {
            textEl.style.overflow = 'hidden';
            textEl.style.resize = 'vertical';
            autoResize(textEl);
            textEl.addEventListener('input', () => autoResize(textEl));

            textEl.addEventListener('keydown', function (e) {
                // Ctrl+Enter or Enter (without Shift) submits
                if ((e.ctrlKey && e.key === 'Enter') || (e.key === 'Enter' && !e.shiftKey)) {
                    e.preventDefault();
                    if (this.form) this.form.submit();
                }
            });
        } else {
            // simple input field: Enter to send
            textEl.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    if (this.form) this.form.submit();
                }
            });
        }

        // focus input so user can type immediately
        try { textEl.focus({preventScroll: true}); } catch (e) { textEl.focus(); }
    }

    // Confirm deletion for elements with .delete-btn
    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.delete-btn');
        if (!btn) return;
        const ok = confirm('Удалить сообщение?');
        if (!ok) {
            e.preventDefault();
            e.stopPropagation();
        }
    }, true);

    // Highlight and autoscroll when new messages arrive
    const chatWindow = document.getElementById('chat-window');
    if (chatWindow) {
        const observer = new MutationObserver(function (mutations) {
            let added = false;
            for (const m of mutations) {
                if (m.addedNodes && m.addedNodes.length) { added = true; break; }
            }
            if (added) {
                // small pulse effect
                chatWindow.classList.add('pulse-new');
                setTimeout(() => chatWindow.classList.remove('pulse-new'), 700);
                // autoscroll to bottom
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }
        });
        observer.observe(chatWindow, {childList: true, subtree: true});
    }

    // Generic copy-to-clipboard for buttons with data-copy attribute
    document.addEventListener('click', async function (e) {
        const btn = e.target.closest('[data-copy]');
        if (!btn) return;
        const selector = btn.dataset.copy;
        const target = document.querySelector(selector);
        if (!target) return;
        const text = target.value || target.textContent || '';
        try {
            await navigator.clipboard.writeText(text);
            const old = btn.textContent;
            btn.textContent = 'Copied';
            setTimeout(() => btn.textContent = old, 1400);
        } catch (err) {
            console.warn('Copy failed', err);
        }
    });
});

/* Small helper CSS class used for pulse in chat - kept here so JS can rely on it.
   Add matching CSS in templates or global stylesheet:
   .pulse-new { box-shadow: 0 0 0 4px rgba(3,102,153,0.06) inset; }
*/