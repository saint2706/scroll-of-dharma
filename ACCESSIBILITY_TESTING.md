# Accessibility Testing Guide

This guide provides comprehensive instructions for testing accessibility in the Scroll of Dharma project. We maintain **WCAG 2.1 Level AA compliance** through automated testing, continuous monitoring, and manual validation.

## Table of Contents

- [Overview](#overview)
- [Automated Testing Tools](#automated-testing-tools)
- [Running Tests Locally](#running-tests-locally)
- [CI/CD Integration](#cicd-integration)
- [Manual Testing](#manual-testing)
- [Test Coverage Goals](#test-coverage-goals)
- [Contributing Guidelines](#contributing-guidelines)
- [Resources](#resources)

## Overview

Our accessibility testing strategy includes:

1. **Automated accessibility tests** (axe-core, Pa11y, Lighthouse)
2. **Unit and integration tests** with 80%+ code coverage
3. **E2E tests** with Playwright for user flows
4. **Manual testing** with screen readers and assistive technologies
5. **Continuous monitoring** in CI/CD pipeline

## Automated Testing Tools

### 1. Playwright + axe-core

**Purpose:** End-to-end accessibility testing with WCAG 2.1 AA validation

**Tests include:**
- Automatic detection of accessibility violations
- Keyboard navigation validation
- Focus indicator visibility
- Color contrast verification
- ARIA landmark structure
- Screen reader compatibility
- Reduced motion support

**Test file:** `tests/e2e/accessibility.spec.ts`

### 2. Pa11y

**Purpose:** Comprehensive accessibility auditing across all pages

**Features:**
- Tests against WCAG 2.1 AA standard
- Multiple runners (axe, HTML CodeSniffer)
- Detailed violation reports with code snippets
- Exit with error on accessibility violations

**Test script:** `scripts/run-pa11y.js`

### 3. Vitest

**Purpose:** Unit and integration testing with coverage reporting

**Features:**
- Fast test execution with watch mode
- Built-in coverage reporting with v8
- TypeScript support
- 80%+ coverage threshold enforcement

**Test files:** `tests/unit/`, `tests/integration/`

### 4. Lighthouse CI

**Purpose:** Performance and accessibility auditing in CI/CD

**Metrics:**
- Performance score ≥ 90%
- Accessibility score ≥ 95%
- Best practices score ≥ 90%
- SEO score ≥ 90%

## Running Tests Locally

### Prerequisites

```bash
# Install dependencies
npm install

# Build the site
npm run build
```

### Run All Tests

```bash
# Unit tests
npm test

# Unit tests with coverage
npm run test:coverage

# Watch mode (for TDD)
npm run test:watch

# Playwright accessibility tests
npm run test:a11y

# Pa11y audit
npm run test:pa11y
```

### Run Specific Test Suites

```bash
# Run only unit tests
npm test tests/unit

# Run only integration tests
npm test tests/integration

# Run specific test file
npm test tests/unit/types.test.ts

# Run Playwright tests in UI mode
npx playwright test --ui

# Run Playwright tests for specific browser
npx playwright test --project=chromium
```

### View Test Results

```bash
# Open Playwright HTML report
npx playwright show-report

# Open coverage report
open coverage/index.html

# View Pa11y results
cat test-results/pa11y-results.json
```

## CI/CD Integration

### GitHub Actions Workflows

We have two main workflows:

#### 1. Accessibility Check Workflow (`.github/workflows/accessibility-check.yml`)

Runs on every push and pull request:

- ✅ **Unit & Integration Tests** - Validates code with 80%+ coverage
- ✅ **Playwright Accessibility Tests** - E2E tests with axe-core
- ✅ **Pa11y Audit** - Comprehensive WCAG 2.1 AA validation
- ✅ **Lighthouse CI** - Performance and accessibility scores

**Artifacts generated:**
- Test coverage reports (HTML, LCOV, JSON)
- Playwright test results and screenshots
- Pa11y violation reports
- Lighthouse performance reports

#### 2. Deploy Workflow (`.github/workflows/deploy.yml`)

Runs on push to main:

- Builds the site with TypeScript checking
- Runs all tests before deployment
- Deploys to GitHub Pages

### Viewing CI Results

1. **Pull Request Checks** - View test results in PR status checks
2. **GitHub Actions Summary** - See coverage and accessibility summaries
3. **Artifacts** - Download detailed reports from workflow runs
4. **Codecov** - View coverage trends at codecov.io (if configured)

## Manual Testing

Automated tests cannot catch everything. Perform manual testing for:

### 1. Keyboard Navigation

**Test checklist:**
- [ ] Tab through all interactive elements
- [ ] Focus indicators are clearly visible
- [ ] Tab order is logical
- [ ] Enter/Space activates buttons and links
- [ ] Escape closes modals and dialogs
- [ ] Arrow keys work in custom controls

**Test command:**
```bash
npm run dev
# Navigate to http://localhost:4321 and test with keyboard only
```

### 2. Screen Reader Testing

**Recommended screen readers:**
- **NVDA** (Windows) - Free, open-source
- **JAWS** (Windows) - Industry standard
- **VoiceOver** (macOS/iOS) - Built-in
- **TalkBack** (Android) - Built-in

**Test checklist:**
- [ ] All content is announced correctly
- [ ] Navigation landmarks work properly
- [ ] Images have meaningful alt text
- [ ] Forms have proper labels
- [ ] ARIA live regions announce updates
- [ ] Page titles are descriptive

**Testing with VoiceOver (macOS):**
```bash
# Enable VoiceOver
Cmd + F5

# Navigate with VoiceOver
Ctrl + Option + Arrow Keys

# Open rotor (navigation menu)
Ctrl + Option + U
```

### 3. Visual Testing

**Test at different zoom levels:**
- [ ] 100% (baseline)
- [ ] 150% (common preference)
- [ ] 200% (WCAG requirement)
- [ ] 400% (extreme case)

**Test color modes:**
- [ ] Light mode (if applicable)
- [ ] Dark mode (if applicable)
- [ ] High contrast mode
- [ ] Color blindness simulation

**Tools:**
- Chrome DevTools (Rendering → Emulate vision deficiencies)
- [Sim Daltonism](https://michelf.ca/projects/sim-daltonism/) (macOS)
- [Color Oracle](https://colororacle.org/) (Windows/macOS/Linux)

### 4. Reduced Motion

**Test with reduced motion preference:**

**macOS:**
```bash
System Preferences → Accessibility → Display → Reduce motion
```

**Windows:**
```bash
Settings → Ease of Access → Display → Show animations
```

**Test checklist:**
- [ ] Animations are disabled or reduced
- [ ] Parallax effects are removed
- [ ] Auto-playing content is paused
- [ ] Essential motion is preserved

## Test Coverage Goals

We maintain **80%+ code coverage** across the codebase:

| Metric | Target | Current |
|--------|--------|---------|
| Lines | ≥ 80% | TBD |
| Statements | ≥ 80% | TBD |
| Functions | ≥ 80% | TBD |
| Branches | ≥ 80% | TBD |

### Coverage Reports

Coverage reports are generated in multiple formats:

- **HTML** - `coverage/index.html` (browse interactively)
- **LCOV** - `coverage/lcov.info` (for CI integration)
- **JSON** - `coverage/coverage-summary.json` (for automation)
- **Text** - Console output with summary

### Improving Coverage

To improve test coverage:

1. Identify untested code:
   ```bash
   npm run test:coverage
   open coverage/index.html
   ```

2. Write tests for uncovered lines:
   - Unit tests for pure functions
   - Integration tests for modules
   - E2E tests for user flows

3. Focus on critical paths:
   - Navigation logic
   - Data transformations
   - User interactions

## Contributing Guidelines

### Before Submitting a PR

1. **Run all tests locally:**
   ```bash
   npm run build
   npm run test:coverage
   npm run test:a11y
   ```

2. **Ensure coverage meets thresholds:**
   - Check that coverage is ≥ 80%
   - Add tests for new features

3. **Verify accessibility:**
   - Run Playwright accessibility tests
   - Test keyboard navigation manually
   - Verify color contrast

4. **Check for violations:**
   ```bash
   npm run test:pa11y
   ```

### Writing Accessible Code

**HTML:**
- Use semantic HTML elements (`<header>`, `<nav>`, `<main>`, `<article>`, etc.)
- Add `alt` text to all images
- Use proper heading hierarchy (h1 → h2 → h3, etc.)
- Include `lang` attribute on `<html>`

**ARIA:**
- Use ARIA sparingly (HTML semantics are preferred)
- Always test with screen readers
- Follow [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)

**CSS:**
- Ensure sufficient color contrast (4.5:1 for normal text, 3:1 for large text)
- Make focus indicators visible (outline or box-shadow)
- Support `prefers-reduced-motion`
- Test at 200% zoom

**JavaScript:**
- Support keyboard navigation
- Manage focus properly
- Announce dynamic content with ARIA live regions
- Provide keyboard alternatives for mouse interactions

### Writing Tests

**Unit tests:**
```typescript
import { describe, it, expect } from 'vitest';

describe('MyComponent', () => {
  it('should render correctly', () => {
    // Test implementation
  });
});
```

**Accessibility tests:**
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('should not have accessibility violations', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

## Resources

### Documentation

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Playwright Testing](https://playwright.dev/docs/intro)
- [axe-core Documentation](https://github.com/dequelabs/axe-core)
- [Pa11y Documentation](https://pa11y.org/)
- [Vitest Documentation](https://vitest.dev/)

### Tools

- [axe DevTools Extension](https://www.deque.com/axe/devtools/) - Browser accessibility testing
- [WAVE Extension](https://wave.webaim.org/extension/) - Visual accessibility evaluation
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - Built into Chrome DevTools
- [Color Contrast Checker](https://webaim.org/resources/contrastchecker/)

### Guides

- [WebAIM Articles](https://webaim.org/articles/) - Comprehensive accessibility guides
- [A11y Project](https://www.a11yproject.com/) - Community-driven accessibility resources
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility) - Web accessibility documentation
- [Inclusive Components](https://inclusive-components.design/) - Accessible component patterns

### Screen Readers

- [NVDA](https://www.nvaccess.org/download/) (Windows, Free)
- [JAWS](https://www.freedomscientific.com/products/software/jaws/) (Windows, Commercial)
- [VoiceOver](https://www.apple.com/accessibility/voiceover/) (macOS/iOS, Built-in)
- [TalkBack](https://support.google.com/accessibility/android/answer/6283677) (Android, Built-in)

## Support

For questions or issues with accessibility testing:

1. Check existing documentation
2. Review [ACCESSIBILITY_AUDIT.md](ACCESSIBILITY_AUDIT.md) for known issues
3. Open an issue on GitHub with the `accessibility` label
4. Reach out to the maintainers

---

**Last Updated:** October 2025  
**Maintained by:** Scroll of Dharma Team
