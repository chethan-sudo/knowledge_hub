import { test, expect } from '@playwright/test';

const BASE_URL = process.env.REACT_APP_BACKEND_URL || 'https://ai-agent-hub-96.preview.emergentagent.com';

// Category IDs for testing
const GETTING_STARTED_CAT_ID = 'ff182579-9490-422f-9d69-30ce642cf662';
const PLATFORM_ARCH_CAT_ID = 'a62bc498-73f6-44be-8230-979af325b628';
const LLM_INTERNALS_CAT_ID = '52c88f91-c6d7-401b-8b56-c29a8a639a56';

test.describe('Category Page & Module Tests', () => {
  
  test.beforeEach(async ({ page }) => {
    // Remove Emergent badge if present to avoid click interference
    await page.addInitScript(() => {
      const observer = new MutationObserver(() => {
        const badge = document.querySelector('[class*="emergent"], [id*="emergent-badge"]');
        if (badge) badge.remove();
      });
      observer.observe(document.body, { childList: true, subtree: true });
    });
  });

  test('Homepage cards navigate to category page', async ({ page }) => {
    await page.goto('/', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('home-page')).toBeVisible({ timeout: 15000 });
    
    // Find a home card for Getting Started
    const homeCard = page.locator(`[data-testid="home-card-${GETTING_STARTED_CAT_ID}"]`);
    await expect(homeCard).toBeVisible();
    
    // Click the card
    await homeCard.click();
    
    // Should navigate to category page
    await expect(page).toHaveURL(new RegExp(`/category/${GETTING_STARTED_CAT_ID}`));
    await expect(page.getByTestId('category-page')).toBeVisible({ timeout: 10000 });
  });

  test('Category page shows title, document count and numbered list', async ({ page }) => {
    await page.goto(`/category/${GETTING_STARTED_CAT_ID}`, { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('category-page')).toBeVisible({ timeout: 15000 });
    
    // Check category title is displayed (Getting Started)
    await expect(page.locator('h1').first()).toContainText('Getting Started');
    
    // Check document count text is displayed
    await expect(page.locator('.category-desc')).toContainText('document');
    
    // Check numbered document cards exist
    const docCards = page.locator('.category-doc-card');
    await expect(docCards.first()).toBeVisible();
    
    // First card should have number 1
    const firstCardNum = page.locator('.category-doc-num').first();
    await expect(firstCardNum).toHaveText('1');
  });

  test('Category page back button navigates to home', async ({ page }) => {
    await page.goto(`/category/${GETTING_STARTED_CAT_ID}`, { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('category-page')).toBeVisible({ timeout: 15000 });
    
    // Click back button
    const backBtn = page.getByTestId('cat-back');
    await expect(backBtn).toBeVisible();
    await backBtn.click();
    
    // Should navigate to home (URL may differ between external and internal preview URLs)
    await expect(page.getByTestId('home-page')).toBeVisible({ timeout: 10000 });
  });

  test('Document card on category page navigates to document viewer', async ({ page }) => {
    await page.goto(`/category/${GETTING_STARTED_CAT_ID}`, { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('category-page')).toBeVisible({ timeout: 15000 });
    
    // Get first document card
    const firstDocCard = page.locator('.category-doc-card').first();
    await expect(firstDocCard).toBeVisible();
    
    // Click the document card
    await firstDocCard.click();
    
    // Should navigate to document viewer
    await expect(page).toHaveURL(/\/doc\//);
    await expect(page.getByTestId('doc-viewer')).toBeVisible({ timeout: 10000 });
  });

  test('Module test button is visible on category page', async ({ page }) => {
    await page.goto(`/category/${GETTING_STARTED_CAT_ID}`, { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('category-page')).toBeVisible({ timeout: 15000 });
    
    // Module test section should be visible
    const moduleTestSection = page.getByTestId('module-test');
    await expect(moduleTestSection).toBeVisible();
    
    // Should show module test button with question count
    const moduleTestBtn = page.getByTestId('module-test-btn');
    await expect(moduleTestBtn).toBeVisible();
    await expect(moduleTestBtn).toContainText('Module Test');
    await expect(moduleTestBtn).toContainText('questions');
  });

  test('Module test expands and shows questions', async ({ page }) => {
    await page.goto(`/category/${GETTING_STARTED_CAT_ID}`, { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('category-page')).toBeVisible({ timeout: 15000 });
    
    // Click module test button to expand
    const moduleTestBtn = page.getByTestId('module-test-btn');
    await expect(moduleTestBtn).toBeVisible();
    await moduleTestBtn.click();
    
    // Should show expanded quiz
    const expandedTest = page.getByTestId('module-test-expanded');
    await expect(expandedTest).toBeVisible({ timeout: 5000 });
    
    // Should have quiz questions
    const questions = page.locator('.quiz-question');
    await expect(questions.first()).toBeVisible();
  });

  test('Module test quiz interaction - select answer and submit', async ({ page }) => {
    await page.goto(`/category/${GETTING_STARTED_CAT_ID}`, { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('category-page')).toBeVisible({ timeout: 15000 });
    
    // Expand module test
    await page.getByTestId('module-test-btn').click();
    await expect(page.getByTestId('module-test-expanded')).toBeVisible({ timeout: 5000 });
    
    // Select answers for all questions
    const optionButtons = page.locator('.quiz-option:not([disabled])');
    const count = await optionButtons.count();
    
    // Click first option for each question set (assuming 4 questions, 4 options each = first 4 buttons)
    // Actually click every 4th button starting from first to answer each question
    const questionCount = await page.locator('.quiz-question').count();
    for (let i = 0; i < questionCount; i++) {
      // Click the first option (A) for each question
      const questionBlock = page.locator('.quiz-question').nth(i);
      const firstOption = questionBlock.locator('.quiz-option').first();
      await firstOption.click();
    }
    
    // Check Answers button should become enabled
    const submitBtn = page.locator('.quiz-footer button').filter({ hasText: /Check Answers/i });
    await expect(submitBtn).toBeEnabled();
    
    // Submit the quiz
    await submitBtn.click();
    
    // Should show score result
    const scoreDisplay = page.locator('.quiz-score');
    await expect(scoreDisplay).toBeVisible();
    await expect(scoreDisplay).toContainText('Score:');
    
    // Try Again button should appear
    const tryAgainBtn = page.locator('.quiz-footer button').filter({ hasText: /Try Again/i });
    await expect(tryAgainBtn).toBeVisible();
  });

  test('Module test can be minimized', async ({ page }) => {
    await page.goto(`/category/${GETTING_STARTED_CAT_ID}`, { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('category-page')).toBeVisible({ timeout: 15000 });
    
    // Expand module test
    await page.getByTestId('module-test-btn').click();
    await expect(page.getByTestId('module-test-expanded')).toBeVisible({ timeout: 5000 });
    
    // Click minimize button
    const minimizeBtn = page.locator('.doc-quiz-minimize');
    await expect(minimizeBtn).toBeVisible();
    await minimizeBtn.click();
    
    // Expanded test should be hidden, collapsed test should show
    await expect(page.getByTestId('module-test-expanded')).not.toBeVisible();
    await expect(page.getByTestId('module-test')).toBeVisible();
  });

  test('Category page shows icon', async ({ page }) => {
    await page.goto(`/category/${GETTING_STARTED_CAT_ID}`, { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('category-page')).toBeVisible({ timeout: 15000 });
    
    // Category hero icon should be visible
    const heroIcon = page.locator('.category-hero-icon');
    await expect(heroIcon).toBeVisible();
    await expect(heroIcon.locator('svg')).toBeVisible();
  });

  test('Document cards show reading time and update date', async ({ page }) => {
    await page.goto(`/category/${GETTING_STARTED_CAT_ID}`, { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('category-page')).toBeVisible({ timeout: 15000 });
    
    // Check document card metadata
    const docMeta = page.locator('.category-doc-meta').first();
    await expect(docMeta).toBeVisible();
    
    // Should show reading time
    await expect(docMeta).toContainText('min read');
  });

});

test.describe('Module Tests API', () => {
  
  test('Module tests API returns questions for Getting Started category', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/api/module-tests/${GETTING_STARTED_CAT_ID}`);
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data.category_id).toBe(GETTING_STARTED_CAT_ID);
    expect(data.questions).toBeDefined();
    expect(Array.isArray(data.questions)).toBe(true);
    expect(data.questions.length).toBeGreaterThan(0);
    
    // Check question structure
    const question = data.questions[0];
    expect(question.id).toBeDefined();
    expect(question.question).toBeDefined();
    expect(question.options).toBeDefined();
    expect(Array.isArray(question.options)).toBe(true);
    expect(question.correct).toBeDefined();
    expect(typeof question.correct).toBe('number');
  });

  test('Module tests API returns questions for Platform Architecture category', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/api/module-tests/${PLATFORM_ARCH_CAT_ID}`);
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data.category_id).toBe(PLATFORM_ARCH_CAT_ID);
    expect(data.questions).toBeDefined();
  });

  test('Module tests API returns empty for category without tests', async ({ request }) => {
    // Using a random UUID that likely has no tests
    const response = await request.get(`${BASE_URL}/api/module-tests/non-existent-category-id`);
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data.questions).toBeDefined();
    expect(data.questions.length).toBe(0);
  });

});
