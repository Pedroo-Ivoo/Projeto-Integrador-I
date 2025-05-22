document.getElementById("zona").addEventListener("change", async function () {
  const regiaoSelecionada = this.value;

  // Faz a requisição ao Flask
  const response = await fetch(
    `http://127.0.0.1:5000/motoristas?regiao=${regiaoSelecionada}`
  );
  const motoristas = await response.json();

  const selectMotoristas = document.getElementById("motoristas");
  selectMotoristas.innerHTML = ""; // Limpa opções anteriores

  motoristas.forEach((nome) => {
    const option = document.createElement("option");
    option.value = nome;
    option.textContent = nome;
    selectMotoristas.appendChild(option);
  });
});

document
  .querySelector(".formulario")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Impede o envio do formulário
    alert("Cadastro realizado");
  });
