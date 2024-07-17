// src/plugins/vuetify.ts
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components' // Import components
import * as directives from 'vuetify/directives' // Import directives
import 'vuetify/styles' // Import Vuetify styles

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
