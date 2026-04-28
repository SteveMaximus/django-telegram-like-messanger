document.addEventListener('DOMContentLoaded', function(){
    const btn = document.getElementById('startCallBtn');
    if(!btn) return;
    btn.addEventListener('click', function(e){
        e.preventDefault();
        const name = '{{ for_user.username }}';
        const ok = confirm('Начать видеозвонок с ' + name + '?');
        if(ok){ window.location.href = btn.href; }
    });
});