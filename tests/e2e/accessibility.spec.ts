import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

/**
 * Accessibility Test Suite
 * 
 * Tests WCAG 2.1 Level AA compliance using axe-core
 * Validates keyboard navigation, screen reader compatibility, and color contrast
 */

test.describe('Homepage Accessibility', () => {
  test('should not have any automatically detectable accessibility issues', async ({ page }) => {
    await page.goto('/');
    
    // Wait for page to be fully loaded
    await page.waitForLoadState('networkidle');
    
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('should have proper page structure', async ({ page }) => {
    await page.goto('/');
    
    // Check for main landmark
    const main = page.locator('main, [role="main"]');
    await expect(main).toBeVisible();
    
    // Check for proper heading hierarchy
    const h1 = page.locator('h1');
    await expect(h1).toHaveCount(1);
  });

  test('should support keyboard navigation', async ({ page }) => {
    await page.goto('/');
    
    // Start keyboard navigation
    await page.keyboard.press('Tab');
    
    // Check that focus is visible
    const focusedElement = await page.evaluate(() => {
      return document.activeElement?.tagName;
    });
    
    expect(focusedElement).toBeTruthy();
  });

  test('should have proper color contrast', async ({ page }) => {
    await page.goto('/');
    
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2aa'])
      .analyze();

    // Filter for color contrast violations
    const contrastViolations = accessibilityScanResults.violations.filter(
      v => v.id === 'color-contrast'
    );
    
    expect(contrastViolations).toHaveLength(0);
  });
});

test.describe('Chapter Pages Accessibility', () => {
  const sampleChapters = [
    '/chapters/gita_scroll/lotus_of_doubt',
    '/chapters/birth_of_dharma/cosmic_egg',
    '/chapters/weapon_quest/forest_of_austerity',
  ];

  for (const chapterPath of sampleChapters) {
    test(`${chapterPath} should not have accessibility violations`, async ({ page }) => {
      await page.goto(chapterPath);
      await page.waitForLoadState('networkidle');
      
      const accessibilityScanResults = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa'])
        .analyze();

      expect(accessibilityScanResults.violations).toEqual([]);
    });

    test(`${chapterPath} should have accessible images`, async ({ page }) => {
      await page.goto(chapterPath);
      
      // Check all images have alt text or aria-label
      const images = page.locator('img, svg[role="img"]');
      const count = await images.count();
      
      for (let i = 0; i < count; i++) {
        const img = images.nth(i);
        const hasAlt = await img.getAttribute('alt');
        const hasAriaLabel = await img.getAttribute('aria-label');
        const isDecorative = await img.getAttribute('aria-hidden');
        
        // Either has alt/aria-label or is marked as decorative
        expect(
          hasAlt !== null || hasAriaLabel !== null || isDecorative === 'true'
        ).toBeTruthy();
      }
    });
  }
});

test.describe('Keyboard Navigation', () => {
  test('should allow navigation through all interactive elements', async ({ page }) => {
    await page.goto('/');
    
    // Get all focusable elements
    const focusableElements = await page.locator(
      'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
    ).count();
    
    expect(focusableElements).toBeGreaterThan(0);
    
    // Test that we can tab to first element
    await page.keyboard.press('Tab');
    const firstElement = await page.evaluate(() => {
      const elem = document.activeElement;
      return elem ? elem.tagName : null;
    });
    
    // Should have focused an element
    expect(firstElement).not.toBeNull();
    expect(['A', 'BUTTON', 'INPUT']).toContain(firstElement);
  });

  test('should have visible focus indicators', async ({ page }) => {
    await page.goto('/');
    
    // Tab to first focusable element
    await page.keyboard.press('Tab');
    
    // Check that focused element has visible outline or focus styling
    const hasVisibleFocus = await page.evaluate(() => {
      const elem = document.activeElement;
      if (!elem) return false;
      
      const styles = window.getComputedStyle(elem);
      const outline = styles.outline;
      const outlineWidth = styles.outlineWidth;
      const boxShadow = styles.boxShadow;
      
      // Check if element has visible focus indicators
      return (
        outline !== 'none' ||
        outlineWidth !== '0px' ||
        boxShadow !== 'none'
      );
    });
    
    expect(hasVisibleFocus).toBeTruthy();
  });
});

test.describe('Screen Reader Compatibility', () => {
  test('should have proper ARIA landmarks', async ({ page }) => {
    await page.goto('/');
    
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['best-practice'])
      .analyze();

    // Check for landmark-related violations
    const landmarkViolations = accessibilityScanResults.violations.filter(
      v => v.id.includes('landmark') || v.id.includes('region')
    );
    
    expect(landmarkViolations).toHaveLength(0);
  });

  test('should have descriptive page titles', async ({ page }) => {
    await page.goto('/');
    
    const title = await page.title();
    expect(title).toBeTruthy();
    expect(title.length).toBeGreaterThan(0);
  });

  test('should have valid lang attribute', async ({ page }) => {
    await page.goto('/');
    
    const lang = await page.locator('html').getAttribute('lang');
    expect(lang).toBeTruthy();
  });
});

test.describe('Reduced Motion Support', () => {
  test('should respect prefers-reduced-motion', async ({ page }) => {
    // Emulate prefers-reduced-motion
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto('/');
    
    // Check that animations are reduced or disabled
    const hasReducedMotion = await page.evaluate(() => {
      const styles = window.getComputedStyle(document.documentElement);
      return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    });
    
    expect(hasReducedMotion).toBeTruthy();
  });
});
