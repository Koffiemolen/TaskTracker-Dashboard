# frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

# Folderstructure
- Routing: Routes for application in the /src/router/index.ts file. Each route will map to a view component.
- State Management: Vuex store in the /src/store directory. Define state, mutations, actions, and getters for managing global state like user authentication and workflow data.
- API Integration: Create services in /src/services to handle API requests. Axios or Vue's built-in fetch API for making HTTP calls to the backend.
- Styling: Apply styles to your components. Using a CSS framework compatible with Vue.js, like Vuetify or BootstrapVue, to speed up the styling process.