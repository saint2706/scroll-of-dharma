import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // Test environment
    environment: 'node',
    
    // Include test files
    include: ['tests/unit/**/*.test.ts', 'tests/integration/**/*.test.ts'],
    
    // Coverage configuration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'tests/',
        'dist/',
        '.astro/',
        '**/*.config.*',
        '**/test_*.py',
        '**/*.test.ts',
        '**/*.spec.ts',
        'app.py',
        'narrative.py',
        'audio_builder.py',
        'ui_constants.py',
        'setup.py',
        'download_fonts.py',
        'scripts/',
        'src/pages/',
        'src/layouts/',
        'src/components/',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 70,
        statements: 80,
      },
    },
  },
});
