import { Page, expect } from '@playwright/test';

export async function waitForAppReady(page: Page) {
  await page.waitForLoadState('domcontentloaded');
}

export async function dismissToasts(page: Page) {
  await page.addLocatorHandler(
    page.locator('[data-sonner-toast], .Toastify__toast, [role="status"].toast, .MuiSnackbar-root'),
    async () => {
      const close = page.locator('[data-sonner-toast] [data-close], [data-sonner-toast] button[aria-label="Close"], .Toastify__close-button, .MuiSnackbar-root button');
      await close.first().click({ timeout: 2000 }).catch(() => {});
    },
    { times: 10, noWaitAfter: true }
  );
}

export async function checkForErrors(page: Page): Promise<string[]> {
  return page.evaluate(() => {
    const errorElements = Array.from(
      document.querySelectorAll('.error, [class*="error"], [id*="error"]')
    );
    return errorElements.map(el => el.textContent || '').filter(Boolean);
  });
}

export async function navigateToHome(page: Page) {
  await page.goto('/', { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('[data-testid="home-page"]', { timeout: 15000 });
}

export async function navigateToLearnPaths(page: Page) {
  await page.goto('/learn', { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('[data-testid="learning-paths-page"]', { timeout: 15000 });
}

export async function navigateToTools(page: Page) {
  await page.goto('/tools', { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('[data-testid="tools-page"]', { timeout: 15000 });
}

export async function navigateToDocument(page: Page, docId: string) {
  await page.goto(`/doc/${docId}`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('[data-testid="doc-viewer"]', { timeout: 15000 });
}

export async function removeEmergentBadge(page: Page) {
  await page.evaluate(() => {
    const badge = document.querySelector('[class*="emergent"], [id*="emergent-badge"]');
    if (badge) badge.remove();
  });
}

export async function navigateToProgress(page: Page) {
  await page.goto('/progress', { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('[data-testid="progress-dashboard"]', { timeout: 15000 });
}

export async function clearProgressLocalStorage(page: Page) {
  await page.evaluate(() => {
    localStorage.removeItem('aa-docs-read');
    localStorage.removeItem('aa-quizzes-passed');
    localStorage.removeItem('aa-modules-passed');
    localStorage.removeItem('aa-learning-progress');
  });
}

export async function setProgressLocalStorage(page: Page, data: {
  docsRead?: string[],
  quizzesPassed?: string[],
  modulesPassed?: string[],
  learningProgress?: Record<string, boolean>
}) {
  await page.evaluate((data) => {
    if (data.docsRead) localStorage.setItem('aa-docs-read', JSON.stringify(data.docsRead));
    if (data.quizzesPassed) localStorage.setItem('aa-quizzes-passed', JSON.stringify(data.quizzesPassed));
    if (data.modulesPassed) localStorage.setItem('aa-modules-passed', JSON.stringify(data.modulesPassed));
    if (data.learningProgress) localStorage.setItem('aa-learning-progress', JSON.stringify(data.learningProgress));
  }, data);
}
