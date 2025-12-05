document.addEventListener("DOMContentLoaded", () => {
    console.log("Frontend da Clínica ABA carregado com sucesso");
    const removedPatients = JSON.parse(localStorage.getItem('permanent_removed_patients') || '[]');
    const removedUsers = JSON.parse(localStorage.getItem('permanent_removed_users') || '[]');

    
    removedPatients.forEach(pid => {
        document.querySelectorAll(`[data-patient-id='${pid}']`).forEach(el => el.remove());
        document.querySelectorAll(`[data-paciente-id='${pid}']`).forEach(el => el.remove());
    });

    
    removedUsers.forEach(uid => {
        document.querySelectorAll(`[data-user-id='${uid}']`).forEach(el => el.remove());
    });

    
    document.querySelectorAll('.btn-perm-remove-patient').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const pid = btn.getAttribute('data-pid');
            if(!pid) return;
            if(!confirm('Excluir permanentemente este paciente para todos os usuários?')) return;
            const arr = JSON.parse(localStorage.getItem('permanent_removed_patients') || '[]');
            if(!arr.includes(pid)) arr.push(pid);
            localStorage.setItem('permanent_removed_patients', JSON.stringify(arr));
            document.querySelectorAll(`[data-patient-id='${pid}']`).forEach(el => el.remove());
            document.querySelectorAll(`[data-paciente-id='${pid}']`).forEach(el => el.remove());
            alert('Paciente removido!')
        })
    });

    
    document.querySelectorAll('.btn-perm-remove-user').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const uid = btn.getAttribute('data-uid');
            if(!uid) return;
            if(!confirm('Excluir permanentemente este usuário?')) return;
            const arr = JSON.parse(localStorage.getItem('permanent_removed_users') || '[]');
            if(!arr.includes(uid)) arr.push(uid);
            localStorage.setItem('permanent_removed_users', JSON.stringify(arr));
            document.querySelectorAll(`[data-user-id='${uid}']`).forEach(el => el.remove());
            alert('Usuário removido!')
        })
    });

    document.querySelectorAll('[data-toggle="toggle-password"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const target = btn.getAttribute('data-target');
            if(!target) return;
            const input = document.querySelector(target) || document.querySelector(target.replace('#',''));
            const el = document.querySelector(target);
            if(!el) return;
            if(el.type === 'password') el.type = 'text'; else el.type = 'password';
        })
    });
});