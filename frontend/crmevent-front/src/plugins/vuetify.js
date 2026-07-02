import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";

import { createVuetify } from "vuetify";

export default createVuetify({
  theme: {
    defaultTheme: "crm",

    themes: {
      crm: {
        dark: false,

        colors: {
          primary: "#2563eb",
          secondary: "#1e293b",
          success: "#22c55e",
          error: "#ef4444",
          warning: "#f59e0b",
          background: "#f8fafc",
          surface: "#ffffff",
        },
      },
    },
  },
});