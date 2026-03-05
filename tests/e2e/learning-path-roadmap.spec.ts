import { test, expect } from '@playwright/test';

const BASE_URL = process.env.REACT_APP_BACKEND_URL || 'https://ai-agent-hub-96.preview.emergentagent.com';

// Learning path ID for testing
const BEGINNER_PATH_ID = '7871ac91-d606-4fdf-b2be-5ee8f08ad8e3';

test.describe('Learning Path Roadmap Enhancements', () => {
  
  test.beforeEach(async ({ page }) => {
    // Clear localStorage for clean test state
    await page.addInitScript(() => {
      localStorage.removeItem('aa-learning-progress');
      localStorage.removeItem('aa-from-path');
      // Remove Emergent badge if present
      const observer = new MutationObserver(() => {
        const badge = document.querySelector('[class*="emergent"], [id*="emergent-badge"]');
        if (badge) badge.remove();
      });
      observer.observe(document.body, { childList: true, subtree: true });
    });
  });

  test('Learning paths page shows path cards', async ({ page }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('learning-paths-page')).toBeVisible({ timeout: 15000 });
    
    // Should have at least one learning path card
    const pathCards = page.locator('.lp-card');
    await expect(pathCards.first()).toBeVisible();
    
    // First path card should be the Beginner path
    const beginnerCard = page.locator(`[data-testid="lp-card-${BEGINNER_PATH_ID}"]`);
    await expect(beginnerCard).toBeVisible();
    await expect(beginnerCard).toContainText('Beginner');
  });

  test('Clicking path card opens detail view with roadmap', async ({ page }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('learning-paths-page')).toBeVisible({ timeout: 15000 });
    
    // Click first path card
    await page.locator('.lp-card').first().click();
    
    // Should show learning path detail
    await expect(page.getByTestId('learning-path-detail')).toBeVisible({ timeout: 10000 });
    
    // Roadmap should be visible
    await expect(page.getByTestId('lp-roadmap')).toBeVisible();
  });

  test('Roadmap shows numbered nodes for each step', async ({ page }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('learning-paths-page')).toBeVisible({ timeout: 15000 });
    
    // Click first path card
    await page.locator('.lp-card').first().click();
    await expect(page.getByTestId('learning-path-detail')).toBeVisible({ timeout: 10000 });
    
    // Check roadmap nodes exist
    const roadNodes = page.locator('[data-testid^="lp-road-"]');
    await expect(roadNodes.first()).toBeVisible();
    
    // First node should have number 1
    const firstNode = page.getByTestId('lp-road-0');
    await expect(firstNode).toBeVisible();
    await expect(firstNode.locator('.lp-road-dot')).toContainText('1');
  });

  test('Progress line exists in roadmap', async ({ page }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('learning-paths-page')).toBeVisible({ timeout: 15000 });
    
    // Click first path card
    await page.locator('.lp-card').first().click();
    await expect(page.getByTestId('learning-path-detail')).toBeVisible({ timeout: 10000 });
    
    // Progress line element should exist
    const progressLine = page.locator('.lp-road-progress-line');
    await expect(progressLine).toBeAttached();
  });

  test('Marking step complete updates roadmap', async ({ page }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('learning-paths-page')).toBeVisible({ timeout: 15000 });
    
    // Click first path card
    await page.locator('.lp-card').first().click();
    await expect(page.getByTestId('learning-path-detail')).toBeVisible({ timeout: 10000 });
    
    // First road node should not have completed class initially
    const firstNode = page.getByTestId('lp-road-0');
    await expect(firstNode).toBeVisible();
    
    // Click Mark Complete button on first step
    const firstStep = page.getByTestId('lp-step-0');
    await expect(firstStep).toBeVisible();
    const markCompleteBtn = firstStep.locator('button').filter({ hasText: 'Mark Complete' });
    await markCompleteBtn.click();
    
    // First road node should now have completed class
    await expect(firstNode).toHaveClass(/completed/);
    
    // First node should show check icon instead of number
    await expect(firstNode.locator('.lp-road-dot svg')).toBeVisible();
  });

  test('Next up step has pulse animation class', async ({ page }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('learning-paths-page')).toBeVisible({ timeout: 15000 });
    
    // Click first path card
    await page.locator('.lp-card').first().click();
    await expect(page.getByTestId('learning-path-detail')).toBeVisible({ timeout: 10000 });
    
    // First node should have next-up class when no progress
    const firstNode = page.getByTestId('lp-road-0');
    await expect(firstNode).toHaveClass(/next-up/);
    
    // Mark first step complete
    const firstStep = page.getByTestId('lp-step-0');
    const markCompleteBtn = firstStep.locator('button').filter({ hasText: 'Mark Complete' });
    await markCompleteBtn.click();
    
    // After marking complete, first should be completed, second should be next-up
    await expect(firstNode).toHaveClass(/completed/);
    await expect(firstNode).not.toHaveClass(/next-up/);
    
    const secondNode = page.getByTestId('lp-road-1');
    await expect(secondNode).toHaveClass(/next-up/);
  });

  test('Step cards show Start Reading and Mark Complete buttons', async ({ page }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('learning-paths-page')).toBeVisible({ timeout: 15000 });
    
    // Click first path card
    await page.locator('.lp-card').first().click();
    await expect(page.getByTestId('learning-path-detail')).toBeVisible({ timeout: 10000 });
    
    // First step should have both buttons
    const firstStep = page.getByTestId('lp-step-0');
    await expect(firstStep).toBeVisible();
    
    await expect(firstStep.locator('button').filter({ hasText: 'Start Reading' })).toBeVisible();
    await expect(firstStep.locator('button').filter({ hasText: 'Mark Complete' })).toBeVisible();
  });

  test('Completed step shows Mark Incomplete button', async ({ page }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('learning-paths-page')).toBeVisible({ timeout: 15000 });
    
    // Click first path card
    await page.locator('.lp-card').first().click();
    await expect(page.getByTestId('learning-path-detail')).toBeVisible({ timeout: 10000 });
    
    // Mark first step complete
    const firstStep = page.getByTestId('lp-step-0');
    await firstStep.locator('button').filter({ hasText: 'Mark Complete' }).click();
    
    // Should now show Mark Incomplete button
    await expect(firstStep.locator('button').filter({ hasText: 'Mark Incomplete' })).toBeVisible();
    
    // Mark Complete button should be hidden
    await expect(firstStep.locator('button').filter({ hasText: 'Mark Complete' })).not.toBeVisible();
  });

  test('Progress bar updates with completed steps', async ({ page }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('learning-paths-page')).toBeVisible({ timeout: 15000 });
    
    // Click first path card
    await page.locator('.lp-card').first().click();
    await expect(page.getByTestId('learning-path-detail')).toBeVisible({ timeout: 10000 });
    
    // Progress bar should show 0% initially
    const progressBar = page.locator('.lp-progress-bar');
    await expect(progressBar).toBeVisible();
    await expect(progressBar).toContainText('0%');
    
    // Mark first step complete
    const firstStep = page.getByTestId('lp-step-0');
    await firstStep.locator('button').filter({ hasText: 'Mark Complete' }).click();
    
    // Progress should update (should be 20% for 1/5 steps on Beginner path)
    await expect(progressBar).toContainText('20%');
  });

  test('Back button returns to all paths', async ({ page }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('learning-paths-page')).toBeVisible({ timeout: 15000 });
    
    // Click first path card
    await page.locator('.lp-card').first().click();
    await expect(page.getByTestId('learning-path-detail')).toBeVisible({ timeout: 10000 });
    
    // Click back button
    await page.getByTestId('lp-back').click();
    
    // Should return to learning paths list
    await expect(page.getByTestId('learning-paths-page')).toBeVisible({ timeout: 10000 });
  });

  test('Start Again button appears at 100% progress', async ({ page }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('learning-paths-page')).toBeVisible({ timeout: 15000 });
    
    // Click first path card
    await page.locator('.lp-card').first().click();
    await expect(page.getByTestId('learning-path-detail')).toBeVisible({ timeout: 10000 });
    
    // Mark all steps complete
    const steps = page.locator('[data-testid^="lp-step-"]');
    const stepCount = await steps.count();
    
    for (let i = 0; i < stepCount; i++) {
      const step = page.getByTestId(`lp-step-${i}`);
      const markCompleteBtn = step.locator('button').filter({ hasText: 'Mark Complete' });
      if (await markCompleteBtn.isVisible()) {
        await markCompleteBtn.click();
      }
    }
    
    // Progress should be 100%
    await expect(page.locator('.lp-progress-bar')).toContainText('100%');
    
    // Start Again button should appear
    await expect(page.getByTestId('lp-reset')).toBeVisible();
    
    // Complete banner should show
    await expect(page.getByTestId('lp-complete')).toBeVisible();
  });

  test('Start Reading navigates to document viewer', async ({ page }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('learning-paths-page')).toBeVisible({ timeout: 15000 });
    
    // Click first path card
    await page.locator('.lp-card').first().click();
    await expect(page.getByTestId('learning-path-detail')).toBeVisible({ timeout: 10000 });
    
    // Click Start Reading on first step
    const firstStep = page.getByTestId('lp-step-0');
    await firstStep.locator('button').filter({ hasText: 'Start Reading' }).click();
    
    // Should navigate to document viewer
    await expect(page).toHaveURL(/\/doc\//);
    await expect(page.getByTestId('doc-viewer')).toBeVisible({ timeout: 10000 });
  });

});

