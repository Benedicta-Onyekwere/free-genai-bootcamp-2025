# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config({
  extends: [
    // Remove ...tseslint.configs.recommended and replace with this
    ...tseslint.configs.recommendedTypeChecked,
    // Alternatively, use this for stricter rules
    ...tseslint.configs.strictTypeChecked,
    // Optionally, add this for stylistic rules
    ...tseslint.configs.stylisticTypeChecked,
  ],
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config({
  plugins: {
    // Add the react-x and react-dom plugins
    'react-x': reactX,
    'react-dom': reactDom,
  },
  rules: {
    // other rules...
    // Enable its recommended typescript rules
    ...reactX.configs['recommended-typescript'].rules,
    ...reactDom.configs.recommended.rules,
  },
})
```

## Development Journey and Challenges

### Initial Setup and Configuration
1. Project Initialization
   - Created React project with Vite using `npm create vite@latest`
   - Integrated TypeScript for type safety
   - Set up Tailwind CSS for styling
   - Configured ShadCN for UI components
   
2. Environment Setup Steps:
   ```bash
   npm install
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   npm install @shadcn/ui
   ```

### Major Components and Features

#### Dashboard
The dashboard provides a summary of student progression and recent activities.
- Implemented last session display
- Added progress tracking metrics
- Integrated activity summaries

[Click here to view the dashboard screenshot](../assets/dashboard.png)

#### Study Activities
A grid of interactive study activity cards with launch and view capabilities.
- Created card components for each activity
- Implemented launch functionality in new tab
- Added view details navigation
- Integrated with group_id parameter system

[Click here to view the study activities screenshot](../assets/study-activities.png)

#### Words Management
Table-based interface for managing Japanese vocabulary with sorting and pagination.
- Built sortable table columns
- Implemented pagination system
- Added sound playback for Japanese words
- Integrated word detail view navigation

[Click here to view the words management screenshot](../assets/words.png)

#### Word Groups
Organized grouping system for vocabulary management.
- Created group listing interface
- Implemented word association system
- Added group detail views
- Built word filtering by group

[Click here to view the word groups screenshot](../assets/word-groups.png)

#### Sessions
Comprehensive session tracking and history visualization.
- Implemented session logging
- Added time tracking functionality
- Created session summary views
- Built group association display

[Click here to view the sessions screenshot](../assets/sessions.png)

#### Settings
User preferences and system configuration interface.
- Implemented dark mode toggle
- Added database reset functionality
- Created confirmation dialogs
- Built theme management system

[Click here to view the settings screenshot](../assets/settings.png)

### Major Challenges and Solutions

#### 1. PostCSS Configuration Issues
- **Initial Challenge**: PostCSS configuration errors with ES modules
  ```
  Failed to load PostCSS config: Package subpath './nesting' is not defined
  ```
- **Investigation Steps**:
  - Checked PostCSS version compatibility
  - Reviewed module system configuration
  - Analyzed package.json settings
- **Solution**: 
  - Updated PostCSS config to use ES module syntax
  - Modified module type declarations
  - Resolved package dependencies

#### 2. Tailwind Integration
- **Initial Challenge**: Tailwind CSS classes not being recognized
  ```
  The 'bg-background' class does not exist
  ```
- **Investigation Steps**:
  - Verified Tailwind configuration
  - Checked class definitions
  - Reviewed theme setup
- **Solution**: 
  - Corrected Tailwind configuration
  - Updated theme setup
  - Added missing class definitions
