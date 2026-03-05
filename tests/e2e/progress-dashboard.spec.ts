import { test, expect } from '@playwright/test';
import { navigateToHome, navigateToProgress, removeEmergentBadge, clearProgressLocalStorage, setProgressLocalStorage } from '../fixtures/helpers';

test.describe('Progress Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await removeEmergentBadge(page);
    // Clear localStorage progress data before each test
    await page.goto('/', { waitUntil: 'domcontentloaded' });
    await clearProgressLocalStorage(page);
  });

  test('progress page renders with all main sections', async ({ page }) => {
    await navigateToProgress(page);
    
    // Check main container
    await expect(page.getByTestId('progress-dashboard')).toBeVisible();
    
    // Check hero section
    await expect(page.getByTestId('progress-hero')).toBeVisible();
    await expect(page.getByTestId('progress-hero').locator('h1')).toHaveText('Your Learning Progress');
    
    // Check progress rings section
    await expect(page.getByTestId('progress-rings')).toBeVisible();
    
    // Check overall mastery section
    await expect(page.getByTestId('progress-overall')).toBeVisible();
    
    // Check learning paths section
    await expect(page.getByTestId('progress-paths')).toBeVisible();
    
    // Check recently read section
    await expect(page.getByTestId('progress-recent')).toBeVisible();
    
    // Check achievements section
    await expect(page.getByTestId('progress-achievements')).toBeVisible();
  });

  test('progress rings display all 4 categories', async ({ page }) => {
    await navigateToProgress(page);
    
    const ringsContainer = page.getByTestId('progress-rings');
    
    // Check for the 4 progress ring labels
    await expect(ringsContainer.locator('.progress-ring-label').filter({ hasText: 'Docs Read' })).toBeVisible();
    await expect(ringsContainer.locator('.progress-ring-label').filter({ hasText: 'Quizzes Passed' })).toBeVisible();
    await expect(ringsContainer.locator('.progress-ring-label').filter({ hasText: 'Modules Passed' })).toBeVisible();
    await expect(ringsContainer.locator('.progress-ring-label').filter({ hasText: 'Paths Completed' })).toBeVisible();
  });

  test('overall mastery bar shows 0% when no progress', async ({ page }) => {
    await navigateToProgress(page);
    
    const overallSection = page.getByTestId('progress-overall');
    await expect(overallSection.locator('h2').first()).toHaveText('Overall Mastery');
    
    // With no progress, should show 0%
    await expect(overallSection.locator('.progress-overall-pct')).toHaveText('0%');
    
    // Check breakdown shows 0 for all
    const breakdown = overallSection.locator('.progress-overall-breakdown');
    await expect(breakdown.locator('span').filter({ hasText: /0 docs/ })).toBeVisible();
    await expect(breakdown.locator('span').filter({ hasText: /0 quizzes/ })).toBeVisible();
    await expect(breakdown.locator('span').filter({ hasText: /0 modules/ })).toBeVisible();
    await expect(breakdown.locator('span').filter({ hasText: /0 paths/ })).toBeVisible();
  });

  test('achievements section shows all 6 badge cards', async ({ page }) => {
    await navigateToProgress(page);
    
    // Check all 6 badges exist
    await expect(page.getByTestId('badge-first-doc')).toBeVisible();
    await expect(page.getByTestId('badge-bookworm')).toBeVisible();
    await expect(page.getByTestId('badge-quiz-master')).toBeVisible();
    await expect(page.getByTestId('badge-module-pro')).toBeVisible();
    await expect(page.getByTestId('badge-path-finder')).toBeVisible();
    await expect(page.getByTestId('badge-halfway')).toBeVisible();
  });

  test('badges are not earned with no progress', async ({ page }) => {
    await navigateToProgress(page);
    
    // None should have earned class
    await expect(page.getByTestId('badge-first-doc')).not.toHaveClass(/earned/);
    await expect(page.getByTestId('badge-bookworm')).not.toHaveClass(/earned/);
    await expect(page.getByTestId('badge-quiz-master')).not.toHaveClass(/earned/);
    await expect(page.getByTestId('badge-module-pro')).not.toHaveClass(/earned/);
    await expect(page.getByTestId('badge-path-finder')).not.toHaveClass(/earned/);
    await expect(page.getByTestId('badge-halfway')).not.toHaveClass(/earned/);
  });

  test('learning paths section shows all 4 paths', async ({ page }) => {
    await navigateToProgress(page);
    
    const pathsSection = page.getByTestId('progress-paths');
    
    // Should have 4 learning path rows
    const pathRows = pathsSection.locator('.progress-path-row');
    await expect(pathRows).toHaveCount(4);
    
    // Each should have title, steps count, mini progress bar, and percentage
    const firstPath = pathRows.first();
    await expect(firstPath.locator('.progress-path-title')).toBeVisible();
    await expect(firstPath.locator('.progress-path-meta')).toBeVisible();
    await expect(firstPath.locator('.progress-mini-bar')).toBeVisible();
    await expect(firstPath.locator('.progress-path-pct')).toBeVisible();
  });

  test('recently read section shows empty message initially', async ({ page }) => {
    await navigateToProgress(page);
    
    const recentSection = page.getByTestId('progress-recent');
    await expect(recentSection.locator('.progress-empty')).toHaveText('Start reading documents to see your progress!');
  });

  test('sidebar has My Progress link that navigates to /progress', async ({ page }) => {
    await navigateToHome(page);
    
    // Check sidebar has My Progress button
    const progressBtn = page.getByTestId('sidebar-progress-btn');
    await expect(progressBtn).toBeVisible();
    await expect(progressBtn.locator('span')).toHaveText('My Progress');
    
    // Click and verify navigation
    await progressBtn.click();
    await page.waitForURL('**/progress');
    await expect(page.getByTestId('progress-dashboard')).toBeVisible();
  });

  test('My Progress link is highlighted when on /progress page', async ({ page }) => {
    await navigateToProgress(page);
    
    const progressBtn = page.getByTestId('sidebar-progress-btn');
    await expect(progressBtn).toHaveClass(/active/);
  });
});

