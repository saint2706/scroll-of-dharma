#!/usr/bin/env node

/**
 * Pa11y Accessibility Testing Script
 * 
 * Runs Pa11y against all pages in the site to detect accessibility issues
 * Generates a detailed report with WCAG 2.1 AA violations
 */

import pa11y from 'pa11y';
import { writeFileSync } from 'fs';
import { join } from 'path';

const baseUrl = process.env.BASE_URL || 'http://localhost:4321';

// Pages to test
const pages = [
  '/',
  '/chapters/gita_scroll/lotus_of_doubt',
  '/chapters/gita_scroll/chakra_of_dharma',
  '/chapters/gita_scroll/spiral_of_vision',
  '/chapters/birth_of_dharma/cosmic_egg',
  '/chapters/birth_of_dharma/first_flame',
  '/chapters/weapon_quest/forest_of_austerity',
  '/chapters/weapon_quest/shiva_and_the_hunter',
  '/chapters/fall_of_dharma/game_of_fate',
  '/chapters/trials_of_karna/suns_gift',
];

// Pa11y configuration
const pa11yConfig = {
  standard: 'WCAG2AA',
  timeout: 30000,
  wait: 2000,
  runners: ['axe', 'htmlcs'],
  ignore: [
    // Ignore specific rules if needed
    // 'WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail'
  ],
};

async function runPa11y() {
  console.log('🔍 Starting Pa11y accessibility tests...\n');
  console.log(`Testing ${pages.length} pages against WCAG 2.1 AA standard\n`);
  
  const results = [];
  let totalIssues = 0;
  let totalErrors = 0;
  let totalWarnings = 0;
  let totalNotices = 0;

  for (const page of pages) {
    const url = `${baseUrl}${page}`;
    console.log(`Testing: ${url}`);
    
    try {
      const result = await pa11y(url, pa11yConfig);
      
      const errors = result.issues.filter(issue => issue.type === 'error');
      const warnings = result.issues.filter(issue => issue.type === 'warning');
      const notices = result.issues.filter(issue => issue.type === 'notice');
      
      totalIssues += result.issues.length;
      totalErrors += errors.length;
      totalWarnings += warnings.length;
      totalNotices += notices.length;
      
      results.push({
        url,
        page,
        issueCount: result.issues.length,
        errors: errors.length,
        warnings: warnings.length,
        notices: notices.length,
        issues: result.issues,
      });
      
      console.log(`  ✓ Complete: ${result.issues.length} issues found`);
      console.log(`    - Errors: ${errors.length}`);
      console.log(`    - Warnings: ${warnings.length}`);
      console.log(`    - Notices: ${notices.length}\n`);
      
    } catch (error) {
      console.error(`  ✗ Error testing ${url}:`, error.message);
      results.push({
        url,
        page,
        error: error.message,
      });
    }
  }

  // Generate summary
  console.log('\n' + '='.repeat(60));
  console.log('Pa11y Test Summary');
  console.log('='.repeat(60));
  console.log(`Total pages tested: ${pages.length}`);
  console.log(`Total issues found: ${totalIssues}`);
  console.log(`  - Errors: ${totalErrors}`);
  console.log(`  - Warnings: ${totalWarnings}`);
  console.log(`  - Notices: ${totalNotices}`);
  console.log('='.repeat(60) + '\n');

  // Save results to file
  const reportPath = join(process.cwd(), 'test-results', 'pa11y-results.json');
  try {
    writeFileSync(reportPath, JSON.stringify(results, null, 2));
    console.log(`📄 Full report saved to: ${reportPath}\n`);
  } catch (err) {
    console.error('Failed to save report:', err.message);
  }

  // Exit with error if there are accessibility errors
  if (totalErrors > 0) {
    console.error(`❌ Pa11y found ${totalErrors} accessibility errors!`);
    process.exit(1);
  } else if (totalWarnings > 0) {
    console.warn(`⚠️  Pa11y found ${totalWarnings} accessibility warnings`);
    console.log('✅ No critical accessibility errors found\n');
    process.exit(0);
  } else {
    console.log('✅ All accessibility tests passed!\n');
    process.exit(0);
  }
}

// Run the tests
runPa11y().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
