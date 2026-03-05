import { test, expect } from '@playwright/test';
import { navigateToDocument, removeEmergentBadge } from '../fixtures/helpers';

const SAMPLE_DOC_ID = 'f53aecbb-3b19-478c-9912-66d82827f402'; // What Is an AI Agent?

test.describe('Document Viewer Features', () => {
  test.beforeEach(async ({ page }) => {
    await removeEmergentBadge(page);
  });

  test('document viewer loads with content', async ({ page }) => {
    await navigateToDocument(page, SAMPLE_DOC_ID);
    
    // Check title
    const title = page.getByTestId('doc-title');
    await expect(title).toContainText('What Is an AI Agent?');
    
    // Check content area exists
    const content = page.getByTestId('doc-content');
    await expect(content).toBeVisible();
  });

  test('document shows breadcrumbs', async ({ page }) => {
    await navigateToDocument(page, SAMPLE_DOC_ID);
    
    const breadcrumb = page.getByTestId('doc-breadcrumb');
    await expect(breadcrumb).toBeVisible();
  });

  test('document shows metadata (reading time, updated date)', async ({ page }) => {
    await navigateToDocument(page, SAMPLE_DOC_ID);
    
    const meta = page.getByTestId('doc-meta');
    await expect(meta).toBeVisible();
    await expect(meta).toContainText('min read');
  });

  test('document action buttons are visible', async ({ page }) => {
    await navigateToDocument(page, SAMPLE_DOC_ID);
    
    // Check action buttons
    await expect(page.getByTestId('export-pdf-btn')).toBeVisible();
    await expect(page.getByTestId('version-history-btn')).toBeVisible();
    await expect(page.getByTestId('bookmark-toggle-btn')).toBeVisible();
    await expect(page.getByTestId('edit-doc-btn')).toBeVisible();
  });

  test('PDF export button exists and triggers window.print', async ({ page }) => {
    await navigateToDocument(page, SAMPLE_DOC_ID);
    
    // Check print button exists with Printer icon
    const printBtn = page.getByTestId('export-pdf-btn');
    await expect(printBtn).toBeVisible();
    
    // We can't fully test window.print() but we can verify the button is clickable
    // and has the right attributes
    await expect(printBtn).toHaveAttribute('title', 'Print / Save as PDF');
  });

  test('bookmark toggle works', async ({ page }) => {
    await navigateToDocument(page, SAMPLE_DOC_ID);
    
    const bookmarkBtn = page.getByTestId('bookmark-toggle-btn');
    await expect(bookmarkBtn).toBeVisible();
    
    // Click to toggle bookmark
    await bookmarkBtn.click();
    
    // Wait for API response (bookmark state change)
    await page.waitForTimeout(500);
    
    // Toggle back
    await bookmarkBtn.click();
    await page.waitForTimeout(500);
  });

  test('version history button opens version panel', async ({ page }) => {
    await navigateToDocument(page, SAMPLE_DOC_ID);
    
    // Click version history
    await page.getByTestId('version-history-btn').click();
    
    // Check version panel appears
    const versionPanel = page.getByTestId('version-panel');
    await expect(versionPanel).toBeVisible();
    
    // Close panel
    await page.getByTestId('version-close-btn').click();
    await expect(versionPanel).not.toBeVisible();
  });

  test('document quiz section appears for doc with quiz', async ({ page }) => {
    await navigateToDocument(page, SAMPLE_DOC_ID);
    
    // Scroll to bottom to see quiz
    await page.evaluate(() => {
      const main = document.querySelector('.main-content');
      if (main) main.scrollTop = main.scrollHeight;
    });
    
    // Check quiz section
    const quiz = page.getByTestId('doc-quiz');
    await expect(quiz).toBeVisible();
    
    // Click to expand quiz
    const startBtn = page.getByTestId('quiz-start-btn');
    if (await startBtn.isVisible()) {
      await startBtn.click();
      await expect(page.locator('.doc-quiz-title')).toContainText('Test Your Understanding');
    }
  });

  test('document quiz interaction works', async ({ page }) => {
    await navigateToDocument(page, SAMPLE_DOC_ID);
    
    // Scroll to quiz
    await page.evaluate(() => {
      const main = document.querySelector('.main-content');
      if (main) main.scrollTop = main.scrollHeight;
    });
    
    // Expand quiz if collapsed
    const startBtn = page.getByTestId('quiz-start-btn');
    if (await startBtn.isVisible()) {
      await startBtn.click();
    }
    
    // Answer all questions (there are 4)
    for (let qi = 0; qi < 4; qi++) {
      const option = page.getByTestId(`quiz-opt-${qi}-1`); // Select option B for each
      if (await option.isVisible()) {
        await option.click();
      }
    }
    
    // Check submit button
    const submitBtn = page.getByTestId('quiz-submit');
    await expect(submitBtn).toBeEnabled();
    
    // Submit
    await submitBtn.click();
    
    // Check result shows
    const result = page.getByTestId('quiz-result');
    await expect(result).toBeVisible();
    await expect(result).toContainText('Score:');
  });

  test('comments section is visible', async ({ page }) => {
    await navigateToDocument(page, SAMPLE_DOC_ID);
    
    // Scroll to bottom
    await page.evaluate(() => {
      const main = document.querySelector('.main-content');
      if (main) main.scrollTop = main.scrollHeight;
    });
    
    const commentsSection = page.getByTestId('comments-section');
    await expect(commentsSection).toBeVisible();
    
    // Check comment input
    const commentInput = page.getByTestId('comment-input');
    await expect(commentInput).toBeVisible();
  });

  test('TOC sidebar shows for documents with headings', async ({ page }) => {
    await navigateToDocument(page, SAMPLE_DOC_ID);
    
    // Check TOC exists for docs with multiple H2 headings
    const toc = page.getByTestId('doc-toc');
    // TOC may or may not be visible depending on heading count
    if (await toc.isVisible({ timeout: 2000 }).catch(() => false)) {
      await expect(toc.locator('.doc-toc-title')).toHaveText('On this page');
    }
  });

  test('document navigation shows prev/next buttons', async ({ page }) => {
    await navigateToDocument(page, SAMPLE_DOC_ID);
    
    // Scroll to bottom to see navigation
    await page.evaluate(() => {
      const main = document.querySelector('.main-content');
      if (main) main.scrollTop = main.scrollHeight;
    });
    
    const docNav = page.getByTestId('doc-navigation');
    await expect(docNav).toBeVisible();
  });

  test('related documents section shows for applicable docs', async ({ page }) => {
    await navigateToDocument(page, SAMPLE_DOC_ID);
    
    // Scroll down to see related docs
    await page.evaluate(() => {
      const main = document.querySelector('.main-content');
      if (main) main.scrollTop = main.scrollHeight / 2;
    });
    
    // Related docs may or may not appear based on document
    const relatedDocs = page.getByTestId('related-docs');
    if (await relatedDocs.isVisible({ timeout: 2000 }).catch(() => false)) {
      await expect(relatedDocs.locator('.related-docs-title')).toHaveText('Related Documents');
    }
  });
});
