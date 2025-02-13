
document.addEventListener('DOMContentLoaded', () => {
  const steps = document.querySelectorAll('.breadcrumb-step .step');
  const formSections = document.querySelectorAll('.form-section');
  const nextButtons = document.querySelectorAll('.btn-next');
  const prevButtons = document.querySelectorAll('.btn-prev');

  function showStep(step) {
    steps.forEach((el, index) => {
      el.classList.toggle('active', index + 1 === step);
      el.classList.toggle('completed', index + 1 < step);
    });

    formSections.forEach((el, index) => {
      el.classList.toggle('active', index + 1 === step);
    });
  }

  nextButtons.forEach(button => {
    button.addEventListener('click', () => {
      const currentStep = [...steps].findIndex(el => el.classList.contains('active')) + 1;
      showStep(currentStep + 1);
    });
  });

  prevButtons.forEach(button => {
    button.addEventListener('click', () => {
      const currentStep = [...steps].findIndex(el => el.classList.contains('active')) + 1;
      showStep(currentStep - 1);
    });
  });
});








function showStep(step) {
  steps.forEach((el, index) => {
      el.classList.toggle('active', index + 1 === step);
      el.classList.toggle('completed', index + 1 < step);
  });

  formSections.forEach((el, index) => {
      el.classList.toggle('active', index + 1 === step);
  });
}
nextButtons.forEach(button => {
  button.addEventListener('click', () => {
      const currentStep = [...steps].findIndex(el => el.classList.contains('active')) + 1;
      showStep(currentStep + 1);
  });
});

prevButtons.forEach(button => {
  button.addEventListener('click', () => {
      const currentStep = [...steps].findIndex(el => el.classList.contains('active')) + 1;
      showStep(currentStep - 1);
  });
});
function showStep(step) {
  console.log("Current step:", step);
  steps.forEach((el, index) => {
      el.classList.toggle('active', index + 1 === step);
      el.classList.toggle('completed', index + 1 < step);
  });

  formSections.forEach((el, index) => {
      el.classList.toggle('active', index + 1 === step);
  });
}
