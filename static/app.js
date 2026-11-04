const form = document.querySelector('#prediction-form');
const panels = [...document.querySelectorAll('.step-panel')];
const progressSteps = [...document.querySelectorAll('.progress-step')];
let currentStep = 1;
const formatCurrency = (value) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);

function showStep(step) {
  currentStep = step;
  panels.forEach((panel) => {
    const active = Number(panel.dataset.step) === step;
    panel.hidden = !active;
    panel.classList.toggle('is-active', active);
  });
  progressSteps.forEach((item) => {
    const itemStep = Number(item.dataset.progressStep);
    item.classList.toggle('is-active', itemStep === step);
    item.classList.toggle('is-complete', itemStep < step);
  });
  if (step < 4) panels.find((panel) => Number(panel.dataset.step) === step).querySelector('input, select')?.focus();
}

function validateStep(step) {
  const panel = panels.find((item) => Number(item.dataset.step) === step);
  const inputs = [...panel.querySelectorAll('input, select')];
  const message = panel.querySelector('.validation-message');
  const invalid = inputs.find((input) => !input.checkValidity());
  message.textContent = invalid ? `Please enter a valid ${invalid.closest('label').childNodes[0].textContent.trim().toLowerCase()}.` : '';
  invalid?.focus();
  return !invalid;
}

document.querySelectorAll('[data-next]').forEach((button) => button.addEventListener('click', () => {
  if (validateStep(currentStep)) showStep(currentStep + 1);
}));
document.querySelectorAll('[data-back]').forEach((button) => button.addEventListener('click', () => showStep(currentStep - 1)));

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!validateStep(3)) return;

  const data = Object.fromEntries(new FormData(form));

  Object.keys(data)
    .filter((key) => key !== "ocean_proximity")
    .forEach((key) => {
      data[key] = Number(data[key]);
    });

  showStep(4);

  const estimate = document.querySelector("#estimate-value");
  const low = document.querySelector("#low-value");
  const high = document.querySelector("#high-value");
  const note = document.querySelector("#result-note");

  estimate.textContent = "Loading...";
  low.textContent = "—";
  high.textContent = "—";
  note.textContent = "Calculating your estimate...";

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "Prediction failed.");
    }

    estimate.textContent = formatCurrency(result.prediction);
    low.textContent = "Range coming next";
    high.textContent = "Range coming next";
    note.textContent =
      "This estimate is based on your saved California housing model.";

  } catch (error) {
    estimate.textContent = "Unavailable";
    low.textContent = "—";
    high.textContent = "—";
    note.textContent = error.message;
  }
});

document.querySelector('#edit-details').addEventListener('click', () => showStep(3));
document.querySelector('#start-over').addEventListener('click', () => { form.reset(); showStep(1); });
