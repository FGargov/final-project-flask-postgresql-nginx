document.addEventListener("DOMContentLoaded", function () {
  console.log("Athena Web Quiz frontend loaded");

  // Basic form validation for quiz creation
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      const requiredInputs = form.querySelectorAll("[required]");
      let isValid = true;
      requiredInputs.forEach((input) => {
        if (!input.value.trim()) {
          isValid = false;
          input.style.borderColor = "red";
        } else {
          input.style.borderColor = "";
        }
      });
      if (!isValid) {
        e.preventDefault();
        alert("Please fill in all required fields.");
      }
    });
  });

  // Dynamic answer field addition (for add_question page)
  const answersDiv = document.getElementById("answers");
  if (answersDiv) {
    const addAnswerBtn = document.createElement("button");
    addAnswerBtn.textContent = "Add Another Answer";
    addAnswerBtn.type = "button";
    addAnswerBtn.addEventListener("click", function () {
      const answerCount = answersDiv.children.length;
      const answerDiv = document.createElement("div");
      answerDiv.className = "answer";
      answerDiv.innerHTML = `
        <input type="text" name="answers" placeholder="Answer ${
          answerCount + 1
        }">
        <input type="radio" name="correct" value="${answerCount}">
      `;
      answersDiv.appendChild(answerDiv);
    });
    answersDiv.parentNode.insertBefore(addAnswerBtn, answersDiv.nextSibling);
  }
});
