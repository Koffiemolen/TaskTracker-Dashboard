// src/plugins/vuetify.ts
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components' // Import components
import * as directives from 'vuetify/directives' // Import directives
import 'vuetify/styles' // Import Vuetify styles

// Define a type for the plugin if needed
// (Optional, mainly if you have custom configurations or need type-checking for the setup)
interface VuetifyOptions {
  components: typeof components
  directives: typeof directives
  // any other options
}

// Create a Vuetify instance with type-checking
const vuetify = createVuetify({
  components,
  directives
  // any other options
} as VuetifyOptions)

export default vuetify
