/**
 * ============================================================================
 * Prakriti: Nature & Belief Explorer - Quiz Engine
 * ============================================================================
 * Handles the "Superstition or Science?" interactive 10-question challenge:
 * - Dynamic question loading and state management
 * - Instant feedback highlighting correct & incorrect answers
 * - In-depth scientific/ecological explanation presentation
 * - Final score computation with cultural & ecological badges
 * - Full breakdown review of all questions answered
 * ============================================================================
 */

document.addEventListener("DOMContentLoaded", function () {
  const quizWrapper = document.getElementById("quizAppWrapper");
  if (!quizWrapper) return;

  // Retrieve quiz data embedded in JSON script tag
  const questionsDataEl = document.getElementById("quizDataJson");
  if (!questionsDataEl) return;

  let questions = [];
  try {
    questions = JSON.parse(questionsDataEl.textContent);
  } catch (err) {
    console.error("Failed to parse quiz questions:", err);
    return;
  }

  if (questions.length === 0) {
    quizWrapper.innerHTML = `
      <div class="quiz-card" style="text-align: center;">
        <h3 style="color: var(--terracotta);">No quiz questions found</h3>
        <p>Please check back later or initialize the database.</p>
      </div>
    `;
    return;
  }

  // Quiz State
  let currentIndex = 0;
  let score = 0;
  let userResponses = []; // stores { questionIndex, selectedOption, isCorrect }

  // DOM Elements
  const progressFill = document.getElementById("quizProgressFill");
  const questionNumberEl = document.getElementById("questionNumberLabel");
  const scoreCounterEl = document.getElementById("currentScoreBadge");
  const questionTextEl = document.getElementById("questionPromptText");
  const optionsContainer = document.getElementById("quizOptionsContainer");
  const explanationBox = document.getElementById("explanationContainer");
  const explanationTitle = document.getElementById("explanationTitle");
  const explanationText = document.getElementById("explanationBodyText");
  const nextBtn = document.getElementById("nextQuestionBtn");
  const quizCard = document.getElementById("mainQuizCard");
  const resultsCard = document.getElementById("quizResultsCard");

  function renderQuestion(index) {
    const q = questions[index];
    const total = questions.length;

    // Reset UI states
    explanationBox.style.display = "none";
    nextBtn.style.display = "none";
    optionsContainer.innerHTML = "";

    // Update Progress
    const progressPercent = ((index + 1) / total) * 100;
    if (progressFill) progressFill.style.width = `${progressPercent}%`;
    if (questionNumberEl) questionNumberEl.textContent = `Question ${index + 1} of ${total}`;
    if (scoreCounterEl) scoreCounterEl.textContent = `Score: ${score}`;

    // Set Question Text
    if (questionTextEl) questionTextEl.textContent = q.question;

    // Build Options (A, B, C, D)
    const options = [
      { key: "A", text: q.option_a },
      { key: "B", text: q.option_b },
      { key: "C", text: q.option_c },
      { key: "D", text: q.option_d },
    ];

    options.forEach((opt) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "option-btn";
      btn.dataset.option = opt.key;
      btn.innerHTML = `
        <span class="option-letter">${opt.key}</span>
        <span class="option-text">${escapeHtml(opt.text)}</span>
      `;

      btn.addEventListener("click", () => handleSelectOption(opt.key, q));
      optionsContainer.appendChild(btn);
    });
  }

  function handleSelectOption(selectedKey, question) {
    const isCorrect = selectedKey === question.correct_option;
    if (isCorrect) {
      score++;
    }

    // Save response for review
    userResponses.push({
      question: question.question,
      selectedKey: selectedKey,
      correctKey: question.correct_option,
      isCorrect: isCorrect,
      explanation: question.explanation,
      options: {
        A: question.option_a,
        B: question.option_b,
        C: question.option_c,
        D: question.option_d,
      },
    });

    // Update buttons UI
    const allButtons = optionsContainer.querySelectorAll(".option-btn");
    allButtons.forEach((btn) => {
      btn.disabled = true;
      const optKey = btn.dataset.option;

      if (optKey === question.correct_option) {
        btn.classList.add("correct");
      } else if (optKey === selectedKey && !isCorrect) {
        btn.classList.add("incorrect");
      }
    });

    // Show Explanation Box
    explanationTitle.innerHTML = isCorrect
      ? `🌿 Excellent! Ecological Science Confirmed`
      : `🌱 Traditional Wisdom & Ecological Science`;
    explanationTitle.style.color = isCorrect
      ? "var(--green-forest)"
      : "var(--terracotta)";
    explanationText.textContent = question.explanation;
    explanationBox.style.display = "block";

    // Show Next or Results Button
    if (currentIndex < questions.length - 1) {
      nextBtn.textContent = "Next Question →";
    } else {
      nextBtn.textContent = "See Final Results 🌟";
    }
    nextBtn.style.display = "inline-flex";

    // Update score counter badge
    if (scoreCounterEl) scoreCounterEl.textContent = `Score: ${score}`;
  }

  // Handle Next Question Click
  if (nextBtn) {
    nextBtn.addEventListener("click", function () {
      currentIndex++;
      if (currentIndex < questions.length) {
        renderQuestion(currentIndex);
      } else {
        renderFinalResults();
      }
    });
  }

  function renderFinalResults() {
    quizCard.style.display = "none";
    resultsCard.style.display = "block";

    const total = questions.length;
    const finalScoreEl = document.getElementById("finalScoreNumber");
    const finalBadgeTitle = document.getElementById("finalBadgeTitle");
    const finalFeedbackEl = document.getElementById("finalFeedbackText");
    const reviewListContainer = document.getElementById("quizReviewList");

    if (finalScoreEl) finalScoreEl.textContent = score;

    let badgeTitle = "";
    let feedback = "";

    if (score >= 9) {
      badgeTitle = "🌿 Prakriti Acharya (Nature Sage)";
      feedback =
        "Exceptional knowledge! You deeply understand how traditional Indian customs gracefully encode ecological conservation, biodiversity preservation, and sustainable coexistence.";
    } else if (score >= 7) {
      badgeTitle = "🌱 Eco-Guardian (Protector of Earth)";
      feedback =
        "Great job! You have a strong grasp of the scientific and ecological reasons anchoring our sacred festivals and reverential traditions.";
    } else if (score >= 5) {
      badgeTitle = "🍃 Curious Seeker (Nature Inquirer)";
      feedback =
        "Well done! You recognize that ancient traditions carry valuable scientific truths. Explore the browse page to learn more about the 12 sacred elements.";
    } else {
      badgeTitle = "🍂 Prakriti Explorer (Beginner Seeker)";
      feedback =
        "A wonderful first exploration! Traditional rituals often hold fascinating ecological wisdom disguised as sacred duties. Review the answers below to discover more!";
    }

    if (finalBadgeTitle) finalBadgeTitle.textContent = badgeTitle;
    if (finalFeedbackEl) finalFeedbackEl.textContent = feedback;

    // Render Full Breakdown Review
    if (reviewListContainer) {
      reviewListContainer.innerHTML = "";
      userResponses.forEach((item, idx) => {
        const reviewItem = document.createElement("div");
        reviewItem.className = "quiz-review-item";
        reviewItem.style.cssText = `
          background: #FFF;
          border: 1px solid var(--border-subtle);
          border-left: 5px solid ${item.isCorrect ? "var(--green-forest)" : "#E74C3C"};
          border-radius: var(--radius-md);
          padding: 20px;
          margin-bottom: 18px;
          text-align: left;
        `;

        reviewItem.innerHTML = `
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 0.82rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">
              Question ${idx + 1}
            </span>
            <span style="font-size: 0.82rem; font-weight: 700; color: ${
              item.isCorrect ? "var(--green-forest)" : "#E74C3C"
            };">
              ${item.isCorrect ? "✓ Correct" : "✕ Incorrect"}
            </span>
          </div>
          <h4 style="font-size: 1.05rem; color: var(--green-deep); margin-bottom: 12px; font-family: inherit;">
            ${escapeHtml(item.question)}
          </h4>
          <p style="font-size: 0.88rem; color: var(--text-body); margin-bottom: 6px;">
            <strong>Your Answer:</strong> <span style="color: ${
              item.isCorrect ? "var(--green-forest)" : "#E74C3C"
            };">(${item.selectedKey}) ${escapeHtml(item.options[item.selectedKey])}</span>
          </p>
          ${
            !item.isCorrect
              ? `<p style="font-size: 0.88rem; color: var(--green-forest); margin-bottom: 8px;">
                   <strong>Correct Answer:</strong> (${item.correctKey}) ${escapeHtml(
                  item.options[item.correctKey]
                )}
                 </p>`
              : ""
          }
          <div style="background: var(--bg-cream); border-radius: var(--radius-sm); padding: 12px; font-size: 0.88rem; color: var(--text-body); margin-top: 10px; line-height: 1.6;">
            <strong style="color: var(--green-forest);">Science & Ecology:</strong> ${escapeHtml(item.explanation)}
          </div>
        `;
        reviewListContainer.appendChild(reviewItem);
      });
    }
  }

  // Handle Retake Quiz
  const retakeBtn = document.getElementById("retakeQuizBtn");
  if (retakeBtn) {
    retakeBtn.addEventListener("click", function () {
      currentIndex = 0;
      score = 0;
      userResponses = [];
      resultsCard.style.display = "none";
      quizCard.style.display = "block";
      renderQuestion(0);
    });
  }

  // Helper function to escape HTML entities
  function escapeHtml(text) {
    if (!text) return "";
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Start with first question
  renderQuestion(0);
});
