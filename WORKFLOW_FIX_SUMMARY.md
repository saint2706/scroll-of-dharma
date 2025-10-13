# GitHub Actions Workflow Fix Summary

## Problem Statement
The GitHub Actions workflow run [#18459631330](https://github.com/saint2706/scroll-of-dharma/actions/runs/18459631330/job/52587896578) was failing during the "Install dependencies" step with the following error:

```
npm error `npm ci` can only install packages when your package.json and package-lock.json or npm-shrinkwrap.json are in sync. Please update your lock file with `npm install` before continuing.
npm error Invalid: lock file's prettier@2.8.7 does not satisfy prettier@3.6.2
npm error Missing: prettier@2.8.7 from lock file
```

## Root Cause Analysis

### The Issue
The `package-lock.json` file was out of sync with the `package.json` file. Specifically:

1. **package-lock.json** contained `prettier@2.8.7`
2. **@astrojs/check** (a devDependency in package.json) requires `prettier@^3.0.0` as a peer dependency
3. The version mismatch caused `npm ci` to fail during the CI/CD pipeline

### Why This Happened
This typically occurs when:
- Dependencies are updated in `package.json` without regenerating `package-lock.json`
- Manual edits to `package.json` without running `npm install`
- Peer dependency requirements change after a package version update

## The Fix

### What Was Changed
Updated `package-lock.json` to resolve the peer dependency conflict by running:
```bash
npm install
```

This command:
1. Analyzed all dependencies and their peer dependencies
2. Resolved `prettier` to version `3.6.2` (satisfies `^3.0.0` requirement from @astrojs/check)
3. Updated the lock file accordingly

### Changes Made
- **File Modified**: `package-lock.json`
- **Key Change**: `prettier` version updated from `2.8.7` to `3.6.2`
- **Additional Changes**: Lock file structure updated to properly handle peer dependencies

## Verification

### Local Testing
✅ **npm ci**: Successfully installs all dependencies
```bash
cd /home/runner/work/scroll-of-dharma/scroll-of-dharma
rm -rf node_modules
npm ci
# Result: Success - 506 packages installed
```

✅ **npm run build**: Successfully builds the Astro site
```bash
npm run build
# Result: Success - 22 pages built
# - All Astro checks passed (0 errors, 0 warnings)
# - Static site generated in ./dist
```

### Expected CI/CD Behavior
When this fix is merged to the `main` branch, the GitHub Actions workflow should:
1. ✅ Checkout code successfully
2. ✅ Setup Node.js successfully
3. ✅ Install dependencies with `npm ci` (previously failed here)
4. ✅ Build with Astro
5. ✅ Upload artifact to GitHub Pages
6. ✅ Deploy to GitHub Pages

## Prevention for Future

### Best Practices
1. **Always run `npm install`** when updating dependencies in `package.json`
2. **Commit both files together**: Always commit `package.json` and `package-lock.json` in the same commit
3. **Use `npm ci` in CI/CD**: This ensures builds fail if lock file is out of sync (which caught this issue)
4. **Regular dependency audits**: Run `npm outdated` and `npm audit` regularly

### Workflow Configuration
The deployment workflow (`.github/workflows/deploy.yml`) is correctly configured:
- Uses `npm ci` instead of `npm install` (enforces lock file sync)
- Caches npm dependencies for faster builds
- Runs on pushes to `main` and `copilot/migrate-to-astro-github-pages` branches

## Related Files
- `.github/workflows/deploy.yml` - GitHub Actions deployment workflow
- `package.json` - Project dependencies
- `package-lock.json` - Dependency lock file (FIXED)
- `astro.config.mjs` - Astro configuration
- `src/` - Source files for the Astro site

## Commit Details
- **Commit**: Fix package-lock.json sync issue with prettier version
- **Branch**: copilot/fix-github-actions-workflow
- **Files Changed**: package-lock.json (23 insertions, 5 deletions)

---

*Issue resolved on: 2025-10-13*
*Workflow Run ID: 18459631330*
*Job ID: 52587896578*
