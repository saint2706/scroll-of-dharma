# Test Suite

This directory contains all automated tests for the Scroll of Dharma project.

## Directory Structure

```
tests/
├── unit/              # Unit tests for TypeScript modules
│   ├── types.test.ts           # Tests for type definitions
│   └── narratives.test.ts      # Tests for narrative data
├── integration/       # Integration tests (future)
├── e2e/               # End-to-end accessibility tests
│   └── accessibility.spec.ts   # Playwright accessibility tests
└── README.md          # This file
```

## Test Categories

### Unit Tests (`tests/unit/`)

Unit tests validate individual functions and modules in isolation.

**Current coverage:**
- Type definitions and constants
- Narrative content validation
- Data structure integrity

**Run unit tests:**
```bash
npm test
npm run test:watch      # Watch mode
npm run test:coverage   # With coverage report
```

### Integration Tests (`tests/integration/`)

Integration tests validate that multiple modules work together correctly. (To be added)

### E2E Tests (`tests/e2e/`)

End-to-end tests validate the entire application from a user's perspective, with a focus on accessibility.

**Current coverage:**
- WCAG 2.1 AA compliance validation
- Keyboard navigation
- Screen reader compatibility
- Color contrast
- Focus indicators
- Reduced motion support

**Run E2E tests:**
```bash
npm run test:a11y           # Run all Playwright tests
npx playwright test --ui    # Interactive UI mode
npx playwright show-report  # View HTML report
```

## Writing Tests

### Unit Tests

Use Vitest for unit testing:

```typescript
import { describe, it, expect } from 'vitest';

describe('MyFunction', () => {
  it('should do something', () => {
    const result = myFunction('input');
    expect(result).toBe('expected');
  });
});
```

### Accessibility Tests

Use Playwright with axe-core for accessibility testing:

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('should not have accessibility violations', async ({ page }) => {
  await page.goto('/');
  
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();
  
  expect(results.violations).toEqual([]);
});
```

## Test Coverage

We maintain **80%+ test coverage** on business logic:

| Metric | Threshold |
|--------|-----------|
| Lines | ≥ 80% |
| Statements | ≥ 80% |
| Functions | ≥ 80% |
| Branches | ≥ 70% |

**View coverage report:**
```bash
npm run test:coverage
open coverage/index.html
```

## CI/CD Integration

All tests run automatically in GitHub Actions:

1. **On Pull Requests**: Unit tests and accessibility tests
2. **On Push to main**: Full test suite + deployment

See `.github/workflows/accessibility-check.yml` for details.

## Debugging Tests

### Debug Unit Tests

```bash
# Run specific test file
npm test tests/unit/types.test.ts

# Debug with console logs
npm test -- --reporter=verbose

# Run with Node debugger
node --inspect-brk node_modules/.bin/vitest
```

### Debug E2E Tests

```bash
# Run in headed mode (see browser)
npx playwright test --headed

# Debug specific test
npx playwright test --debug tests/e2e/accessibility.spec.ts

# Run specific test by name
npx playwright test -g "should have proper page structure"

# View trace for failed test
npx playwright show-trace test-results/.../trace.zip
```

## Best Practices

1. **Write descriptive test names** - Test names should explain what is being tested
2. **Test one thing at a time** - Each test should have a single assertion focus
3. **Use arrange-act-assert pattern** - Structure tests clearly
4. **Mock external dependencies** - Tests should be isolated and fast
5. **Test edge cases** - Include tests for error conditions
6. **Keep tests maintainable** - Avoid complex logic in tests

## Resources

- [Vitest Documentation](https://vitest.dev/)
- [Playwright Documentation](https://playwright.dev/)
- [axe-core Rules](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
- [ACCESSIBILITY_TESTING.md](../ACCESSIBILITY_TESTING.md) - Complete testing guide

## Contributing

Before submitting a PR:

1. Run all tests: `npm test && npm run test:a11y`
2. Check coverage: `npm run test:coverage`
3. Fix any failing tests
4. Add tests for new features

See [ACCESSIBILITY_TESTING.md](../ACCESSIBILITY_TESTING.md) for detailed guidelines.
