// viacep.js — máscara + busca (robusto)
(function () {
  function qs(selector) {
    return document.querySelector(selector);
  }

  function findCepInput() {
    return qs('#cep') || qs('input[name="cep"]') || qs('input[data-cep]');
  }

  function formatCepValue(v) {
    const digits = v.replace(/\D/g, '').slice(0, 8);
    if (digits.length > 5) {
      return digits.replace(/(\d{5})(\d{1,3})/, '$1-$2');
    }
    return digits;
  }

  function setCaretToEnd(el) {
    try {
      const len = el.value.length;
      el.setSelectionRange(len, len);
    } catch (e) { /* ignore */ }
  }

  async function fetchCep(cep, onSuccess, onError) {
    try {
      const res = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
      const data = await res.json();
      if (data.erro) {
        onError && onError('CEP não encontrado');
      } else {
        onSuccess && onSuccess(data);
      }
    } catch (err) {
      onError && onError('Erro na requisição');
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    const cepInput = findCepInput();
    if (!cepInput) {
      console.warn('viacep.js: campo de CEP não encontrado (id="cep" ou name="cep").');
      return;
    }

    // Máscara: input
    cepInput.addEventListener('input', function (e) {
      const old = this.value;
      const formatted = formatCepValue(old);
      this.value = formatted;
      // tenta manter o cursor ao final (suficiente pra maioria dos casos)
      setCaretToEnd(this);
    });

    // Busca: blur (quando o usuário sair do campo)
    cepInput.addEventListener('blur', function () {
      const cepDigits = this.value.replace(/\D/g, '');
      if (cepDigits.length !== 8) return;

      // elementos alvo (procura por ids)
      const ruaEl = qs('#rua') || qs('input[name="rua"]');
      const bairroEl = qs('#bairro') || qs('input[name="bairro"]');
      const cidadeEl = qs('#cidade') || qs('input[name="cidade"]');
      const ufEl = qs('#uf') || qs('input[name="uf"]');

      fetchCep(cepDigits, function (data) {
        if (ruaEl) ruaEl.value = data.logradouro || '';
        if (bairroEl) bairroEl.value = data.bairro || '';
        if (cidadeEl) cidadeEl.value = data.localidade || '';
        if (ufEl) ufEl.value = data.uf || '';
      }, function (errMsg) {
        console.warn('viacep:', errMsg);
        // opcional: mostrar aviso ao usuário
        // alert(errMsg);
      });
    });
  });
})();
