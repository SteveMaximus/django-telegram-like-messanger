// Contact search functionality
    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('contact-search');
        const contactsList = document.getElementById('contacts-list');
        const userLinks = contactsList.querySelectorAll('.user-link');

        if (searchInput) {
            searchInput.addEventListener('input', function(e) {
                const searchTerm = e.target.value.toLowerCase().trim();
                
                userLinks.forEach(link => {
                    const username = link.dataset.username.toLowerCase();
                    const contactInfo = link.querySelector('.contact-name').textContent.toLowerCase();
                    
                    if (username.includes(searchTerm) || contactInfo.includes(searchTerm)) {
                        link.parentElement.style.display = '';
                    } else {
                        link.parentElement.style.display = 'none';
                    }
                });
            });
        }

        // Auto-scroll to bottom on load
        const chatWindow = document.getElementById('chat-window');
        if (chatWindow) {
            setTimeout(() => {
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }, 100);
        }

        // Send message on Ctrl+Enter for textarea
        const messageInput = document.querySelector('textarea[name="message"]');
        if (messageInput) {
            messageInput.addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key === 'Enter') {
                    e.preventDefault();
                    this.form.submit();
                }
            });
        }

        // Header menu toggle and wallpaper handling
        const menuBtn = document.getElementById('menuBtn');
        const headerMenu = document.getElementById('headerMenu');
        const changeWallpaper = document.getElementById('changeWallpaper');
        const wallpaperUpload = document.getElementById('wallpaperUpload');
        const wallpaperBtns = document.querySelectorAll('.wallpaper-btn');
        const chatWrapper = document.querySelector('.chat-wrapper');

        menuBtn && menuBtn.addEventListener('click', function(e){
            e.stopPropagation();
            headerMenu.style.display = headerMenu.style.display === 'none' ? 'block' : 'none';
        });

        // close menu on outside click
        document.addEventListener('click', function(){ if(headerMenu) headerMenu.style.display = 'none'; });

        changeWallpaper && changeWallpaper.addEventListener('click', function(){ wallpaperUpload.click(); });
        wallpaperUpload && wallpaperUpload.addEventListener('change', function(e){
            const f = e.target.files[0];
            if(!f) return;
            const url = URL.createObjectURL(f);
            localStorage.setItem('chat_wallpaper', url);
            applyWallpaper();
        });

        wallpaperBtns.forEach(b=> b.addEventListener('click', function(){
            const v = this.dataset.bg;
            localStorage.setItem('chat_wallpaper', v);
            applyWallpaper();
        }));

        function applyWallpaper(){
            const v = localStorage.getItem('chat_wallpaper') || 'default';
            if(!chatWrapper) return;
            if(v === 'default'){
                chatWrapper.style.background = 'linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%)';
                chatWrapper.style.backgroundSize = '';
            } else if(v === 'pattern'){
                chatWrapper.style.background = "repeating-linear-gradient( -45deg, #f8fbfd, #f8fbfd 10px, #f0f6fb 10px, #f0f6fb 20px)";
            } else if(v === 'grid'){
                chatWrapper.style.background = "linear-gradient(#f5f5f5, #fff)";
                chatWrapper.style.backgroundImage = "linear-gradient(0deg, rgba(0,0,0,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(0,0,0,0.02) 1px, transparent 1px)";
                chatWrapper.style.backgroundSize = '24px 24px, 24px 24px';
            } else if(v.startsWith('blob:') || v.startsWith('data:') || v.startsWith('http')){
                chatWrapper.style.background = `url(${v}) center/cover no-repeat`;
            }
        }

        // apply wallpaper on load
        applyWallpaper();
    });