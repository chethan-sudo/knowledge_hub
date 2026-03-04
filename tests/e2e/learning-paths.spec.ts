import { test, expect } from '@playwright/test';
import { navigateToLearnPaths, navigateToDocument, removeEmergentBadge } from '../fixtures/helpers';

const BEGINNER_PATH_ID = '7871ac91-d606-4fdf-b2be-5ee8f08ad8e3';

test.describe('Learning Paths Features', () => {
  test.beforeEach(async ({ page }) => {
    await removeEmergentBadge(page);
    // Clear learning progress for clean test state
    await page.addInitScript(() => {
      localStorage.removeItem('aa-learning-progress');
      localStorage.removeItem('aa-from-path');
    });
  });

  test('learning paths page shows 4 path cards', async ({ page }) => {
    await navigateToLearnPaths(page);
    
    // Check hero
    const hero = page.locator('.lp-hero h1');
    await expect(hero).toHaveText('Learning Paths');
    
    // Check 4 learning path cards exist
    const cards = page.locator('.lp-card');
    await expect(cards).toHaveCount(4);
  });

  test('learning path cards show difficulty badges', async ({ page }) => {
    await navigateToLearnPaths(page);
    
    // Check difficulty badges exist
    await expect(page.locator('.lp-badge-beginner').first()).toBeVisible();
    await expect(page.locator('.lp-badge-intermediate').first()).toBeVisible();
    await expect(page.locator('.lp-badge-advanced').first()).toBeVisible();
  });

  test('learning path cards show estimated time and lesson count', async ({ page }) => {
    await navigateToLearnPaths(page);
    
    // Check first card meta info
    const firstCard = page.getByTestId(`lp-card-${BEGINNER_PATH_ID}`);
    await expect(firstCard).toBeVisible();
    await expect(firstCard.locator('.lp-card-meta')).toContainText('min');
    await expect(firstCard.locator('.lp-card-meta')).toContainText('lessons');
  });

  test('clicking a path card opens path detail view', async ({ page }) => {
    await navigateToLearnPaths(page);
    
    // Click beginner path
    await page.getByTestId(`lp-card-${BEGINNER_PATH_ID}`).click();
    
    // Check detail view appears
    const detail = page.getByTestId('learning-path-detail');
    await expect(detail).toBeVisible();
    await expect(detail.locator('h1')).toContainText('Beginner');
  });

  test('path detail shows steps with numbers', async ({ page }) => {
    await navigateToLearnPaths(page);
    await page.getByTestId(`lp-card-${BEGINNER_PATH_ID}`).click();
    
    // Check steps exist (beginner has 5 steps)
    const step0 = page.getByTestId('lp-step-0');
    await expect(step0).toBeVisible();
    
    const step4 = page.getByTestId('lp-step-4');
    await expect(step4).toBeVisible();
  });

  test('path detail shows progress bar', async ({ page }) => {
    await navigateToLearnPaths(page);
    await page.getByTestId(`lp-card-${BEGINNER_PATH_ID}`).click();
    
    // Check progress bar
    const progressBar = page.locator('.lp-progress-bar');
    await expect(progressBar).toBeVisible();
    await expect(progressBar).toContainText('0%');
  });

  test('path detail shows roadmap visualization', async ({ page }) => {
    await navigateToLearnPaths(page);
    await page.getByTestId(`lp-card-${BEGINNER_PATH_ID}`).click();
    
    // Check roadmap
    const roadmap = page.getByTestId('lp-roadmap');
    await expect(roadmap).toBeVisible();
    
    // Check nodes
    const node0 = page.getByTestId('lp-road-0');
    await expect(node0).toBeVisible();
  });

  test('mark complete button updates progress', async ({ page }) => {
    await navigateToLearnPaths(page);
    await page.getByTestId(`lp-card-${BEGINNER_PATH_ID}`).click();
    
    // Find Mark Complete button in first step
    const step0 = page.getByTestId('lp-step-0');
    const markCompleteBtn = step0.getByRole('button', { name: 'Mark Complete' });
    await expect(markCompleteBtn).toBeVisible();
    
    // Click it
    await markCompleteBtn.click();
    
    // Progress should update from 0% to 20% (1/5)
    const progressBar = page.locator('.lp-progress-bar');
    await expect(progressBar).toContainText('20%');
    
    // Step should show completed state
    await expect(step0).toHaveClass(/completed/);
  });

  test('Start Reading button navigates to document', async ({ page }) => {
    await navigateToLearnPaths(page);
    await page.getByTestId(`lp-card-${BEGINNER_PATH_ID}`).click();
    
    // Click Start Reading on first step
    const step0 = page.getByTestId('lp-step-0');
    const startReadingBtn = step0.getByRole('button', { name: 'Start Reading' });
    await startReadingBtn.click();
    
    // Should navigate to document
    await page.waitForURL('**/doc/**');
    await expect(page.getByTestId('doc-viewer')).toBeVisible();
  });

  test('back to path button shows when coming from learning path', async ({ page }) => {
    await navigateToLearnPaths(page);
    await page.getByTestId(`lp-card-${BEGINNER_PATH_ID}`).click();
    
    // Start Reading
    const step0 = page.getByTestId('lp-step-0');
    await step0.getByRole('button', { name: 'Start Reading' }).click();
    
    // Wait for doc page
    await page.waitForURL('**/doc/**');
    
    // Check back to path button
    const backBtn = page.getByTestId('back-to-path');
    await expect(backBtn).toBeVisible();
  });

  test('All Paths button returns to paths list', async ({ page }) => {
    await navigateToLearnPaths(page);
    await page.getByTestId(`lp-card-${BEGINNER_PATH_ID}`).click();
    
    // Click All Paths back button
    await page.getByTestId('lp-back').click();
    
    // Should be back at paths list
    await expect(page.getByTestId('learning-paths-page')).toBeVisible();
  });

  test('path test section shows when all lessons complete', async ({ page }) => {
    // Set all lessons as complete via localStorage
    await page.addInitScript(() => {
      const progress = {
        '7871ac91-d606-4fdf-b2be-5ee8f08ad8e3:f53aecbb-3b19-478c-9912-66d82827f402': true,
        '7871ac91-d606-4fdf-b2be-5ee8f08ad8e3:6c753d08-d469-4e3f-8f3b-017d11c365c0': true,
        '7871ac91-d606-4fdf-b2be-5ee8f08ad8e3:b1abbfef-70c7-4c36-a5ed-11bc7b237d9c': true,
        '7871ac91-d606-4fdf-b2be-5ee8f08ad8e3:a6248371-7ced-4bb6-8343-fb7c2a31a2ae': true,
        '7871ac91-d606-4fdf-b2be-5ee8f08ad8e3:faa447ea-8011-4636-b9f2-92bb8baa9d11': true,
      };
      localStorage.setItem('aa-learning-progress', JSON.stringify(progress));
    });
    
    await navigateToLearnPaths(page);
    await page.getByTestId(`lp-card-${BEGINNER_PATH_ID}`).click();
    
    // Progress should be 100%
    await expect(page.locator('.lp-progress-bar')).toContainText('100%');
    
    // Complete banner should show
    const completeBanner = page.getByTestId('lp-complete');
    await expect(completeBanner).toBeVisible();
    
    // Path test button should be enabled
    const pathTestBtn = page.getByTestId('path-test-btn');
    await expect(pathTestBtn).toBeVisible();
    await expect(pathTestBtn).toBeEnabled();
    
    // Start Again button should be visible at 100%
    const resetBtn = page.getByTestId('lp-reset');
    await expect(resetBtn).toBeVisible();
  });

  test('Start Again button resets progress', async ({ page }) => {
    // Set all lessons as complete
    await page.addInitScript(() => {
      const progress = {
        '7871ac91-d606-4fdf-b2be-5ee8f08ad8e3:f53aecbb-3b19-478c-9912-66d82827f402': true,
        '7871ac91-d606-4fdf-b2be-5ee8f08ad8e3:6c753d08-d469-4e3f-8f3b-017d11c365c0': true,
        '7871ac91-d606-4fdf-b2be-5ee8f08ad8e3:b1abbfef-70c7-4c36-a5ed-11bc7b237d9c': true,
        '7871ac91-d606-4fdf-b2be-5ee8f08ad8e3:a6248371-7ced-4bb6-8343-fb7c2a31a2ae': true,
        '7871ac91-d606-4fdf-b2be-5ee8f08ad8e3:faa447ea-8011-4636-b9f2-92bb8baa9d11': true,
      };
      localStorage.setItem('aa-learning-progress', JSON.stringify(progress));
    });
    
    await navigateToLearnPaths(page);
    await page.getByTestId(`lp-card-${BEGINNER_PATH_ID}`).click();
    
    // Accept dialog for reset
    page.on('dialog', dialog => dialog.accept());
    
    // Click Start Again
    await page.getByTestId('lp-reset').click();
    
    // Progress should reset to 0%
    await expect(page.locator('.lp-progress-bar')).toContainText('0%');
  });
});