test.describe('Progress Dashboard - With Injected Progress Data', () => {
  test.beforeEach(async ({ page }) => {
    await removeEmergentBadge(page);
    await page.goto('/', { waitUntil: 'domcontentloaded' });
    await clearProgressLocalStorage(page);
  });

  test('reading a document adds to aa-docs-read and updates Recently Read', async ({ page }) => {
    // Navigate to a document
    await page.goto('/doc/f53aecbb-3b19-478c-9912-66d82827f402', { waitUntil: 'domcontentloaded' });
    await expect(page.getByTestId('doc-viewer')).toBeVisible({ timeout: 15000 });
    
    // Now go to progress page
    await navigateToProgress(page);
    
    // Recently Read should have an entry
    const recentSection = page.getByTestId('progress-recent');
    await expect(recentSection.locator('.progress-recent-row')).toHaveCount(1, { timeout: 5000 });
    
    // Docs Read ring should show 1
    const ringsContainer = page.getByTestId('progress-rings');
    // The ring wrapper with "Docs Read" label should have "1/" text inside
    await expect(ringsContainer.locator('text').filter({ hasText: /1\// })).toBeVisible();
  });

  test('first-doc badge is earned after reading 1 document', async ({ page }) => {
    // Inject progress data
    await setProgressLocalStorage(page, {
      docsRead: ['f53aecbb-3b19-478c-9912-66d82827f402']
    });
    
    await navigateToProgress(page);
    
    // First Steps badge should be earned
    await expect(page.getByTestId('badge-first-doc')).toHaveClass(/earned/);
    
    // Bookworm should NOT be earned (needs 10)
    await expect(page.getByTestId('badge-bookworm')).not.toHaveClass(/earned/);
  });

  test('progress displays correctly with multiple docs read', async ({ page }) => {
    // Inject 5 docs read
    await setProgressLocalStorage(page, {
      docsRead: [
        'f53aecbb-3b19-478c-9912-66d82827f402',
        'doc-id-2',
        'doc-id-3',
        'doc-id-4',
        'doc-id-5'
      ]
    });
    
    await navigateToProgress(page);
    
    // Check overall breakdown shows 5 docs
    const overallSection = page.getByTestId('progress-overall');
    await expect(overallSection.locator('.progress-overall-breakdown span').filter({ hasText: /5 docs/ })).toBeVisible();
    
    // First Steps badge earned
    await expect(page.getByTestId('badge-first-doc')).toHaveClass(/earned/);
  });

  test('clicking a learning path row navigates to learning paths page', async ({ page }) => {
    await navigateToProgress(page);
    
    const pathsSection = page.getByTestId('progress-paths');
    const firstPathRow = pathsSection.locator('.progress-path-row').first();
    await firstPathRow.click();
    
    await page.waitForURL('**/learn');
    // Should navigate to learn page with the path expanded/selected
    // Check the sidebar Learning Paths is active
    await expect(page.getByTestId('sidebar-learn-btn')).toHaveClass(/active/);
  });

  test('clicking a recent doc navigates to the document', async ({ page }) => {
    // Inject a doc that exists
    await setProgressLocalStorage(page, {
      docsRead: ['f53aecbb-3b19-478c-9912-66d82827f402']
    });
    
    await navigateToProgress(page);
    
    // Click the recent doc
    const recentRow = page.getByTestId('progress-recent-f53aecbb-3b19-478c-9912-66d82827f402');
    await expect(recentRow).toBeVisible();
    await recentRow.click();
    
    await page.waitForURL('**/doc/f53aecbb-3b19-478c-9912-66d82827f402');
    await expect(page.getByTestId('doc-viewer')).toBeVisible();
  });

  test('level changes based on overall progress percentage', async ({ page }) => {
    // With 0 progress, should be Newcomer
    await navigateToProgress(page);
    const heroSection = page.getByTestId('progress-hero');
    // Use getByText to find the Newcomer text specifically
    await expect(heroSection.getByText('Newcomer', { exact: true })).toBeVisible();
  });
});
