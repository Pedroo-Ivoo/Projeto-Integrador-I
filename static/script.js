const zona = document.getElementById("zona")
if (zona) {
  zona.addEventListener("change", async function () {
  
  const regiaoSelecionada = this.value; // Obtém a região escolhida pelo usuário
  console.log(regiaoSelecionada)
  // Faz a requisição ao Flask para obter os motoristas
  const response = await fetch(
    `/motoristas_por_regiao?regiao=${regiaoSelecionada}`
  );
  const motoristas = await response.json(); // Converte a resposta em JSON

  const selectMotoristas = document.getElementById("motoristas");
  selectMotoristas.innerHTML = ""; // Limpa opções anteriores


// Configura o option do motoristas na seleção do cadastro do aluno
  const optionPadrao = document.createElement("option");
  optionPadrao.value = "";
  optionPadrao.textContent = "Selecione um motorista";
  selectMotoristas.appendChild(optionPadrao);

  // Adiciona os motoristas ao dropdown
  motoristas.forEach(({ id, nome }) => {
    const option = document.createElement("option");
    option.value = id;
    option.textContent = nome;
    selectMotoristas.appendChild(option);
  });
});
}


window.addEventListener("DOMContentLoaded", async () => {
  const motoristaAtual = "{{ motorista_id }}";  // só existe na edição
  const regiaoSelecionada = zona.value;

  // Somente carrega os motoristas se estivermos no modo de edição
  if (regiaoSelecionada && motoristaAtual) {
    const response = await fetch(`/motoristas_por_regiao?regiao=${regiaoSelecionada}`);
    const motoristas = await response.json();
    const selectMotoristas = document.getElementById("motoristas");
    selectMotoristas.innerHTML = "";

    const optionPadrao = document.createElement("option");
    optionPadrao.value = "";
    optionPadrao.textContent = "Selecione um motorista";
    selectMotoristas.appendChild(optionPadrao);

    motoristas.forEach(({ id, nome }) => {
      const option = document.createElement("option");
      option.value = id;
      option.textContent = nome;
      if (String(id) === motoristaAtual) {
        option.selected = true;
      }
      selectMotoristas.appendChild(option);
    });
  }
});


// Configuração do Accordion
const accordions = document.querySelectorAll('.accordion');

accordions.forEach(accordion => {
    accordion.addEventListener('click', () => {
        const body = accordion.querySelector('.accordion-body');
        body.classList.toggle('active');
    })
})

//Configuração do inputmask
$(document).ready(function () {
  $("#celular").inputmask("(99) 99999-9999");
});

//Função do botão deletar. Antes de deletar o cadastro pede a confirmação.
const deletar = document.getElementById("deletar");
deletar.addEventListener("click", function (event) {
  if(confirm("Deletar um cadastro é irreversível, tem certeza?")) {
  
  } else{
    event.preventDefault();
  }
  
})