test.describe('Learning Paths API', () => {
  
  test('Learning paths API returns list of paths', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/api/learning-paths`);
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(Array.isArray(data)).toBe(true);
    expect(data.length).toBeGreaterThan(0);
    
    // Check path structure
    const path = data[0];
    expect(path.id).toBeDefined();
    expect(path.title).toBeDefined();
    expect(path.description).toBeDefined();
    expect(path.difficulty).toBeDefined();
    expect(path.estimated_time).toBeDefined();
    expect(path.steps).toBeDefined();
    expect(Array.isArray(path.steps)).toBe(true);
  });

  test('Learning path detail API returns steps with document IDs', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/api/learning-paths/${BEGINNER_PATH_ID}`);
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data.id).toBe(BEGINNER_PATH_ID);
    expect(data.steps).toBeDefined();
    expect(Array.isArray(data.steps)).toBe(true);
    expect(data.steps.length).toBeGreaterThan(0);
    
    // Check step structure
    const step = data.steps[0];
    expect(step.document_id).toBeDefined();
    expect(step.title).toBeDefined();
    expect(step.description).toBeDefined();
  });

  test('Path test API returns questions', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/api/path-tests/${BEGINNER_PATH_ID}`);
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data.path_id).toBeDefined();
    expect(data.questions).toBeDefined();
    expect(Array.isArray(data.questions)).toBe(true);
  });

});
