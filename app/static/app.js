const form = document.getElementById('filtros');
const list = document.getElementById('lista');
const meta = document.getElementById('meta');

function renderJobs(data) {
  meta.textContent = `${data.total} vaga(s) encontrada(s).`;

  if (!data.total) {
    list.innerHTML = '<p>Nenhuma vaga encontrada para os filtros informados.</p>';
    return;
  }

  list.innerHTML = data.vagas
    .map(
      (job) => `
      <article class="card">
        <h3>${job.titulo}</h3>
        <span class="badge">${job.area_especifica}</span>
        <p><strong>Instituição:</strong> ${job.empresa}</p>
        <p><strong>Localidade:</strong> ${job.localidade}</p>
        <p>${job.descricao}</p>
        <p><strong>Requisitos:</strong> ${job.requisitos.join(', ')}</p>
        <a href="${job.link}" target="_blank" rel="noreferrer">Ver vaga</a>
      </article>
    `,
    )
    .join('');
}

async function searchJobs(event) {
  if (event) event.preventDefault();

  const params = new URLSearchParams();
  const localidade = document.getElementById('localidade').value.trim();
  const area = document.getElementById('area').value;

  if (localidade) params.set('localidade', localidade);
  if (area) params.set('area', area);

  const response = await fetch(`/api/vagas?${params.toString()}`);
  const data = await response.json();
  renderJobs(data);
}

form.addEventListener('submit', searchJobs);
searchJobs();
