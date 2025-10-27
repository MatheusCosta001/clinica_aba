// captura evento de blur no campo cep e preenche os campos
document.addEventListener("DOMContentLoaded", function(){
  const cepInput = document.getElementById("cep");
  if (!cepInput) return;
  cepInput.addEventListener("blur", function(){
    const cep = cepInput.value.replace(/\D/g, "");
    if (cep.length !== 8) return;
    fetch(`https://viacep.com.br/ws/${cep}/json/`)
      .then(resp => resp.json())
      .then(data => {
        if (data.erro) {
          alert("CEP não encontrado.");
          return;
        }
        document.getElementById("rua").value = data.logradouro || "";
        document.getElementById("bairro").value = data.bairro || "";
        document.getElementById("cidade").value = data.localidade || "";
        document.getElementById("uf").value = data.uf || "";
      })
      .catch(err => {
        console.error(err);
        alert("Erro ao consultar ViaCEP.");
      });
  });
});
