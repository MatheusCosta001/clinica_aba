function buscaCep(cepInputId) {
  const cepField = document.getElementById(cepInputId);
  if (!cepField) return;
  const cep = cepField.value.replace(/\D/g, '');
  if (!cep) return;
  fetch(`https://viacep.com.br/ws/${cep}/json/`)
    .then(res => res.json())
    .then(data => {
      if (data.erro) return;
      const rua = document.getElementById('rua');
      const bairro = document.getElementById('bairro');
      const cidade = document.getElementById('cidade');
      const uf = document.getElementById('uf');
      if (rua) rua.value = data.logradouro || '';
      if (bairro) bairro.value = data.bairro || '';
      if (cidade) cidade.value = data.localidade || '';
      if (uf) uf.value = data.uf || '';
    }).catch(err => console.error(err));
}
