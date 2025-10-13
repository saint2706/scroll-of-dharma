import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright configuration for accessibility testing
 * See https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './tests/e2e',
  
  // Run tests in files in parallel
  fullyParallel: true,
  
  // Fail the build on CI if you accidentally left test.only in the source code
  forbidOnly: !!process.env.CI,
  
  // Retry on CI only
  retries: process.env.CI ? 2 : 0,
  
  // Opt out of parallel tests on CI
  workers: process.env.CI ? 1 : undefined,
  
  // Reporter to use
  reporter: [
    ['html'],
    ['list'],
    ['json', { outputFile: 'test-results/a11y-results.json' }]
  ],
  
  use: {
    // Base URL for tests
    baseURL: 'http://localhost:4321/scroll-of-dharma',
    
    // Collect trace when retrying the failed test
    trace: 'on-first-retry',
    
    // Screenshot on failure
    screenshot: 'only-on-failure',
  },

  // Configure projects for major browsers
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  // Run local dev server before starting tests
  webServer: {
    command: 'npm run preview',
    url: 'http://localhost:4321/scroll-of-dharma',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
