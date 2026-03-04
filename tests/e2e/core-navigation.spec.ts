import { test, expect } from '@playwright/test';
import { navigateToHome, navigateToLearnPaths, navigateToTools, removeEmergentBadge } from '../fixtures/helpers';

test.describe('Core Navigation & Homepage', () => {
  test.beforeEach(async ({ page }) => {
    await removeEmergentBadge(page);
  });

  test('homepage loads with category cards', async ({ page }) => {
    await navigateToHome(page);
    
    // Check hero section
    const hero = page.locator('.home-hero h1');
    await expect(hero).toHaveText('Agent Anatomy');
    
    // Check category cards exist (at least 10, accounting for data changes)
    const cards = page.locator('.home-card');
    const count = await cards.count();
    expect(count).toBeGreaterThanOrEqual(10);
  });

  test('sidebar navigation elements are visible', async ({ page }) => {
    await navigateToHome(page);
    
    // Check sidebar links
    await expect(page.getByTestId('sidebar-home-btn')).toBeVisible();
    await expect(page.getByTestId('sidebar-bookmarks-btn')).toBeVisible();
    await expect(page.getByTestId('sidebar-learn-btn')).toBeVisible();
    await expect(page.getByTestId('sidebar-progress-btn')).toBeVisible();
    await expect(page.getByTestId('sidebar-tools-btn')).toBeVisible();
    await expect(page.getByTestId('sidebar-trash-btn')).toBeVisible();
    await expect(page.getByTestId('sidebar-analytics-btn')).toBeVisible();
    await expect(page.getByTestId('sidebar-settings-btn')).toBeVisible();
  });

  test('clicking sidebar Learning Paths navigates to /learn', async ({ page }) => {
    await navigateToHome(page);
    
    await page.getByTestId('sidebar-learn-btn').click();
    await page.waitForURL('**/learn');
    await expect(page.getByTestId('learning-paths-page')).toBeVisible();
  });

  test('clicking sidebar Tools navigates to /tools', async ({ page }) => {
    await navigateToHome(page);
    
    await page.getByTestId('sidebar-tools-btn').click();
    await page.waitForURL('**/tools');
    await expect(page.getByTestId('tools-page')).toBeVisible();
  });

  test('clicking sidebar Bookmarks navigates to /bookmarks', async ({ page }) => {
    await navigateToHome(page);
    
    await page.getByTestId('sidebar-bookmarks-btn').click();
    await page.waitForURL('**/bookmarks');
    await expect(page.getByTestId('bookmarks-page')).toBeVisible();
  });

  test('sidebar collapse/expand works', async ({ page }) => {
    await navigateToHome(page);
    
    // Initially sidebar should be expanded
    const sidebar = page.getByTestId('sidebar');
    await expect(sidebar).not.toHaveClass(/sidebar-collapsed/);
    
    // Click collapse button
    await page.getByTestId('sidebar-collapse-btn').click();
    await expect(sidebar).toHaveClass(/sidebar-collapsed/);
    
    // Click again to expand
    await page.getByTestId('sidebar-collapse-btn').click();
    await expect(sidebar).not.toHaveClass(/sidebar-collapsed/);
  });

  test('theme toggle switches between dark and light mode', async ({ page }) => {
    await navigateToHome(page);
    
    // App starts in dark mode
    const html = page.locator('html');
    await expect(html).toHaveClass(/dark/);
    
    // Click theme toggle
    await page.getByTestId('theme-toggle-btn').click();
    await expect(html).not.toHaveClass(/dark/);
    
    // Toggle back
    await page.getByTestId('theme-toggle-btn').click();
    await expect(html).toHaveClass(/dark/);
  });

  test('search input is visible and functional', async ({ page }) => {
    await navigateToHome(page);
    
    // Check search input exists
    const searchInput = page.getByTestId('search-input');
    await expect(searchInput).toBeVisible();
    
    // Type in search
    await searchInput.fill('transformer');
    
    // Wait for search results
    await expect(page.getByTestId('search-results')).toBeVisible({ timeout: 5000 });
  });

  test('404 page shows for invalid routes', async ({ page }) => {
    await page.goto('/nonexistent-page-xyz', { waitUntil: 'domcontentloaded' });
    
    const notFoundPage = page.getByTestId('not-found-page');
    await expect(notFoundPage).toBeVisible({ timeout: 10000 });
    await expect(notFoundPage.locator('h2')).toHaveText('Page not found');
    
    // Click Go Home
    await page.getByRole('button', { name: 'Go Home' }).click();
    await page.waitForURL('**/');
    await expect(page.getByTestId('home-page')).toBeVisible();
  });
});
